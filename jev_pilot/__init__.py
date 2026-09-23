"""
jev-pilot: Fast System-1 Decision, Arbitration & Safety Engine for AI Agents.
Works with any LLM (Claude, GPT, Gemini, Llama, Hermes, DeepSeek).
"""

from .client import JevPilot, DecisionResult, SafetyResult, StuckResult, FactResult
from .decorators import guardrail, best_of_n, loop_breaker

__version__ = "0.1.0"
__all__ = [
    "JevPilot",
    "DecisionResult",
    "SafetyResult",
    "StuckResult",
    "FactResult",
    "guardrail",
    "best_of_n",
    "loop_breaker"
]
