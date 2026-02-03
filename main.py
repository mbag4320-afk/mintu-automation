import os
import requests
import feedparser
import time

def send_telegram_post(title, link, image_url):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    amazon_tag = "offerslive24-21"

    if "amazon.in" in link:
        connector = "&" if "?" in link else "?"
        link = f"{link}{connector}tag={amazon_tag}"

    caption = f"🛍️ *{title}*\n\n🔥 *Limited Time Deal! Grab it now!*\n\n👉 [Click Here to Buy]({link})"

    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {
        "chat_id": chat_id,
        "photo": image_url,
        "caption": caption,
        "parse_mode": "Markdown"
    }
    
    try:
        res = requests.post(url, data=payload)
        print(f"Telegram response for {title}: {res.status_code}")
    except Exception as e:
        print(f"Error sending post: {e}")

def get_and_post_deals():
    # একাধিক ডিল সোর্স (যদি একটি কাজ না করে অন্যটি করবে)
    urls = [
        "https://indiafreestuff.in/feed",
        "https://www.desidime.com/new.atom"
    ]
    
    found_any = False
    for url in urls:
        print(f"Checking feed: {url}")
        feed = feedparser.parse(url)
        
        if feed.entries:
            found_any = True
            print(f"Found {len(feed.entries)} deals in {url}")
            for entry in feed.entries[:3]: # প্রতিবার ৩টি করে সেরা ডিল পাঠাবে
                title = entry.title.split('|')[0].strip()
                link = entry.link
                
                # ইমেজ খুঁজে বের করার ভালো পদ্ধতি
                image_url = "https://img.freepik.com/free-vector/special-offer-modern-sale-banner-template_1017-20667.jpg"
                if 'media_content' in entry:
                    image_url = entry.media_content[0]['url']
                elif 'links' in entry:
                    for l in entry.links:
                        if 'image' in l.get('type', ''):
                            image_url = l.href
                
                send_telegram_post(title, link, image_url)
                time.sleep(3) # পোস্টের মাঝে ৩ সেকেন্ড বিরতি
            break # একটি সোর্স থেকে ডিল পেয়ে গেলে আর পরেরটা চেক করবে না
            
    if not found_any:
        print("No active deals found at this moment.")

if __name__ == "__main__":
    get_and_post_deals()
