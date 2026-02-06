import os
import requests
import feedparser
import time
import math
import yfinance as yf
from bs4 import BeautifulSoup

# ১. মার্কেট ডাটা সংগ্রহের ফাংশন (Crypto, Gold, Stocks)
def get_market_summary():
    try:
        # ক্রিপ্টো প্রাইস
        crypto_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        c_data = requests.get(crypto_url, timeout=15).json()
        btc = f"${c_data['bitcoin']['usd']:,}"
        eth = f"${c_data['ethereum']['usd']:,}"

        # গোল্ড, সিলভার, নিফটি, সেনসেক্স (Yahoo Finance)
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

# ২. স্টোর শনাক্ত করার ফাংশন (অ্যামাজন, ফ্লিপকার্ট ইত্যাদি)
def detect_store(link, title):
    l, t = link.lower(), title.lower()
    if "amazon" in l or "amazon" in t: return "AMAZON 🧡", "🛒"
    if "flipkart" in l or "flipkart" in t: return "FLIPKART 💙", "🛍️"
    if "myntra" in l or "myntra" in t: return "MYNTRA ❤️", "👗"
    if "nykaa" in l or "nykaa" in t: return "NYKAA 💖", "💄"
    if "meesho" in l or "meesho" in t: return "MEESHO 💜", "📦"
    if "ajio" in l or "ajio" in t: return "AJIO 🖤", "👟"
    return "TRUSTED DEAL 🌟", "🛒"

# ৩. টেলিগ্রামে প্রফেশনাল পোস্ট পাঠানোর ফাংশন
def send_deal(title, link, img_url, market_text):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    amazon_tag = "offerslive24-21" # আপনার আমাজন ট্যাগ

    store_name, icon = detect_store(link, title)
    if "amazon.in" in link:
        link = f"{link}&tag={amazon_tag}" if "?" in link else f"{link}?tag={amazon_tag}"

    caption = (
        f"{icon} <b>STORE: {store_name}</b>\n\n"
        f"🔥 <b>{title.upper()}</b>\n\n"
        f"✅ <b>Status:</b> 100% Verified Loot\n"
        f"📢 <b>Price Drop Alert! Grab it fast.</b>\n\n"
        f"👉 <a href='{link}'>CLICK HERE TO BUY NOW</a>\n"
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

# ৪. ইমেজ পরিষ্কার করার ফাংশন
def get_clean_image(entry):
    content = entry.get('summary', '') + entry.get('description', '')
    soup = BeautifulSoup(content, 'html.parser')
    img_tag = soup.find('img')
    fallback = "https://cdn-icons-png.flaticon.com/512/1162/1162499.png"
    if img_tag and img_tag.get('src'):
        src = img_tag.get('src')
        return fallback if any(x in src.lower() for x in ["pixel", "logo", "not-viewable"]) else src
    return fallback

# ৫. মেইন রানার (শক্তিশালী ব্ল্যাকলিস্ট সহ)
def start_bot():
    print("🚀 Starting Bot with Blacklist Filter...")
    market_text = get_market_summary()
    
    feeds = [
        "https://www.desidime.com/feed", 
        "https://indiafreestuff.in/feed",
        "https://www.freekaamaal.com/feed"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # শক্তিশালী ব্ল্যাকলিস্ট: এই শব্দগুলো থাকলে পোস্ট হবে না (আর্টিকেল ফিল্টার)
    blacklist = [
        "how to", "guide", "review", "expired", "7 ways", "boost your", "indian homes",
        "detergent", "cleaner", "soap", "toothpaste", "shampoo", "best", "top", 
        "worth", "every drop", "nutrition", "tips", "tricks", "registration", "alchemy"
    ]

    posted = 0
    for url in feeds:
        try:
            print(f"📡 Checking: {url}")
            resp = requests.get(url, headers=headers, timeout=20)
            feed = feedparser.parse(resp.content)
            
            for entry in feed.entries[:8]:
                title = entry.title.split('|')[0].strip()
                
                # ব্ল্যাকলিস্ট চেক (টাইটেল থেকে আর্টিকেল ফিল্টার করা)
                if any(word in title.lower() for word in blacklist):
                    print(f"⏭️ Skipping Article: {title[:40]}...")
                    continue
                
                img = get_clean_image(entry)
                if send_deal(title, entry.link, img, market_text):
                    print(f"✅ Success: {title[:30]}")
                    posted += 1
                    time.sleep(15) # স্প্যাম প্রোটেকশন
                if posted >= 5: break
            if posted >= 5: break
        except Exception as e:
            print(f"❌ Error in {url}: {e}")

    if posted == 0:
        print("🛑 No new verified deals found. Feeds might be empty or filtered.")

if __name__ == "__main__":
    start_bot()
