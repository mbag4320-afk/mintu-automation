import os
import requests
import feedparser
import time
from bs4 import BeautifulSoup

# ১. টেলিগ্রামে মেসেজ পাঠানোর ফাংশন
def send_deal(title, link, img_url):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    amazon_tag = "offerslive24-21" 

    if "amazon.in" in link:
        link = f"{link}&tag={amazon_tag}" if "?" in link else f"{link}?tag={amazon_tag}"
    
    caption = (
        f"🚨 <b>MEGA LOOT DEAL</b> 🚨\n\n"
        f"🛒 <b>{title.upper()}</b>\n\n"
        f"🔥 <b>Status:</b> Price Drop Alert!\n\n"
        f"👉 <a href='{link}'>GRAB THIS DEAL NOW</a>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎁 <b>Extra:</b> <a href='https://www.amazon.in/gp/goldbox?tag={amazon_tag}'>Amazon</a> | <a href='https://fktr.in/7WhPb8j'>Flipkart</a>"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": img_url, "caption": caption, "parse_mode": "HTML"}
    
    try:
        r = requests.post(url, data=payload)
        print(f"Post Attempt: {title[:20]}... | Status: {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

# ২. ইমেজ বের করার ফাংশন
def get_clean_image(entry):
    content = entry.get('summary', '') + entry.get('description', '')
    soup = BeautifulSoup(content, 'html.parser')
    img = soup.find('img')
    if img and img.get('src'):
        return img.get('src')
    return "https://i.imgur.com/uP1pY9u.png" # Default Image

# ৩. মেইন স্টার্টার
def start_bot():
    # সরাসরি একটি কানেকশন টেস্ট
    print("🚀 Sending Connection Test Message...")
    send_deal("CONNECTION TEST - SUCCESSFUL ✅", "https://google.com", "https://i.imgur.com/uP1pY9u.png")
    
    feeds = [
        "https://indiafreestuff.in/feed", 
        "https://www.desidime.com/new.atom"
    ]
    
    print("🔍 Searching for deals...")
    posted_count = 0
    blacklist = ["alchemy", "expired", "registration", "how to"]

    for f_url in feeds:
        feed = feedparser.parse(f_url)
        print(f"📡 Found {len(feed.entries)} items in {f_url}")
        
        for entry in feed.entries[:10]:
            title = entry.title.split('|')[0].strip()
            if any(word in title.lower() for word in blacklist):
                continue
            
            img = get_clean_image(entry)
            if send_deal(title, entry.link, img):
                posted_count += 1
                time.sleep(10)
            
            if posted_count >= 5: break
        if posted_count >= 5: break

if __name__ == "__main__":
    start_bot()
