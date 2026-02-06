import os
import requests
import feedparser
import time
from bs4 import BeautifulSoup

# ১. টেলিগ্রামে প্রফেশনাল ডিল পোস্ট পাঠানোর ফাংশন
def send_deal(title, link, img_url, store_name):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    amazon_tag = "offerslive24-21" # আপনার আমাজন ট্যাগ
    
    # আমাজন লিঙ্ক হলে আপনার ট্যাগ যোগ হবে
    if "amazon.in" in link:
        link = f"{link}&tag={amazon_tag}" if "?" in link else f"{link}?tag={amazon_tag}"
        store_display = "🛒 Store: AMAZON 🇮🇳"
    elif "flipkart.com" in link:
        store_display = "🛒 Store: FLIPKART 🛍️"
    else:
        store_display = f"🛒 Store: {store_name.upper()}"
    
    # প্রফেশনাল ক্যাপশন (মানুষের ভরসা জেতার জন্য ডিজাইন)
    caption = (
        f"🌟 <b>TRUSTED LOOT DEAL</b> 🌟\n\n"
        f"🔥 <b>{title.upper()}</b>\n\n"
        f"{store_display}\n"
        f"✅ <b>Status:</b> Verified & Handpicked\n"
        f"📢 <b>Price Drop Alert! Grab it now.</b>\n\n"
        f"👉 <a href='{link}'>CLICK HERE TO BUY NOW</a>\n"
        f"👉 <a href='{link}'>CLICK HERE TO BUY NOW</a>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎁 <b>More Deals:</b> <a href='https://www.amazon.in/gp/goldbox?tag={amazon_tag}'>Today's Deals</a>\n"
        f"⚡ <i>Join @offers_live_24 for verified loots!</i>"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": img_url, "caption": caption, "parse_mode": "HTML"}
    
    try:
        r = requests.post(url, data=payload)
        return r.status_code == 200
    except:
        return False

# ২. ডিল থেকে আসল ছবি বের করার ফাংশন
def get_clean_image(entry):
    content = entry.get('summary', '') + entry.get('description', '')
    soup = BeautifulSoup(content, 'html.parser')
    img = soup.find('img')
    
    # ডিফল্ট প্রফেশনাল শপিং ব্যানার (যদি ছবি না পাওয়া যায়)
    fallback_img = "https://cdn-icons-png.flaticon.com/512/1162/1162499.png"

    if img and img.get('src'):
        img_url = img.get('src')
        if "pixel" in img_url or "logo" in img_url:
            return fallback_img
        return img_url
    return fallback_img

# ৩. মেইন রানার (বিশ্বস্ত সোর্স থেকে ডিল খোঁজা)
def start_bot():
    # ভারতের সবচেয়ে বিশ্বস্ত ৩টি ডিল ফিড
    feeds = [
        {"name": "DesiDime", "url": "https://www.desidime.com/new.atom"},
        {"name": "IndiaFreeStuff", "url": "https://indiafreestuff.in/feed"},
        {"name": "FreeKaaMaal", "url": "https://www.freekaamaal.com/feed"}
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    print("🔍 Searching for trusted deals...")
    posted_count = 0
    
    # ফিল্টার: আর্টিকেল বা অপ্রয়োজনীয় কন্টেন্ট বাদ দেওয়ার জন্য
    blacklist = ["how to", "guide", "review", "expired", "registration", "best floor cleaner", "indian homes"]

    for source in feeds:
        try:
            resp = requests.get(source['url'], headers=headers, timeout=15)
            feed = feedparser.parse(resp.content)
            
            for entry in feed.entries[:5]:
                title = entry.title.split('|')[0].strip()
                
                # যদি টাইটেলে ব্ল্যাকলিস্ট করা কোনো শব্দ থাকে তবে তা বাদ দেবে
                if any(word in title.lower() for word in blacklist):
                    continue
                
                img = get_clean_image(entry)
                link = entry.link
                
                if send_deal(title, link, img, source['name']):
                    print(f"✅ Success: {title[:30]} from {source['name']}")
                    posted_count += 1
                    time.sleep(15) # স্প্যাম রোধে বিরতি
            
            if posted_count >= 6: break # একবারে ৬টির বেশি পোস্ট করবে না
        except:
            continue

if __name__ == "__main__":
    start_bot()
