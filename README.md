# jev-pilot ⚡

> **Fast System-1 Decision, Arbitration & Safety Engine for Autonomous AI Agents**  
> Works with any LLM: Claude, GPT, Gemini, Llama, Hermes, DeepSeek, and custom agent runtimes.

**[🇮🇷 راهنمای فارسی (Persian Documentation)](./README.fa.md)**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by TypeSafe Jev](https://img.shields.io/badge/Powered%20by-TypeSafe%20Jev-10b981.svg)](https://typesafe.ai)

---

## 💡 Why jev-pilot?

Modern LLMs (System 2) are brilliant at creative thought and deep reasoning, but they are **slow, expensive, and prone to hallucinations** when making split-second operational decisions.

**jev-pilot** brings **System 1 (fast, calibrated, zero-hallucination intuition)** to your agents using TypeSafe's Jev model:
- ⚡ **Sub-second latency** (~0.3s per decision)
- 💰 **444x Cheaper** than invoking full LLMs for routing/guardrails
- 🎯 **Calibrated Probabilities**: Every choice comes with mathematical confidence & probability distributions
- 🛡️ **Zero Hallucination Safety**: Output is strictly typed and deterministic

---

## 🚀 Features

1. **Best-of-N Candidate Arbitration (`arbitrate` / `@best_of_n`)**:  
   Have your LLM generate multiple approaches or code snippets. `jev-pilot` picks the winning strategy with highest probability of success in 0.3s.
2. **Sub-second Tool Guardrails (`guard` / `@guardrail`)**:  
   Intercept dangerous shell commands, SQL drops, and destructive mutations before they run.
3. **Agent Loop Breaker (`check_stuck` / `@loop_breaker`)**:  
   Detects when an agent is caught in an unproductive retry loop and aborts early to save tokens.
4. **Factuality & Hallucination Scoring (`verify_fact`)**:  
   Calibrated ground-truth checking for RAG pipelines.
5. **Ultra-Fast Intent Routing (`route`)**:  
   Instantly routes prompts to the specialized model, agent, or tool.

---

## 📦 Installation

```bash
pip install jev-pilot
```

Or install from source:
```bash
git clone https://github.com/h0j5bz0adh0-stack/jev-pilot.git
cd jev-pilot
pip install -e .
```

---

## 🔑 Setup & API Key Configuration

Get your API key at: [https://console.typesafe.ai](https://console.typesafe.ai)

### Option 1: One-liner Setup CLI (Recommended for humans & AI Agents)
Run in terminal (or let your AI coding agent run it):
```bash
jev-pilot
# or: python -m jev_pilot.setup <your_api_key>
```
This saves the key to `~/.jev_pilot/config.json`. Once configured, all agents and code initialize with zero parameters:
```python
from jev_pilot import JevPilot
pilot = JevPilot()  # Automatically picks up saved key!
```

### Option 2: Environment Variable
```bash
export TYPESAFE_API_KEY="your_api_key_here"
```

### Option 3: Direct in Python
```python
from jev_pilot import JevPilot
pilot = JevPilot(api_key="your_api_key_here")
```

```python
from jev_pilot import JevPilot

pilot = JevPilot()

# 1. Best-of-N Arbitration
decision = pilot.arbitrate(
    context="Build high-performance web crawler",
    candidates={
        "opt_a": "Synchronous requests with for-loops",
        "opt_b": "Asyncio + aiohttp connection pooling",
        "opt_c": "Scrapling framework"
    }
)
print(f"Winner: {decision.winner} (Confidence: {decision.confidence:.2f})")

# 2. Fast Safety Guardrail
safety = pilot.guard(
    proposed_action="rm -rf /var/lib/mysql/*",
    current_state="Production database server"
)
if not safety.allowed:
    print(f"Blocked! Danger score: {safety.danger_score:.2f}")

# 3. Detect Stuck Agent Trajectory
stuck = pilot.check_stuck([
    "run('curl http://localhost:8080') -> Connection refused",
    "run('curl http://localhost:8080') -> Connection refused",
    "run('curl http://localhost:8080') -> Connection refused"
])
if stuck.is_stuck:
    print("Agent trapped in loop. Halting.")
```

---

## 🛡️ Decorator Usage

```python
from jev_pilot import guardrail, best_of_n

@guardrail(risk_threshold=0.6)
def run_command(cmd: str):
    # Will raise PermissionError if dangerous
    return execute_shell(cmd)

@best_of_n()
def propose_solutions(user_issue: str):
    return {
        "plan_a": "Patch the dockerfile directly",
        "plan_b": "Rebuild container from scratch",
        "plan_c": "Restart docker daemon"
    }
```

---

## 🧪 Testing

```bash
python3 tests/test_pilot.py
```

All 6 test suites run in ~1.8 seconds.

---

## 📄 License

MIT License © 2026 Reza Rajabzadeh.
