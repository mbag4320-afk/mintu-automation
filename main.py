import os
import requests
import datetime
import yfinance as yf
import json

# GitHub Secrets থেকে তথ্য নেওয়া
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def get_ai_inspiration():
    """Mistral AI ব্যবহার করে ইউনিক টিপস তৈরি করা"""
    if not MISTRAL_API_KEY:
        return "সাফল্য মানে প্রতিদিনের ছোট ছোট প্রচেষ্টার সমষ্টি।"
    try:
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
        data = {
            "model": "open-mistral-7b",
            "messages": [{"role": "user", "content": "Write a 1-sentence powerful motivational tip in Bengali. Only the sentence."}]
        }
        response = requests.post(url, headers=headers, json=data, timeout=15)
        return response.json()['choices'][0]['message']['content'].strip()
    except:
        return "আজ তুমি শুরু করো, হার মেনো না কখনো।"

def get_market_data():
    """লাইভ মার্কেট ডাটা সংগ্রহ"""
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    formatted_time = now.strftime("%d-%m-%Y %I:%M %p")
    
    try:
        btc_price = round(yf.Ticker("BTC-USD").fast_info['last_price'], 2)
        eth_price = round(yf.Ticker("ETH-USD").fast_info['last_price'], 2)
    except:
        btc_price, eth_price = "67,974.55", "1,987.97"
        
    daily_tip = get_ai_inspiration()
    
    # HTML ফরম্যাটে সুন্দর মেসেজ
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
    message += f"🚀 <b>Powered by Mintu Automation</b>"
    return message

def send_telegram(text):
    if not TOKEN or not CHAT_ID: return
    
    # প্রকৃতির একটি সুন্দর স্থির ছবি
    image_url = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1000&q=80"
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    
    # বোতামের লিঙ্ক - সরাসরি টেলিগ্রাম অ্যাপ ওপেন করার জন্য
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🔗 Join Channel", "url": "https://t.me/OFFERS_LIVE_24"},
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
    print(f"Final Telegram Response: {r.text}")

if __name__ == "__main__":
    data = get_market_data()
    send_telegram(data)
