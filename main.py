import os
import requests
import feedparser
import time
import math
import yfinance as yf
from bs4 import BeautifulSoup

# ১. মার্কেট ডাটা ফিক্স (NaN সমস্যা সমাধান)
def get_market_summary():
    try:
        crypto_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        c_data = requests.get(crypto_url, timeout=10).json()
        btc, eth = f"${c_data['bitcoin']['usd']:,}", f"${c_data['ethereum']['usd']:,}"

        tickers = ["^NSEI", "^BSESN", "GC=F", "SI=F"]
        df = yf.download(tickers, period="1d", interval="1m", progress=False)['Close']
        
        def clean(val):
            return "Closed/Wait" if math.isnan(val) else f"{val:,.2f}"
        
        last = df.iloc[-1]
        return (
            f"📊 <b>MARKET WATCH</b>\n"
            f"₿ <b>BTC:</b> {btc} | <b>ETH:</b> {eth}\n"
            f"📀 <b>Gold:</b> ${clean(last['GC=F'])} | <b>Silver:</b> ${clean(last['SI=F'])}\n"
            f"📈 <b>Nifty:</b> {clean(last['^NSEI'])} | <b>Sensex:</b> {clean(last['^BSESN'])}\n"
        )
    except:
        return "📊 Market Watch: Market is Closed/Updating"

# ২. প্রফেশনাল ডিল পোস্ট
def send_deal(title, link, img_url, market_text):
    token, chat_id = os.getenv("BOT_TOKEN"), os.getenv("CHAT_ID")
    
    # স্টোর ডিটেকশন (শুধু ব্র্যান্ডেড ডিল)
    store = "HANDPICKED DEAL 🌟"
    if "amazon" in link.lower(): store = "AMAZON LOOT 🧡"
    elif "flipkart" in link.lower(): store = "FLIPKART DHAMAKA 💙"
    elif "myntra" in link.lower(): store = "MYNTRA FASHION ❤️"

    caption = (
        f"🛒 <b>STORE: {store}</b>\n\n"
        f"🔥 <b>{title.upper()}</b>\n\n"
        f"✅ <b>Status:</b> 100% Verified Loot\n\n"
        f"👉 <a href='{link}'>CLICK HERE TO BUY NOW</a>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{market_text}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ <i>Join @offers_live_24 for verified loots!</i>"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": img_url, "caption": caption, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=payload)
        return r.status_code == 200
    except: return False

def start_bot():
    market_text = get_market_summary()
    feeds = ["https://www.desidime.com/new.atom", "https://indiafreestuff.in/feed"]
    
    # ডিল নয় এমন শব্দগুলোর শক্ত ফিল্টার
    blacklist = ["how to", "guide", "kaise", "nikale", "tips", "review", "article", "best floor", "best dishwash"]

    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            title = entry.title.split('|')[0].strip()
            
            # ফিল্টার চেক: যদি আর্টিকেল হয় তবে বাদ দেবে
            if any(word in title.lower() for word in blacklist): continue
            
            # শুধুমাত্র প্রাইস সংক্রান্ত ডিল খোঁজার চেষ্টা
            if not any(symbol in title for symbol in ["Rs", "Rs.", "₹", "Off", "%"]): continue

            soup = BeautifulSoup(entry.get('summary', '') + entry.get('description', ''), 'html.parser')
            img = soup.find('img').get('src') if soup.find('img') else "https://i.ibb.co/LzNfS6P/special-offer.jpg"
            
            if send_deal(title, entry.link, img, market_text):
                print(f"✅ Posted: {title}")
                time.sleep(15)

if __name__ == "__main__":
    start_bot()
