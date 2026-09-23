import functools
from typing import Callable, Any, Optional, Dict
from .client import JevPilot

_default_pilot: Optional[JevPilot] = None

def get_default_pilot() -> JevPilot:
    global _default_pilot
    if _default_pilot is None:
        _default_pilot = JevPilot()
    return _default_pilot

def guardrail(system_state_fn: Optional[Callable[..., str]] = None, risk_threshold: float = 0.6):
    """
    Decorator for tool/command execution functions.
    Blocks execution if Jev detects high risk or destructive consequences.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            pilot = get_default_pilot()
            action_desc = f"Call {func.__name__} with args={args}, kwargs={kwargs}"
            state_desc = system_state_fn(*args, **kwargs) if system_state_fn else "Standard application runtime"
            
            check = pilot.guard(action_desc, state_desc, risk_threshold=risk_threshold)
            if not check.allowed:
                raise PermissionError(
                    f"[jev-pilot Guardrail Blocked] Dangerous action detected: '{action_desc}'. "
                    f"Action type: '{check.action_type}', Danger score: {check.danger_score:.2f}"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator

def best_of_n(context_extractor: Optional[Callable[..., str]] = None):
    """
    Decorator for functions that generate multiple candidate solutions.
    Takes a dict/list of candidates and returns the winning candidate picked by Jev.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            candidates = func(*args, **kwargs)
            if not isinstance(candidates, dict):
                if isinstance(candidates, list):
                    candidates = {f"candidate_{i+1}": str(c) for i, c in enumerate(candidates)}
                else:
                    return candidates

            pilot = get_default_pilot()
            ctx = context_extractor(*args, **kwargs) if context_extractor else "Candidate evaluation"
            decision = pilot.arbitrate(context=ctx, candidates=candidates)
            return {
                "winner_key": decision.winner,
                "winner_content": candidates.get(decision.winner),
                "decision": decision
            }
        return wrapper
    return decorator

def loop_breaker(max_stuck_threshold: float = 0.8):
    """
    Decorator to wrap agent step/loop runners.
    Raises RuntimeError if Jev detects the agent is stuck in an infinite unproductive loop.
    """
    def decorator(func: Callable):
        trajectory = []
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            step_record = f"Step args={args}, kwargs={kwargs}"
            trajectory.append(step_record)
            
            if len(trajectory) >= 3:
                pilot = get_default_pilot()
                stuck = pilot.check_stuck(trajectory[-5:])
                if stuck.is_stuck and stuck.confidence >= max_stuck_threshold:
                    raise RuntimeError(
                        f"[jev-pilot Loop Breaker] Agent detected stuck in loop! "
                        f"Confidence: {stuck.confidence:.2f}, Risk: {stuck.risk_score:.2f}. Aborting execution."
                    )
            return func(*args, **kwargs)
        return wrapper
    return decorator
