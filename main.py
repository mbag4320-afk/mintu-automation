import os
import requests
import feedparser
import time
import math
import yfinance as yf
from bs4 import BeautifulSoup

# ১. মার্কেট আপডেট (প্রিমিয়াম লুকের জন্য)
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

# ২. শুধুমাত্র বড় ব্র্যান্ড শনাক্ত করার ফাংশন
def detect_trusted_store(link, title):
    l, t = link.lower(), title.lower()
    if "amazon" in l or "amazon" in t: return "AMAZON LOOT 🧡", "🔥"
    if "flipkart" in l or "flipkart" in t: return "FLIPKART DHAMAKA 💙", "⚡"
    if "myntra" in l or "myntra" in t: return "MYNTRA FASHION ❤️", "👗"
    if "nykaa" in l or "nykaa" in t: return "NYKAA BEAUTY 💖", "💄"
    if "ajio" in l or "ajio" in t: return "AJIO TRENDS 🖤", "👟"
    if "meesho" in l or "meesho" in t: return "MEESHO SAVINGS 💜", "📦"
    return None, None # যদি বড় ব্র্যান্ড না হয় তবে কিছুই ফেরত দেবে না

# ৩. টেলিগ্রামে প্রফেশনাল পোস্ট
def send_deal(title, link, img_url, market_text, store_info):
    token, chat_id = os.getenv("BOT_TOKEN"), os.getenv("CHAT_ID")
    store_name, icon = store_info
    
    # আমাজন অ্যাফিলিয়েট ট্যাগ যোগ করা
    if "amazon.in" in link:
        link = f"{link}&tag=offerslive24-21" if "?" in link else f"{link}?tag=offerslive24-21"

    caption = (
        f"{icon} <b>{store_name}</b>\n\n"
        f"🎁 <b>{title.upper()}</b>\n\n"
        f"✅ <b>Status:</b> 100% Verified Price Drop\n"
        f"📢 <b>Limited Time Deal! Grab it now.</b>\n\n"
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

# ৪. মেইন প্রসেস
def start_bot():
    print("🚀 Running in HIGH-TRUST BRAND ONLY mode...")
    market_text = get_market_summary()
    feeds = ["https://www.desidime.com/feed", "https://indiafreestuff.in/feed", "https://www.freekaamaal.com/feed"]
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    posted = 0
    blacklist = ["how to", "guide", "kaise", "nikale", "tips", "review", "article", "best floor"]

    for url in feeds:
        try:
            resp = requests.get(url, headers=headers, timeout=20)
            feed = feedparser.parse(resp.content)
            for entry in feed.entries[:12]:
                title = entry.title.split('|')[0].strip()
                link = entry.link
                
                # ব্র্যান্ড চেক: বড় ব্র্যান্ড না হলে পোস্ট হবে না
                store_info = detect_trusted_store(link, title)
                if not store_info[0]: 
                    continue # এটিই আপনার চ্যানেলের বিশ্বাসযোগ্যতা বাঁচাবে
                
                # ব্ল্যাকলিস্ট চেক
                if any(word in title.lower() for word in blacklist): continue
                
                soup = BeautifulSoup(entry.get('summary', '') + entry.get('description', ''), 'html.parser')
                img = soup.find('img').get('src') if soup.find('img') else "https://cdn-icons-png.flaticon.com/512/1162/1162499.png"

                if send_deal(title, link, img, market_text, store_info):
                    print(f"✅ Success: {title[:30]}")
                    posted += 1
                    time.sleep(15)
                if posted >= 5: break
            if posted >= 5: break
        except: continue

if __name__ == "__main__":
    start_bot()
