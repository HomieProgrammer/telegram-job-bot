import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "8336822306:AAH8dJ9bfNCrwEmpF8TOSNpviSuqWxwsuDs"
CHANNEL_ID = "-1003115930403"   # channel id or @channelusername

async def main():
    bot = Bot(token=TOKEN)

    job_post = """
    🔹 Job Title: Expert Video Editor
    📍 Location: Addis Ababa
    🕒 Deadline: October 14, 2025
    """

    # Inline button for applying
    keyboard = [
        [InlineKeyboardButton("📩 Apply Now", url="https://forms.gle/your-google-form-link")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=job_post,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

if __name__ == "__main__":
    asyncio.run(main())
