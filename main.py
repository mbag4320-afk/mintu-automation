import os
import requests
import feedparser
import time
from bs4 import BeautifulSoup

# ১. টেলিগ্রামে প্রফেশনাল ফটো মেসেজ পাঠানোর ফাংশন
def send_deal(title, link, img_url):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    amazon_tag = "offerslive24-21" # আপনার আমাজন ট্যাগ

    if "amazon.in" in link:
        link = f"{link}&tag={amazon_tag}" if "?" in link else f"{link}?tag={amazon_tag}"
    
    caption = (
        f"🚨 <b>MEGA LOOT DEAL</b> 🚨\n\n"
        f"🛒 <b>{title.upper()}</b>\n\n"
        f"🔥 <b>Status:</b> Price Drop Alert! 📉\n\n"
        f"👉 <a href='{link}'>GRAB THIS DEAL NOW</a>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ <i>Join @offers_live_24 for more Loots!</i>"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": img_url, "caption": caption, "parse_mode": "HTML"}
    
    try:
        r = requests.post(url, data=payload)
        return r.status_code == 200
    except:
        return False

# ২. ডিল থেকে ইমেজ বের করার নিখুঁত ফাংশন
def get_image(entry):
    try:
        content = entry.get('summary', '') + entry.get('description', '')
        soup = BeautifulSoup(content, 'html.parser')
        img = soup.find('img')
        if img and img.get('src'):
            img_url = img.get('src')
            # অকেজো বা ছোট পিক্সেলের ছবি ফিল্টার
            if "pixel" in img_url or "not-viewable" in img_url:
                return "https://i.ibb.co/LzNfS6P/special-offer.jpg" # নতুন স্ট্যাবল ডিফল্ট ইমেজ
            return img_url
    except:
        pass
    return "https://i.ibb.co/LzNfS6P/special-offer.jpg"

# ৩. মেইন রানার
def start_bot():
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    feeds = ["https://indiafreestuff.in/feed", "https://www.desidime.com/new.atom"]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    posted_any = False
    print("🔍 Checking feeds for deals...")

    for f_url in feeds:
        try:
            # সরাসরি লিঙ্ক ওপেন করে ডেটা পড়া
            resp = requests.get(f_url, headers=headers, timeout=15)
            feed = feedparser.parse(resp.content)
            
            for entry in feed.entries[:5]: # প্রতি সোর্স থেকে ৫টি ডিল
                title = entry.title.split('|')[0].strip()
                
                # ফিল্টার: বাজে কন্টেন্ট বাদ
                if any(x in title.lower() for x in ["review", "how to", "guide", "expired"]): 
                    continue
                
                img = get_image(entry)
                if send_deal(title, entry.link, img):
                    posted_any = True
                    print(f"✅ Success: {title}")
                    time.sleep(10) # স্প্যাম প্রোটেকশন
        except Exception as e:
            print(f"Error checking feed {f_url}: {e}")

    # যদি কোনো ডিল না পাওয়া যায় তবে সেটি চ্যানেলে জানাবে
    if not posted_any:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      data={"chat_id": chat_id, "text": "⚠️ No new deals found in the feeds right now. Will check again later!"})

if __name__ == "__main__":
    start_bot()
