from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Main menu with 5 buttons
    keyboard = [
        ["Post a Job", "My Company"],
        ["My Job Posts", "My Wallet"],
        ["Settings"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Welcome! Please choose an option:",
        reply_markup=reply_markup
    )

# Handle text menu selections
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Post a Job":
        # Inline button opens your Netlify form
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                text="📋 Open Job Form",
                web_app=WebAppInfo(url="https://scintillating-taffy-7d1644.netlify.app")
            )]
        ])
        await update.message.reply_text("Click below to fill the job form:", reply_markup=keyboard)

    else:
        await update.message.reply_text(f"You selected: {text}")

# Handle WebApp form submission
async def handle_webapp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.web_app_data:
        data = json.loads(update.message.web_app_data.data)
        await update.message.reply_text(
            f"✅ Job received!\n\n"
            f"📌 Title: {data.get('job_title', 'N/A')}\n"
            f"🌍 Location: {data.get('city', 'N/A')}, {data.get('country', 'N/A')}\n"
            f"💰 Salary: {data.get('salary', 'N/A')} {data.get('currency', '')}"
        )
        # 👉 Here you can save data to a database or file

def main():
    app = Application.builder().token("8336822306:AAH8dJ9bfNCrwEmpF8TOSNpviSuqWxwsuDs").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp))

    app.run_polling()

if __name__ == "__main__":
    main()
