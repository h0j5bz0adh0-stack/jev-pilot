# jev-pilot ⚡

> **Fast System-1 Decision, Arbitration & Safety Engine for AI Agents**  
> Works with any LLM: Claude, GPT, Gemini, Llama, Hermes, DeepSeek.

**[🇮🇷 راهنمای ساده فارسی](./README.fa.md)**

[![PyPI Version](https://img.shields.io/pypi/v/jev-pilot.svg)](https://pypi.org/project/jev-pilot/)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📦 1. Install

```bash
pip install jev-pilot
```

## 🚀 2. Quickstart

Get a free key at [console.typesafe.ai](https://console.typesafe.ai).  
Pass your key with `save=True` once — it is remembered permanently on your machine:

```python
from jev_pilot import JevPilot

# Run once with your key:
pilot = JevPilot(api_key="your_key_here", save=True)

# 1. Pick the best solution (Best-of-N in 0.3s):
decision = pilot.arbitrate(
    context="Build a high-performance web crawler",
    candidates={
        "opt_a": "Requests with for loops",
        "opt_b": "Asyncio + aiohttp",
        "opt_c": "Scrapling framework"
    }
)
print(f"Winner: {decision.winner}")

# 2. Block dangerous commands:
safety = pilot.guard("rm -rf /var/lib/mysql/*", "Production database")
if not safety.allowed:
    print("Action blocked for safety!")
```

From now on, in any script or agent you can simply call:
```python
pilot = JevPilot()
```

---

## 📄 License

MIT © 2026 Reza Rajabzadeh.
