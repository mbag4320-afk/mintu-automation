import os
import requests
import feedparser
import time
import random

def send_mega_deal_post(title, link, image_url):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    amazon_tag = "offerslive24-21"

    # ডিল লিঙ্কটি আপনার আমাজন আইডি দিয়ে তৈরি করা
    if "amazon.in" in link:
        link = f"{link}&tag={amazon_tag}" if "?" in link else f"{link}?tag={amazon_tag}"

    # ভিডিওর মতো প্রফেশনাল মেসেজ ফরম্যাট
    caption = (
        f"🔥 *MEGA LOOT DEAL* 🔥\n\n"
        f"📦 *{title}*\n\n"
        f"💰 *Price:* Check Link for Best Offer\n"
        f"🚚 *Free Delivery Available*\n\n"
        f"👉 [Click Here to Buy Now]({link})\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔗 *More Stores:* [Flipkart](https://fktr.in/7WhPb8j) | [Myntra](https://myntr.it/b9SAtFm)"
    )

    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {
        "chat_id": chat_id,
        "photo": image_url,
        "caption": caption,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

def get_and_post_deals():
    # অনেকগুলো ডিল সোর্স যাতে কখনোই খালি না থাকে
    urls = [
        "https://indiafreestuff.in/feed",
        "https://www.freekaamaal.com/feed"
    ]
    
    found_deals = []
    for url in urls:
        feed = feedparser.parse(url, agent='Mozilla/5.0')
        if feed.entries:
            found_deals.extend(feed.entries[:3]) # প্রতি সাইট থেকে ৩টি করে নেবে

    if found_deals:
        # ব্যানার ইমেজের ব্যাকআপ
        banners = [
            "https://img.freepik.com/free-vector/special-offer-modern-sale-banner-template_1017-20667.jpg",
            "https://img.freepik.com/free-vector/gradient-mobile-store-sale-background_23-2150319114.jpg"
        ]

        for entry in found_deals[:4]: # সর্বোচ্চ ৪টি পোস্ট করবে
            title = entry.title.split('|')[0].strip()
            link = entry.link
            
            # ছবি খুঁজে বের করা
            img = random.choice(banners)
            if 'media_content' in entry:
                img = entry.media_content[0]['url']
            elif 'links' in entry:
                for l in entry.links:
                    if 'image' in l.get('type', ''):
                        img = l.href
            
            send_mega_deal_post(title, link, img)
            time.sleep(5) # প্রতিটি পোস্টের মাঝে ৫ সেকেন্ড গ্যাপ
    else:
        print("No new deals to post.")

if __name__ == "__main__":
    # নিউজ ও প্রাইজ ছাড়াই সরাসরি ডিল পোস্ট হবে (ভিডিওর মতো)
    get_and_post_deals()
