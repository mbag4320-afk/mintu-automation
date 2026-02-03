import os
import requests
import feedparser
import random
import time

# ১. ক্রিপ্টো প্রাইজ ও নিউজ
def get_crypto_update():
    try:
        price_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        res = requests.get(price_url).json()
        btc, eth = res['bitcoin']['usd'], res['ethereum']['usd']
        
        news_api = os.getenv("NEWS_API_KEY")
        news_url = f"https://newsapi.org/v2/everything?q=crypto&pageSize=2&apiKey={news_api}"
        n_res = requests.get(news_url).json()
        articles = n_res.get('articles', [])
        
        msg = f"📊 *Live Market:* BTC: ${btc} | ETH: ${eth}\n\n"
        msg += "*Breaking News:*\n"
        for art in articles:
            msg += f"🔹 [{art['title'][:65]}...]({art['url']})\n"
        return msg + "\n"
    except:
        return "📊 *Market Update:* Synchronizing data...\n\n"

# ২. মাল্টি-সোর্স ডিল হান্টার (উন্নত ভার্সন)
def post_mega_deals():
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    amazon_tag = "offerslive24-21"
    
    sources = [
        "https://indiafreestuff.in/feed",
        "https://www.freekaamaal.com/feed",
        "https://www.desidime.com/new.atom"
    ]
    
    all_entries = []
    for url in sources:
        feed = feedparser.parse(url, agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
        if feed.entries:
            all_entries.extend(feed.entries[:3])
    
    # ব্যানার ইমেজের লিস্ট
    banners = [
        "https://img.freepik.com/free-vector/special-offer-modern-sale-banner-template_1017-20667.jpg",
        "https://img.freepik.com/free-vector/gradient-mobile-store-sale-background_23-2150319114.jpg",
        "https://img.freepik.com/free-vector/fashion-sale-banner-template_23-2148522533.jpg"
    ]

    if all_entries:
        random.shuffle(all_entries)
        for entry in all_entries[:3]:
            title = entry.title.split('|')[0].strip()
            link = entry.link
            if "amazon.in" in link:
                link = f"{link}&tag={amazon_tag}" if "?" in link else f"{link}?tag={amazon_tag}"
            
            img = random.choice(banners)
            caption = f"🛍️ *{title}*\n\n🔥 *Loot Deal! Don't miss out!*\n\n👉 [Click to Grab the Offer]({link})"
            requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", data={"chat_id": chat_id, "photo": img, "caption": caption, "parse_mode": "Markdown"})
            time.sleep(4)
    else:
        # যদি কোনো লাইভ ডিল না থাকে, তবে একটি রিকমেন্ডেড প্রোডাক্ট পাঠাবে (ইনকাম সচল রাখতে)
        fallbacks = [
            {"t": "Top Budget Smartphones Under 15k", "l": "https://www.amazon.in/s?k=smartphones+under+15000"},
            {"t": "Best Selling Wireless Headphones", "l": "https://www.amazon.in/s?k=wireless+headphones"},
            {"t": "Today's Lightning Deals on Electronics", "l": "https://www.amazon.in/gp/goldbox"}
        ]
        pick = random.choice(fallbacks)
        link = f"{pick['l']}?tag={amazon_tag}"
        caption = f"⭐ *Recommended for You:*\n*{pick['t']}*\n\n🔥 *Check out the best prices right now!*\n\n👉 [Shop Now]({link})"
        requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", data={"chat_id": chat_id, "photo": banners[0], "caption": caption, "parse_mode": "Markdown"})

# ৩. হেলথ টিপস ও ক্যাটাগরি মেনু
def get_footer():
    tips = ["💧 পর্যাপ্ত জল পান করুন।", "🥗 লবণ কম খান।", "😴 ৭-৮ ঘণ্টা ঘুমান।", "🚶‍♂️ ২০ মিনিট হাঁটার অভ্যাস করুন।"]
    tag = "offerslive24-21"
    
    footer = f"🍎 *Daily Health Tip:* _{random.choice(tips)}_\n\n"
    footer += "━━━━━━━━━━━━━━━━━━━━\n"
    footer += f"📱 [Mobile Deals](https://www.amazon.in/mobiles?tag={tag}) | 💻 [Laptops](https://www.amazon.in/electronics?tag={tag})\n"
    footer += f"👗 [Fashion Deals](https://myntr.it/b9SAtFm) | 🎁 [Flipkart Loot](https://fktr.in/7WhPb8j)\n\n"
    footer += "✨ *Hurry! Grab these before prices go up!*"
    return footer

if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    
    # ধাপ ১: নিউজ ও প্রাইজ
    header = get_crypto_update()
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": header, "parse_mode": "Markdown", "disable_web_page_preview": True})
    
    # ধাপ ২: ডিল পোস্ট
    post_mega_deals()
    
    # ধাপ ৩: মেনু ও টিপস
    footer = get_footer()
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": footer, "parse_mode": "Markdown", "disable_web_page_preview": True})
