import os
import asyncio
from datetime import datetime
from telegram import Bot
from dotenv import load_dotenv

# === 載入環境變數 ===
load_dotenv()

# === Telegram 設定 ===
BOT_TOKEN = os.getenv("FORWARD_BOT_TOKEN", "7640340584:AAFRegFmJmrx-44r93wnQJFNPmtVQ_M0pKc")
SOURCE_GROUP_ID = int(os.getenv("FORWARD_GROUP_ID", "-4760638966"))
TARGET_CHANNEL = os.getenv("FORWARD_TARGET_CHANNEL", "@hottxvideos18plus")

# === 每幾小時執行一次 ===
INTERVAL_HOURS = 4

# === 建立 Bot 實例 ===
bot = Bot(token=BOT_TOKEN)

async def forward_recent_messages():
    print(f"\n🚀 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 開始抓取群組訊息...")

    try:
        messages = await bot.get_chat_history(chat_id=SOURCE_GROUP_ID, limit=50)
        print(f"📦 取得 {len(messages)} 則訊息，準備轉發中...")

        for msg in reversed(messages):  # 保持原始順序
            try:
                await bot.forward_message(
                    chat_id=TARGET_CHANNEL,
                    from_chat_id=SOURCE_GROUP_ID,
                    message_id=msg.message_id
                )
                await asyncio.sleep(2)  # 避免被 Telegram 限速
            except Exception as e:
                print(f"⚠️ 無法轉發訊息 ID {msg.message_id}: {e}")

        print("✅ 本輪轉發完成。")

    except Exception as e:
        print(f"❌ 抓取或轉發出錯: {e}")


async def scheduler():
    while True:
        await forward_recent_messages()
        print(f"🕒 等待 {INTERVAL_HOURS} 小時後再次執行...\n")
        await asyncio.sleep(INTERVAL_HOURS * 3600)


if __name__ == "__main__":
    print("🤖 Forward Bot 已啟動（每 4 小時自動轉發群組訊息）")
    asyncio.run(scheduler())
