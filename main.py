import os
import requests
import datetime
import random

# GitHub Secrets থেকে তথ্য নেওয়া
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_ai_inspiration():
    """AI ব্যবহার করে নিজে থেকে মোটিভেশনাল টিপস তৈরি করা"""
    if not GEMINI_API_KEY:
        return "🌱 আজকের ছোট ছোট বিনিয়োগই আপনার ভবিষ্যতের বড় সম্পদ।" # API না থাকলে ফলব্যাক টিপস

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        prompt = "Write a very short (1 sentence) unique motivational tip or a family life tip in Bengali. Start with a relevant emoji. Make it inspiring."
        
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        # AI জেনারেটেড টেক্সট বের করা
        ai_message = result['candidates'][0]['content']['parts'][0]['text']
        return ai_message.strip()
    except Exception as e:
        print(f"AI Error: {e}")
        return "🚀 সাফল্যের মূল চাবিকাঠি হলো কাজ শুরু করা এবং হাল না ছাড়া।"

def get_market_data():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    formatted_time = now.strftime("%d-%m-%Y %I:%M %p")
    
    # AI থেকে টিপস নেওয়া
    daily_tip = get_ai_inspiration()
    
    message = f"🌟 *MARKET WATCH (DAILY UPDATE)* 🌟\n"
    message += f"━━━━━━━━━━━━━━━━━━━━\n"
    message += f"📅 *Date:* `{formatted_time}`\n\n"
    
    message += f"💰 *CRYPTO PRICES*\n"
    message += f"• BTC: `$68,418` 📈\n"
    message += f"• ETH: `$1,987.97` ✨\n\n"
    
    message += f"📊 *STOCK MARKET*\n"
    message += f"• Nifty: `25,756.30` ✅\n"
    message += f"• Gold: `Closed (Weekend)` 🔒\n\n"
    
    message += f"✨ *AI Daily Inspiration:*\n"
    message += f"_{daily_tip}_\n"
    
    message += f"━━━━━━━━━━━━━━━━━━━━\n"
    message += f"🚀 *Powered by Mintu Automation*"
    
    return message

def send_telegram_animation(text):
    if not TOKEN or not CHAT_ID:
        return

    animation_url = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbnJ4Z2YyYm94bmR5YmZ4bmR5YmZ4bmR5YmZ4bmR5YmZ4bmR5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/v9XoNIdV9uN17u28jT/giphy.gif"

    url = f"https://api.telegram.org/bot{TOKEN}/sendAnimation"
    
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
        "animation": animation_url,
        "caption": text,
        "parse_mode": "Markdown",
        "reply_markup": keyboard
    }
    
    requests.post(url, json=payload)

if __name__ == "__main__":
    data = get_market_data()
    send_telegram_animation(data)
