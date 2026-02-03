import os
import requests
import feedparser
import random
import time

# ১. সরাসরি টেলিগ্রামে ফটোসহ পোস্ট পাঠানোর ফাংশন
def send_deal(title, link, img):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    amazon_tag = "offerslive24-21"
    
    # আমাজন লিঙ্ক হলে আপনার ট্যাগ যোগ হবে
    if "amazon.in" in link:
        link = f"{link}&tag={amazon_tag}" if "?" in link else f"{link}?tag={amazon_tag}"
    
    caption = (
        f"🚨 *MEGA LOOT DEAL* 🚨\n\n"
        f"🛒 *{title.upper()}*\n\n"
        f"🔥 *Status:* Hot Deal / Price Drop\n\n"
        f"👉 [GRAB THIS DEAL NOW]({link})\n"
        f"👉 [GRAB THIS DEAL NOW]({link})\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎁 *More Stores:* [Amazon](https://www.amazon.in/gp/goldbox?tag={amazon_tag}) | [Flipkart](https://fktr.in/7WhPb8j)"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": img, "caption": caption, "parse_mode": "Markdown"}
    r = requests.post(url, data=payload)
    print(f"Posted: {title} | Status: {r.status_code}")

# ২. ডিল হান্টিং লজিক
def start_bot():
    # ডিল সোর্সগুলো
    feeds = ["https://indiafreestuff.in/feed", "https://www.desidime.com/new.atom"]
    
    all_entries = []
    for f_url in feeds:
        feed = feedparser.parse(f_url, agent='Mozilla/5.0')
        if feed.entries:
            all_entries.extend(feed.entries[:5])

    # ডাইনামিক ইমেজের লিস্ট
    banners = [
        "https://img.freepik.com/free-vector/special-offer-modern-sale-banner-template_1017-20667.jpg",
        "https://img.freepik.com/free-vector/gradient-mobile-store-sale-background_23-2150319114.jpg",
        "https://img.freepik.com/free-vector/fashion-sale-banner-template_23-2148522533.jpg"
    ]

    if all_entries:
        # ওয়েবসাইট থেকে পাওয়া ডিলগুলো পোস্ট হবে
        for entry in all_entries[:3]:
            title = entry.title.split('|')[0].strip()
            # গাইড বা রিভিউ বাদ দেওয়ার ফিল্টার
            if any(x in title.lower() for x in ["how to", "review", "guide"]): continue
            
            send_deal(title, entry.link, random.choice(banners))
            time.sleep(5)
    else:
        # যদি কোনো সাইট থেকে ডিল না পাওয়া যায়, তবে এই "সেরা ৩টি ডিল" অবশ্যই যাবে
        print("No live deals found, sending fallback deals...")
        fallback_deals = [
            {"t": "Top Budget Smartphones Under 15000", "l": "https://www.amazon.in/s?k=smartphones+under+15000"},
            {"t": "Best Selling Smartwatches & Gadgets", "l": "https://www.amazon.in/s?k=smartwatches"},
            {"t": "Today's Biggest Price Drops on Laptops", "l": "https://www.amazon.in/s?k=laptops+deals"}
        ]
        for deal in fallback_deals:
            send_deal(deal['t'], deal['l'], random.choice(banners))
            time.sleep(5)

if __name__ == "__main__":
    start_bot()
