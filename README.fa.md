# jev-pilot ⚡ (راهنمای فارسی)

> **موتور فوق‌سریع تصمیم‌گیری و گاردریل امنیتی (System 1) برای تمام ایجنت‌های هوش مصنوعی**  
> سازگار با Claude، GPT، Gemini، Llama، Hermes و غیره.

---

## ۱. نصب

```bash
pip install jev-pilot
```

## ۲. استفاده سریع

کلید رایگان خود را از [console.typesafe.ai](https://console.typesafe.ai) بگیرید.  
فقط بار اول کلید را همراه با `save=True` بدهید تا برای همیشه در سیستمتان ذخیره شود:

```python
from jev_pilot import JevPilot

# اجرای بار اول برای ذخیره کلید:
pilot = JevPilot(api_key="کلید_شما", save=True)

# ۱. انتخاب بهترین راه‌حل در ۰.۳ ثانیه:
decision = pilot.arbitrate(
    context="ساخت وب کراولر با سرعت و پایداری بالا",
    candidates={
        "opt_a": "استفاده از requests با حلقه معمولی",
        "opt_b": "استفاده از asyncio و aiohttp",
        "opt_c": "استفاده از فریمورک Scrapling"
    }
)
print(f"راه‌حل برنده: {decision.winner}")

# ۲. جلوگیری از اجرای دستورات مخرب:
safety = pilot.guard("rm -rf /var/lib/mysql/*", "دیتابیس اصلی سرور")
if not safety.allowed:
    print("دستور به دلیل خطر مسدود شد!")
```

از دفعات بعد در هر برنامه‌ای فقط کافیست بنویسید:
```python
pilot = JevPilot()
```

---

## لایسنس

MIT © 2026 سید رضا رجب‌زاده.
