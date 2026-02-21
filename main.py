import os
import requests
import datetime

# GitHub Secrets থেকে অটোমেটিক টোকেন ও আইডি নেওয়ার জন্য
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_market_data():
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    
    # প্রফেশনাল মেসেজ ফরম্যাট
    message = f"🌟 *MARKET WATCH (DAILY UPDATE)* 🌟\n"
    message += f"📅 _Date: {now}_\n\n"
    
    message += f"💰 *CRYPTO PRICES*\n"
    message += f"• BTC: `$68,418` 📈\n"
    message += f"• ETH: `$1,987.97` ✨\n\n"
    
    message += f"📊 *STOCK MARKET*\n"
    message += f"• Nifty: `25,756.30` ✅\n"
    message += f"• Gold: `Closed (Weekend)` 🔒\n\n"
    
    message += f"📢 *Alert:* Stay tuned for upcoming deals!\n\n"
    message += f"🔗 [Join Our Channel](https://t.me/offers_live_24)\n"
    message += f"🚀 *Powered by Mintu Automation*"
    
    return message

def send_telegram_msg(text):
    if not TOKEN or not CHAT_ID:
        print("Error: BOT_TOKEN or CHAT_ID not found in Secrets!")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("Success: Message sent to Telegram!")
    else:
        print(f"Failed: Status Code {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    data = get_market_data()
    send_telegram_msg(data)
