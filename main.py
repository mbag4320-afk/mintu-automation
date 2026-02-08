import os
import requests
import feedparser
import time
import math
import yfinance as yf
from bs4 import BeautifulSoup

# ১. মার্কেট ডাটা সংগ্রহ (রবিবার ও বন্ধের দিন হ্যান্ডেল করা হয়েছে)
def get_market_summary():
    try:
        crypto_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        c_data = requests.get(crypto_url, timeout=10).json()
        btc, eth = f"${c_data['bitcoin']['usd']:,}", f"${c_data['ethereum']['usd']:,}"

        tickers = ["^NSEI", "^BSESN", "GC=F", "SI=F"]
        df = yf.download(tickers, period="1d", interval="1m", progress=False)['Close']
        
        def clean(val):
            return "Closed" if math.isnan(val) else f"{val:,.2f}"
        
        last = df.iloc[-1]
        return (
            f"📊 <b>MARKET OVERVIEW</b>\n"
            f"₿ <b>BTC:</b> {btc} | <b>ETH:</b> {eth}\n"
            f"📀 <b>Gold:</b> ${clean(last['GC=F'])} | <b>Silver:</b> ${clean(last['SI=F'])}\n"
            f"📈 <b>Nifty:</b> {clean(last['^NSEI'])} | <b>Sensex:</b> {clean(last['^BSESN'])}\n"
        )
    except:
        return "📊 Market Watch: Market Closed for Weekend"

# ২. ব্র্যান্ড এবং লোগো ডিটেকশন (Trust বাড়ানোর জন্য)
def get_brand_details(link, title):
    l, t = link.lower(), title.lower()
    # ব্র্যান্ড লোগো (ইমেজ না পাওয়া গেলে এগুলো ব্যবহার হবে)
    logos = {
        "amazon": "https://i.ibb.co/LzNfS6P/special-offer.jpg", # Amazon Logo Placeholder
        "flipkart": "https://i.ibb.co/LzNfS6P/special-offer.jpg", # Flipkart Logo Placeholder
        "myntra": "https://i.ibb.co/LzNfS6P/special-offer.jpg",
        "ajio": "https://i.ibb.co/LzNfS6P/special-offer.jpg"
    }
    
    if "amazon" in l or "amazon" in t: return "AMAZON LOOT 🧡", "🛒", logos["amazon"]
    if "flipkart" in l or "flipkart" in t: return "FLIPKART DHAMAKA 💙", "🛍️", logos["flipkart"]
    if "myntra" in l or "myntra" in t: return "MYNTRA FASHION ❤️", "👗", logos["myntra"]
    if "ajio" in l or "ajio" in t: return "AJIO TRENDS 🖤", "👟", logos["ajio"]
    if "nykaa" in l or "nykaa" in t: return "NYKAA BEAUTY 💖", "💄", logos["ajio"]
    if "meesho" in l or "meesho" in t: return "MEESHO SAVINGS 💜", "📦", logos["ajio"]
    
    return None, None, None # অন্য কোনো ব্র্যান্ড বা ব্লগ হলে বাদ দেবে

# ৩. প্রফেশনাল ক্যাপশন ডিজাইন
def send_mega_deal(title, link, img_url, market_text, brand_info):
    token, chat_id = os.getenv("BOT_TOKEN"), os.getenv("CHAT_ID")
    brand_name, icon, fallback_img = brand_info
    
    # আমাজন লিঙ্ক ফিক্স
    if "amazon.in" in link:
        link = f"{link}&tag=offerslive24-21" if "?" in link else f"{link}?tag=offerslive24-21"

    # ইমেজ যদি ব্লক থাকে তবে ডিফল্ট লোগো ব্যবহার হবে
    final_img = img_url if "http" in img_url and "pixel" not in img_url else fallback_img

    caption = (
        f"{icon} <b>{brand_name}</b>\n\n"
        f"🎁 <b>{title.upper()}</b>\n\n"
        f"✅ <b>Status:</b> 100% Verified Loot\n"
        f"📢 <b>Limited Time Offer! Grab it now.</b>\n\n"
        f"👉 <a href='{link}'>CLICK HERE TO BUY NOW</a>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{market_text}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ <i>Join @offers_live_24 for Mega Loots!</i>"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": final_img, "caption": caption, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=payload, timeout=25)
        return r.status_code == 200
    except: return False

def start_bot():
    print("🚀 Mega Deal Bot Started. Filtering for Trusted Brands...")
    market_text = get_market_summary()
    feeds = ["https://www.desidime.com/new.atom", "https://indiafreestuff.in/feed"]
    
    posted_count = 0
    # কড়া ব্ল্যাকলিস্ট
    blacklist = ["how to", "guide", "kaise", "nikale", "tips", "review", "article", "insurance", "7 ways"]

    for url in feeds:
        print(f"📡 Checking Source: {url}")
        feed = feedparser.parse(url)
        
        for entry in feed.entries[:15]: # ১৫টি পর্যন্ত চেক করবে ব্র্যান্ড ডিল পেতে
            title = entry.title.split('|')[0].strip()
            link = entry.link
            
            # ১. ব্র্যান্ড চেক (শুধুমাত্র বড় ব্র্যান্ডের ডিল নেবে)
            brand_info = get_brand_details(link, title)
            if not brand_info[0]:
                continue
            
            # ২. ব্ল্যাকলিস্ট চেক
            if any(word in title.lower() for word in blacklist):
                continue
            
            # ৩. ইমেজ এক্সট্রাকশন
            soup = BeautifulSoup(entry.get('summary', '') + entry.get('description', ''), 'html.parser')
            img_tag = soup.find('img')
            img_url = img_tag.get('src') if img_tag else ""

            if send_mega_deal(title, link, img_url, market_text, brand_info):
                print(f"✅ MEGA DEAL POSTED: {title[:30]}")
                posted_count += 1
                time.sleep(15)
            
            if posted_count >= 5: break
        if posted_count >= 5: break

    if posted_count == 0:
        print("🛑 No brand-specific loots found in this run.")

if __name__ == "__main__":
    start_bot()
