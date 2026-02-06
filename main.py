import os
import requests
import feedparser
import time
from bs4 import BeautifulSoup

# ১. টেলিগ্রামে প্রফেশনাল ডিল পাঠানোর ফাংশন
def send_deal(title, link, img_url):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    amazon_tag = "offerslive24-21" 

    # আমাজন লিঙ্ক হলে আপনার ট্যাগ যোগ হবে
    if "amazon.in" in link:
        link = f"{link}&tag={amazon_tag}" if "?" in link else f"{link}?tag={amazon_tag}"
    
    caption = (
        f"🚨 <b>MEGA LOOT DEAL</b> 🚨\n\n"
        f"🛒 <b>{title.upper()}</b>\n\n"
        f"🔥 <b>Status:</b> Price Drop Alert! 📉\n\n"
        f"👉 <a href='{link}'>GRAB THIS DEAL NOW</a>\n"
        f"👉 <a href='{link}'>GRAB THIS DEAL NOW</a>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎁 <b>Extra:</b> <a href='https://www.amazon.in/gp/goldbox?tag={amazon_tag}'>Amazon</a> | <a href='https://fktr.in/7WhPb8j'>Flipkart</a>\n"
        f"⚡ <i>Join @offers_live_24 for more Loots!</i>"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    # নতুন এবং গ্লোবাল ইমেজ লিঙ্ক ব্যবহার করা হয়েছে
    payload = {"chat_id": chat_id, "photo": img_url, "caption": caption, "parse_mode": "HTML"}
    
    try:
        r = requests.post(url, data=payload)
        print(f"Post Attempt: {title[:20]}... | Status: {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

# ২. ডিল থেকে ইমেজ বের করার এবং ফিল্টার করার ফাংশন
def get_clean_image(entry):
    content = entry.get('summary', '') + entry.get('description', '')
    soup = BeautifulSoup(content, 'html.parser')
    img = soup.find('img')
    
    # এটি একটি গ্লোবাল এবং স্টেবল লুন ব্যানার
    fallback_img = "https://img.freepik.com/free-vector/special-offer-sale-discount-banner_23-2148425139.jpg"

    if img and img.get('src'):
        img_url = img.get('src')
        # অকেজো বা ব্লকড ইমেজ ফিল্টার
        bad_words = ["ytimg", "pixel", "not-viewable", "logo", "icon"]
        if any(word in img_url.lower() for word in bad_words):
            return fallback_img
        return img_url
    
    return fallback_img

# ৩. মেইন প্রসেসর
def start_bot():
    print("🔍 Searching for deals...")
    
    feeds = [
        "https://indiafreestuff.in/feed", 
        "https://www.desidime.com/new.atom"
    ]
    
    posted_count = 0
    # অপ্রয়োজনীয় আর্টিকেল বাদ দেওয়ার জন্য ফিল্টার
    blacklist = ["best", "top", "review", "how to", "guide", "alchemy", "expired"]

    for f_url in feeds:
        feed = feedparser.parse(f_url)
        print(f"📡 Found {len(feed.entries)} items in {f_url}")
        
        for entry in feed.entries[:8]: 
            title = entry.title.split('|')[0].strip()
            
            if any(word in title.lower() for word in blacklist):
                continue
            
            img = get_clean_image(entry)
            
            if send_deal(title, entry.link, img):
                posted_count += 1
                time.sleep(15) # স্প্যাম প্রোটেকশন
            
            if posted_count >= 5: break 
        if posted_count >= 5: break

if __name__ == "__main__":
    start_bot()
