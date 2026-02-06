import os
import requests
import feedparser
import time
from bs4 import BeautifulSoup

def send_deal(title, link, img_url):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    
    # প্রফেশনাল মেসেজ ফরম্যাট
    caption = (
        f"🚨 <b>MEGA LOOT DEAL</b> 🚨\n\n"
        f"🛒 <b>{title.upper()}</b>\n\n"
        f"👉 <a href='{link}'>GRAB THIS DEAL NOW</a>\n\n"
        f"⚡ <i>Join @offers_live_24 for more!</i>"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": img_url, "caption": caption, "parse_mode": "HTML"}
    
    try:
        r = requests.post(url, data=payload)
        print(f"Post Attempt: {title[:20]}... | Status: {r.status_code}")
        return r.status_code == 200
    except:
        return False

def get_image(entry):
    # ইমেজ খোঁজার লজিক
    try:
        content = entry.get('summary', '') + entry.get('description', '')
        soup = BeautifulSoup(content, 'html.parser')
        img = soup.find('img')
        if img and img.get('src'):
            return img.get('src')
    except:
        pass
    return "https://i.imgur.com/uP1pY9u.png" # ডিফল্ট ইমেজ

def start_bot():
    # প্রথমে একটি টেস্ট মেসেজ পাঠানো (কানেকশন চেক করার জন্য)
    requests.post(f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/sendMessage", 
                  data={"chat_id": os.getenv("CHAT_ID"), "text": "🚀 Bot started successfully and checking feeds..."})

    feeds = ["https://indiafreestuff.in/feed", "https://www.desidime.com/new.atom"]
    
    for f_url in feeds:
        print(f"📡 Checking: {f_url}")
        feed = feedparser.parse(f_url)
        for entry in feed.entries[:5]:
            title = entry.title.split('|')[0].strip()
            # বেহুদা কন্টেন্ট বাদ দেওয়া
            if any(x in title.lower() for x in ["review", "how to", "guide"]): continue
            
            img = get_image(entry)
            send_deal(title, entry.link, img)
            time.sleep(5)

if __name__ == "__main__":
    # টোকেন চেক
    if not os.getenv("BOT_TOKEN") or not os.getenv("CHAT_ID"):
        print("❌ Error: BOT_TOKEN or CHAT_ID missing in Secrets!")
    else:
        start_bot()
