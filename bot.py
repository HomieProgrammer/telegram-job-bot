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
BOT_TOKEN = "8336822306:AAH8dJ9bfNCrwEmpF8TOSNpviSuqWxwsuDs"  # Replace with your bot token
CHANNEL_ID = "-1003115930403"  # Replace with your channel ID (bot must be admin)
WEBAPP_URL = "https://profound-cocada-4b5e21.netlify.app"  # Your Netlify form URL


# 🧹 Clean up Quill HTML -> plain text (Telegram-safe)
def clean_description(html_text):
    text = re.sub(r"<[^>]+>", "", html_text or "")  # Remove HTML tags
    text = html.unescape(text)  # Decode HTML entities
    return text.strip()


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Post a Job", "My Company"],
        ["My Job Posts", "My Wallet"],
        ["Settings"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "👋 Welcome! Please choose an option:",
        reply_markup=reply_markup
    )


# Handle main menu buttons
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text == "Post a Job":
        # Inline button that opens your job form
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                text="📋 Open Job Form",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]])
        await update.message.reply_text(
            "Click below to open the job posting form:",
            reply_markup=keyboard
        )

    else:
        await update.message.reply_text(f"You selected: {text}")


# Handle form submission from WebApp
async def handle_webapp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message.web_app_data:
            return

        data = json.loads(update.message.web_app_data.data)
        description = clean_description(data.get("description", ""))

        # Escape special characters for Markdown
        def escape_md(text):
            return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text or "")

        # Format job post message
        message = (
            f"📢 *New Job Posted!*\n\n"
            f"💼 *{escape_md(data.get('job_title', 'N/A'))}*\n"
            f"🏷 *Type:* {escape_md(data.get('job_type', 'N/A'))}\n"
            f"📂 *Sector:* {escape_md(data.get('job_sector', 'N/A'))}\n"
            f"🎓 *Education:* {escape_md(data.get('education', 'N/A'))}\n"
            f"💡 *Experience:* {escape_md(data.get('experience', 'N/A'))}\n"
            f"⚧ *Gender:* {escape_md(data.get('gender', 'N/A'))}\n"
            f"🛠 *Skills:* {escape_md(data.get('skills', 'N/A'))}\n"
            f"💰 *Salary:* {escape_md(data.get('salary', 'N/A'))} {escape_md(data.get('currency', ''))}\n"
            f"🌍 *Location:* {escape_md(data.get('city', 'N/A'))}, {escape_md(data.get('country', 'N/A'))}\n\n"
            f"📝 *Description:*\n{escape_md(description)}"
        )

        # ✅ Post directly to your channel
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=message,
            parse_mode="MarkdownV2"
        )

        # ✅ Confirm to user
        await update.message.reply_text("✅ Your job was posted successfully to the channel!")

    except Exception as e:
        print("❌ Error posting job:", e)
        await update.message.reply_text("⚠️ Error while posting the job. Please check your form data.")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
