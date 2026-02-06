import os
import requests
import feedparser
import time
from bs4 import BeautifulSoup

# ১. টেলিগ্রামে পোস্ট পাঠানোর ফাংশন
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
        f"👉 <a href='{link}'>GRAB THIS DEAL NOW</a>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎁 <b>More:</b> <a href='https://www.amazon.in/gp/goldbox?tag={amazon_tag}'>Amazon</a> | <a href='https://fktr.in/7WhPb8j'>Flipkart</a>"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": img_url, "caption": caption, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=payload)
        return r.status_code == 200
    except:
        return False

# ২. ইমেজ বের করার প্রফেশনাল ফাংশন
def get_image(entry):
    soup = BeautifulSoup(entry.get('summary', '') + entry.get('description', ''), 'html.parser')
    img = soup.find('img')
    if img and img.get('src'):
        return img.get('src')
    return "https://i.imgur.com/uP1pY9u.png" # Default Sale Image

# ৩. মেইন রানার
def start_bot():
    feeds = ["https://indiafreestuff.in/feed", "https://www.desidime.com/new.atom"]
    
    for f_url in feeds:
        feed = feedparser.parse(f_url)
        for entry in feed.entries[:3]: # প্রতিবার লেটেস্ট ৩টি করে চেক করবে
            title = entry.title.split('|')[0].strip()
            if any(x in title.lower() for x in ["how to", "review", "guide"]): continue
            
            img = get_image(entry)
            success = send_deal(title, entry.link, img)
            if success:
                print(f"Posted: {title}")
                time.sleep(10) # স্প্যাম এড়াতে বিরতি

if __name__ == "__main__":
    start_bot()
