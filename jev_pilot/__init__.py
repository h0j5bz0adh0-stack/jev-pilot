"""
jev-pilot: Fast System-1 Decision, Arbitration & Safety Engine for AI Agents.
Works with any LLM (Claude, GPT, Gemini, Llama, Hermes, DeepSeek).
"""

from importlib.metadata import version, PackageNotFoundError
from .client import JevPilot, DecisionResult, SafetyResult, StuckResult, FactResult, RouteResult
from .decorators import guardrail, best_of_n, loop_breaker

try:
    __version__ = version("jev-pilot")
except PackageNotFoundError:
    __version__ = "0.1.1"

__all__ = [
    "JevPilot",
    "DecisionResult",
    "SafetyResult",
    "StuckResult",
    "FactResult",
    "RouteResult",
    "guardrail",
    "best_of_n",
    "loop_breaker"
]
