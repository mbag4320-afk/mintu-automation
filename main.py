import os
import requests
import feedparser
import time
import math
import yfinance as yf
from bs4 import BeautifulSoup

# ১. মার্কেট সামারি সংগ্রহ
def get_market_summary():
    try:
        crypto_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        c_data = requests.get(crypto_url, timeout=15).json()
        btc, eth = f"${c_data['bitcoin']['usd']:,}", f"${c_data['ethereum']['usd']:,}"
        
        tickers = ["^NSEI", "^BSESN", "GC=F", "SI=F"]
        df = yf.download(tickers, period="1d", interval="1m", progress=False, group_by='ticker')
        def clean(t):
            try:
                v = df[t]['Close'].iloc[-1]
                return f"{v:,.2f}" if not math.isnan(v) else "Closed (Weekend)"
            except: return "Closed"
        
        return (
            f"₿ <b>BTC:</b> {btc} | <b>ETH:</b> {eth}\n"
            f"📀 <b>Gold:</b> ${clean('GC=F')} | <b>Silver:</b> ${clean('SI=F')}\n"
            f"📈 <b>Nifty:</b> {clean('^NSEI')} | <b>Sensex:</b> {clean('^BSESN')}"
        )
    except: return "📊 Market Watch: Updating data..."

# ২. শুধুমাত্র বড় ব্র্যান্ড শনাক্ত করা
def detect_trusted_store(link, title):
    l, t = link.lower(), title.lower()
    brands = {
        "amazon": ("AMAZON LOOT 🧡", "🔥"),
        "flipkart": ("FLIPKART DHAMAKA 💙", "⚡"),
        "myntra": ("MYNTRA FASHION ❤️", "👗"),
        "nykaa": ("NYKAA BEAUTY 💖", "💄"),
        "ajio": ("AJIO TRENDS 🖤", "👟"),
        "meesho": ("MEESHO SAVINGS 💜", "📦"),
        "samsung": ("SAMSUNG STORE 📱", "💎"),
        "boat": ("BOAT AUDIO 🎧", "🔊"),
        "adidas": ("ADIDAS SPORTS 👟", "🏆"),
        "puma": ("PUMA LOOT 🐆", "👟")
    }
    for key, val in brands.items():
        if key in l or key in t: return val
    return None, None

# ৩. প্রফেশনাল ডিল পোস্ট পাঠানোর ফাংশন
def send_deal(title, link, img_url, market_text, store_info):
    token, chat_id = os.getenv("BOT_TOKEN"), os.getenv("CHAT_ID")
    store_name, icon = store_info
    
    if "amazon.in" in link:
        link = f"{link}&tag=offerslive24-21" if "?" in link else f"{link}?tag=offerslive24-21"

    caption = (
        f"{icon} <b>{store_name}</b>\n\n"
        f"🎁 <b>{title.upper()}</b>\n\n"
        f"✅ <b>Status:</b> 100% Verified Loot\n"
        f"📢 <b>Limited Time Deal! Grab it fast.</b>\n\n"
        f"👉 <a href='{link}'>CLICK HERE TO BUY NOW</a>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 <b>MARKET OVERVIEW</b>\n{market_text}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ <i>Join @offers_live_24 for Mega Loots!</i>"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": img_url, "caption": caption, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=payload, timeout=25)
        return r.status_code == 200
    except: return False

# ৪. মেইন প্রসেসর
def start_bot():
    print("🚀 Mega Deal Bot started. Running analysis...")
    token, chat_id = os.getenv("BOT_TOKEN"), os.getenv("CHAT_ID")
    market_text = get_market_summary()
    
    feeds = [
        "https://www.desidime.com/feed", 
        "https://indiafreestuff.in/feed",
        "https://www.freekaamaal.com/feed"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    posted_count = 0

    for url in feeds:
        try:
            resp = requests.get(url, headers=headers, timeout=20)
            feed = feedparser.parse(resp.content)
            for entry in feed.entries[:15]:
                title, link = entry.title.split('|')[0].strip(), entry.link
                
                store_info = detect_trusted_store(link, title)
                if not store_info[0]: continue 
                
                soup = BeautifulSoup(entry.get('summary', '') + entry.get('description', ''), 'html.parser')
                img = soup.find('img').get('src') if soup.find('img') else "https://i.ibb.co/LzNfS6P/special-offer.jpg"

                if send_deal(title, link, img, market_text, store_info):
                    print(f"✅ Posted: {title[:30]}")
                    posted_count += 1
                    time.sleep(15)
                if posted_count >= 5: break
            if posted_count >= 5: break
        except: continue

    # যদি কোনো ব্র্যান্ডের ডিল না পাওয়া যায়, তবে শুধু মার্কেট আপডেট পাঠাবে
    if posted_count == 0:
        print("🛑 No brand-specific loots found. Sending Market Summary only...")
        market_msg = (
            f"📊 <b>MARKET WATCH (DAILY UPDATE)</b>\n\n"
            f"{market_text}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📢 <i>No mega loots found right now. Stay tuned for upcoming deals!</i>\n"
            f"⚡ Join @offers_live_24"
        )
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, data={"chat_id": chat_id, "text": market_msg, "parse_mode": "HTML"})

if __name__ == "__main__":
    start_bot()
