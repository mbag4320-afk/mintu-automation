import os
import requests
import feedparser
import time
import math
import yfinance as yf
from bs4 import BeautifulSoup

# ১. মার্কেট ডেটা ফিক্স (yfinance এরর হ্যান্ডলিং সহ)
def get_market_summary():
    try:
        crypto_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        c_data = requests.get(crypto_url, timeout=15).json()
        btc = f"${c_data['bitcoin']['usd']:,}"
        eth = f"${c_data['ethereum']['usd']:,}"

        # yfinance এরর এড়াতে নতুন টেকনিক
        tickers = ["^NSEI", "^BSESN", "GC=F", "SI=F"]
        data_summary = ""
        try:
            df = yf.download(tickers, period="1d", interval="1m", progress=False, group_by='ticker')
            def clean_val(ticker_name):
                try:
                    val = df[ticker_name]['Close'].iloc[-1]
                    return f"{val:,.2f}" if not math.isnan(val) else "Closed"
                except: return "Updating.."
            
            data_summary = (
                f"📀 <b>Gold:</b> ${clean_val('GC=F')} | <b>Silver:</b> ${clean_val('SI=F')}\n"
                f"📈 <b>Nifty:</b> {clean_val('^NSEI')} | <b>Sensex:</b> {clean_val('^BSESN')}\n"
            )
        except:
            data_summary = "📊 Market: Weekend/Updating..\n"

        return (
            f"📊 <b>MARKET WATCH</b>\n"
            f"₿ <b>BTC:</b> {btc} | <b>ETH:</b> {eth}\n"
            f"{data_summary}"
        )
    except:
        return "📊 Market Data: Refreshing..."

# ২. স্টোর শনাক্ত করার ফাংশন
def detect_store(link, title):
    l, t = link.lower(), title.lower()
    if "amazon" in l or "amazon" in t: return "AMAZON 🧡", "🛒"
    if "flipkart" in l or "flipkart" in t: return "FLIPKART 💙", "🛍️"
    if "myntra" in l or "myntra" in t: return "MYNTRA ❤️", "👗"
    if "nykaa" in l or "nykaa" in t: return "NYKAA 💖", "💄"
    if "meesho" in l or "meesho" in t: return "MEESHO 💜", "📦"
    if "ajio" in l or "ajio" in t: return "AJIO 🖤", "👟"
    return "TRUSTED DEAL 🌟", "🛒"

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
        f"👉 <a href='{link}'>CLICK HERE TO BUY NOW</a>\n"
        f"👉 <a href='{link}'>CLICK HERE TO BUY NOW</a>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{market_text}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ <i>Join @offers_live_24 for more!</i>"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": img_url, "caption": caption, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=payload, timeout=20)
        return r.status_code == 200
    except: return False

def start_bot():
    print("🚀 Bot Started. Bypassing anti-bot measures...")
    market_text = get_market_summary()
    
    # স্ট্যাবল ফিড ইউআরএল (Amazon, Flipkart এর ডিল বেশি পাওয়ার জন্য)
    feeds = [
        "https://www.desidime.com/feed", # atom এর বদলে RSS ব্যবহার করা হলো
        "https://indiafreestuff.in/feed",
        "https://www.freekaamaal.com/feed"
    ]
    
    # ব্রাউজার হিসেবে পরিচয় দেওয়ার জন্য অ্যাডভান্সড হেডার
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    
    posted = 0
    blacklist = ["how to", "guide", "review", "expired", "7 ways"]

    for url in feeds:
        try:
            print(f"📡 Checking: {url}")
            # টাইমআউট ৩০ সেকেন্ড করা হলো এবং হেডার যোগ করা হলো
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code != 200:
                print(f"⚠️ Website blocked access (Code: {resp.status_code})")
                continue
                
            feed = feedparser.parse(resp.content)
            print(f"📊 Items found: {len(feed.entries)}")
            
            for entry in feed.entries[:8]:
                title = entry.title.split('|')[0].strip()
                if any(w in title.lower() for w in blacklist): continue
                
                soup = BeautifulSoup(entry.get('summary', '') + entry.get('description', ''), 'html.parser')
                img_tag = soup.find('img')
                img = img_tag.get('src') if img_tag else "https://cdn-icons-png.flaticon.com/512/1162/1162499.png"

                if send_deal(title, entry.link, img, market_text):
                    print(f"✅ Success: {title[:30]}")
                    posted += 1
                    time.sleep(15)
                if posted >= 5: break
            if posted >= 5: break
        except Exception as e:
            print(f"❌ Error in feed {url}: {e}")

    if posted == 0:
        print("🛑 Final Result: No deals could be sent due to connection issues or empty feeds.")

if __name__ == "__main__":
    start_bot()
