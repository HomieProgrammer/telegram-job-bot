from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Create keyboard with 5 buttons
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

def main():
    app = Application.builder().token("8336822306:AAH8dJ9bfNCrwEmpF8TOSNpviSuqWxwsuDs").build()
    
    app.add_handler(CommandHandler("start", start))
    
    app.run_polling()

if __name__ == "__main__":
    main()
