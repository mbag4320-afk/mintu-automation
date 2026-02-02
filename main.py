import os
import requests
import feedparser # এটি ডিল খুঁজে বের করবে

# ১. সেরা ডিল খুঁজে বের করার ফাংশন
def get_latest_deals():
    # ইন্ডিয়ার একটি জনপ্রিয় ডিল সাইটের ফিড ব্যবহার করছি
    url = "https://www.desidime.com/new.atom"
    feed = feedparser.parse(url)
    amazon_tag = "offerslive24-21"
    
    deals_text = "🚨 *LOOT ALERT: Top Discounts Right Now!* 🚨\n\n"
    
    # সর্বশেষ ৪টি সেরা ডিল নেওয়া হচ্ছে
    for entry in feed.entries[:4]:
        title = entry.title
        link = entry.link
        
        # যদি লিঙ্কটি আমাজনের হয়, তবে আপনার আইডি যোগ হবে
        if "amazon.in" in link:
            if "?" in link:
                link = f"{link}&tag={amazon_tag}"
            else:
                link = f"{link}?tag={amazon_tag}"
        
        deals_text += f"🔥 *{title}*\n👉 [Click to Grab the Deal]({link})\n\n"
    
    deals_text += "✨ *Hurry! Prices may change anytime.*"
    return deals_text

# ২. হেলথ টিপস ফাংশন (আগের মতোই থাকবে)
def get_health_tip():
    tips = ["💧 ৮-১০ গ্লাস জল খান।", "🥗 লবণ কম খান।", "😴 ৭-৮ ঘণ্টা ঘুমান।", "🍎 প্রতিদিন ফল খান।"]
    import random
    return f"\n🍎 *Daily Health Tip:*\n_{random.choice(tips)}_\n"

# ৩. টেলিগ্রামে মেসেজ পাঠানোর ফাংশন
def send_telegram_message(message):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id, 
        "text": message, 
        "parse_mode": "Markdown", 
        "disable_web_page_preview": False 
    }
    requests.post(url, data=payload)

if __name__ == "__main__":
    # এখন আমরা শুধু ডিল এবং হেলথ টিপস পাঠাব (নিউজ বাদ দিচ্ছি যাতে ফোকাস ডিলে থাকে)
    final_message = get_latest_deals() + get_health_tip()
    send_telegram_message(final_message)
    print("Deal Hunter Automation Successful!")
