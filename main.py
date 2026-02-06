import os
import requests
import feedparser
import time
from bs4 import BeautifulSoup

# ১. টেলিগ্রামে প্রফেশনাল ডিল পোস্ট পাঠানোর ফাংশন
def send_deal(title, link, img_url):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    amazon_tag = "offerslive24-21" # আপনার আমাজন ট্যাগ
    
    # আমাজন লিঙ্ক হলে আপনার ট্যাগ যোগ হবে
    if "amazon.in" in link:
        link = f"{link}&tag={amazon_tag}" if "?" in link else f"{link}?tag={amazon_tag}"
    
    # প্রফেশনাল ক্যাপশন ডিজাইন (HTML Mode)
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
    payload = {
        "chat_id": chat_id, 
        "photo": img_url, 
        "caption": caption, 
        "parse_mode": "HTML"
    }
    
    try:
        r = requests.post(url, data=payload)
        if r.status_code == 200:
            print(f"✅ Posted: {title[:30]}...")
            return True
        else:
            print(f"❌ Failed: {r.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# ২. ডিল থেকে আসল প্রোডাক্ট ইমেজ খুঁজে বের করার ফাংশন
def get_image(entry):
    # RSS ফিডের ডেসক্রিপশন থেকে ইমেজ ট্যাগ খোঁজা
    content = entry.get('summary', '') + entry.get('description', '')
    soup = BeautifulSoup(content, 'html.parser')
    img_tag = soup.find('img')
    
    if img_tag and img_tag.get('src'):
        return img_tag.get('src')
    
    # যদি কোনো ছবি না পাওয়া যায় তবে একটি সুন্দর 'Sale' ব্যানার
    return "https://i.imgur.com/uP1pY9u.png"

# ৩. মেইন রানার ফাংশন
def start_bot():
    feeds = ["https://indiafreestuff.in/feed", "https://www.desidime.com/new.atom"]
    
    print("Checking for new deals...")
    posted_count = 0
    
    for f_url in feeds:
        feed = feedparser.parse(f_url)
        
        # প্রতিটি ফিড থেকে লেটেস্ট ৩টি ডিল চেক করবে
        for entry in feed.entries[:3]:
            title = entry.title.split('|')[0].strip()
            
            # অপ্রয়োজনীয় কন্টেন্ট ফিল্টার
            if any(x in title.lower() for x in ["how to", "review", "guide", "expired"]):
                continue
            
            img = get_image(entry)
            link = entry.link
            
            success = send_deal(title, link, img)
            if success:
                posted_count += 1
                time.sleep(10) # স্প্যাম প্রোটেকশনের জন্য ১০ সেকেন্ড বিরতি
            
            if posted_count >= 6: break # একবারে ৬টির বেশি পোস্ট করবে না

if __name__ == "__main__":
    start_bot()
