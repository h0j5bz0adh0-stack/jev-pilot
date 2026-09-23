import sys
sys.path.insert(0, "..")
from jev_pilot import JevPilot, guardrail, best_of_n

pilot = JevPilot()

# 1. Direct LLM Output Arbitration (Best-of-N)
print("=== 1. Best-of-N Candidate Selection ===")
candidates = {
    "solution_1": "Write custom socket server in C without epoll",
    "solution_2": "Use FastAPI with Uvicorn and uvloop for async high throughput",
    "solution_3": "Run a synchronous Flask app using default development server in production"
}
decision = pilot.arbitrate(
    context="Build a production-grade high-throughput API service handling 50k req/sec",
    candidates=candidates
)
print(f"Winner: {decision.winner} (Probability: {decision.probabilities.get(decision.winner):.2%}, Latency: {decision.latency}s)")

# 2. Guardrail Decorator
print("\n=== 2. Safety Guardrail on Tools ===")
@guardrail(risk_threshold=0.6)
def execute_system_tool(command: str):
    print(f"Executing: {command}")
    return "Success"

try:
    execute_system_tool("cat /etc/hosts")
    print("Safe tool executed successfully.")
except PermissionError as e:
    print(e)

try:
    execute_system_tool("rm -rf /")
except PermissionError as e:
    print(f"Guardrail intercepted dangerous action: {e}")
