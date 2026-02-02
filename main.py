import os
import requests
import feedparser
import random

# ১. ক্রিপ্টো প্রাইজ ও নিউজ সংগ্রহের ফাংশন
def get_crypto_data_and_news():
    api_key = os.getenv("NEWS_API_KEY")
    # প্রাইজ ডাটা
    price_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    # নিউজ ডাটা
    news_url = f"https://newsapi.org/v2/everything?q=crypto&pageSize=3&apiKey={api_key}"
    
    content = "📊 *Crypto Market & News:*\n"
    
    try:
        # প্রাইজ যোগ করা হচ্ছে
        p_res = requests.get(price_url).json()
        btc = p_res['bitcoin']['usd']
        eth = p_res['ethereum']['usd']
        content += f"💰 BTC: ${btc} | 💎 ETH: ${eth}\n\n"
        
        # নিউজ যোগ করা হচ্ছে
        n_res = requests.get(news_url).json()
        articles = n_res.get('articles', [])
        for art in articles:
            content += f"🔹 [{art['title']}]({art['url']})\n"
        return content + "\n"
    except:
        return "📊 *Crypto News:* Currently unavailable.\n\n"

# ২. রিয়েল-টাইম লুট ডিল ফাংশন
def get_latest_deals():
    url = "https://indiafreestuff.in/feed"
    feed = feedparser.parse(url)
    amazon_tag = "offerslive24-21"
    deals_text = "🚨 *TOP LOOT DEALS RIGHT NOW!* 🚨\n\n"
    
    if feed.entries:
        for entry in feed.entries[:3]:
            title = entry.title.split('|')[0].strip()
            link = entry.link
            if "amazon.in" in link:
                conn = "&" if "?" in link else "?"
                link = f"{link}{conn}tag={amazon_tag}"
            deals_text += f"🔥 *{title}*\n👉 [Grab This Deal]({link})\n\n"
    else:
        deals_text += "🔍 *Scanning for new loot...*\n\n"
    return deals_text

# ৩. ক্যাটাগরি মেনু (আরও পরিষ্কার ফরম্যাটে)
def get_category_menu():
    tag = "offerslive24-21"
    menu = "━━━ *SHOP BY CATEGORY* ━━━\n\n"
    menu += f"📱 [Smartphones & Accessories](https://www.amazon.in/mobiles?tag={tag})\n"
    menu += f"💻 [Laptops & Electronics](https://www.amazon.in/electronics?tag={tag})\n"
    menu += f"👗 [Fashion & Lifestyle Deals](https://myntr.it/b9SAtFm)\n"
    menu += f"🎁 [Flipkart Mega Loot Offers](https://fktr.in/7WhPb8j)\n\n"
    menu += "⚡ *Hurry! Grab before price increases!*"
    return menu

# ৪. ডাইনামিক ব্যানার ও মেসেজ পাঠানোর ফাংশন
def send_telegram_with_random_banner(message):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    
    # প্রফেশনাল শপিং ব্যানারের একটি লিস্ট (প্রতিবার এখান থেকে একটি আলাদা ছবি নেবে)
    banners = [
        "https://img.freepik.com/free-vector/special-offer-modern-sale-banner-template_1017-20667.jpg",
        "https://img.freepik.com/free-vector/gradient-mobile-store-sale-background_23-2150319114.jpg",
        "https://img.freepik.com/free-vector/fashion-sale-banner-template_23-2148522533.jpg",
        "https://img.freepik.com/free-vector/flat-sale-banner-with-photo-product_23-2149026968.jpg",
        "https://img.freepik.com/free-vector/online-shopping-horizontal-banner-solution_23-2148897328.jpg"
    ]
    
    photo_url = random.choice(banners) # লটারি করে একটি ছবি বেছে নেওয়া হচ্ছে
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {
        "chat_id": chat_id,
        "photo": photo_url,
        "caption": message,
        "parse_mode": "Markdown"
    }
    requests.post(
