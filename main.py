import os
import requests
import feedparser
import time
import re
from bs4 import BeautifulSoup

# ১. সরাসরি টেলিগ্রামে ফটোসহ পোস্ট পাঠানোর ফাংশন
def send_deal(title, link, img_url):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    amazon_tag = "offerslive24-21" # আপনার আমাজন ট্যাগ
    
    # আমাজন লিঙ্ক হলে আপনার ট্যাগ যোগ হবে
    if "amazon.in" in link:
        link = f"{link}&tag={amazon_tag}" if "?" in link else f"{link}?tag={amazon_tag}"
    
    # প্রফেশনাল ক্যাপশন ডিজাইন (HTML Mode ব্যবহার করা হয়েছে)
    caption = (
        f"🔥 <b>{title.upper()}</b>\n\n"
        f"💰 <b>Deal Status:</b> Live & Hot!\n"
        f"📢 <b>Price Drop Alert! Grab it fast.</b>\n\n"
        f"🛒 <b>Buy Now:</b> <a href='{link}'>Click Here to Buy</a>\n"
        f"🛒 <b>Buy Now:</b> <a href='{link}'>Click Here to Buy</a>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎁 <b>Extra Stores:</b> "
        f"<a href='https://www.amazon.in/gp/goldbox?tag={amazon_tag}'>Amazon</a> | "
        f"<a href='https://fktr.in/7WhPb8j'>Flipkart</a>\n"
        f"⚡ <i>Join @YourChannelUsernaem for more Loots!</i>"
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
        print(f"Posted: {title[:30]}... | Status: {r.status_code}")
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

# ২. ডিল থেকে ইমেজ খুঁজে বের করার ফাংশন
def get_image_from_entry(entry):
    # ১. যদি সরাসরি মিডিয়া লিঙ্ক থাকে
    if 'links' in entry:
        for link in entry.links:
            if 'image' in link.get('type', ''):
                return link.get('href')
    
    # ২. ডেসক্রিপশন বা সামারি থেকে ছবি খোঁজা (BeautifulSoup ব্যবহার করে)
    content = entry.get('summary', '') or entry.get('description', '')
    soup = BeautifulSoup(content, 'html.parser')
    img_tag = soup.find('img')
    
    if img_tag and img_tag.get('src'):
        return img_tag.get('src')
    
    # ৩. যদি কোনো ছবি না পাওয়া যায় তবে একটি প্রফেশনাল ডিফল্ট ইমেজ
    return "https://i.imgur.com/uP1pY9u.png" # এটি একটি সুন্দর 'Sale' ব্যানার

# ৩. ডিল হান্টিং লজিক
def start_bot():
    feeds = ["https://indiafreestuff.in/feed", "https://www.desidime.com/new.atom"]
    
    processed_count = 0
    for f_url in feeds:
        print(f"Checking feed: {f_url}")
        feed = feedparser.parse(f_url)
        
        for entry in feed.entries[:5]: # প্রতিটি সাইট থেকে লেটেস্ট ৫টি ডিল দেখবে
            title = entry.title.split('|')[0].strip()
            
            # ফিল্টার: বাজে কন্টেন্ট বাদ দেওয়া
            if any(x in title.lower() for x in ["how to", "review", "guide", "expired"]): 
                continue
            
            # ইমেজ এবং লিঙ্ক সংগ্রহ
            img_url = get_image_from_entry(entry)
            link = entry.link
            
            # পোস্ট পাঠানো
            send_deal(title, link, img_url)
            processed_count += 1
            time.sleep(8) # টেলিগ্রাম স্প্যাম রোধে বিরতি
            
            if processed_count >= 10: break # একবারে ১০টির বেশি পোস্ট করবে না

if __name__ == "__main__":
    # BeautifulSoup লাইব্রেরি না থাকলে ইন্সটল করতে হবে: pip install beautifulsoup4
    start_bot()
