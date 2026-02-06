import os
import requests
import feedparser
import time
import math
import yfinance as yf
from bs4 import BeautifulSoup

# ১. মার্কেট সামারি (Gold, Crypto, Stocks)
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
                return f"{v:,.2f}" if not math.isnan(v) else "Closed"
            except: return "Updating.."
        
        return (
            f"📊 <b>MARKET WATCH</b>\n"
            f"₿ <b>BTC:</b> {btc} | <b>ETH:</b> {eth}\n"
            f"📀 <b>Gold:</b> ${clean('GC=F')} | <b>Silver:</b> ${clean('SI=F')}\n"
            f"📈 <b>Nifty:</b> {clean('^NSEI')} | <b>Sensex:</b> {clean('^BSESN')}\n"
        )
    except: return "📊 Market Watch: Updating..."

# ২. স্টোর ডিটেকশন
def detect_store(link, title):
    l, t = link.lower(), title.lower()
    if "amazon" in l or "amazon" in t: return "AMAZON 🧡", "🛒"
    if "flipkart" in l or "flipkart" in t: return "FLIPKART 💙", "🛍️"
    if "myntra" in l or "myntra" in t: return "MYNTRA ❤️", "👗"
    if "nykaa" in l or "nykaa" in t: return "NYKAA 💖", "💄"
    if "meesho" in l or "meesho" in t: return "MEESHO 💜", "📦"
    return "HANDPICKED DEAL 🌟", "🛒"

# ৩. প্রফেশনাল পোস্ট পাঠানো
def send_deal(title, link, img_url, market_text):
    token, chat_id = os.getenv("BOT_TOKEN"), os.getenv("CHAT_ID")
    amazon_tag = "offerslive24-21" 

    store_name, icon = detect_store(link, title)
    if "amazon.in" in link:
        link = f"{link}&tag={amazon_tag}" if "?" in link else f"{link}?tag={amazon_tag}"

    caption = (
        f"{icon} <b>STORE: {store_name}</b>\n\n"
        f"🔥 <b>{title.upper()}</b>\n\n"
        f"✅ <b>Status:</b> 100% Verified Loot\n"
        f"📢 <b>Limited Time Offer! Grab it fast.</b>\n\n"
        f"👉 <a href='{link}'>CLICK HERE TO BUY NOW</a>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{market_text}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ <i>Join @offers_live_24 for verified loots!</i>"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": img_url, "caption": caption, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=payload, timeout=25)
        return r.status_code == 200
    except: return False

# ৪. মেইন বট (স্মার্ট ডিল ফিল্টার সহ)
def start_bot():
    print("🚀 Bot checking for REAL deals only...")
    market_text = get_market_summary()
    feeds = ["https://www.desidime.com/feed", "https://indiafreestuff.in/feed", "https://www.freekaamaal.com/feed"]
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # শক্তিশালী ব্ল্যাকলিস্ট (আর্টিকেল এবং ব্লগ ফিল্টার করার জন্য)
    blacklist = [
        "insurance", "health", "mental", "policy", "loan", "card", "benefit", 
        "ways", "boost", "guide", "review", "how to", "7 ways", "tips", "care", 
        "safety", "financial", "best floor", "detergent", "article"
    ]

    posted = 0
    for url in feeds:
        try:
            resp = requests.get(url, headers=headers, timeout=20)
            feed = feedparser.parse(resp.content)
            
            for entry in feed.entries[:10]:
                title, link = entry.title.split('|')[0].strip(), entry.link.lower()
                
                # ১. টাইটেল চেক (ব্ল্যাকলিস্ট)
                if any(word in title.lower() for word in blacklist): continue
                
                # ২. লিঙ্ক চেক (যদি লিঙ্কে শপিং ক্যাটাগরি না থাকে তবে স্কিপ)
                # ব্লগ বা আর্টিকেল লিঙ্কগুলো সাধারণত বড় হয় এবং তাতে /blog/ বা /self-care/ জাতীয় শব্দ থাকে
                if any(word in link for word in ["blog", "article", "mental-health", "insurance", "news"]):
                    continue
                
                # ৩. ইমেজ বের করা
                soup = BeautifulSoup(entry.get('summary', '') + entry.get('description', ''), 'html.parser')
                img_tag = soup.find('img')
                img = img_tag.get('src') if img_tag else "https://cdn-icons-png.flaticon.com/512/1162/1162499.png"

                if send_deal(title, entry.link, img, market_text):
                    print(f"✅ Success: {title[:30]}")
                    posted += 1
                    time.sleep(15)
                if posted >= 5: break
            if posted >= 5: break
        except: continue

if __name__ == "__main__":
    start_bot()
