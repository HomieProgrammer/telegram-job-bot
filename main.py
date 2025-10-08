from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8336822306:AAH8dJ9bfNCrwEmpF8TOSNpviSuqWxwsuDs"

app = Flask(__name__)

telegram_app = Application.builder().token(BOT_TOKEN).build()

# === COMMAND HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is alive and working on Render!")

telegram_app.add_handler(CommandHandler("start", start))

# === WEBHOOK ROUTE ===
@app.route("/", methods=["POST"])
async def webhook():
    update = Update.de_json(await request.get_json(), telegram_app.bot)
    await telegram_app.process_update(update)
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)