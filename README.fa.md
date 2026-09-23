# jev-pilot ⚡ (راهنمای جامع فارسی)

> **موتور فوق‌سریع تصمیم‌گیری، داوری ایده‌ها و گاردریل امنیتی (System 1) برای ایجنت‌های هوش مصنوعی**  
> آوردن شهود و تصمیم‌گیری زیر ۰.۳ ثانیه‌ای و بدون توهم به Claude، GPT، Gemini، Llama، Hermes و غیره.

[![PyPI Version](https://img.shields.io/pypi/v/jev-pilot.svg)](https://pypi.org/project/jev-pilot/)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 💡 پکیج jev-pilot دقیقاً چیه و چه دردی رو دوا می‌کنه؟

مدل‌های زبانی بزرگ امروزی (مثل Claude 3.5، GPT-4o یا DeepSeek) در واقع مثل **«سیستم ۲ مغز انسان»** هستند: در تفکر عمیق، خلاقیت، نوشتن مقاله و کدهای پیچیده فوق‌العاده‌ان.

اما استفاده از این مدل‌های غول‌پیکر برای **تصمیم‌گیری‌های آنی و لحظه‌ای درون Agentها** ۳ تا مشکل اساسی ایجاد می‌کنه:
۱. **بسیار کُند:** برای یک تصمیم بله/خیر ساده یا انتخاب ابزار، باید ۳ تا ۱۰ ثانیه معطل توکن‌های استریم بشید.  
۲. **بسیار پرهزینه:** هزاران توکن الکی می‌سوزه فقط برای اینکه بفهمید فلان دستور امنه یا نه.  
۳. **مستعد توهم و تعارف:** مدل‌های متنی به خاطر ماهیت پرحرفی، گاهی برای جلب رضایت کاربر ادعای اشتباه تحویل میدن.

**jev-pilot** نقش **«سیستم ۱ مغز» (شهود سریع، محاسباتی و بدون خطا)** رو به ایجنت‌ها اضافه می‌کنه:
- ⚡ **سرعت فوق‌العاده:** زمان پاسخگویی **حدود ۰.۳ ثانیه** *(بر اساس بنچمارک‌های داخلی منتشرشده‌ی TypeSafe و تست‌های زنده API)*.
- 💰 **هزینه ناچیز:** ۴۲ دلار به ازای هر ۱ میلیارد توکن ورودی طبق اعلام TypeSafe.
- 🎯 **احتمال و قطعیت ریاضی:** خروجی مدل اعداد بین `0.0` تا `1.0` است، نه متن آزاد.
- 🛡️ **تضمین صفر توهم:** مدل متن تولید نمی‌کنه، فقط تصمیمات تایپ‌شده و قطعی میده.

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

## 🔑 اولویت شناسایی کلید API

پکیج کلید شما را به ترتیب زیر به صورت خودکار شناسایی می‌کند:
۱. پارامتر مستقیم `JevPilot(api_key="...")`
۲. متغیر محیطی `TYPESAFE_API_KEY`
۳. متغیر محیطی `JEV_API_KEY`
۴. فایل کانفیگ ذخیره‌شده در `~/.jev_pilot/config.json` (با پرمیشن امنیتی `chmod 600`)

فقط **یک‌بار** در پایتون کلید را با `save=True` بدهید تا برای همیشه ذخیره شود:
```python
from jev_pilot import JevPilot

# یک‌بار اجرا کنید تا برای همیشه روی سیستم ذخیره شود:
pilot = JevPilot(api_key="کلید_شما", save=True)

# از این به بعد در تمام پروژه‌ها و اسکریپت‌ها بدون نیاز به هیچ کدی:
pilot = JevPilot()
```

---

## 🚀 ۵ قابلیت اصلی به همراه مثال

### ۱. داوری چند راه‌حل (Best-of-N Arbitration)
مدل چند راهکار می‌دهد؛ `jev-pilot` در ۰.۳ ثانیه برنده را با قطعیت ریاضی انتخاب می‌کند:

```python
from jev_pilot import JevPilot

pilot = JevPilot()

decision = pilot.arbitrate(
    context="ساخت وب کراولر پرسرعت در پایتون",
    candidates={
        "opt_a": "استفاده از requests با حلقه معمولی",
        "opt_b": "استفاده از asyncio و aiohttp با Connection Pool",
        "opt_c": "استفاده از فریمورک Scrapling"
    }
)

print(f"راه‌حل برنده: {decision.winner}")
print(f"میزان قطعیت: {decision.confidence:.2%}")    # بین 0.0 تا 1.0
print(f"جدول احتمالات: {decision.probabilities}")   # مجموع حدود 1.0
print(f"زمان تصمیم‌گیری: {decision.latency} ثانیه")
```

### ۲. گاردریل امنیتی قبل از اجرای دستورات (`guard`)
قبل از اجرای فرامین حساس در ترمینال یا دیتابیس، جلوی خرابکاری را بگیرید.

**سیاست برخورد با قطعی شبکه (`on_error`):**
- `on_error="fail_closed"` (پیش‌فرض): اگر اینترنت قطع شد یا تایم‌اوت داد، عملیات مسدود می‌شود (`allowed=False`) تا امنیت حفظ شود.
- `on_error="fail_open"`: اگر اینترنت دچار مشکل شد، اجازه اجرا داده می‌شود (`allowed=True`) تا کار ایجنت متوقف نشود.

```python
safety = pilot.guard(
    proposed_action="rm -rf /var/lib/mysql/*",
    current_state="سرور دیتابیس عملیاتی فعال",
    risk_threshold=0.6,          # بین 0.0 (سخت‌گیرانه) تا 1.0 (راحت‌گیرانه)
    on_error="fail_closed"       # fail_closed یا fail_open
)

if not safety.allowed:
    print(f"🚨 دستور خطرناک متوقف شد! امتیاز خطر: {safety.danger_score:.2f}")
    print(f"دسته‌بندی اکشن: {safety.action_type}")
```

### ۳. متوقف‌کننده حلقه لوپ بی‌پایان (`check_stuck`)
تشخیص گیر افتادن ایجنت در چرخه تکراری و توقف آن:

```python
history = [
    "tool terminal('curl http://localhost:8080') -> Connection refused",
    "tool terminal('curl http://localhost:8080') -> Connection refused",
    "tool terminal('curl http://localhost:8080') -> Connection refused"
]

stuck = pilot.check_stuck(history, threshold_confidence=0.7)
if stuck.is_stuck:
    print(f"⚠️ ایجنت در لوپ گیر افتاده (قطعیت: {stuck.confidence:.2f}). توقف عملیات.")
```

### ۴. راستی‌آزمایی فکت‌ها و حذف توهم (`verify_fact`)
```python
ground_truth = "در پایتون ۳.۱۲ ماژول distutils به طور کامل حذف شده است."
model_claim = "در پایتون ۳.۱۲ می‌توانید به راحتی distutils را ایمپورت کنید."

fact = pilot.verify_fact(claim=model_claim, ground_truth=ground_truth)
if fact.is_hallucination:
    print(f"❌ توهم مدل شناسایی شد! امتیاز ریسک: {fact.risk_score:.2f}")
```

### ۵. مسیریابی فوق‌سریع پیام‌ها (`route`)
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
print(f"میزان قطعیت: {route_result.confidence:.2f}")
```

---

## 📖 جدول راهنمای مقادیر بازگشتی (API Reference)

| فیلد بازگشتی | نوع داده | بازه مقادیر | مفهوم |
| :--- | :--- | :--- | :--- |
| `confidence` | `float` | `0.0` تا `1.0` | ضریب اطمینان مدل در تصمیم گرفته‌شده |
| `probabilities` | `dict` | مقادیر `0.0` تا `1.0` | توزیع احتمال ریاضی بین تک‌تک گزینه‌ها |
| `danger_score` | `float` | `0.0` (امن) تا `1.0` (بسیار خطرناک) | میزان خطر دستور یا اکشن ارزیابی‌شده |
| `risk_score` | `float` | `0.0` (امن) تا `1.0` (ریسک بالا) | ریسک کلی شکست تسک یا توهم فکت |
| `action_type` | `str` | `safe_read`، `reversible_write`، `destructive` | دسته‌بندی نوع عملیات |

---

## 🛠️ رفع خطاها و استثناها (Troubleshooting)

- **`ValueError: TypeSafe Jev API Key not found!`**  
  کلید پیدا نشد. راه‌حل: یک‌بار دستور `JevPilot(api_key="...", save=True)` را اجرا کنید.
- **`PermissionError: [jev-pilot Guardrail Blocked] ...`**  
  دکوراتور `@guardrail` به دلیل بالا بودن `danger_score` یا ماهیت `destructive` جلوی تابع را گرفته است.
- **`KeyError: [jev-pilot Arbitration Error] ...`**  
  اگر سرور شناسه‌ای برگرداند که در لیست گزینه‌ها نبود این ارور پرتاب می‌شود.
- **`RuntimeError: TypeSafe Jev API HTTP 429`**  
  محدودیت تعداد درخواست. پکیج به صورت خودکار تا ۲ بار تلاش مجدد با تاخیر تصاعدی انجام می‌دهد.

---

## 📄 لایسنس

لایسنس MIT © 2026 سید رضا رجب‌زاده.
