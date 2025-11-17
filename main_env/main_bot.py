import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_path = "main_env/images/girl-03.jpeg"
    user = update.effective_user

    # 避免 NoneType
    user_name = user.first_name or user.username or "there"

    caption = (
        f"🤝𝐖𝐄𝐋𝐂𝐎𝐌𝐄 {user_name}, \n\n"
        "Before We Start, If You're Not A Robot,\n"
        "Kindly Tap「I'M NOT A ROBOT」\n"
        "To Get Unlimited Bonus Rewards 🎁\n\n"
        "Earn Affiliate Commission Cash\n"
        "Share More & Earn More 💰\n\n"
        "Win More With This Sexy Vibes,\n"
        "Try Tap「CHAT WITH HER」▶︎ •၊၊||၊|။|| 0:10"
    )

    keyboard = [
        [InlineKeyboardButton("I'M NOT A ROBOT 🟢", url="https://t.me/addlist/vU9C9Dvo_TJkZThl")],
        [InlineKeyboardButton("I'M NOT A ROBOT 🟢", url="https://heylink.me/tpaaustralia/")],
        [InlineKeyboardButton("CHAT WITH HER ﾒ૦ﾒ૦💋", url="https://t.me/hottxvideos18plus")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 防止 "NoneType reply" 错误（/start 在群组或按钮点击时可能没有 message）
    if update.message:
        with open(photo_path, "rb") as photo:
            await update.message.reply_photo(photo=photo, caption=caption, reply_markup=reply_markup)
    else:
        # 回 fallback：如果由按钮触发（没有 message）
        await update.callback_query.message.reply_text("Please use /start in private chat.")

def main():
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise RuntimeError("❌ BOT_TOKEN is missing in environment!")

    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(CommandHandler("start", start))

    print("✅ Main Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
