import os
import requests
import feedparser
import time
import random

def get_product_image(entry):
    # ছবি খোঁজার জন্য বিভিন্ন সোর্স চেক করা
    img = "https://img.freepik.com/free-vector/special-offer-modern-sale-banner-template_1017-20667.jpg"
    if 'media_content' in entry:
        img = entry.media_content[0]['url']
    elif 'links' in entry:
        for l in entry.links:
            if 'image' in l.get('type', ''):
                img = l.href
    return img

def send_mega_deal_post(title, link, image_url):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    amazon_tag = "offerslive24-21"

    if "amazon.in" in link:
        conn = "&" if "?" in link else "?"
        link = f"{link}{conn}tag={amazon_tag}"

    # ভিডিওর মতো প্রফেশনাল ডিজাইন
    caption = (
        f"🚨 *SUPER LOOT DEAL* 🚨\n\n"
        f"🛒 *{title.upper()}*\n\n"
        f"🔥 *Status:* Hot Deal / Price Drop\n"
        f"✅ *Verified Quality*\n\n"
        f"👉 [GRAB THIS DEAL NOW]({link})\n"
        f"👉 [GRAB THIS DEAL NOW]({link})\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎁 *More Stores:* [Amazon](https://www.amazon.in/gp/goldbox?tag={amazon_tag}) | [Flipkart](https://fktr.in/7WhPb8j)"
    )

    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": image_url, "caption": caption, "parse_mode": "Markdown"}
    
    r = requests.post(url, data=payload)
    print(f"Sent: {title} | Status: {r.status_code}")

def get_deals():
    # ডিল সোর্স
    urls = [
        "https://indiafreestuff.in/feed",
        "https://www.desidime.com/new.atom"
    ]
    
    posted = 0
    for url in urls:
        print(f"Checking: {url}")
        feed = feedparser.parse(url, agent='Mozilla/5.0')
        
        if not feed.entries:
            print(f"No entries found in {url}")
            continue

        for entry in feed.entries:
            title = entry.title
            link = entry.link
            
            # আগের চেয়ে সহজ ফিল্টার: শুধু 'how to' বা 'review' টাইপ পোস্ট বাদ দেবে
            skip = ["how to", "review", "guide", "tips"]
            if any(x in title.lower() for x in skip):
                continue
            
            img = get_product_image(entry)
            send_mega_deal_post(title, link, img)
            posted += 1
            time.sleep(5)
            
            if posted >= 3: return # একবারে ৩টি ডিল

if __name__ == "__main__":
    get_deals()
