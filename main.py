from flask import Flask, request
from telegram import (
    Bot,
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)
from telegram.ext import (
    Dispatcher,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import os
import json
import html
import re

# === CONFIG ===
BOT_TOKEN = os.getenv("BOT_TOKEN", "8336822306:AAH8dJ9bfNCrwEmpF8TOSNpviSuqWxwsuDs")
CHANNEL_ID = "-1003115930403"
WEBAPP_URL = "https://telegram-bot-zeta-snowy.vercel.app/"

bot = Bot(BOT_TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, use_context=True)

# === HELPERS ===
def clean_description(html_text):
    text = re.sub(r"<[^>]+>", "", html_text or "")
    text = html.unescape(text)
    return text.strip()

# === HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Post a Job", "My Company"],
        ["My Job Posts", "My Wallet"],
        ["Settings"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("👋 Welcome! Please choose an option:", reply_markup=reply_markup)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Post a Job":
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("📝 Open Job Form", web_app=WebAppInfo(url=WEBAPP_URL))]])
        await update.message.reply_text("Click below to fill out the job form:", reply_markup=keyboard)
    else:
        await update.message.reply_text(f"You selected: {text}")

async def handle_webapp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📬 WebApp handler triggered!")
    web_app_data = update.message.web_app_data
    if web_app_data:
        try:
            print("📥 Received WebApp data:", web_app_data.data)
            data = json.loads(web_app_data.data)
            description = clean_description(data.get("description", ""))

            message = (
                f"📢 *New Job Posted!*\n\n"
                f"💼 *{data.get('job_title', 'N/A')}*\n"
                f"🏷 *Type:* {data.get('job_type', 'N/A')}\n"
                f"📂 *Sector:* {data.get('job_sector', 'N/A')}\n"
                f"🎓 *Education:* {data.get('education', 'N/A')}\n"
                f"💡 *Experience:* {data.get('experience', 'N/A')}\n"
                f"⚧ *Gender:* {data.get('gender', 'N/A')}\n"
                f"🛠 *Skills:* {data.get('skills', 'N/A')}\n"
                f"💰 *Salary:* {data.get('salary', 'N/A')} {data.get('currency', '')}\n"
                f"🌍 *Location:* {data.get('city', 'N/A')}, {data.get('country', 'N/A')}\n\n"
                f"📝 *Description:*\n{description}"
            )

            await context.bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")
            await update.message.reply_text("✅ Job posted successfully to the channel!")
        except Exception as e:
            print("❌ Error posting job:", e)
            await update.message.reply_text("⚠️ Error while posting job. Please check your data.")
    else:
        print("⚠️ No WebApp data found in update.")

# === SETUP DISPATCHER ===
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
dispatcher.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp))

# === FLASK ROUTES ===
@app.route('/')
def home():
    return "🤖 Bot is running via webhook!", 200

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok", 200

# === RUN SERVER LOCALLY ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))