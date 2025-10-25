import os
import requests
import random
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz
import subprocess

# === Telegram 設定 ===
BOT_TOKEN = os.getenv("VIDEO_BOT_TOKEN", "7961665345:AAFtGJsNNqNRRntKXQCFxuCLwqGzln6hbhM")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@hottxvideos18plus")

# === 澳洲時區設定 ===
AU_TZ = pytz.timezone("Australia/Sydney")

# === 影片來源連結 ===
CATEGORY_URLS = [
    "https://xhamster3.com/channels/naughty-america",
    "https://xhamster3.com/creators/msbreewc",
    "https://xhamster3.com/creators/comatozze",
    "https://xhamster3.com/channels/raptor-llc",
    "https://xhamster3.com/channels/school-girls-hd-channel",
    "https://xhamster3.com/categories/russian",
    "https://xhamster3.com/categories/japanese",
    "https://xhamster3.com/channels/av-stockings",
    "https://xhamster3.com/channels/modelmediaasia",
    "https://xhamster3.com/channels/jav-hd",
    "https://xhamster3.com/channels/jav-hd/best",
    "https://xhamster3.com/creators/pornforce",
    "https://xhamster3.com/channels/av-tits",
    "https://xhamster3.com/creators/elina-lizz",
    "https://xhamster3.com/creators/bootyfrutti",
    "https://xhamster3.com/creators/hot-pearl"
]

VIDEOS_PER_ROUND = 10
INTERVAL_HOURS = 6  # 每6小時執行一次


# === 抓取影片 ===
def fetch_from_url(url, max_videos=3):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")

        videos = []
        for a in soup.select("a.thumb-image-container, a.video-thumb__image-container"):
            href = a.get("href")
            img_tag = a.find("img")
            if not href:
                continue
            video_url = "https://xhamster3.com" + href if href.startswith("/") else href
            thumbnail = img_tag.get("data-src") or img_tag.get("src") if img_tag else None
            videos.append({"url": video_url, "thumbnail": thumbnail})

        random.shuffle(videos)
        return videos[:max_videos]
    except Exception as e:
        print(f"⚠️ Error fetching from {url}: {e}")
        return []


def fetch_videos():
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


# === Telegram 發送 ===
def send_photo(chat_id, photo_url, caption, parse_mode="HTML"):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    data = {"chat_id": chat_id, "photo": photo_url, "caption": caption, "parse_mode": parse_mode}
    response = requests.post(url, data=data)
    return response.status_code == 200


def send_message(chat_id, text, parse_mode="HTML"):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
    response = requests.post(url, data=data)
    return response.status_code == 200


# === 發送影片流程 ===
def send_to_channel():
    print(f"\n🚀 Sending videos at {datetime.now(AU_TZ).strftime('%Y-%m-%d %H:%M:%S %Z')}")
    videos = fetch_videos()
    print(f"✅ Total collected: {len(videos)} videos\n")

    if not videos:
        print("⚠️ No videos found — check page structure or network.")
        return False

    success_count = 0
    for v in videos:
        caption = (
            f"💦 <a href=\"{v['url']}\">Click here to unlock full videos 🔗</a>\n"
            f"🔞 <a href=\"https://tinyurl.com/3zh5zvrf\">More hot videos here 🔥</a>"
        )
        ok = send_photo(CHANNEL_ID, v["thumbnail"], caption) if v["thumbnail"] else send_message(CHANNEL_ID, caption)
        if ok:
            success_count += 1
        time.sleep(3)

    print(f"✅ Sent {success_count}/{len(videos)} videos successfully.")
    return success_count == len(videos)


# === 主循環 ===
if __name__ == "__main__":
    print("✅ Auto Multi-Source Video Poster Started (Australia timezone, every 6 hours).")

    while True:
        now = datetime.now(AU_TZ)
        print(f"\n🕓 Current Time (Sydney): {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        print("🚀 Starting new video batch...")

        ok = send_to_channel()

        if ok:
            print("🎯 All videos sent successfully. Running forward script...")
            script_path = os.path.join(os.path.dirname(__file__), "..", "forward_bot", "forward_group_to_channel.py")
            script_path = os.path.abspath(script_path)
            subprocess.run(["python3", script_path])
        else:
            print("⚠️ Some videos failed, skipping forwarding this round.")

        # 等待6小時
        next_run = datetime.now(AU_TZ) + timedelta(hours=INTERVAL_HOURS)
        print(f"🕒 Next batch scheduled at {next_run.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        time.sleep(INTERVAL_HOURS * 3600)
