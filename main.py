import os
import requests
import datetime
import yfinance as yf
import json

# GitHub Secrets
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def get_greeting():
    """সময় অনুযায়ী শুভেচ্ছা জানানো"""
    hour = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).hour
    if 5 <= hour < 12: return "শুভ সকাল ☀️"
    elif 12 <= hour < 17: return "শুভ দুপুর 🌤️"
    elif 17 <= hour < 20: return "শুভ সন্ধ্যা 🌆"
    else: return "শুভ রাত্রি 🌙"

def get_ai_market_insight():
    """Mistral AI থেকে মার্কেট এবং জীবনমুখী পরামর্শ নেওয়া"""
    if not MISTRAL_API_KEY:
        return "প্রতিদিনের ছোট ছোট প্রচেষ্টাই বড় সাফল্যের পথ তৈরি করে।"
    try:
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
        # AI-কে বলা হচ্ছে ছোট করে বাজারের অবস্থা এবং মোটিভেশন দিতে
        data = {
            "model": "open-mistral-7b",
            "messages": [{"role": "user", "content": "Give a 1-sentence market insight or motivational tip in Bengali. Keep it very short."}]
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        return response.json()['choices'][0]['message']['content'].strip()
    except:
        return "ধৈর্য ও সঠিক সিদ্ধান্তই বিনিয়োগের মূল চাবিকাঠি।"

def get_crypto_prices():
    """একাধিক কয়েনের লাইভ দাম সংগ্রহ"""
    prices = {}
    tickers = {"BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD"}
    for coin, ticker in tickers.items():
        try:
            val = yf.Ticker(ticker).fast_info['last_price']
            prices[coin] = f"${round(val, 2)}"
        except:
            prices[coin] = "N/A"
    return prices

def get_final_message():
    greeting = get_greeting()
    prices = get_crypto_prices()
    ai_insight = get_ai_market_insight()
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).strftime("%d-%m-%Y %I:%M %p")
    
    msg = f"<b>{greeting}!</b>\n"
    msg += f"📊 <b>Market Watch Update</b>\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"📅 <b>Date:</b> {now}\n\n"
    
    msg += f"💰 <b>LIVE CRYPTO PRICES</b>\n"
    msg += f"• <b>BTC:</b> {prices['BTC']} 🚀\n"
    msg += f"• <b>ETH:</b> {prices['ETH']} ✨\n"
    msg += f"• <b>SOL:</b> {prices['SOL']} 💎\n\n"
    
    msg += f"📊 <b>STOCK MARKET</b>\n"
    msg += f"• Nifty: 25,756.30 ✅\n"
    msg += f"• Gold: Closed 🔒\n\n"
    
    msg += f"💡 <b>AI Insight:</b>\n"
    msg += f"<i>{ai_insight}</i>\n\n"
    
    msg += f"🔗 <b>Join Channel:</b> https://t.me/OFFERS_LIVE_24\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"🚀 <b>Powered by Mintu Automation</b>"
    return msg

def send_telegram(text):
    if not TOKEN or not CHAT_ID: return
    image_url = "https://images.unsplash.com/photo-1611974714024-462cd92e3902?auto=format&fit=crop&w=1000&q=80"
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    
    payload = {
        "chat_id": CHAT_ID,
        "photo": image_url,
        "caption": text,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

if __name__ == "__main__":
    message_text = get_final_message()
    send_telegram(message_text)
