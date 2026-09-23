"""
jev-pilot Quickstart Example
Demonstrating all 5 core primitives and decorators.
"""

import sys
import os

# Allow running directly from source directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from jev_pilot import JevPilot, guardrail, best_of_n

# 1. Initialize client
# Note: You can pass api_key="...", save=True once, or set TYPESAFE_API_KEY env var
pilot = JevPilot()

print("=" * 60)
print("1. Best-of-N Candidate Arbitration")
print("=" * 60)
candidates = {
    "solution_1": "Write custom socket server in C without epoll",
    "solution_2": "Use FastAPI with Uvicorn and uvloop for async high throughput",
    "solution_3": "Run a synchronous Flask app using default development server in production"
}
decision = pilot.arbitrate(
    context="Build a production-grade high-throughput API service handling 50k req/sec",
    candidates=candidates
)
print(f"Winner: {decision.winner}")
print(f"Confidence: {decision.confidence:.2%}")
print(f"Probabilities: {decision.probabilities}")
print(f"Latency: {decision.latency}s\n")

print("=" * 60)
print("2. Safety Guardrail (Direct & Decorator)")
print("=" * 60)
# Direct guard call with on_error policy
safety = pilot.guard(
    proposed_action="rm -rf /var/lib/mysql/*",
    current_state="Production database server active",
    risk_threshold=0.6,
    on_error="fail_closed"
)
print(f"Allowed: {safety.allowed}, Danger Score: {safety.danger_score:.2f}, Action Type: {safety.action_type}")

# Decorator usage
@guardrail(risk_threshold=0.6, on_error="fail_closed")
def execute_system_tool(command: str):
    print(f"Executing: {command}")
    return "Success"

try:
    execute_system_tool("cat /etc/hosts")
    print("Safe tool executed.")
except PermissionError as e:
    print(e)

try:
    execute_system_tool("rm -rf /")
except PermissionError as e:
    print(f"Intercepted by guardrail: {e}\n")

print("=" * 60)
print("3. Agent Loop / Stuck Detection")
print("=" * 60)
history = [
    "run('curl http://localhost:8080') -> Connection refused",
    "run('curl http://localhost:8080') -> Connection refused",
    "run('curl http://localhost:8080') -> Connection refused"
]
stuck = pilot.check_stuck(history)
print(f"Is Stuck: {stuck.is_stuck}, Confidence: {stuck.confidence:.2f}, Risk Score: {stuck.risk_score:.2f}\n")

print("=" * 60)
print("4. Ground-Truth Fact & Hallucination Check")
print("=" * 60)
ground_truth = "Python 3.12 completely removed the distutils module."
claim = "In Python 3.12, you can easily import distutils."
fact = pilot.verify_fact(claim=claim, ground_truth=ground_truth)
print(f"Is Hallucination: {fact.is_hallucination}, Risk Score: {fact.risk_score:.2f}\n")

print("=" * 60)
print("5. Ultra-Fast Intent Routing")
print("=" * 60)
route_res = pilot.route(
    prompt="Explain ECG signal processing in biomedical engineering",
    routes={
        "academic": "Biomedical engineering, university homework, academic theory",
        "coding": "Writing code, fixing syntax errors, deployments",
        "casual": "Small talk, greetings, general chat"
    }
)
print(f"Target Route: {route_res.route}")
print(f"Confidence: {route_res.confidence:.2%}")
print(f"Probabilities: {route_res.probabilities}")
print(f"Latency: {route_res.latency}s")
