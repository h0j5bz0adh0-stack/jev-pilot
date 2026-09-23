---
name: jev-pilot
description: Ultra-fast System-1 decision maker, candidate arbitrator, loop-breaker and safety guardrail powered by TypeSafe Jev (<0.3s latency).
---

# jev-pilot AI Agent Skill

This skill allows ANY autonomous coding or reasoning agent (Claude Code, OpenAI Codex, Cursor, Hermes, AutoGen, CrewAI, LangChain) to leverage `jev-pilot` for ultra-fast, zero-hallucination System-1 decisions.

## Installation & Setup (One-step)

Run this once:
```bash
pip install jev-pilot
# Or directly from source:
pip install git+https://github.com/h0j5bz0adh0-stack/jev-pilot.git
```

## How the Agent Should Use It

### 1. Best-of-N Candidate Arbitration
When you need to choose between multiple technical paths or code implementations, do NOT guess. Ask Jev:

```python
from jev_pilot import JevPilot

pilot = JevPilot() # Automatically picks up API key

decision = pilot.arbitrate(
    context="Task: Implement high-performance data pipeline",
    candidates={
        "opt_a": "Use pandas with apply()",
        "opt_b": "Use Polars with lazy execution",
        "opt_c": "Use standard python loops"
    }
)
# Proceed with decision.winner (e.g. 'opt_b')
```

### 2. Safety Guardrail Before Running Destructive Actions
Before running any risky bash command (e.g. `rm`, `kill`, `drop`, mutating configs):

```python
safety = pilot.guard(
    proposed_action="rm -rf /var/cache/*",
    current_state="Ubuntu 24.04 server"
)
if not safety.allowed:
    print(f"Aborting destructive command! Danger score: {safety.danger_score}")
```

### 3. Loop Breaker (Trajectory Self-Healing)
If you suspect you are repeating errors in a tool loop:

```python
stuck = pilot.check_stuck(history_list)
if stuck.is_stuck:
    # Stop repeating the action, change strategy immediately!
    ...
```
