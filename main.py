import os
import requests
import datetime

# GitHub Secrets
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
        
        # Mistral-এর জন্য প্রম্পট
        data = {
            "model": "open-mistral-7b",
            "messages": [
                {"role": "user", "content": "Write a one-sentence unique motivational or family life tip in Bengali with a relevant emoji. No intro, just the quote."}
            ]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        result = response.json()
        
        if 'choices' in result:
            return result['choices'][0]['message']['content'].strip()
        else:
            return "💡 ধৈর্য ধরুন, ভালো জিনিস পেতে কিছুটা সময় লাগে।"
    except Exception as e:
        print(f"Error: {e}")
        return "🚀 সাফল্যের মূল চাবিকাঠি হলো কাজ শুরু করা এবং হাল না ছাড়া।"

def get_market_data():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    formatted_time = now.strftime("%d-%m-%Y %I:%M %p")
    
    daily_tip = get_ai_inspiration()
    
    message = f"🌟 *MARKET WATCH (DAILY UPDATE)* 🌟\n"
    message += f"━━━━━━━━━━━━━━━━━━━━\n"
    message += f"📅 *Date:* `{formatted_time}`\n\n"
    
    message += f"💰 *CRYPTO PRICES*\n"
    message += f"• BTC: `$68,418` ✅\n"
    message += f"• ETH: `$1,987.97` ✨\n\n"
    
    message += f"📊 *STOCK MARKET*\n"
    message += f"• Nifty: `25,756.30` 📈\n"
    message += f"• Gold: `Closed (Weekend)` 🔒\n\n"
    
    message += f"✨ *AI Daily Inspiration:*\n"
    message += f"_{daily_tip}_\n"
    
    message += f"━━━━━━━━━━━━━━━━━━━━\n"
    message += f"🚀 *Powered by Mintu Automation*"
    return message

def send_telegram_animation(text):
    if not TOKEN or not CHAT_ID: return

    # এই লিঙ্কটি সরাসরি একটি ভিডিও ফাইল, যা টেলিগ্রাম অ্যানিমেশন হিসেবে দেখাবে
    animation_url = "https://assets.mixkit.co/videos/preview/mixkit-clouds-and-blue-sky-background-996-large.mp4"

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
