import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# === 載入環境變數 ===
load_dotenv()
BOT_TOKEN = os.getenv("MAIN_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_path = "main_env/images/girl-03.jpeg"

    caption = (
        "Hey there! 😘\n"
        "If you're not a robot, tap the buttons below 👇\n"
        "Help this babe grow her channel 💋\n\n"
        "Daily bonus rain and lucky spins are waiting for you 🎁🎰"
    )

    keyboard = [
        [InlineKeyboardButton("FREE CREDIT BONUS", url="https://t.me/addlist/PbLUCPdgcG0yZWY9")],
        [InlineKeyboardButton("PARTNERSHIP 13AUTEAM", url="https://www.13auteam.com/")],
        [InlineKeyboardButton("HOT VIDEOS 18+", url="https://t.me/hottxvideos18plus")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open(photo_path, "rb") as photo:
        await update.message.reply_photo(photo=photo, caption=caption, reply_markup=reply_markup)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("✅ Main Bot is running...")
    app.run_polling()
