import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
    ContextTypes
)

# Enable logging (helps debugging)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Replace with your bot token and channel
TOKEN = "8336822306:AAH8dJ9bfNCrwEmpF8TOSNpviSuqWxwsuDs"
CHANNEL_ID = "-1003115930403"   # or @yourchannelusername

# Conversation states
JOB_TITLE, LOCATION, DEADLINE = range(3)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("➕ Post a Job", callback_data="post_job")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Welcome! Use the button below to post a job:",
        reply_markup=reply_markup
    )

# Button handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "post_job":
        await query.message.reply_text("Please enter the Job Title:")
        return JOB_TITLE

# Collect job title
async def job_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["job_title"] = update.message.text
    await update.message.reply_text("Enter the Location:")
    return LOCATION

# Collect location
async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["location"] = update.message.text
    await update.message.reply_text("Enter the Application Deadline (e.g. Oct 15, 2025):")
    return DEADLINE

# Collect deadline and post job
async def deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["deadline"] = update.message.text

    job_post = f"""
🔹 Job Title: {context.user_data['job_title']}
📍 Location: {context.user_data['location']}
🕒 Deadline: {context.user_data['deadline']}
"""

    # Send job post to channel
    await context.bot.send_message(chat_id=CHANNEL_ID, text=job_post)

    await update.message.reply_text("✅ Job posted successfully!")
    return ConversationHandler.END

# Cancel command
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Job posting cancelled.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CallbackQueryHandler(button)
        ],
        states={
            JOB_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, job_title)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, location)],
            DEADLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, deadline)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv_handler)

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
