import os
import requests
import feedparser
import time
import math
import yfinance as yf
from bs4 import BeautifulSoup

# ১. মার্কেট ডেটা চেক এবং সংগ্রহ (NaN সমস্যা সমাধান সহ)
def get_market_summary():
    try:
        # ক্রিপ্টো
        crypto_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        c_data = requests.get(crypto_url, timeout=10).json()
        btc = f"${c_data['bitcoin']['usd']:,}"
        eth = f"${c_data['ethereum']['usd']:,}"

        # স্টক ও মেটাল
        tickers = ["^NSEI", "^BSESN", "GC=F", "SI=F"]
        df = yf.download(tickers, period="1d", interval="1m", progress=False)['Close']
        
        def clean(val): return "Closed" if math.isnan(val) else f"{val:,.2f}"
        
        last = df.iloc[-1]
        summary = (
            f"📊 <b>MARKET WATCH</b>\n"
            f"₿ <b>BTC:</b> {btc} | <b>ETH:</b> {eth}\n"
            f"📀 <b>Gold:</b> ${clean(last['GC=F'])} | <b>Silver:</b> ${clean(last['SI=F'])}\n"
            f"📈 <b>Nifty:</b> {clean(last['^NSEI'])} | <b>Sensex:</b> {clean(last['^BSESN'])}\n"
        )
        return summary
    except:
        return "📊 Market Data: Updating..."

# ২. স্টোর শনাক্ত করার ফাংশন
def detect_store(link, title):
    link = link.lower()
    title = title.lower()
    if "amazon" in link or "amazon" in title: return "AMAZON 🧡", "🛒"
    if "flipkart" in link or "flipkart" in title: return "FLIPKART 💙", "🛍️"
    if "myntra" in link or "myntra" in title: return "MYNTRA ❤️", "👗"
    if "nykaa" in link or "nykaa" in title: return "NYKAA 💖", "💄"
    if "meesho" in link or "meesho" in title: return "MEESHO 💜", "📦"
    if "ajio" in link or "ajio" in title: return "AJIO 🖤", "👟"
    return "TOP STORE 🌟", "🛒"

# ৩. টেলিগ্রামে ডিল পাঠানোর ফাংশন
def send_deal(title, link, img_url, market_text):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    amazon_tag = "offerslive24-21" 

    store_name, icon = detect_store(link, title)
    
    if "amazon.in" in link:
        link = f"{link}&tag={amazon_tag}" if "?" in link else f"{link}?tag={amazon_tag}"

    caption = (
        f"{icon} <b>STORE: {store_name}</b>\n\n"
        f"🔥 <b>{title.upper()}</b>\n\n"
        f"✅ <b>Status:</b> 100% Verified Loot\n"
        f"📢 <b>Limited Time Offer! Grab it fast.</b>\n\n"
        f"👉 <a href='{link}'>CLICK HERE TO BUY</a>\n"
        f"👉 <a href='{link}'>CLICK HERE TO BUY</a>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{market_text}"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ <i>Join @offers_live_24 for more!</i>"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": img_url, "caption": caption, "parse_mode": "HTML"}
    
    try:
        r = requests.post(url, data=payload)
        return r.status_code == 200
    except:
        return False

def get_clean_image(entry):
    content = entry.get('summary', '') + entry.get('description', '')
    soup = BeautifulSoup(content, 'html.parser')
    img = soup.find('img')
    fallback = "https://cdn-icons-png.flaticon.com/512/1162/1162499.png"
    if img and img.get('src'):
        src = img.get('src')
        return fallback if "pixel" in src or "logo" in src else src
    return fallback

def start_bot():
    market_text = get_market_summary()
    feeds = ["https://www.desidime.com/new.atom", "https://indiafreestuff.in/feed"]
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    posted = 0
    # ডিল নয় এমন আর্টিকেল বাদ দেওয়ার জন্য শক্তিশালী ফিল্টার
    blacklist = ["7 ways", "boost your", "how to", "guide", "nutrition", "review"]

    for url in feeds:
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            feed = feedparser.parse(resp.content)
            for entry in feed.entries[:5]:
                title = entry.title.split('|')[0].strip()
                if any(w in title.lower() for w in blacklist): continue
                
                img = get_clean_image(entry)
                if send_deal(title, entry.link, img, market_text):
                    posted += 1
                    time.sleep(15)
                if posted >= 5: break
            if posted >= 5: break
        except: continue

if __name__ == "__main__":
    start_bot()
