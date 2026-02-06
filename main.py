import os
import requests
import feedparser
import time
import math
import yfinance as yf
from bs4 import BeautifulSoup

# ১. মার্কেট সামারি (সবসময় কারেক্ট ডেটা দেখাবে)
def get_market_summary():
    try:
        crypto_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        c_data = requests.get(crypto_url, timeout=10).json()
        btc = f"${c_data['bitcoin']['usd']:,}"
        eth = f"${c_data['ethereum']['usd']:,}"

        tickers = ["^NSEI", "^BSESN", "GC=F", "SI=F"]
        df = yf.download(tickers, period="1d", interval="1m", progress=False)['Close']
        
        def clean(val): return "Updating.." if math.isnan(val) else f"{val:,.2f}"
        
        last = df.iloc[-1]
        return (
            f"📊 <b>MARKET WATCH</b>\n"
            f"₿ <b>BTC:</b> {btc} | <b>ETH:</b> {eth}\n"
            f"📀 <b>Gold:</b> ${clean(last['GC=F'])} | <b>Silver:</b> ${clean(last['SI=F'])}\n"
            f"📈 <b>Nifty:</b> {clean(last['^NSEI'])} | <b>Sensex:</b> {clean(last['^BSESN'])}\n"
        )
    except:
        return "📊 Market Data: Refreshing..."

# ২. স্টোর শনাক্ত করার উন্নত ফাংশন
def detect_store(link, title):
    l, t = link.lower(), title.lower()
    if "amazon" in l or "amazon" in t: return "AMAZON 🧡", "🛒"
    if "flipkart" in l or "flipkart" in t: return "FLIPKART 💙", "🛍️"
    if "myntra" in l or "myntra" in t: return "MYNTRA ❤️", "👗"
    if "nykaa" in l or "nykaa" in t: return "NYKAA 💖", "💄"
    if "meesho" in l or "meesho" in t: return "MEESHO 💜", "📦"
    if "ajio" in l or "ajio" in t: return "AJIO 🖤", "👟"
    return "HANDPICKED DEAL 🌟", "🛒"

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
        f"{market_text}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ <i>Join @offers_live_24 for more!</i>"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": img_url, "caption": caption, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=payload)
        return r.status_code == 200
    except: return False

def start_bot():
    print("🚀 Bot Started. Checking feeds...")
    market_text = get_market_summary()
    
    # আরও বেশি বিশ্বস্ত সোর্স যোগ করা হলো ডিল পাওয়ার জন্য
    feeds = [
        "https://www.desidime.com/new.atom",
        "https://indiafreestuff.in/feed",
        "https://www.freekaamaal.com/feed"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    posted = 0
    # ব্ল্যাকলিস্ট একটু শিথিল করা হলো যাতে ডিল পাওয়া যায়
    blacklist = ["how to", "guide", "review", "expired", "7 ways"]

    for url in feeds:
        try:
            print(f"📡 Checking Source: {url}")
            resp = requests.get(url, headers=headers, timeout=15)
            feed = feedparser.parse(resp.content)
            print(f"📊 Items found: {len(feed.entries)}")
            
            for entry in feed.entries[:10]: # এখন ১০টি করে আইটেম চেক করবে
                title = entry.title.split('|')[0].strip()
                
                # যদি আর্টিকেল হয় তবে স্কিপ করবে
                if any(w in title.lower() for w in blacklist): 
                    print(f"⏭️ Skipping Article: {title[:30]}...")
                    continue
                
                # ইমেজ খোঁজা
                soup = BeautifulSoup(entry.get('summary', '') + entry.get('description', ''), 'html.parser')
                img = soup.find('img').get('src') if soup.find('img') else "https://cdn-icons-png.flaticon.com/512/1162/1162499.png"

                if send_deal(title, entry.link, img, market_text):
                    print(f"✅ Posted Successfully: {title[:30]}")
                    posted += 1
                    time.sleep(15)
                
                if posted >= 5: break
            if posted >= 5: break
        except Exception as e:
            print(f"⚠️ Error in feed: {e}")

    if posted == 0:
        print("❌ No new deals sent in this run.")

if __name__ == "__main__":
    start_bot()
