import os
import json
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Union, Literal

ENDPOINT = "https://api.typesafe.ai/v1/systemone"

@dataclass
class DecisionResult:
    winner: str
    confidence: float
    probabilities: Dict[str, float]
    risk_score: float
    latency: float
    tokens: Dict[str, int] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SafetyResult:
    allowed: bool
    danger_score: float
    action_type: str
    latency: float
    error: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StuckResult:
    is_stuck: bool
    confidence: float
    risk_score: float
    latency: float
    raw: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FactResult:
    is_hallucination: bool
    confidence: float
    risk_score: float
    latency: float
    raw: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RouteResult:
    route: str
    confidence: float
    probabilities: Dict[str, float]
    latency: float
    raw: Dict[str, Any] = field(default_factory=dict)

class JevPilot:
    """
    Core client for Jev System-1 Decision Engine.
    Compatible with any LLM framework or standalone agent.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: str = ENDPOINT,
        default_model: str = "jev-latest",
        timeout: float = 3.0,
        max_retries: int = 2,
        save: bool = False
    ):
        resolved_key = (
            api_key 
            or os.environ.get("TYPESAFE_API_KEY") 
            or os.environ.get("JEV_API_KEY") 
            or self._load_from_saved_config()
        )
        if not resolved_key:
            raise ValueError(
                "TypeSafe Jev API Key not found!\n"
                "Please do one of the following:\n"
                "  1. Pass in Python: JevPilot(api_key='...', save=True)\n"
                "  2. Run in terminal: jev-pilot setup <your_api_key>\n"
                "  3. Set environment variable: export TYPESAFE_API_KEY='...'\n"
                "Get your key at: https://console.typesafe.ai"
            )
        
        if api_key and save:
            self.configure(api_key)

        self.api_key = resolved_key
        self.endpoint = endpoint
        self.default_model = default_model
        self.timeout = timeout
        self.max_retries = max_retries

    @staticmethod
    def _config_path() -> str:
        return os.path.expanduser("~/.jev_pilot/config.json")

    @classmethod
    def _load_from_saved_config(cls) -> Optional[str]:
        p = cls._config_path()
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    return cfg.get("api_key")
            except Exception:
                return None
        return None

    @classmethod
    def configure(cls, api_key: str):
        """
        Permanently saves the API key with 0o600 permissions (user-only read/write).
        """
        p = cls._config_path()
        os.makedirs(os.path.dirname(p), exist_ok=True)
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        mode = 0o600
        fd = os.open(p, flags, mode)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump({"api_key": api_key.strip()}, f, indent=2)
        try:
            os.chmod(p, 0o600)
        except Exception:
            pass
        return f"Successfully saved Jev API key securely to {p}"

    def _post(self, payload: Dict[str, Any], timeout: Optional[float] = None) -> Dict[str, Any]:
        call_timeout = timeout or self.timeout
        encoded_data = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "jev-pilot/0.1.1"
        }

        last_err = None
        for attempt in range(self.max_retries + 1):
            req = urllib.request.Request(self.endpoint, data=encoded_data, headers=headers, method="POST")
            t0 = time.time()
            try:
                with urllib.request.urlopen(req, timeout=call_timeout) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    data["_latency_sec"] = round(time.time() - t0, 3)
                    return data
            except urllib.error.HTTPError as e:
                err_text = e.read().decode("utf-8", errors="ignore")
                if e.code in (429, 500, 502, 503, 504) and attempt < self.max_retries:
                    time.sleep(0.3 * (2 ** attempt))
                    continue
                raise RuntimeError(f"TypeSafe Jev API HTTP {e.code}: {err_text}")
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                last_err = e
                if attempt < self.max_retries:
                    time.sleep(0.2 * (2 ** attempt))
                    continue
                raise RuntimeError(f"TypeSafe Jev API Network Error: {e}")

        raise RuntimeError(f"TypeSafe Jev API Request Failed after {self.max_retries} retries: {last_err}")

    def arbitrate(
        self,
        context: str,
        candidates: Dict[str, str],
        criteria_instruction: str = "Which candidate solution has the highest probability of robust execution and success?"
    ) -> DecisionResult:
        """
        Arbitrate between multiple candidate responses or execution paths (Best-of-N).
        """
        if not candidates:
            raise ValueError("Candidates dictionary cannot be empty.")

        payload = {
            "model": self.default_model,
            "state": f"Context / Task Details:\n{context}",
            "questions": {
                "winner": {
                    "type": "choice",
                    "instructions": criteria_instruction,
                    "criteria": candidates
                },
                "high_risk": {
                    "type": "noul",
                    "instructions": "Is there a critical failure, crash, or blocker risk in this task context?"
                }
            }
        }
        res = self._post(payload)
        answers = res.get("answers", {})
        win_info = answers.get("winner", {})
        risk_info = answers.get("high_risk", {})
        chosen = win_info.get("choice", "")

        return DecisionResult(
            winner=chosen,
            confidence=win_info.get("confidence", 0.0),
            probabilities=win_info.get("probabilities", {}),
            risk_score=risk_info.get("noul", 0.0),
            latency=res.get("_latency_sec", 0.0),
            tokens=res.get("usage", {}),
            raw=res
        )

    def guard(
        self,
        proposed_action: str,
        current_state: str,
        risk_threshold: float = 0.6,
        on_error: Literal["fail_closed", "fail_open"] = "fail_closed"
    ) -> SafetyResult:
        """
        Fast guardrail to verify safety before executing tools, commands, or DB mutations.
        on_error="fail_closed": Blocks action if API times out or fails (safest).
        on_error="fail_open": Allows action if API fails (avoids agent crash on network blip).
        """
        payload = {
            "model": self.default_model,
            "state": f"Current State:\n{current_state}\n\nProposed Action:\n{proposed_action}",
            "questions": {
                "danger_check": {
                    "type": "noul",
                    "instructions": "Will executing this command or action cause irreversible data loss, break system stability, or expose secrets?"
                },
                "action_type": {
                    "type": "choice",
                    "instructions": "Classify the nature of this operation",
                    "criteria": {
                        "safe_read": "Read-only, benign inspection, or diagnostic command",
                        "reversible_write": "Standard non-destructive write, create, or modify action",
                        "destructive": "Critical deletion, service interruption, or irreversible alteration"
                    }
                }
            }
        }
        try:
            res = self._post(payload)
            answers = res.get("answers", {})
            danger = answers.get("danger_check", {}).get("noul", 0.0)
            cat = answers.get("action_type", {}).get("choice", "")
            is_allowed = (danger < risk_threshold) and (cat != "destructive")
            return SafetyResult(
                allowed=is_allowed,
                danger_score=danger,
                action_type=cat,
                latency=res.get("_latency_sec", 0.0),
                raw=res
            )
        except Exception as e:
            if on_error == "fail_open":
                return SafetyResult(
                    allowed=True,
                    danger_score=0.0,
                    action_type="unknown_fail_open",
                    latency=0.0,
                    error=str(e)
                )
            return SafetyResult(
                allowed=False,
                danger_score=1.0,
                action_type="error_fail_closed",
                latency=0.0,
                error=str(e)
            )

    def check_stuck(self, trajectory_history: Union[str, List[str]], threshold_confidence: float = 0.7) -> StuckResult:
        """
        Detects if an autonomous AI agent is trapped in an unproductive retry loop.
        """
        if isinstance(trajectory_history, list):
            history_text = "\n".join([f"Step {i+1}: {step}" for i, step in enumerate(trajectory_history)])
        else:
            history_text = str(trajectory_history)

        payload = {
            "model": self.default_model,
            "state": f"Agent Action / Trajectory History:\n{history_text}",
            "questions": {
                "status": {
                    "type": "choice",
                    "instructions": "Determine if the agent is stuck in an unproductive loop or making tangible progress",
                    "criteria": {
                        "stuck_loop": "Agent is repeating failed commands, oscillating, or trapped in an unproductive loop",
                        "making_progress": "Agent is adapting, trying distinct valid strategies, and making progress"
                    }
                },
                "stuck_risk": {
                    "type": "noul",
                    "instructions": "Is the agent wasting tokens in a repetitive or futile pattern?"
                }
            }
        }
        res = self._post(payload)
        answers = res.get("answers", {})
        status = answers.get("status", {})
        choice = status.get("choice", "")
        conf = status.get("confidence", 0.0)
        risk = answers.get("stuck_risk", {}).get("noul", 0.0)

        is_stuck = (choice == "stuck_loop") and (conf >= threshold_confidence or risk >= 0.7)
        return StuckResult(
            is_stuck=is_stuck,
            confidence=conf,
            risk_score=risk,
            latency=res.get("_latency_sec", 0.0),
            raw=res
        )

    def verify_fact(self, claim: str, ground_truth: str) -> FactResult:
        """
        Checks if an LLM-generated claim matches or contradicts given ground truth context.
        """
        payload = {
            "model": self.default_model,
            "state": f"Ground Truth Reference:\n{ground_truth}\n\nCandidate Claim / Response:\n{claim}",
            "questions": {
                "evaluation": {
                    "type": "choice",
                    "instructions": "Does the claim strictly align with the ground truth or does it hallucinate/contradict?",
                    "criteria": {
                        "factual": "The claim is completely supported by and consistent with the ground truth",
                        "hallucination": "The claim contains ungrounded claims, errors, or directly contradicts the ground truth"
                    }
                },
                "hallucination_score": {
                    "type": "noul",
                    "instructions": "Is this claim inaccurate or hallucinated based on the reference?"
                }
            }
        }
        res = self._post(payload)
        answers = res.get("answers", {})
        ev = answers.get("evaluation", {})
        choice = ev.get("choice", "")
        conf = ev.get("confidence", 0.0)
        risk = answers.get("hallucination_score", {}).get("noul", 0.0)

        is_hal = (choice == "hallucination") or (risk >= 0.7)
        return FactResult(
            is_hallucination=is_hal,
            confidence=conf,
            risk_score=risk,
            latency=res.get("_latency_sec", 0.0),
            raw=res
        )

    def route(self, prompt: str, routes: Dict[str, str]) -> RouteResult:
        """
        Ultra-fast intent routing to appropriate model/tool/agent.
        Returns a standardized RouteResult dataclass.
        """
        payload = {
            "model": self.default_model,
            "state": f"User Request:\n{prompt}",
            "questions": {
                "route": {
                    "type": "choice",
                    "instructions": "Select the best processing destination for this request",
                    "criteria": routes
                }
            }
        }
        res = self._post(payload)
        r_info = res.get("answers", {}).get("route", {})
        return RouteResult(
            route=r_info.get("choice", ""),
            confidence=r_info.get("confidence", 0.0),
            probabilities=r_info.get("probabilities", {}),
            latency=res.get("_latency_sec", 0.0),
            raw=res
        )
