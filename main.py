import os
import requests
import feedparser
import random

# ১. ক্রিপ্টো নিউজ সংগ্রহের ফাংশন (যা আপনি আবার দেখতে চেয়েছিলেন)
def get_crypto_news():
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/everything?q=crypto&pageSize=3&apiKey={api_key}"
    try:
        response = requests.get(url).json()
        articles = response.get('articles', [])
        news_text = "📰 *Latest Crypto News:*\n"
        for art in articles:
            news_text += f"🔹 [{art['title']}]({art['url']})\n"
        return news_text + "\n"
    except:
        return "📰 *News currently unavailable.*\n\n"

# ২. ডিল খুঁজে বের করার ফাংশন
def get_latest_deals():
    url = "https://indiafreestuff.in/feed"
    feed = feedparser.parse(url)
    amazon_tag = "offerslive24-21"
    deals_text = "🚨 *LOOT ALERT: Best Discounts Now!* 🚨\n\n"
    
    if feed.entries:
        for entry in feed.entries[:3]: # ৩টি সেরা ডিল
            title = entry.title.split('|')[0].strip()
            link = entry.link
            if "amazon.in" in link:
                connector = "&" if "?" in link else "?"
                link = f"{link}{connector}tag={amazon_tag}"
            deals_text += f"🔥 *{title}*\n👉 [Grab Deal]({link})\n\n"
    else:
        deals_text += "🔍 *Scanning for new loot deals...*\n\n"
    return deals_text

# ৩. ডেইলি হেলথ টিপস
def get_health_tip():
    tips = ["💧 পর্যাপ্ত জল খান।", "🥗 লবণ কম খান।", "😴 ৭-৮ ঘণ্টা ঘুমান।", "🍎 প্রতিদিন ফল খান।"]
    return f"🍎 *Daily Health Tip:* _{random.choice(tips)}_\n\n"

# ৪. শপিং ক্যাটাগরি (ইমোজি সহ সুন্দর সাজানো)
def get_category_menu():
    tag = "offerslive24-21"
    menu = "🛍️ *Shop by Categories:*\n"
    menu += f"📱 [Smartphones](https://www.amazon.in/mobiles?tag={tag}) | 💻 [Laptops](https://www.amazon.in/electronics?tag={tag})\n"
    menu += f"👗 [Fashion Deals](https://myntr.it/b9SAtFm) | 🎁 [Loot Offers](https://fktr.in/7WhPb8j)\n\n"
    menu += "✨ *Hurry! Grab before prices go up!*"
    return menu

# ৫. টেলিগ্রামে ছবি সহ মেসেজ পাঠানোর ফাংশন
def send_telegram_with_photo(message):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    
    # একটি প্রফেশনাল শপিং ব্যানারের ছবি লিঙ্ক
    photo_url = "https://img.freepik.com/free-vector/shopping-online-banner-with-discount-tags_52683-11671.jpg"
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {
        "chat_id": chat_id,
        "photo": photo_url,
        "caption": message, # পুরো মেসেজটি ছবির নিচে ক্যাপশন হিসেবে যাবে
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

if __name__ == "__main__":
    # সব ডাটা একসাথে সাজানো (নিউজ + ডিল + টিপস + ক্যাটাগরি)
    final_content = get_crypto_news() + get_latest_deals() + get_health_tip() + get_category_menu()
    send_telegram_with_photo(final_content)
    print("Beautiful Post with News and Photo Sent!")
