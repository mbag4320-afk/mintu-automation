import os
import requests
import feedparser
import time
import random
import re

def get_product_image(entry):
    # সোর্স থেকে আসল ছবি খুঁজে বের করার চেষ্টা
    img = "https://img.freepik.com/free-vector/special-offer-modern-sale-banner-template_1017-20667.jpg"
    if 'media_content' in entry:
        img = entry.media_content[0]['url']
    elif 'description' in entry:
        # ডেসক্রিপশনের ভেতর থেকে ইমেজ ট্যাগ খোঁজা
        match = re.search(r'<img [^>]*src="([^"]+)"', entry.description)
        if match:
            img = match.group(1)
    return img

def send_mega_deal_post(title, link, image_url):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    amazon_tag = "offerslive24-21"

    # ডিরেক্ট আমাজন লিঙ্ক তৈরির চেষ্টা
    if "amazon.in" in link:
        link = f"{link}&tag={amazon_tag}" if "?" in link else f"{link}?tag={amazon_tag}"

    # মেসেজ ডিজাইন (আরো পরিষ্কার ও বড় ফন্ট)
    caption = (
        f"🚨 *SUPER LOOT DEAL* 🚨\n\n"
        f"🛒 *{title.upper()}*\n\n"
        f"💰 *Status:* Limited Stock / Price Drop\n"
        f"✅ *Verified Deal*\n\n"
        f"👉 [GRAB THIS DEAL NOW]({link})\n"
        f"👉 [GRAB THIS DEAL NOW]({link})\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎁 *More Offers:* [Amazon](https://www.amazon.in/gp/goldbox?tag={amazon_tag}) | [Flipkart](https://fktr.in/7WhPb8j)"
    )

    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": image_url, "caption": caption, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def get_filtered_deals():
    # ডিল সোর্স (অধিক নির্ভরযোগ্য সোর্স যোগ করা হয়েছে)
    urls = ["https://www.desidime.com/new.atom", "https://indiafreestuff.in/feed"]
    
    posted_count = 0
    for url in urls:
        feed = feedparser.parse(url, agent='Mozilla/5.0')
        if not feed.entries: continue

        for entry in feed.entries:
            title = entry.title
            link = entry.link

            # ফিল্টার: অপ্রয়োজনীয় আর্টিকেল বা সাধারণ পোস্ট বাদ দেওয়া হচ্ছে
            skip_keywords = ["best of", "how to", "top 10", "guide", "review", "tips"]
            if any(word in title.lower() for word in skip_keywords):
                continue
            
            # শুধুমাত্র সেই ডিলগুলো নেবে যাতে ডিসকাউন্ট বা নির্দিষ্ট দামের কথা আছে
            if not any(x in title for x in ["Rs.", "₹", "%", "Off", "Loot", "Deal"]):
                continue

            img = get_product_image(entry)
            send_mega_deal_post(title, link, img)
            posted_count += 1
            time.sleep(5)
            
            if posted_count >= 3: return # একবারে সর্বোচ্চ ৩টি ডিল পাঠাবে

if __name__ == "__main__":
    get_filtered_deals()
