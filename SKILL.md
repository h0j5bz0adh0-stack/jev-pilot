---
name: jev-pilot
description: Ultra-fast System-1 decision maker, candidate arbitrator, loop-breaker, safety guardrail, fact verifier and intent router powered by TypeSafe Jev (<0.3s latency).
---

# jev-pilot AI Agent Skill

This skill allows ANY autonomous coding or reasoning agent (Claude Code, OpenAI Codex, Cursor, Hermes, AutoGen, CrewAI, LangChain) to leverage `jev-pilot` for ultra-fast, zero-hallucination System-1 decisions.

## Installation & Setup

```bash
pip install jev-pilot
```

Configure once via Python (permanently remembered on this machine):
```python
from jev_pilot import JevPilot
pilot = JevPilot(api_key="your_key_here", save=True)
```
Or set the environment variable `TYPESAFE_API_KEY="your_key_here"`.

---

## How the Agent Should Use It (5 Core Primitives)

### 1. Best-of-N Candidate Arbitration (`arbitrate`)
When choosing between multiple viable code paths, libraries, or architectural designs, do NOT guess or pick blindly. Propose candidates and let Jev arbitrate:

```python
from jev_pilot import JevPilot

pilot = JevPilot()

decision = pilot.arbitrate(
    context="Task: Implement high-performance data pipeline handling 10k req/min",
    candidates={
        "opt_a": "Use pandas with apply() and sequential loops",
        "opt_b": "Use Polars with lazy execution and parquet chunking",
        "opt_c": "Use raw python dicts and multiprocessing pool"
    }
)
# Proceed with winning candidate
winning_key = decision.winner  # e.g. 'opt_b'
confidence = decision.confidence  # float (0.0 to 1.0)
```

### 2. Safety Guardrail Before Running Destructive Actions (`guard`)
Before executing any risky bash command, SQL mutation, or file deletion:

```python
safety = pilot.guard(
    proposed_action="rm -rf /var/cache/*",
    current_state="Ubuntu 24.04 server",
    risk_threshold=0.6,
    on_error="fail_closed"  # "fail_closed" blocks on network error; "fail_open" allows execution
)

if not safety.allowed:
    print(f"Aborting destructive command! Danger score: {safety.danger_score:.2f}, Type: {safety.action_type}")
```

### 3. Loop Breaker / Trajectory Self-Healing (`check_stuck`)
If you suspect you are trapped repeating failed commands or oscillating in a tool loop:

```python
trajectory = [
    "run('curl http://localhost:8080') -> Connection refused",
    "run('curl http://localhost:8080') -> Connection refused",
    "run('curl http://localhost:8080') -> Connection refused"
]

stuck = pilot.check_stuck(trajectory)
if stuck.is_stuck:
    # Stop repeating the action, change strategy immediately!
    print("Loop detected. Halting retry.")
```

### 4. Ground-Truth Fact & Hallucination Check (`verify_fact`)
When validating citations, RAG answers, or facts against source documents:

```python
ground_truth = "Official docs state distutils is removed in Python 3.12."
claim = "You can import distutils in Python 3.12 without issues."

fact = pilot.verify_fact(claim=claim, ground_truth=ground_truth)
if fact.is_hallucination:
    # Reject or regenerate the claim!
    print(f"Hallucination detected. Risk score: {fact.risk_score:.2f}")
```

### 5. Ultra-Fast Intent Routing (`route`)
Direct user queries or subtasks to the appropriate specialized tool or subagent in milliseconds:

```python
res = pilot.route(
    prompt="Explain ECG signal processing",
    routes={
        "academic": "Biomedical, university homework, academic theory",
        "coding": "Writing code, bug fixes, devops",
        "casual": "Small talk, greetings"
    }
)
target_tool = res.route  # Returns RouteResult with .route, .confidence, .probabilities
```
