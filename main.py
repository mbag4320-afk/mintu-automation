import os
import requests
import feedparser
import time
import yfinance as yf
from bs4 import BeautifulSoup

# ১. মার্কেট ডেটা সংগ্রহ করার ফাংশন
def get_market_summary():
    try:
        # ক্রিপ্টো প্রাইস (BTC & ETH) - CoinGecko থেকে
        crypto_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        crypto_data = requests.get(crypto_url, timeout=10).json()
        btc_price = f"${crypto_data['bitcoin']['usd']:,}"
        eth_price = f"${crypto_data['ethereum']['usd']:,}"

        # স্টক মার্কেট এবং গোল্ড/সিলভার - Yahoo Finance থেকে
        # ^NSEI (Nifty 50), ^BSESN (Sensex), GC=F (Gold), SI=F (Silver)
        tickers = ["^NSEI", "^BSESN", "GC=F", "SI=F"]
        data = yf.download(tickers, period="1d", interval="1m")['Close'].iloc[-1]
        
        nifty = f"{data['^NSEI']:.2f}"
        sensex = f"{data['^BSESN']:.2f}"
        gold = f"${data['GC=F']:.2f}"   # প্রতি আউন্স (USD)
        silver = f"${data['SI=F']:.2f}" # প্রতি আউন্স (USD)

        summary = (
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 <b>MARKET OVERVIEW</b>\n"
            f"₿ <b>BTC:</b> {btc_price} | <b>ETH:</b> {eth_price}\n"
            f"📀 <b>Gold:</b> {gold} | <b>Silver:</b> {silver}\n"
            f"📈 <b>Nifty 50:</b> {nifty} | <b>Sensex:</b> {sensex}\n"
        )
        return summary
    except Exception as e:
        print(f"Market data error: {e}")
        return ""

# ২. টেলিগ্রামে পোস্ট পাঠানোর ফাংশন
def send_deal(title, link, img_url, market_text):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    amazon_tag = "offerslive24-21" 

    if "amazon.in" in link:
        link = f"{link}&tag={amazon_tag}" if "?" in link else f"{link}?tag={amazon_tag}"
    
    caption = (
        f"🌟 <b>TRUSTED LOOT DEAL</b> 🌟\n\n"
        f"🔥 <b>{title.upper()}</b>\n\n"
        f"✅ <b>Status:</b> Verified & Handpicked\n"
        f"📢 <b>Price Drop Alert! Grab it now.</b>\n\n"
        f"👉 <a href='{link}'>CLICK HERE TO BUY NOW</a>\n\n"
        f"{market_text}" # এখানে মার্কেট ডেটা যুক্ত হবে
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ <i>Join @offers_live_24 for verified loots!</i>"
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
    fallback_img = "https://cdn-icons-png.flaticon.com/512/1162/1162499.png"
    if img and img.get('src'):
        img_url = img.get('src')
        if "pixel" in img_url or "logo" in img_url: return fallback_img
        return img_url
    return fallback_img

def start_bot():
    # প্রথমে মার্কেট ডেটা একবার সংগ্রহ করে নিচ্ছি
    market_text = get_market_summary()
    
    feeds = ["https://www.desidime.com/new.atom", "https://indiafreestuff.in/feed"]
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    posted_count = 0
    blacklist = ["how to", "guide", "review", "expired", "registration"]

    for f_url in feeds:
        try:
            resp = requests.get(f_url, headers=headers, timeout=15)
            feed = feedparser.parse(resp.content)
            
            for entry in feed.entries[:3]:
                title = entry.title.split('|')[0].strip()
                if any(word in title.lower() for word in blacklist): continue
                
                img = get_clean_image(entry)
                if send_deal(title, entry.link, img, market_text):
                    posted_count += 1
                    time.sleep(15)
            
            if posted_count >= 5: break
        except: continue

if __name__ == "__main__":
    start_bot()
