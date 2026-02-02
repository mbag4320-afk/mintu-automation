import os
import requests
import feedparser
import random

# ১. সরাসরি সেরা ডিল খুঁজে বের করার ফাংশন (Active Feed)
def get_latest_deals():
    # ইন্ডিয়ার সবথেকে সক্রিয় একটি ডিল সাইটের ফিড ব্যবহার করছি
    url = "https://indiafreestuff.in/feed"
    feed = feedparser.parse(url)
    amazon_tag = "offerslive24-21"
    
    deals_text = "🚨 *LOOT ALERT: Best Discounts Right Now!* 🚨\n\n"
    
    # যদি ফিড খালি না থাকে
    if feed.entries:
        # সর্বশেষ ৫টি সেরা ডিল নেওয়া হচ্ছে
        for entry in feed.entries[:5]:
            title = entry.title
            link = entry.link
            
            # টাইটেলটি একটু সুন্দর করা (অপ্রয়োজনীয় অংশ বাদ দেওয়া)
            clean_title = title.split('|')[0].strip()
            
            # আমাজন লিঙ্ক হলে আপনার ট্যাগ যোগ হবে
            if "amazon.in" in link:
                connector = "&" if "?" in link else "?"
                link = f"{link}{connector}tag={amazon_tag}"
            
            deals_text += f"🔥 *{clean_title}*\n👉 [View Deal & Shop Here]({link})\n\n"
    else:
        # যদি ডিল না পাওয়া যায় তবে ব্যাকআপ ক্যাটাগরি দেখাবে
        deals_text += "🔍 *Scanning for new loot deals...*\nIn the meantime, check our top categories below! 👇\n\n"
    
    return deals_text

# ২. হেলথ টিপস
def get_health_tip():
    tips = [
        "💧 পর্যাপ্ত জল পান করুন, এটি শরীর সতেজ রাখে।",
        "🥗 খাবারে লবণের পরিমাণ কমান, রক্তচাপ নিয়ন্ত্রণে থাকবে।",
        "😴 রাতে অন্তত ৭-৮ ঘণ্টা ঘুমানোর অভ্যাস করুন।",
        "🍎 প্রতিদিন অন্তত একটি ঋতুভিত্তিক ফল খান।",
        "🚶‍♂️ দিনে অন্তত ২০ মিনিট দ্রুত হাঁটার অভ্যাস করুন।"
    ]
    return f"🍎 *Daily Health Tip:*\n_{random.choice(tips)}_\n"

# ৩. পার্মানেন্ট শপিং মেনু (যাতে মেসেজ কখনো খালি না দেখায়)
def get_permanent_menu():
    tag = "offerslive24-21"
    menu = "\n🛍️ *Shop by Categories:*\n"
    menu += f"📱 [Mobiles](https://www.amazon.in/mobiles?tag={tag}) | 💻 [Laptops](https://www.amazon.in/electronics?tag={tag})\n"
    menu += f"👗 [Fashion]({os.getenv('MYNTRA_LINK', 'https://myntr.it/b9SAtFm')}) | 🛍️ [Flipkart Loot]({os.getenv('FLIPKART_LINK', 'https://fktr.in/7WhPb8j')})\n"
    menu += "\n✨ *Hurry! Offers are valid for a limited time.*"
    return menu

# ৪. টেলিগ্রামে মেসেজ পাঠানোর ফাংশন
def send_telegram_message(message):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id, 
        "text": message, 
        "parse_mode": "Markdown", 
        "disable_web_page_preview": True 
    }
    requests.post(url, data=payload)

if __name__ == "__main__":
    # সব ডাটা একসাথে সাজানো
    final_message = get_latest_deals() + get_health_tip() + get_permanent_menu()
    send_telegram_message(final_message)
    print("Deal Hunter 2.0 Successful!")
