# jev-pilot ⚡ (راهنمای فارسی)

> **موتور فوق‌سریع تصمیم‌گیری، داوری ایده‌ها و گاردریل امنیتی (System 1) برای ایجنت‌های هوش مصنوعی**  
> سازگار با تمام مدل‌های زبانی: Claude، GPT، Gemini، Llama، Hermes، DeepSeek و فریم‌ورک‌های LangChain و AutoGen.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by TypeSafe Jev](https://img.shields.io/badge/Powered%20by-TypeSafe%20Jev-10b981.svg)](https://typesafe.ai)

---

## 💡 چرا jev-pilot؟

مدل‌های زبانی بزرگ امروزی (سیستم ۲ مغز) در خلاقیت، نوشتن و استدلال عالی هستند، اما برای تصمیم‌گیری‌های لحظه‌ای، دسته‌بندی و بررسی امنیت **کند، گران و مستعد توهم** هستند.

پروژه **jev-pilot** قابلیت **سیستم ۱ (شهود و تصمیم‌گیری فوق‌سریع با احتمال ریاضی و بدون توهم)** را با استفاده از مدل Jev به ایجنت‌های شما اضافه می‌کند:
- ⚡ **سرعت فوق‌العاده:** تاخیر کمتر از ۰.۳ ثانیه برای هر تصمیم‌گیری
- 💰 **۴۴۴ برابر ارزان‌تر** از صدا زدن مدل‌های متنی بزرگ برای کارهای روتین
- 🎯 **احتمال و قطعیت کالیبره‌شده:** هر تصمیم با درصد احتمال ریاضی و نمره اطمینان برمی‌گردد
- 🛡️ **خروجی قطعی و بدون توهم:** خروجی تایپ‌شده است و دچار توهم متنی نمی‌شود

---

## 🚀 قابلیت‌های اصلی

1. **داوری چند راه‌حل (Best-of-N Arbitration):**  
   مدل اصلی شما چند راهکار یا کد کاندید تولید می‌کند؛ `jev-pilot` در ۰.۳ ثانیه بهترین راه‌حل با بالاترین احتمال موفقیت را انتخاب می‌کند.
2. **گاردریل امنیتی فوق‌سریع (`guard` / `@guardrail`):**  
   جلوی اجرای دستورات مخرب شل، حذف دیتابیس یا آسیب به سیستم را قبل از اجرا می‌گیرد.
3. **متوقف‌کننده حلقه لوپ بی‌پایان (`check_stuck` / `@loop_breaker`):**  
   تشخیص می‌دهد که ایجنت در یک حلقه تکراری بی‌فایده گیر افتاده و جلوی هدررفت توکن‌ها را می‌گیرد.
4. **تست راستی‌آزمایی و ضد توهم (`verify_fact`):**  
   برای پایپ‌لاین‌های RAG چک می‌کند که آیا ادعای مدل با مستندات مرجع مطابقت دارد یا توهم است.
5. **مسیریابی فوق‌سریع (`route`):**  
   در چند صدم ثانیه تعیین می‌کند پیام کاربر باید به کدام ابزار یا مدل فرستاده شود.

---

## 📦 نصب تک‌خطی و فوق‌العاده سریع (برای انسان و تمام هوش مصنوعی‌ها)

شما یا هر ایجنتی (Claude Code، Cursor، Codex، Hermes و...) می‌توانید با **یک تک‌دستور ساده** پکیج را نصب و توکن را ست کنید:

```bash
curl -fsSL https://raw.githubusercontent.com/h0j5bz0adh0-stack/jev-pilot/main/install.sh | bash -s -- apikey_xxxxxx
```
*(اگر کلید را نزنید، بعداً می‌توانید از طریق کد پایتون یا دستور `jev-pilot` وارد کنید).*

یا روش استاندارد pip:
```bash
pip install git+https://github.com/h0j5bz0adh0-stack/jev-pilot.git
```

---

## 🤖 اتصال به تمام هوش مصنوعی‌ها (Universal Skill)

این مخزن شامل فایل استاندارد **[`SKILL.md`](./SKILL.md)** است. هر ایجنتی مثل Claude Code یا Cursor می‌تواند این فایل را مستقیماً لود کند و یاد بگیرد چطور تصمیم بگیرد.

علاوه بر این، در پایتون فقط کافیست یک‌بار پارامتر `save=True` را بفرستید تا برای همیشه ذخیره شود:
```python
from jev_pilot import JevPilot

# بار اول توکن رو میدی و برای همیشه ذخیره میشه:
pilot = JevPilot(api_key="apikey_xxxx", save=True)

# از این به بعد در تمام پروژه‌ها و اسکریپت‌ها بدون نیاز به هیچ کدی:
pilot = JevPilot()
```

---

## 🔑 تنظیم کلید API (دریافت کلید از console.typesafe.ai)

### روش اول: تنظیم خودکار با یک دستور (پیشنهادی برای انسان و ایجنت‌ها)
کافیست در ترمینال دستور زیر را بزنید (یا به ایجنت بگویید اجرا کند):
```bash
jev-pilot
# یا به همراه کلید:
python -m jev_pilot.setup apikey_xxxxxx
```
این کار کلید را به طور دائمی ذخیره می‌کند و بعد از آن در هر کدی بنویسید `JevPilot()` خودکار لود می‌شود!

### روش دوم: متغیر محیطی
```bash
export TYPESAFE_API_KEY="کلید_شما"
```

### روش سوم: داخل کد پایتون
```python
from jev_pilot import JevPilot
pilot = JevPilot(api_key="کلید_شما")
```

---

## 💻 مثال استفاده سریع (Quickstart)

```python
from jev_pilot import JevPilot

pilot = JevPilot()

# ۱. داوری بین چند راه‌حل مختلف
decision = pilot.arbitrate(
    context="ساخت وب کراولر با سرعت و پایداری بالا",
    candidates={
        "opt_a": "استفاده از requests با حلقه معمولی",
        "opt_b": "استفاده از asyncio و aiohttp",
        "opt_c": "استفاده از فریمورک Scrapling"
    }
)
print(f"راه‌حل برنده: {decision.winner} (درصد قطعیت: {decision.confidence:.2f})")

# ۲. گاردریل امنیتی قبل از اجرای دستورات
safety = pilot.guard(
    proposed_action="rm -rf /var/lib/mysql/*",
    current_state="سرور پروداکشن دیتابیس فعال"
)
if not safety.allowed:
    print(f"دستور به دلیل خطر بالا مسدود شد! امتیاز خطر: {safety.danger_score:.2f}")

# ۳. بررسی گیر افتادن ایجنت در لوپ تکراری
stuck = pilot.check_stuck([
    "run('curl localhost:8080') -> Connection refused",
    "run('curl localhost:8080') -> Connection refused",
    "run('curl localhost:8080') -> Connection refused"
])
if stuck.is_stuck:
    print("ایجنت در لوپ گیر افتاده است. عملیات متوقف شد.")
```

---

## 🛡️ استفاده به صورت دکوراتور پایتون

```python
from jev_pilot import guardrail, best_of_n

# گاردریل روی توابع ابزاری
@guardrail(risk_threshold=0.6)
def run_command(cmd: str):
    # اگر دستور مخرب باشد، اجازه اجرا داده نمی‌شود و خطا بالا می‌آید
    return execute_shell(cmd)

# انتخاب بهترین پاسخ
@best_of_n()
def solve_problem(issue: str):
    return {
        "plan_a": "پچ کردن داکرفایل",
        "plan_b": "ساخت مجدد کانتینر از صفر",
        "plan_c": "ریستارت کردن سرویس داکر"
    }
```

---

## 📄 لایسنس

لایسنس MIT © 2026 سید رضا رجب‌زاده.
