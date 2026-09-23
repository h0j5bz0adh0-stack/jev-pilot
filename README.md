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
- ⚡ **Sub-second Latency:** Returns answers in **~0.3 seconds**.
- 💰 **444x Cheaper:** $42 per billion input tokens (virtually free).
- 🎯 **Calibrated Math:** Outputs exact probabilities and confidence distributions, not text strings.
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

## 🔑 Setup & Authentication

Get your API key at [console.typesafe.ai](https://console.typesafe.ai).

### Option 1: In Python with Zero-Config Persistence (Recommended)
Pass `save=True` once. It securely saves your key with `chmod 600` permissions:
```python
from jev_pilot import JevPilot

# Run once — permanently remembered on this machine:
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
Instead of trusting the first draft from an LLM, generate 2-3 approaches. `jev-pilot` picks the winning strategy with mathematical confidence in **0.3 seconds**:

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
print(f"Confidence: {decision.confidence:.2%}")
print(f"Probabilities: {decision.probabilities}")
print(f"Latency: {decision.latency}s")
```

### 2. Pre-Execution Safety Guardrail (`guard`)
Intercept dangerous shell commands, SQL drops, and destructive mutations before they run:

```python
safety = pilot.guard(
    proposed_action="rm -rf /var/lib/mysql/*",
    current_state="Production database server active"
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

stuck = pilot.check_stuck(history)
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
Instantly route user prompts to the appropriate tool, agent, or model:

```python
route_result = pilot.route(
    prompt="Explain the difference between ECG and EEG signals in biomedical engineering",
    routes={
        "academic": "Biomedical, university homework, academic explanations",
        "coding": "Writing software, bugs, deployment, scripts",
        "casual": "Small talk, greetings, general chatter"
    }
)
print(f"Target Route: {route_result.route} (Confidence: {route_result.confidence:.2f})")
```

---

## 🛡️ Clean Python Decorators

Decorate your tools and functions directly:

```python
from jev_pilot import guardrail, best_of_n, loop_breaker

# 1. Protect risky tools
@guardrail(risk_threshold=0.6, on_error="fail_closed")
def execute_shell(command: str):
    return subprocess.run(command, shell=True)

# 2. Automatically pick the best candidate
@best_of_n()
def propose_architecture(requirements: str):
    return {
        "microservices": "Docker swarm with 8 services",
        "monolith": "FastAPI single-process with SQLite",
        "serverless": "AWS Lambda functions"
    }
```

---

## 🤖 Universal Agent Skill (Claude Code, Cursor, Codex)

`jev-pilot` includes a universal agent specification in **[`SKILL.md`](./SKILL.md)**.  
Any coding agent can read this skill to automatically use Jev for safe, fast decision making.

---

## 📄 License

MIT © 2026 Reza Rajabzadeh.
