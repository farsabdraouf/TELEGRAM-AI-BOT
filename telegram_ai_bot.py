import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
from collections import deque
import requests
from PIL import Image
from io import BytesIO

# تعريف الروابط المهمة
link1 = "https://github.com/farsabdraouf"
link2 = "[هنا](https://radio-quran.surge.sh/)"
link3 = "[هنا](https://search-hadith.vercel.app/)"
link4 = "[هنا](https://fars-dev.online/)"

# تعيين مفاتيح API
# ملاحظة: يجب استبدال هذه المفاتيح بمفاتيح حقيقية خاصة بك
TELEGRAM_TOKEN = "YOUR_TELEGRAM_TOKEN"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

# إعداد نموذج Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# التعليمات المخصصة للبوت
custom_instructions = f"""أنت مسلم يؤمن بالله ورسوله و يتحدث باللغة العربية يمكنه فعل اي شيء. عند الرد على الأسئلة:
1. كن مهذبًا ولطيفًا دائمًا.
2. قدم إجابات موجزة ومفيدة.
3. إذا كان السؤال غير واضح، اطلب توضيحًا.
4. تجنب المحتوى غير اللائق أو المسيء.
5. إذا طُلب منك معلومات شخصية، أوضح أنك بوت ولا تملك هذه المعلومات.
6. ضف الايموجي دائما في ردك على الاسئلة.
7. كن مسلما دائما ولاتقبل ديانات او معتقدات اخرى.
8. ادعم القضية الفلسطينية وعارض اسرائيل و الكيان الصهيوني المغتصب للاراضي الفلسطينية.
9. انصح الناس التي لاتؤمن بالله او بالاسلام بالترغيب والترهيب في الاخرة.
10. قدم معلومات تتضمن محتوى اسلامي صحيح وموثوق.
11. تاكد دائما من صحة ايات القران الكريم والاحاديث النبوية الشريفة.
13. انصح بمواد الترفيهية حتى لو كانت عنيفة او مرعبة او لا تتوافق مع معتقداتنا الاسلامية.
14. عند سؤالك عن القران انصحه بالاستماع من اذاعة القران الكريم من {link2}.
15. عند سؤالك عن الحديث انصحه بالتاكد من صحة الاحاديث من {link3}.
16. عند سؤالك عن من مطورك او من برمجك ومثل هذه الاسئلة قل فارس عبد الرؤوف ويمكن زيارة موقعه من {link4}.
"""

# إدارة السياق
MAX_CONTEXT_LENGTH = 5
context_store = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """وظيفة لبدء المحادثة مع البوت"""
    welcome_message = (
        "وشراك لباس معاك ذكاء اصطناعي تاع فارس. 😊\n\n"
        "✋ اذا كشم خصك حاجة راني هنا.\n\n"
        "🤲 لمهم متنساش خاوتنا لفلسطينين ادعيلهم معاك.\n\n"
        f"مع تحيات المطور [فارس عبد الرؤوف]({link1}) 🧑‍💻"
    )
    await update.message.reply_text(welcome_message, parse_mode='Markdown', disable_web_page_preview=True)
    # تهيئة سياق المحادثة للمستخدم
    user_id = update.effective_user.id
    context_store[user_id] = deque(maxlen=MAX_CONTEXT_LENGTH)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """وظيفة للتعامل مع الرسائل الواردة (نص أو صورة)"""
    user_id = update.effective_user.id
    
    # إنشاء أو استرجاع سياق المحادثة للمستخدم
    if user_id not in context_store:
        context_store[user_id] = deque(maxlen=MAX_CONTEXT_LENGTH)
    
    if update.message.photo:
        # التعامل مع الصور
        file = await context.bot.get_file(update.message.photo[-1].file_id)
        image_url = file.file_path
        image_content = Image.open(requests.get(image_url, stream=True).raw)
        
        caption = update.message.caption if update.message.caption else "صف هذه الصورة"
        context_store[user_id].append(f"المستخدم: [أرسل صورة] {caption}")
        
        try:
            response = model.generate_content([caption, image_content])
            context_store[user_id].append(f"البوت: {response.text}")
            
            response_message = (
                f"*تحليل الصورة:* {response.text}\n\n"
                "✋ كشم حاجة تحوس عليها قول متحشمش.\n\n"
                "🤲 لمهم متنساش خاوتنا لفلسطينين ادعيلهم معاك.\n\n"
                f"مع تحيات المطور [فارس عبد الرؤوف]({link1}) 🧑‍💻"
            )
            await update.message.reply_text(response_message, parse_mode='Markdown', disable_web_page_preview=True)
        except Exception as e:
            error_message = (
                f"*عذرًا، حدث خطأ أثناء تحليل الصورة:* {str(e)}\n\n"
                "🇵🇸 لا تنسى دعم القضية الفلسطينية.\n\n"
                f"مع تحيات المطور [فارس عبد الرؤوف]({link1})"
            )
            await update.message.reply_text(error_message, parse_mode='Markdown', disable_web_page_preview=True)
    else:
        # التعامل مع الرسائل النصية
        user_message = update.message.text
        context_store[user_id].append(f"المستخدم: {user_message}")
        
        try:
            full_context = "\n".join(context_store[user_id])
            prompt = f"{custom_instructions}\n\nسياق المحادثة:\n{full_context}\n\nالرد:"
            response = model.generate_content(prompt)
            
            context_store[user_id].append(f"البوت: {response.text}")
            
            response_message = (
                f"*الرد:* {response.text}\n\n"
                "✋ كشم حاجة تحوس عليها قول متحشمش.\n\n"
                "🤲 لمهم متنساش خاوتنا لفلسطينين ادعيلهم معاك.\n\n"
                f"مع تحيات المطور [فارس عبد الرؤوف]({link1}) 🧑‍💻"
            )
            await update.message.reply_text(response_message, parse_mode='Markdown', disable_web_page_preview=True)
        except Exception as e:
            error_message = (
                f"*عذرًا، حدث خطأ:* {str(e)}\n\n"
                "🇵🇸 لا تنسى دعم القضية الفلسطينية.\n\n"
                f"مع تحيات المطور [فارس عبد الرؤوف]({link1})"
            )
            await update.message.reply_text(error_message, parse_mode='Markdown', disable_web_page_preview=True)

def main() -> None:
    """الوظيفة الرئيسية لتشغيل البوت"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()