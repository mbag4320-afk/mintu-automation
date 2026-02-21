import os
import requests
import datetime
import random

# GitHub Secrets থেকে তথ্য নেওয়া
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_inspiration():
    tips = [
        "🌱 আজকের ছোট ছোট বিনিয়োগই আপনার ভবিষ্যতের বড় সম্পদ।",
        "👨‍👩‍👧‍👦 পরিবারের সাথে কাটানো সময় হলো জীবনের সেরা বিনিয়োগ।",
        "💡 ধৈর্য ধরুন, ভালো জিনিস পেতে কিছুটা সময় লাগে।",
        "🚀 সাফল্যের মূল চাবিকাঠি হলো কাজ শুরু করা এবং হাল না ছাড়া।",
        "💰 সঞ্চয় করার মানে হলো নিজের ভবিষ্যৎকে নিরাপদ করা।",
        "🌟 প্রতিদিন নিজেকে অন্তত ১% উন্নত করার চেষ্টা করুন।",
        "🍎 সুস্বাস্থ্যই সকল সুখের মূল। আজ থেকেই নিজের যত্ন নিন।",
        "📚 প্রতিদিন নতুন কিছু শিখুন, জ্ঞানই আপনাকে অন্যদের থেকে এগিয়ে রাখবে।"
    ]
    return random.choice(tips)

def get_market_data():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    formatted_time = now.strftime("%d-%m-%Y %I:%M %p")
    daily_tip = get_inspiration()
    
    # মেসেজ ফরম্যাট (Caption হিসেবে থাকবে)
    message = f"🌟 *MARKET WATCH (DAILY UPDATE)* 🌟\n"
    message += f"━━━━━━━━━━━━━━━━━━━━\n"
    message += f"📅 *Date:* `{formatted_time}`\n\n"
    
    message += f"💰 *CRYPTO PRICES*\n"
    message += f"• BTC: `$68,418` 📈\n"
    message += f"• ETH: `$1,987.97` ✨\n\n"
    
    message += f"📊 *STOCK MARKET*\n"
    message += f"• Nifty: `25,756.30` ✅\n"
    message += f"• Gold: `Closed (Weekend)` 🔒\n\n"
    
    message += f"✨ *Daily Inspiration & Tips:*\n"
    message += f"_{daily_tip}_\n"
    
    message += f"━━━━━━━━━━━━━━━━━━━━\n"
    message += f"🚀 *Powered by Mintu Automation*"
    
    return message

def send_telegram_animation(text):
    if not TOKEN or not CHAT_ID:
        return

    # এখানে একটি সুন্দর শান্ত বা মোটিভেশনাল অ্যানিমেশনের লিঙ্ক দেওয়া হয়েছে
    # আপনি চাইলে আপনার পছন্দের যেকোনো GIF লিঙ্ক এখানে দিতে পারেন
    animation_url = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJndXIzZmx6bmx3bm93eHptZ3RsczZ4bm93eHptZ3RsczZ4bm8mZXA9djFfaW50ZXJuYWxfZ2lmX2J5X2lkJmN0PWc/3o7TKVUn7iM8FMEU24/giphy.gif"

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
        "caption": text, # আপনার টেক্সটটি এখন ক্যাপশন হিসেবে যাবে
        "parse_mode": "Markdown",
        "reply_markup": keyboard
    }
    
    requests.post(url, json=payload)

if __name__ == "__main__":
    data = get_market_data()
    send_telegram_animation(data)
