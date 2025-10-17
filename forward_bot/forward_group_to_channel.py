import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("FORWARD_BOT_TOKEN", "7640340584:AAFRegFmJmrx-44r93wnQJFNPmtVQ_M0pKc")
SOURCE_GROUP_ID = int(os.getenv("FORWARD_GROUP_ID", "-4760638966"))
TARGET_CHANNEL = os.getenv("FORWARD_TARGET_CHANNEL", "@hottxvideos18plus")

async def forward_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg and msg.chat.id == SOURCE_GROUP_ID:
        try:
            # debug — 印出 chat id 方便確認
            print(f"🔍 來源群組: {msg.chat.id}, 目標頻道: {TARGET_CHANNEL}")

            # 轉發所有訊息類型
            await msg.forward(chat_id=TARGET_CHANNEL)
            print(f"✅ 成功轉發訊息 ID: {msg.message_id}")

        except Exception as e:
            print(f"⚠️ 轉發失敗: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, forward_all))
    print("🤖 Forward Bot 已啟動，正在監聽群組訊息...")
    app.run_polling()
