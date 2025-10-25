import os
import asyncio
import pytz
from datetime import datetime, timedelta
from telegram import Bot
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

BOT_TOKEN = os.getenv("FORWARD_BOT_TOKEN", "7640340584:AAFRegFmJmrx-44r93wnQJFNPmtVQ_M0pKc")
SOURCE_GROUP_ID = int(os.getenv("FORWARD_GROUP_ID", "-1003199070793"))
TARGET_CHANNEL = os.getenv("FORWARD_TARGET_CHANNEL", "@hottxvideos18plus")

# === Define message groups ===
MESSAGE_GROUPS = [
    [47, 48, 49, 50, 51],   # Round 1
    [52, 53, 54, 55, 56],   # Round 2
    [57, 58, 59, 60, 61],   # Round 3
]

# === Define Australian timezone ===
AU_TZ = pytz.timezone("Australia/Sydney")
INTERVAL_HOURS = 6  # 每6小时运行一次

bot = Bot(token=BOT_TOKEN)


async def forward_messages(message_ids, round_label):
    print("=" * 70)
    print(f"🕓 Time: {datetime.now(AU_TZ).strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"🚀 Sending batch ({round_label}): {message_ids}")
    print("-" * 70)

    for msg_id in message_ids:
        try:
            await bot.forward_message(
                chat_id=TARGET_CHANNEL,
                from_chat_id=SOURCE_GROUP_ID,
                message_id=msg_id
            )
            print(f"✅ Forwarded message ID: {msg_id}")
            await asyncio.sleep(3)
        except Exception as e:
            print(f"⚠️ Failed to forward {msg_id}: {e}")

    print(f"✅ Batch {round_label} complete.")
    print("=" * 70)


async def schedule_loop():
    print("🤖 Bot started (Australia/Sydney timezone, runs every 6 hours).")

    # 保存上次执行的轮次 (状态文件)
    state_file = "forward_state.txt"
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            round_index = int(f.read().strip())
    else:
        round_index = 0

    while True:
        current_group = MESSAGE_GROUPS[round_index]
        label = f"Round {round_index + 1}"

        await forward_messages(current_group, label)

        # 保存下一轮的索引
        next_index = (round_index + 1) % len(MESSAGE_GROUPS)
        with open(state_file, "w") as f:
            f.write(str(next_index))

        # 计算下一次执行时间（6小时后）
        next_run = datetime.now(AU_TZ) + timedelta(hours=INTERVAL_HOURS)
        print(f"🕒 Next batch scheduled at {next_run.strftime('%Y-%m-%d %H:%M:%S %Z')} "
              f"(Group {next_index + 1}) — waiting {INTERVAL_HOURS} hours.")
        await asyncio.sleep(INTERVAL_HOURS * 3600)

        round_index = next_index


if __name__ == "__main__":
    asyncio.run(schedule_loop())
