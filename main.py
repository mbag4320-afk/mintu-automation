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
        return "🌱 আজকের ছোট ছোট বিনিয়োগই আপনার ভবিষ্যতের বড় সম্পদ।"
    try:
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
        data = {
            "model": "open-mistral-7b",
            "messages": [{"role": "user", "content": "Write a 1-sentence motivational or family life tip in Bengali with an emoji. Simple and clean."}]
        }
        response = requests.post(url, headers=headers, json=data, timeout=15)
        text = response.json()['choices'][0]['message']['content'].strip()
        # Markdown এরর এড়াতে কিছু চিহ্ন পরিষ্কার করা
        return text.replace("_", "-").replace("*", "")
    except:
        return "💡 ধৈর্য ধরুন, ভালো জিনিস পেতে কিছুটা সময় লাগে।"

def get_market_data():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    formatted_time = now.strftime("%d-%m-%Y %I:%M %p")
    
    try:
        btc_price = round(yf.Ticker("BTC-USD").fast_info['last_price'], 2)
    except:
        btc_price = "67,974.55"
        
    daily_tip = get_ai_inspiration()
    
    message = f"🌟 *MARKET WATCH (DAILY UPDATE)* 🌟\n"
    message += f"━━━━━━━━━━━━━━━━━━━━\n"
    message += f"📅 *Date:* {formatted_time}\n\n"
    message += f"💰 *CRYPTO PRICES*\n"
    message += f"• BTC: ${btc_price} 📈\n"
    message += f"• ETH: $1,987.97 ✨\n\n"
    message += f"📊 *STOCK MARKET*\n"
    message += f"• Nifty: 25,756.30 ✅\n"
    message += f"• Gold: Closed (Weekend) 🔒\n\n"
    message += f"✨ *AI Daily Inspiration:*\n"
    message += f"{daily_tip}\n\n"
    message += f"🚀 *Powered by Mintu Automation*"
    return message

def send_telegram(text):
    if not TOKEN or not CHAT_ID: return
    
    image_url = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1000&q=80"
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    
    # বোতামের সঠিক লিঙ্ক এবং ফরম্যাট
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
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(keyboard) # বোতামকে JSON ফরম্যাটে পাঠানো হচ্ছে
    }
    
    r = requests.post(url, data=payload)
    print(f"Final Telegram Log: {r.text}")

if __name__ == "__main__":
    data = get_market_data()
    send_telegram(data)
