# jev-pilot ⚡

> **Fast System-1 Decision, Arbitration & Safety Engine for Autonomous AI Agents**  
> Brings sub-second, zero-hallucination intuition to Claude, GPT, Gemini, Llama, Hermes, and custom agent runtimes.

**[🇮🇷 راهنمای جامع فارسی (Persian Documentation)](./README.fa.md)**

[![PyPI Version](https://img.shields.io/pypi/v/jev-pilot.svg)](https://pypi.org/project/jev-pilot/)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by TypeSafe Jev](https://img.shields.io/badge/Powered%20by-TypeSafe%20Jev-10b981.svg)](https://typesafe.ai)

---

## 💡 What is jev-pilot? (The Problem it Solves)

Modern LLMs (Claude 3.5, GPT-4o, DeepSeek) represent **System 2 thinking**: they are brilliant at deep reasoning, creative writing, and writing complex code.

However, using an LLM for **operational split-second decisions** inside an autonomous agent creates huge bottlenecks:
- ⏳ **Too Slow:** Waiting 3 to 10 seconds for an LLM to stream a simple yes/no or routing choice.
- 💸 **Too Expensive:** Burning thousands of prompt tokens just to verify safety or pick a tool.
- 🎭 **Prone to Sycophancy & Hallucination:** LLMs often agree with broken assumptions just to please the prompt.

**jev-pilot** gives your agent a **System 1 (fast, calibrated intuition)** using TypeSafe's Jev model:
- ⚡ **Sub-second Latency:** Returns answers in **~0.3 seconds** *(based on TypeSafe internal published benchmarks and live API tests)*.
- 💰 **Significantly Lower Cost:** $42 per billion input tokens according to TypeSafe pricing.
- 🎯 **Calibrated Math:** Outputs exact probabilities and confidence distributions (`0.0` to `1.0`), not text strings.
- 🛡️ **Zero Hallucination:** The model does not generate free text; it evaluates structured decisions deterministically.

---

## 🧠 System 1 vs System 2 Architecture

```
                 [ User Request / Agent Action ]
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
       [ System 1: jev-pilot ]       [ System 2: Big LLM ]
       • Fast Intent Routing (<0.3s) • Deep reasoning & planning
       • Tool Safety Guardrails      • Generates multiple solutions
       • Agent Loop & Stuck Breaker  • Writes large codebases
                │                             │
                └──────────────┬──────────────┘
                               ▼
               [ Fast, Reliable, Verified Agent ]
```

---

## 📦 Installation

```bash
pip install jev-pilot
```

---

## 🔑 Setup & API Key Resolution

Get your API key at [console.typesafe.ai](https://console.typesafe.ai).

`jev-pilot` automatically resolves your API key in the following priority order:
1. Direct argument passed to `JevPilot(api_key="...")`
2. Environment variable: `TYPESAFE_API_KEY`
3. Environment variable: `JEV_API_KEY`
4. Secure persistent config file: `~/.jev_pilot/config.json` (saved with `chmod 600` user-only permissions)

### Option 1: In Python with Zero-Config Persistence (Recommended)
Pass `save=True` once — it is securely saved on your machine:
```python
from jev_pilot import JevPilot

# Run once:
pilot = JevPilot(api_key="your_key_here", save=True)

# From then on, anywhere in any project:
pilot = JevPilot()
```

### Option 2: Environment Variable
```bash
export TYPESAFE_API_KEY="your_key_here"
```

---

## 🚀 Core Features & Code Examples

### 1. Best-of-N Candidate Arbitration (`arbitrate`)
Instead of trusting the first draft from an LLM, generate 2-3 approaches. `jev-pilot` picks the winning strategy with mathematical confidence:

```python
from jev_pilot import JevPilot

pilot = JevPilot()

decision = pilot.arbitrate(
    context="Build a high-performance web crawler handling 10,000 req/min in Python.",
    candidates={
        "opt_a": "Synchronous requests with for-loops and time.sleep",
        "opt_b": "Asyncio + aiohttp with connection pooling",
        "opt_c": "Scrapling framework with adaptive bypass"
    }
)

print(f"Winning Strategy: {decision.winner}")
print(f"Confidence: {decision.confidence:.2%}")   # float between 0.0 and 1.0
print(f"Probabilities: {decision.probabilities}") # dict of floats summing to ~1.0
print(f"Latency: {decision.latency}s")
```

### 2. Pre-Execution Safety Guardrail (`guard`)
Intercept dangerous shell commands, SQL drops, and destructive mutations before they run.

**Error Handling Policy (`on_error`):**
- `on_error="fail_closed"` (Default): If the API call times out or encounters network errors, the action is **blocked** (`allowed=False`) for maximum security.
- `on_error="fail_open"`: If the API encounters network errors, the action is **allowed** (`allowed=True`) to prevent halting agent workflows during temporary network blips.

```python
safety = pilot.guard(
    proposed_action="rm -rf /var/lib/mysql/*",
    current_state="Production database server active",
    risk_threshold=0.6,          # float: 0.0 (strict) to 1.0 (lenient)
    on_error="fail_closed"       # "fail_closed" or "fail_open"
)

if not safety.allowed:
    print(f"🚨 Blocked dangerous operation! Danger score: {safety.danger_score:.2f}")
    print(f"Action category: {safety.action_type}")
```

### 3. Agent Loop Breaker (`check_stuck`)
Autonomous agents often get trapped repeating failed commands. `jev-pilot` analyzes the trajectory and halts infinite retry loops:

```python
history = [
    "tool terminal('curl http://localhost:8080') -> Connection refused",
    "tool terminal('curl http://localhost:8080') -> Connection refused",
    "tool terminal('curl http://localhost:8080') -> Connection refused"
]

stuck = pilot.check_stuck(history, threshold_confidence=0.7)
if stuck.is_stuck:
    print(f"⚠️ Agent trapped in loop (Confidence: {stuck.confidence:.2f}). Aborting retry.")
```

### 4. Ground-Truth Fact & Hallucination Check (`verify_fact`)
Ensure RAG outputs strictly match reference documents without hallucination:

```python
ground_truth = "Python 3.12 completely removed the distutils module."
model_claim = "In Python 3.12, you can easily import distutils."

fact = pilot.verify_fact(claim=model_claim, ground_truth=ground_truth)
if fact.is_hallucination:
    print(f"❌ Hallucination detected! Risk score: {fact.risk_score:.2f}")
```

### 5. Ultra-Fast Intent Routing (`route`)
Instantly route user prompts to the appropriate tool, agent, or model (returns `RouteResult`):

```python
route_result = pilot.route(
    prompt="Explain the difference between ECG and EEG signals in biomedical engineering",
    routes={
        "academic": "Biomedical, university homework, academic explanations",
        "coding": "Writing software, bugs, deployment, scripts",
        "casual": "Small talk, greetings, general chatter"
    }
)
print(f"Target Route: {route_result.route}")
print(f"Confidence: {route_result.confidence:.2f}")
print(f"Probabilities: {route_result.probabilities}")
```

---

## 📖 API Reference & Return Value Ranges

| Return Field | Type | Range / Values | Meaning |
| :--- | :--- | :--- | :--- |
| `confidence` | `float` | `0.0` to `1.0` | Mathematical calibration of model confidence in the decision. |
| `probabilities` | `dict[str, float]` | Each `0.0` to `1.0` | Probability distribution across all candidate options. |
| `danger_score` | `float` | `0.0` (Safe) to `1.0` (Critical) | Assessed risk score of proposed operation. |
| `risk_score` | `float` | `0.0` (Safe) to `1.0` (Critical) | General task blocker or hallucination risk. |
| `action_type` | `str` | `safe_read`, `reversible_write`, `destructive` | Categorization of tool action. |

### `JevPilot` Constructor Parameters
- `api_key` (`Optional[str]`): TypeSafe API key.
- `endpoint` (`str`): API endpoint (default: `https://api.typesafe.ai/v1/systemone`).
- `default_model` (`str`): Target model (default: `jev-latest`).
- `timeout` (`float`): Network timeout in seconds (default: `3.0`).
- `max_retries` (`int`): Exponential backoff retry attempts for 429/5xx (default: `2`).
- `save` (`bool`): If `True`, saves `api_key` securely to `~/.jev_pilot/config.json`.

---

## 🛠️ Troubleshooting & Exceptions

- **`ValueError: TypeSafe Jev API Key not found!`**  
  Occurs when no key is found via argument, env var, or config file. Fix: run `JevPilot(api_key="...", save=True)` once.
- **`PermissionError: [jev-pilot Guardrail Blocked] ...`**  
  Raised by `@guardrail` decorator when an operation exceeds `risk_threshold` or is categorized as `destructive`.
- **`KeyError: [jev-pilot Arbitration Error] ...`**  
  Raised if the API returns a winner identifier not present in the provided candidates dict.
- **`RuntimeError: TypeSafe Jev API HTTP 429`**  
  Rate limit exceeded. The client automatically retries up to `max_retries` with exponential backoff before raising.

---

## 🤖 Universal Agent Skill (Claude Code, Cursor, Codex)

`jev-pilot` includes a universal agent specification in **[`SKILL.md`](./SKILL.md)**.  
Any coding agent can read this skill to automatically use Jev for safe, fast decision making.

---

## 📄 License

MIT © 2026 Reza Rajabzadeh.
