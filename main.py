import os
import requests
import datetime

# GitHub Secrets থেকে অটোমেটিক টোকেন ও আইডি নেওয়ার জন্য
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_market_data():
    # বিদেশের সময়ের সাথে ৫ ঘণ্টা ৩০ মিনিট যোগ করে স্থানীয় সময় বের করা (IST/BST)
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    formatted_time = now.strftime("%d-%m-%Y %I:%M %p")
    
    message = f"🌟 *MARKET WATCH (DAILY UPDATE)* 🌟\n"
    message += f"━━━━━━━━━━━━━━━━━━━━\n"
    message += f"📅 *Date:* `{formatted_time}`\n\n"
    
    message += f"💰 *CRYPTO PRICES*\n"
    message += f"• BTC: `$68,418` 📈\n"
    message += f"• ETH: `$1,987.97` ✨\n\n"
    
    message += f"📊 *STOCK MARKET*\n"
    message += f"• Nifty: `25,756.30` ✅\n"
    message += f"• Gold: `Closed (Weekend)` 🔒\n\n"
    
    message += f"📢 *Alert:* Stay tuned for upcoming deals!\n"
    message += f"━━━━━━━━━━━━━━━━━━━━\n"
    message += f"🚀 *Powered by Mintu Automation*"
    
    return message

def send_telegram_msg(text):
    if not TOKEN or not CHAT_ID:
        print("Error: TOKEN or CHAT_ID not found!")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # ইনলাইন বাটন যোগ করা
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
        "text": text,
        "parse_mode": "Markdown",
        "reply_markup": keyboard # এখানে বাটন সেট করা হয়েছে
    }
    
    requests.post(url, json=payload)

if __name__ == "__main__":
    data = get_market_data()
    send_telegram_msg(data)
