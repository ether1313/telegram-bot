# 🤖 Telegram Auto Video Poster Bot

Auto posts video links and thumbnails from multiple xHamster sources  
to a Telegram channel every few hours.  
After posting, it will also forward preset messages from a group to the same channel.

---

## 🚀 Deploy on Railway

1. Fork this repo to your GitHub.  
2. Go to [Railway.app](https://railway.app)  
3. Create **New Project → Deploy from GitHub**.  
4. Add these Environment Variables:
   - VIDEO_BOT_TOKEN=
   - CHANNEL_ID=
   - INTERVAL_HOURS=6
   - FORWARD_BOT_TOKEN=
   - FORWARD_GROUP_ID=
   - FORWARD_TARGET_CHANNEL=
   - FORWARD_INTERVAL_HOURS=6
5. Click **Deploy** ✅  
Railway will host and run your bot 24/7.

---

## ⚙️ How It Works

- Fetches random videos and thumbnails from xHamster  
- Sends them to your Telegram channel  
- Then forwards message IDs from a source group  
- Repeats every few hours automatically