import os
import requests
import random
import time
from bs4 import BeautifulSoup
from datetime import datetime
from telegram import Bot
from dotenv import load_dotenv

# === Load env ===
load_dotenv()

# === Telegram 設定 ===
BOT_TOKEN = os.getenv("VIDEO_BOT_TOKEN", "7961665345:AAFtGJsNNqNRRntKXQCFxuCLwqGzln6hbhM")
FORWARD_BOT_TOKEN = os.getenv("FORWARD_BOT_TOKEN", "7640340584:AAFRegFmJmrx-44r93wnQJFNPmtVQ_M0pKc")
SOURCE_GROUP_ID = int(os.getenv("FORWARD_GROUP_ID", "-1003199070793"))
CHANNEL_ID = os.getenv("CHANNEL_ID", "@hottxvideos18plus")
INTERVAL_HOURS = int(os.getenv("INTERVAL_HOURS", 6))  # 每6小時發送一次

# === 信息 ID 群組 ===
MESSAGE_GROUPS = [
    [47, 48, 49, 50, 51],
    [52, 53, 54, 55, 56],
    [57, 58, 59, 60, 61],
]

VIDEOS_PER_ROUND = 10
video_bot = Bot(token=BOT_TOKEN)
forward_bot = Bot(token=FORWARD_BOT_TOKEN)


# === 抓影片 ===
def fetch_from_url(url, max_videos=3):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
        )
    }
    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")

        selectors = [
            "a.thumb-image-container",
            "a.video-thumb__image-container",
            "a.video-thumb",
            "div.thumb a",
            "a.video-item__link",
            "a.thumb__link",
        ]

        videos = []
        for selector in selectors:
            for a in soup.select(selector):
                href = a.get("href")
                img_tag = a.find("img")
                if not href:
                    continue

                video_url = "https://xhamster3.com" + href if href.startswith("/") else href
                thumbnail = (
                    img_tag.get("data-src")
                    or img_tag.get("data-thumb")
                    or img_tag.get("src")
                    if img_tag else None
                )
                videos.append({"url": video_url, "thumbnail": thumbnail})

            if len(videos) >= max_videos:
                break

        random.shuffle(videos)
        return videos[:max_videos]
    except Exception as e:
        print(f"⚠️ Error fetching from {url}: {e}")
        return []


def fetch_videos():
    CATEGORY_URLS = [
        "https://xhamster3.com/channels/naughty-america",
        "https://xhamster3.com/creators/msbreewc",
        "https://xhamster3.com/creators/comatozze",
        "https://xhamster3.com/channels/raptor-llc",
        "https://xhamster3.com/channels/school-girls-hd-channel",
        "https://xhamster3.com/categories/russian",
        "https://xhamster3.com/categories/japanese",
        "https://xhamster3.com/channels/av-stockings",
        "https://xhamster3.com/channels/jav-hd",
        "https://xhamster3.com/channels/jav-hd/best",
        "https://xhamster3.com/creators/pornforce",
        "https://xhamster3.com/channels/av-tits",
        "https://xhamster3.com/creators/elina-lizz",
        "https://xhamster3.com/creators/bootyfrutti",
        "https://xhamster3.com/creators/hot-pearl"
    ]
    selected_sources = random.sample(CATEGORY_URLS, k=5)
    print(f"🌐 Selected sources ({len(selected_sources)}):")
    for s in selected_sources:
        print(f"  - {s}")

    all_videos = []
    for source in selected_sources:
        vids = fetch_from_url(source, max_videos=2)
        all_videos.extend(vids)
        time.sleep(1)
    random.shuffle(all_videos)
    return all_videos[:VIDEOS_PER_ROUND]


# === 發送影片 ===
def send_to_channel():
    print(f"\n🚀 Sending videos at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    videos = fetch_videos()
    print(f"✅ Total collected: {len(videos)} videos\n")
    if not videos:
        print("⚠️ No videos found.")
        return False

    success_count = 0
    for v in videos:
        caption = (
            f"💦 <a href=\"{v['url']}\">Click here to unlock full videos: [Link...]</a>\n"
            f"🔞 <a href=\"https://tinyurl.com/3zh5zvrf\">Tap here for more videos: [Link...]</a>"
        )
        try:
            if v["thumbnail"]:
                video_bot.send_photo(chat_id=CHANNEL_ID, photo=v["thumbnail"], caption=caption, parse_mode="HTML")
            else:
                video_bot.send_message(chat_id=CHANNEL_ID, text=caption, parse_mode="HTML")
            success_count += 1
            time.sleep(3)
        except Exception as e:
            print(f"⚠️ Failed to send one video: {e}")

    print(f"✅ Sent {success_count}/{len(videos)} videos.")
    return success_count > 0


# === 轉發信息 ID ===
def forward_messages(group_index):
    current_group = MESSAGE_GROUPS[group_index]
    label = f"Round {group_index + 1}"
    print("=" * 60)
    print(f"🕓 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 🚀 Sending batch ({label}): {current_group}")
    print("-" * 60)

    for msg_id in current_group:
        try:
            forward_bot.forward_message(
                chat_id=CHANNEL_ID,
                from_chat_id=SOURCE_GROUP_ID,
                message_id=msg_id
            )
            print(f"✅ Forwarded message ID: {msg_id}")
            time.sleep(3)
        except Exception as e:
            print(f"⚠️ Failed to forward {msg_id}: {e}")

    print(f"✅ Batch {label} complete.")
    print("=" * 60)


# === 主控制循環 ===
if __name__ == "__main__":
    print("🤖 Auto Video + Forward Bot Started (6-hour cycle)\n")

    round_index = 0
    while True:
        try:
            # STEP 1️⃣ 先發送影片
            all_ok = send_to_channel()

            if all_ok:
                print("🎯 Videos sent successfully. Starting message forward task...")
                time.sleep(30)  # 小緩衝
                forward_messages(round_index)
            else:
                print("⚠️ Skip message forwarding this round (video sending failed).")

            # STEP 2️⃣ 更新下次的 round
            round_index = (round_index + 1) % len(MESSAGE_GROUPS)

            # STEP 3️⃣ 等 6 小時再進下一輪
            print(f"🕒 Waiting {INTERVAL_HOURS} hours before next round...\n")
            time.sleep(INTERVAL_HOURS * 3600)

        except Exception as e:
            print(f"❗ Unexpected error: {e}")
            print("🔁 Restarting loop in 60 seconds...\n")
            time.sleep(60)
