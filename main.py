import os
import requests
import feedparser
import time
from bs4 import BeautifulSoup

def send_deal(title, link, img_url):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    amazon_tag = "offerslive24-21" 

    # আমাজন অ্যাফিলিয়েট লিঙ্ক তৈরি
    if "amazon.in" in link:
        link = f"{link}&tag={amazon_tag}" if "?" in link else f"{link}?tag={amazon_tag}"
    
    # প্রফেশনাল ক্যাপশন
    caption = (
        f"🚨 <b>MEGA LOOT DEAL</b> 🚨\n\n"
        f"🛒 <b>{title.upper()}</b>\n\n"
        f"🔥 <b>Status:</b> Price Drop Alert! 📉\n\n"
        f"👉 <a href='{link}'>GRAB THIS DEAL NOW</a>\n"
        f"👉 <a href='{link}'>GRAB THIS DEAL NOW</a>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎁 <b>Extra Stores:</b> <a href='https://www.amazon.in/gp/goldbox?tag={amazon_tag}'>Amazon</a> | <a href='https://fktr.in/7WhPb8j'>Flipkart</a>\n"
        f"⚡ <i>Join @offers_live_24 for more Loots!</i>"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": img_url, "caption": caption, "parse_mode": "HTML"}
    
    try:
        r = requests.post(url, data=payload)
        return r.status_code == 200
    except:
        return False

def get_valid_image(entry):
    # ডেসক্রিপশন থেকে ইমেজ বের করা
    content = entry.get('summary', '') + entry.get('description', '')
    soup = BeautifulSoup(content, 'html.parser')
    img = soup.find('img')
    
    if img and img.get('src'):
        img_url = img.get('src')
        # কিছু ওয়েবসাইটের ছবি টেলিগ্রামে ব্লক থাকে, সেগুলো ফিল্টার করা
        if "ytimg" in img_url or "not-viewable" in img_url or "pixel" in img_url:
            return "https://i.imgur.com/uP1pY9u.png" # Default High Quality Banner
        return img_url
    
    return "https://i.imgur.com/uP1pY9u.png"

def start_bot():
    # ডিল সোর্স (বেশি ডিল পাওয়ার জন্য)
    feeds = [
        "https://indiafreestuff.in/feed", 
        "https://www.desidime.com/new.atom",
        "https://www.freekaamaal.com/feed"
    ]
    
    print("🔍 Searching for professional deals...")
    posted_count = 0
    
    # ফিল্টার করার জন্য নিষিদ্ধ শব্দ (এই শব্দগুলো থাকলে পোস্ট হবে না)
    blacklist = ["alchemy", "course", "review", "how to", "guide", "expired", "registration"]

    for f_url in feeds:
        feed = feedparser.parse(f_url)
        for entry in feed.entries[:6]: 
            title = entry.title.split('|')[0].strip()
            
            # ব্ল্যাকলিস্ট ফিল্টার
            if any(word in title.lower() for word in blacklist):
                continue
            
            img = get_valid_image(entry)
            
            # পোস্ট পাঠানো
            if send_deal(title, entry.link, img):
                print(f"✅ Success: {title[:30]}")
                posted_count += 1
                time.sleep(15) # স্প্যাম রোধে ১৫ সেকেন্ড গ্যাপ
            
            if posted_count >= 5: break # প্রতিবার সর্বোচ্চ ৫টি ডিল পোস্ট হবে
        if posted_count >= 5: break

if __name__ == "__main__":
    start_bot()
