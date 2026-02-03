import os
import requests
import feedparser

def send_test_message():
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # এটি চেক করার জন্য একটি সাধারণ মেসেজ
    test_payload = {
        "chat_id": chat_id,
        "text": "🔍 *বট এখন ডিল চেক করছে... সংযোগ ঠিক আছে!*",
        "parse_mode": "Markdown"
    }
    r = requests.post(url, data=test_payload)
    print(f"Test Message Status: {r.status_code}, Response: {r.text}")

def get_and_post_deals():
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    amazon_tag = "offerslive24-21"
    
    # ডিল সোর্স
    feed_url = "https://indiafreestuff.in/feed"
    feed = feedparser.parse(feed_url)
    
    if feed.entries:
        for entry in feed.entries[:3]:
            title = entry.title.split('|')[0].strip()
            link = entry.link
            
            if "amazon.in" in link:
                connector = "&" if "?" in link else "?"
                link = f"{link}{connector}tag={amazon_tag}"
            
            caption = f"🛍️ *{title}*\n\n👉 [Click to Buy]({link})"
            
            # সরাসরি টেক্সট মেসেজ হিসেবে পাঠানোর চেষ্টা (যাতে ছবি লোড না হলেও মেসেজ যায়)
            post_url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": caption,
                "parse_mode": "Markdown"
            }
            requests.post(post_url, data=payload)
            print(f"Posted: {title}")
    else:
        print("No deals found in feed.")

if __name__ == "__main__":
    # প্রথমে কানেকশন চেক করবে
    send_test_message()
    # তারপর ডিল পোস্ট করার চেষ্টা করবে
    get_and_post_deals()
