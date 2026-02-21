import os
import requests
import datetime
import yfinance as yf
import json

# GitHub Secrets
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# আপনার কপি করা ইনভাইট লিঙ্কটি এখানে বসান (যেমন: https://t.me/+Abc123...)
INVITE_LINK = "https://t.me/OFFERS_LIVE_24" 

def get_ai_inspiration():
    try:
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
        data = {
            "model": "open-mistral-7b",
            "messages": [{"role": "user", "content": "Write a short Bengali motivational quote."}]
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        return response.json()['choices'][0]['message']['content'].strip()
    except:
        return "সাফল্য মানে প্রতিদিনের ছোট ছোট প্রচেষ্টার সমষ্টি।"

def get_market_data():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    formatted_time = now.strftime("%d-%m-%Y %I:%M %p")
    try:
        btc = round(yf.Ticker("BTC-USD").fast_info['last_price'], 2)
    except:
        btc = "67,974"
    
    daily_tip = get_ai_inspiration()
    
    message = f"🌟 <b>MARKET WATCH (DAILY UPDATE)</b> 🌟\n"
    message += f"━━━━━━━━━━━━━━━━━━━━\n"
    message += f"📅 <b>Date:</b> {formatted_time}\n\n"
    message += f"💰 <b>CRYPTO PRICES</b>\n"
    message += f"• BTC: ${btc} 📈\n\n"
    message += f"✨ <b>AI Inspiration:</b>\n"
    message += f"<i>{daily_tip}</i>\n\n"
    message += f"🚀 <b>Powered by Mintu Automation</b>"
    return message

def send_telegram(text):
    if not TOKEN or not CHAT_ID: return
    
    image_url = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1000&q=80"
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    
    # বোতামের লিঙ্ক
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🔗 Join Our Channel", "url": https://t.me/offers_live_24},
                {"text": "📊 Charts", "url": "https://www.tradingview.com/"}
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
    
    requests.post(url, data=payload)

if __name__ == "__main__":
    data = get_market_data()
    send_telegram(data)
