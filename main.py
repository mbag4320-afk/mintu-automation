import os
import requests
import feedparser
import time
from bs4 import BeautifulSoup

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
        f"👉 <a href='{link}'>GRAB THIS DEAL NOW</a>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎁 <b>Extra:</b> <a href='https://www.amazon.in/gp/goldbox?tag={amazon_tag}'>Amazon</a> | <a href='https://fktr.in/7WhPb8j'>Flipkart</a>"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": img_url, "caption": caption, "parse_mode": "HTML"}
    
    try:
        r = requests.post(url, data=payload)
        return r.status_code == 200
    except:
        return False

def get_image(entry):
    content = entry.get('summary', '') + entry.get('description', '')
    soup = BeautifulSoup(content, 'html.parser')
    img = soup.find('img')
    return img.get('src') if img else "https://i.imgur.com/uP1pY9u.png"

def start_bot():
    # আরও কিছু ফিড যোগ করা হলো বেশি ডিল পাওয়ার জন্য
    feeds = [
        "https://indiafreestuff.in/feed", 
        "https://www.desidime.com/new.atom",
        "https://www.freekaamaal.com/feed"
    ]
    
    print("🔍 Searching for deals...")
    found_any = False

    for f_url in feeds:
        feed = feedparser.parse(f_url)
        print(f"📡 Checking Source: {f_url} (Found {len(feed.entries)} items)")
        
        for entry in feed.entries[:5]: # প্রতি সোর্স থেকে ৫টি করে ডিল দেখবে
            title = entry.title.split('|')[0].strip()
            
            # ফিল্টার একটু সহজ করা হলো
            if any(x in title.lower() for x in ["how to", "review", "expired"]): continue
            
            img = get_image(entry)
            print(f"📤 Posting: {title}")
            if send_deal(title, entry.link, img):
                found_any = True
                time.sleep(10) # বিরতি

    if not found_any:
        print("⚠️ No valid deals found in current feeds. Will try again in the next run.")

if __name__ == "__main__":
    start_bot()
