import os
import requests
import feedparser
import time

def send_telegram_post(title, link, image_url):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    amazon_tag = "offerslive24-21"

    # আমাজন লিঙ্ক হলে আপনার আইডি যোগ করা হচ্ছে
    if "amazon.in" in link:
        connector = "&" if "?" in link else "?"
        link = f"{link}{connector}tag={amazon_tag}"

    # মেসেজ ফরম্যাট (ভিডিওর মতো পরিষ্কার)
    caption = f"🛍️ *{title}*\n\n🔥 *Limited Time Deal! Grab it now!*\n\n👉 [Click Here to Buy]({link})"

    # টেলিগ্রামে পোস্ট পাঠানো
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {
        "chat_id": chat_id,
        "photo": image_url,
        "caption": caption,
        "parse_mode": "Markdown"
    }
    
    try:
        res = requests.post(url, data=payload)
        print(f"Post Sent: {title}")
    except Exception as e:
        print(f"Error sending post: {e}")

def get_and_post_deals():
    # লেটেস্ট ডিল সোর্স
    url = "https://indiafreestuff.in/feed"
    feed = feedparser.parse(url)
    
    if not feed.entries:
        print("No new deals found.")
        return

    # সর্বশেষ ৫টি ডিল আলাদা আলাদা ভাবে পোস্ট করা হবে
    for entry in feed.entries[:5]:
        title = entry.title.split('|')[0].strip()
        link = entry.link
        
        # ডিল থেকে ছবি বের করার চেষ্টা
        image_url = "https://img.freepik.com/free-vector/special-offer-modern-sale-banner-template_1017-20667.jpg" # ডিফল্ট ছবি
        if 'media_content' in entry:
            image_url = entry.media_content[0]['url']
        elif 'links' in entry:
            for l in entry.links:
                if 'image' in l.get('type', ''):
                    image_url = l.href
        
        # প্রতি পোস্টের মাঝে ৫ সেকেন্ড বিরতি (টেলিগ্রাম স্প্যাম রোধ করতে)
        send_telegram_post(title, link, image_url)
        time.sleep(5)

if __name__ == "__main__":
    get_and_post_deals()
    print("All Deals Posted in MEGA Deals Style!")
