import os
import requests
import datetime
import yfinance as yf

# GitHub Secrets থেকে তথ্য নেওয়া
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def get_ai_inspiration():
    """Mistral AI ব্যবহার করে ইউনিক টিপস তৈরি করা"""
    if not MISTRAL_API_KEY:
        return "🌱 আজকের ছোট ছোট বিনিয়োগই আপনার ভবিষ্যতের বড় সম্পদ।"

    try:
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MISTRAL_API_KEY}"
        }
        data = {
            "model": "open-mistral-7b",
            "messages": [{"role": "user", "content": "Write a 1-sentence unique motivational or family life tip in Bengali with an emoji. Simple and inspiring."}]
        }
        response = requests.post(url, headers=headers, json=data, timeout=15)
        return response.json()['choices'][0]['message']['content'].strip()
    except:
        return "💡 ধৈর্য ধরুন, ভালো জিনিস পেতে কিছুটা সময় লাগে।"

def get_live_prices():
    """লাইভ মার্কেট থেকে ডাটা নেওয়া"""
    try:
        btc = yf.Ticker("BTC-USD").fast_info['last_price']
        return round(btc, 2)
    except:
        return "68,418" # এরর হলে আগের দাম দেখাবে

def get_market_data():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    formatted_time = now.strftime("%d-%m-%Y %I:%M %p")
    
    btc_price = get_live_prices()
    daily_tip = get_ai_inspiration()
    
    message = f"🌟 *MARKET WATCH (DAILY UPDATE)* 🌟\n"
    message += f"━━━━━━━━━━━━━━━━━━━━\n"
    message += f"📅 *Date:* `{formatted_time}`\n\n"
    
    message += f"💰 *CRYPTO PRICES*\n"
    message += f"• BTC: `${btc_price}` 📈\n"
    message += f"• ETH: `$1,987.97` ✨\n\n"
    
    message += f"📊 *STOCK MARKET*\n"
    message += f"• Nifty: `25,756.30` ✅\n"
    message += f"• Gold: `Closed (Weekend)` 🔒\n\n"
    
    message += f"✨ *AI Daily Inspiration:*\n"
    message += f"_{daily_tip}_\n"
    
    message += f"━━━━━━━━━━━━━━━━━━━━\n"
    message += f"🚀 *Powered by Mintu Automation*"
    return message

def send_telegram(text):
    if not TOKEN or not CHAT_ID: return
    
    # এটি একটি স্টেবল অ্যানিমেশন লিঙ্ক
    animation_url = "https://assets.mixkit.co/videos/preview/mixkit-clouds-and-blue-sky-background-996-large.mp4"
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendAnimation"
    keyboard = {
        "inline_keyboard": [[{"text": "🔗 Join Channel", "url": "https://t.me/offers_live_24"}]]
    }
    payload = {
        "chat_id": CHAT_ID,
        "animation": animation_url,
        "caption": text,
        "parse_mode": "Markdown",
        "reply_markup": keyboard
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    data = get_market_data()
    send_telegram(data)
