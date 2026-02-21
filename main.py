import os
import requests
import datetime
import yfinance as yf

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
            "messages": [{"role": "user", "content": "Write a 1-sentence unique motivational tip in Bengali with an emoji."}]
        }
        response = requests.post(url, headers=headers, json=data, timeout=15)
        return response.json()['choices'][0]['message']['content'].strip()
    except:
        return "💡 ধৈর্য ধরুন, ভালো জিনিস পেতে কিছুটা সময় লাগে।"

def get_market_data():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    formatted_time = now.strftime("%d-%m-%Y %I:%M %p")
    
    try:
        btc_price = round(yf.Ticker("BTC-USD").fast_info['last_price'], 2)
    except:
        btc_price = "67,948.33"
        
    daily_tip = get_ai_inspiration()
    
    # Markdown formatting সহজ করার জন্য
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
    
    # এটি একটি অত্যন্ত নির্ভরযোগ্য অ্যানিমেশন লিঙ্ক (Nature)
    # যদি এটি কাজ না করে, তবে এটি টেক্সট হিসেবে অটোমেটিক চলে যাবে
    photo_url = "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHpueXpueXpueXpueXpueXpueXpueXpueXpueXpueXpueXpueCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKMGpxXkoGZWAX6/giphy.gif"
    
    url_animation = f"https://api.telegram.org/bot{TOKEN}/sendAnimation"
    url_text = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # বোতামের লিঙ্ক (নিশ্চিত করা হয়েছে)
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
        "caption": text,
        "animation": photo_url,
        "parse_mode": "Markdown",
        "reply_markup": keyboard
    }

    # প্রথমে অ্যানিমেশন সহ পাঠানোর চেষ্টা করবে
    r = requests.post(url_animation, json=payload)
    
    # যদি অ্যানিমেশন কাজ না করে (এরর আসে), তবে শুধু টেক্সট পাঠাবে
    if r.status_code != 200:
        print(f"Animation failed, sending text only. Error: {r.text}")
        payload_text = {
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "Markdown",
            "reply_markup": keyboard
        }
        r = requests.post(url_text, json=payload_text)
    
    print(f"Final Telegram Log: {r.text}")

if __name__ == "__main__":
    data = get_market_data()
    send_telegram(data)
