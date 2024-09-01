# بوت الذكاء الاصطناعي على تيليجرام

هذا المشروع عبارة عن بوت ذكاء اصطناعي لتيليجرام يستخدم نموذج Gemini من Google لتوفير ردود ذكية على رسائل المستخدمين. البوت قادر على التعامل مع النصوص والصور، ويقدم إجابات مخصصة بناءً على مجموعة من التعليمات المحددة مسبقًا.

## الميزات الرئيسية

- الرد على الرسائل النصية باستخدام نموذج Gemini
- تحليل وتفسير الصور المرسلة
- الحفاظ على سياق المحادثة لكل مستخدم
- دعم اللغة العربية
- توجيه إسلامي وثقافي في الردود

## المتطلبات

- Python 3.7+
- مكتبات Python: `python-telegram-bot`, `google-generativeai`, `Pillow`, `requests`
- مفتاح API لـ Telegram Bot
- مفتاح API لـ Google Gemini

## التثبيت

1. قم بنسخ المستودع:
   ```
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. قم بتثبيت المكتبات المطلوبة:
   ```
   pip install python-telegram-bot google-generativeai Pillow requests
   ```

3. قم بإنشاء ملف `.env` في المجلد الرئيسي وأضف مفاتيح API الخاصة بك:
   ```
   TELEGRAM_TOKEN=your_telegram_token
   GEMINI_API_KEY=your_gemini_api_key
   ```

## الاستخدام

1. قم بتعديل المتغيرات `TELEGRAM_TOKEN` و `GEMINI_API_KEY` في الكود باستخدام مفاتيح API الخاصة بك.

2. قم بتشغيل البوت:
   ```
   python telegram_ai_bot.py
   ```

3. ابدأ محادثة مع البوت على تيليجرام باستخدام الأمر `/start`.

## التخصيص

يمكنك تعديل التعليمات المخصصة للبوت في المتغير `custom_instructions` لتغيير سلوك البوت وطريقة رده.

## المساهمة

نرحب بالمساهمات! يرجى إرسال pull requests أو فتح issues لأي اقتراحات أو تحسينات.

## الترخيص

هذا المشروع مرخص تحت [MIT License](LICENSE).

## الاتصال

للمزيد من المعلومات، يمكنك التواصل مع المطور [فارس عبد الرؤوف](https://github.com/farsabdraouf).

---

تم إنشاء هذا المشروع بواسطة [فارس عبد الرؤوف](https://fars-dev.online/) 🧑‍💻