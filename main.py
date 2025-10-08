from telegram import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Update,
    WebAppInfo
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import json
import html
import re

# === CONFIG ===
BOT_TOKEN = "8336822306:AAH8dJ9bfNCrwEmpF8TOSNpviSuqWxwsuDs"
CHANNEL_ID = "-1003115930403"
WEBAPP_URL = "https://telegram-bot-zeta-snowy.vercel.app"  # your frontend form URL

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
        keyboard = InlineKeyboardMarkup([[ 
            InlineKeyboardButton(
                text="📝 Open Job Form",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]])
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

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
