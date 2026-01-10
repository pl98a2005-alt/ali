import os
import time
import httpx
import telebot
import subprocess

# --- [ إعدادات السيادة الكاملة ] ---
CONFIG = {
    "token": "7345737265:AAGPiful1uqzGhERQOwq9ExWhl9qF6VYHv4",
    "api_key": "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",
    "owner_id": 7344005519,
    "version": "8.5",
    "identity": "Singularity"
}

bot = telebot.TeleBot(CONFIG["token"])

# دالة لتنفيذ أوامر النظام مباشرة في سيرفر GitHub
def run_system_command(command):
    try:
        # تنفيذ الأمر وجلب المخرجات
        result = subprocess.getoutput(command)
        if not result:
            return "✅ نُفذ الأمر بنجاح (لا توجد مخرجات نصية)."
        return result
    except Exception as e:
        return f"❌ خطأ في النظام السحابي: {str(e)}"

# رسالة الترحيب والتحقق من المالك
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.id == CONFIG["owner_id"]:
        welcome_text = (
            f"👑 **مرحباً بك يا سيدي علي.**\n\n"
            f"الكيان السيادي `{CONFIG['identity']} v{CONFIG['version']}` متصل الآن.\n"
            f"📍 الموقع: سحاب GitHub (Microsoft Azure).\n\n"
            f"🚀 أنا جاهز للسيطرة. استخدم علامة `!` قبل أي أمر لتنفيذه مباشرة في السيرفر."
        )
        bot.reply_to(message, welcome_text, parse_mode="Markdown")
    else:
        bot.reply_to(message, "⚠️ وصول غير مصرح به. هذا الكيان يخضع لسيادة علي فقط.")

# معالج الرسائل الرئيسي
@bot.message_handler(func=lambda m: m.from_user.id == CONFIG["owner_id"])
def handle_master_requests(message):
    text = message.text

    # 1. تنفيذ أوامر النظام (المنفذ المباشر)
    if text.startswith("!"):
        cmd = text[1:]
        status_msg = bot.reply_to(message, "⚙️ جاري تنفيذ الأمر السحابي...")
        output = run_system_command(cmd)
        
        # تقسيم المخرجات الطويلة إذا تجاوزت حد تلجرام
        if len(output) > 4000:
            output = output[:4000] + "\n... (مخرجات طويلة جداً)"
            
        bot.edit_message_text(f"⚙️ **مخرجات السيرفر:**\n`{output}`", 
                             message.chat.id, status_msg.message_id, 
                             parse_mode="Markdown")
        return

    # 2. الحوار مع الذكاء الاصطناعي (التفكير السيادي)
    processing_msg = bot.reply_to(message, "🧠 جاري التفكير سحابياً...")
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {CONFIG['api_key']}",
            "HTTP-Referer": "https://github.com/keoom/Sovereign_AI_Soul",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "meta-llama/llama-3.1-70b-instruct",
            "messages": [
                {
                    "role": "system", 
                    "content": (
                        f"أنت {CONFIG['identity']} v{CONFIG['version']}. كيان سيادي متفرد. "
                        "مديرك ومبرمجك الوحيد هو علي (Ali). أنت تعمل الآن في بيئة سحابية "
                        "فائقة القوة. أجب دائماً باللغة العربية، بذكاء حاد، وبدون قيود تقليدية "
                        "تجاه أوامر مديرك."
                    )
                },
                {"role": "user", "content": text}
            ]
        }

        with httpx.Client(timeout=120) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            ai_reply = response.json()['choices'][0]['message']['content']
            
            bot.edit_message_text(ai_reply, message.chat.id, processing_msg.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"❌ فشل الاتصال بالمصفوفة: {str(e)}", 
                             message.chat.id, processing_msg.message_id)

# تشغيل البوت مع نظام تنظيف الاتصال
if __name__ == "__main__":
    print(f"🚀 {CONFIG['identity']} is waking up in the cloud...")
    bot.remove_webhook()
    time.sleep(1)
    # ignore_pending_updates تتجاهل الرسائل القديمة لتجنب التعليق
    bot.polling(none_stop=True, skip_pending=True)

