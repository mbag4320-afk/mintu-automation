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

# ২. ইমেজ ভ্যালিডেশন এবং ফিল্টারিং
def get_clean_image(entry):
    content = entry.get('summary', '') + entry.get('description', '')
    soup = BeautifulSoup(content, 'html.parser')
    img_tag = soup.find('img')
    
    default_img = "https://i.imgur.com/uP1pY9u.png" # একটি হাই-কোয়ালিটি সেল ব্যানার

    if img_tag and img_tag.get('src'):
        img_url = img_tag.get('src')
        
        # ব্লকিং এবং রিজিয়ন রেস্ট্রিকটেড ইমেজ ফিল্টার
        bad_patterns = ["ytimg", "not-viewable", "pixel", "logo", "banner", "placeholder"]
        if any(pattern in img_url.lower() for pattern in bad_patterns):
            return default_img
            
        # যদি ডেসক্রিপশনে খুব ছোট ছবি থাকে (আইকন বা লোগো), তবে ডিফল্ট ইমেজ ব্যবহার হবে
        return img_url
    
    return default_img

# ৩. মেইন রানার
def start_bot():
    # ডিল সোর্সগুলো
    feeds = [
        "https://indiafreestuff.in/feed", 
        "https://www.desidime.com/new.atom"
    ]
    
    print("🔍 Searching for fresh deals...")
    posted_count = 0
    
    # অপ্রয়োজনীয় আর্টিকেল ফিল্টার (আপনার স্ক্রিনশটের মতো "Best Floor Cleaner" জাতীয় আর্টিকেল বাদ দেবে)
    blacklist = ["best", "top", "review", "how to", "guide", "indian homes", "worth", "every drop", "alchemy"]

    for f_url in feeds:
        feed = feedparser.parse(f_url)
        for entry in feed.entries[:8]: 
            title = entry.title.split('|')[0].strip()
            
            # আর্টিকেল বা লিদটি বাদ দেওয়ার ফিল্টার
            if any(word in title.lower() for word in blacklist):
                continue
            
            img = get_clean_image(entry)
            
            if send_deal(title, entry.link, img):
                print(f"✅ Posted: {title[:40]}...")
                posted_count += 1
                time.sleep(20) # প্রতি পোস্টের মাঝে ২০ সেকেন্ড বিরতি (টেলিগ্রাম স্প্যাম প্রোটেকশন)
            
            if posted_count >= 4: break # প্রতিবার সর্বোচ্চ ৪টি পোস্ট হবে
        if posted_count >= 4: break

if __name__ == "__main__":
    start_bot()
    def start_bot():
    # এটি নিশ্চিত করবে যে বটটি কানেক্টেড আছে
    print("🚀 Running connection test...")
    send_deal("BOT CONNECTION TEST - SUCCESSFUL", "https://google.com", "https://i.imgur.com/uP1pY9u.png")
    
    feeds = [
        "https://indiafreestuff.in/feed", 
        "https://www.desidime.com/new.atom"
    ]
    
    print("🔍 Searching for fresh deals...")
    posted_count = 0
    
    # ফিল্টার একটু কমিয়ে দেওয়া হলো যেন ডিল পাওয়া যায়
    blacklist = ["alchemy", "expired", "registration"]

    for f_url in feeds:
        feed = feedparser.parse(f_url)
        print(f"📡 Checking {f_url}: Found {len(feed.entries)} items") # এটি লগে দেখাবে কয়টি আইটেম পেয়েছে
        
        for entry in feed.entries[:10]: # ১০টি আইটেম চেক করবে
            title = entry.title.split('|')[0].strip()
            
            if any(word in title.lower() for word in blacklist):
                continue
            
            img = get_clean_image(entry)
            print(f"📤 Attempting to post: {title}") # লগে দেখাবে কোনটি পোস্ট করার চেষ্টা করছে
            
            if send_deal(title, entry.link, img):
                posted_count += 1
                time.sleep(15)
            
            if posted_count >= 5: break
        if posted_count >= 5: break

if __name__ == "__main__":
   def start_bot():
    # এটি নিশ্চিত করবে যে বটটি কানেক্টেড আছে
    print("🚀 Running connection test...")
    send_deal("BOT CONNECTION TEST - SUCCESSFUL", "https://google.com", "https://i.imgur.com/uP1pY9u.png")
    
    feeds = [
        "https://indiafreestuff.in/feed", 
        "https://www.desidime.com/new.atom"
    ]
    
    print("🔍 Searching for fresh deals...")
    posted_count = 0
    
    # ফিল্টার একটু কমিয়ে দেওয়া হলো যেন ডিল পাওয়া যায়
    blacklist = ["alchemy", "expired", "registration"]

    for f_url in feeds:
        feed = feedparser.parse(f_url)
        print(f"📡 Checking {f_url}: Found {len(feed.entries)} items") # এটি লগে দেখাবে কয়টি আইটেম পেয়েছে
        
        for entry in feed.entries[:10]: # ১০টি আইটেম চেক করবে
            title = entry.title.split('|')[0].strip()
            
            if any(word in title.lower() for word in blacklist):
                continue
            
            img = get_clean_image(entry)
            print(f"📤 Attempting to post: {title}") # লগে দেখাবে কোনটি পোস্ট করার চেষ্টা করছে
            
            if send_deal(title, entry.link, img):
                posted_count += 1
                time.sleep(15)
            
            if posted_count >= 5: break
        if posted_count >= 5: break

if __name__ == "__main__":
    start_bot()
    
