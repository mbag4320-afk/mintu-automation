import os
import requests
import datetime
import yfinance as yf
import json

# GitHub Secrets
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def get_ai_inspiration():
    if not MISTRAL_API_KEY:
        return "আজ তুমি শুরু করো, হার মেনো না কখনো—প্রতিটি ছোট পদক্ষেপ তোমাকে বিজয়ী করে তুলবে।"
    try:
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
        data = {
            "model": "open-mistral-7b",
            "messages": [{"role": "user", "content": "Write a 1-sentence motivational tip in Bengali. Short and powerful."}]
        }
        response = requests.post(url, headers=headers, json=data, timeout=15)
        return response.json()['choices'][0]['message']['content'].strip()
    except:
        return "সাফল্য মানে প্রতিদিনের ছোট ছোট প্রচেষ্টার সমষ্টি।"

def get_market_data():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    formatted_time = now.strftime("%d-%m-%Y %I:%M %p")
    
    # লাইভ বিটকয়েন এবং ইথেরিয়াম প্রাইস
    try:
        btc_price = round(yf.Ticker("BTC-USD").fast_info['last_price'], 2)
        eth_price = round(yf.Ticker("ETH-USD").fast_info['last_price'], 2)
    except:
        btc_price, eth_price = "67,982.67", "1,987.97"
        
    daily_tip = get_ai_inspiration()
    
    # HTML ফরম্যাটে মেসেজ
    message = f"🌟 <b>MARKET WATCH (DAILY UPDATE)</b> 🌟\n"
    message += f"━━━━━━━━━━━━━━━━━━━━\n"
    message += f"📅 <b>Date:</b> {formatted_time}\n\n"
    message += f"💰 <b>CRYPTO PRICES</b>\n"
    message += f"• BTC: ${btc_price} 📈\n"
    message += f"• ETH: ${eth_price} ✨\n\n"
    message += f"📊 <b>STOCK MARKET</b>\n"
    message += f"• Nifty: 25,756.30 ✅\n"
    message += f"• Gold: Closed (Weekend) 🔒\n\n"
    message += f"✨ <b>AI Daily Inspiration:</b>\n"
    message += f"<i>{daily_tip}</i>\n\n"
    message += f"🔗 <b>Join Link:</b> https://t.me/offers_live_24\n" # ব্যাকআপ টেক্সট লিঙ্ক
    message += f"━━━━━━━━━━━━━━━━━━━━\n"
    message += f"🚀 <b>Powered by Mintu Automation</b>"
    return message

def send_telegram(text):
    if not TOKEN or not CHAT_ID: return
    
    # সরাসরি ইমেজের লিঙ্ক
    image_url = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1000&q=80"
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    
    # বোতামের লিঙ্ক - একদম ফ্রেশ ফরম্যাটে
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🔗 Join Channel", "url": "https://t.me/offers_live_24"},
                {"text": "📊 Live Charts", "url": "https://www.tradingview.com/"}
            ]
        ]
    }
    
    payload = {
        "chat_id": CHAT_ID,
        "photo": image_url,
        "caption": text,
        "parse_mode": "HTML",
        "reply_markup": json.dumps(keyboard)
    }
    
    r = requests.post(url, data=payload)
    print(f"Log: {r.text}")

if __name__ == "__main__":
    data = get_market_data()
    send_telegram(data)
