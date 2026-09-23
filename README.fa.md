# jev-pilot ⚡ (راهنمای جامع فارسی)

> **موتور فوق‌سریع تصمیم‌گیری، داوری ایده‌ها و گاردریل امنیتی (System 1) برای ایجنت‌های هوش مصنوعی**  
> آوردن شهود و تصمیم‌گیری زیر ۰.۳ ثانیه‌ای و بدون توهم به Claude، GPT، Gemini، Llama، Hermes و غیره.

[![PyPI Version](https://img.shields.io/pypi/v/jev-pilot.svg)](https://pypi.org/project/jev-pilot/)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 💡 پکیج jev-pilot دقیقاً چیه و چه دردی رو دوا می‌کنه؟

مدل‌های زبانی بزرگ امروزی (مثل Claude 3.5، GPT-4o یا DeepSeek) در واقع مثل **«سیستم ۲ مغز انسان»** هستند: در تفکر عمیق، خلاقیت، نوشتن مقاله و کدهای پیچیده فوق‌العاده‌ان.

اما استفاده از این مدل‌های غول‌پیکر برای **تصمیم‌گیری‌های آنی و لحظه‌ای درون Agentها** ۳ تا فاجعه درست می‌کنه:
۱. **بسیار کُند:** برای یک تصمیم بله/خیر ساده یا انتخاب ابزار، باید ۳ تا ۱۰ ثانیه معطل توکن‌های استریم بشید.  
۲. **بسیار پرهزینه:** هزاران توکن الکی می‌سوزه فقط برای اینکه بفهمید فلان دستور امنه یا نه.  
۳. **مستعد توهم و تعارف:** مدل‌های متنی به خاطر آموزش با RLHF، گاهی برای جلب رضایت کاربر به جای واقعیت، ادعای غلط رو تایید می‌کنن.

**jev-pilot** نقش **«سیستم ۱ مغز» (شهود سریع، محاسباتی و بدون خطا)** رو به ایجنت‌ها اضافه می‌کنه:
- ⚡ **سرعت فوق‌العاده:** زمان پاسخگویی **حدود ۰.۳ ثانیه** (زیر ۴۰۰ میلی‌ثانیه).
- 💰 **۴۴۴ برابر ارزان‌تر:** حدود ۴۲ دلار برای هر **۱ میلیارد توکن** ورودی (عملاً رایگان).
- 🎯 **احتمال و قطعیت ریاضی:** خروجی متن آزاد نیست؛ درصد احتمال ریاضی کالیبره‌شده است.
- 🛡️ **تضمین صفر توهم:** مدل خروجی متنی پرحرف تولید نمی‌کنه، فقط تصمیمات ساختاریافته میده.

---

## 🧠 معماری سیستم ۱ و سیستم ۲ در ایجنت شما

```
                 [ درخواست کاربر یا اکشن ایجنت ]
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
       [ سیستم ۱: jev-pilot ]        [ سیستم ۲: مدل‌های بزرگ ]
       • مسیریابی فوری (<۰.۳ ثانیه)   • استدلال عمیق و برنامه‌ریزی
       • گاردریل امنیتی ابزارها       • تولید چند راه‌حل مختلف
       • شکستن لوپ‌های خطای تکراری    • نوشتن کدهای طولانی
                │                             │
                └──────────────┬──────────────┘
                               ▼
               [ ایجنت سریع، امن و بدون خطا ]
```

---

## 📦 نحوه نصب

```bash
pip install jev-pilot
```

---

## 🔑 تنظیم کلید API

کلید رایگان خود را از [console.typesafe.ai](https://console.typesafe.ai) دریافت کنید.

فقط **یک‌بار** در پایتون کلید را همراه با `save=True` بدهید؛ برای همیشه با پرمیشن امنیتی `chmod 600` روی سیستمتان ذخیره می‌شود:

```python
from jev_pilot import JevPilot

# یک‌بار اجرا کنید تا برای همیشه روی سیستم ذخیره شود:
pilot = JevPilot(api_key="کلید_شما", save=True)

# از این به بعد در تمام پروژه‌ها و اسکریپت‌ها بدون نیاز به هیچ کدی:
pilot = JevPilot()
```

---

## 🚀 ۵ قابلیت کلیدی با مثال‌های کاربردی

### ۱. داوری چند راه‌حل (Best-of-N Arbitration)
به جای اینکه به اولین کد تولیدشده توسط مدل اعتماد کنید، بگویید ۲ یا ۳ راه‌حل مختلف بدهد. `jev-pilot` در **۰.۳ ثانیه** و با درصد احتمال ریاضی بهترین راهکار را انتخاب می‌کند:

```python
from jev_pilot import JevPilot

pilot = JevPilot()

decision = pilot.arbitrate(
    context="ساخت یک سیستم وب کراولر پرسرعت در پایتون",
    candidates={
        "opt_a": "استفاده از requests با حلقه معمولی",
        "opt_b": "استفاده از asyncio و aiohttp با Connection Pool",
        "opt_c": "استفاده از فریمورک Scrapling با بایپس هوشمند"
    }
)

print(f"راه‌حل برنده: {decision.winner}")
print(f"میزان قطعیت: {decision.confidence:.2%}")
print(f"جدول احتمالات: {decision.probabilities}")
print(f"زمان تصمیم‌گیری: {decision.latency} ثانیه")
```

### ۲. گاردریل امنیتی قبل از اجرای دستورات (`guard`)
قبل از اجرای دستورات حساس شل یا دیتابیس، جلوی خرابکاری را بگیرید:

```python
safety = pilot.guard(
    proposed_action="rm -rf /var/lib/mysql/*",
    current_state="سرور دیتابیس عملیاتی فعال"
)

if not safety.allowed:
    print(f"🚨 دستور خطرناک متوقف شد! امتیاز خطر: {safety.danger_score:.2f}")
    print(f"دسته‌بندی اکشن: {safety.action_type}")
```

### ۳. متوقف‌کننده حلقه لوپ بی‌پایان (`check_stuck`)
ایجنت‌های مستقل گاهی در یک چرخه تکراری خطادار گیر می‌کنند. `jev-pilot` رفتار ایجنت را تحلیل کرده و چرخه را متوقف می‌کند:

```python
history = [
    "tool terminal('curl http://localhost:8080') -> Connection refused",
    "tool terminal('curl http://localhost:8080') -> Connection refused",
    "tool terminal('curl http://localhost:8080') -> Connection refused"
]

stuck = pilot.check_stuck(history)
if stuck.is_stuck:
    print(f"⚠️ ایجنت در لوپ تکراری گیر افتاده (قطعیت: {stuck.confidence:.2f}). توقف عملیات.")
```

### ۴. راستی‌آزمایی فکت‌ها و حذف توهم (`verify_fact`)
برای سیستم‌های RAG بررسی کنید که آیا ادعای مدل با مستندات مرجع مطابقت دارد یا توهم است:

```python
ground_truth = "در پایتون ۳.۱۲ ماژول distutils به طور کامل حذف شده است."
model_claim = "در پایتون ۳.۱۲ می‌توانید به راحتی distutils را ایمپورت کنید."

fact = pilot.verify_fact(claim=model_claim, ground_truth=ground_truth)
if fact.is_hallucination:
    print(f"❌ توهم مدل شناسایی شد! امتیاز ریسک: {fact.risk_score:.2f}")
```

### ۵. مسیریابی فوق‌سریع پیام‌ها (`route`)
در چند میلی‌ثانیه تعیین کنید درخواست کاربر باید به کدام ابزار یا مدل تخصصی فرستاده شود:

```python
route_result = pilot.route(
    prompt="کد پایتون برای الگوریتم مرتب‌سازی سریع بنویس",
    routes={
        "coding": "کدنویسی، اسکریپت، رفع باگ",
        "academic": "مقالات علمی، سوالات دانشگاهی",
        "chat": "چت روزمره و احوال‌پرسی"
    }
)
print(f"مقصد هدایت: {route_result.route}")
```

---

## 🛡️ استفاده به صورت دکوراتور پایتون

```python
from jev_pilot import guardrail, best_of_n

# گاردریل روی توابع ابزاری حساس
@guardrail(risk_threshold=0.6, on_error="fail_closed")
def execute_system_tool(command: str):
    return run_shell(command)

# داوری خودکار روی چند راه‌حل
@best_of_n()
def solve_problem(issue: str):
    return {
        "plan_a": "پچ کردن مستقیم فایل",
        "plan_b": "بیلد مجدد کانتینر",
        "plan_c": "ریستارت سرویس"
    }
```

---

## 📄 لایسنس

لایسنس MIT © 2026 سید رضا رجب‌زاده.
