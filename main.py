import requests
import datetime

# আপনার তথ্য এখানে দিন
TOKEN = "আপনার_বট_টোকেন"
CHAT_ID = "আপনার_চ্যাট_আইডি"

def get_market_data():
    # এখানে ক্রিপ্টো এবং স্টকের দামের এপিআই কল হবে (উদাহরণস্বরূপ)
    # আপনি যদি নির্দিষ্ট কোনো সাইট থেকে ডেটা নেন, তবে সেই লজিক এখানে থাকবে
    # আমি একটি স্যাম্পল ফরম্যাট দিচ্ছি যা দেখতে প্রফেশনাল লাগবে
    
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    
    message = f"🌟 *MARKET WATCH (DAILY UPDATE)* 🌟\n"
    message += f"📅 _Date: {now}_\n\n"
    
    message += f"💰 *CRYPTO PRICES*\n"
    message += f"• BTC: `$68,418` 📈\n"
    message += f"• ETH: `$1,987.97` ✨\n\n"
    
    message += f"📊 *STOCK MARKET*\n"
    message += f"• Nifty: `25,756.30` ✅\n"
    message += f"• Gold: `Closed (Weekend)` 🔒\n\n"
    
    message += f"📢 *Alert:* No mega loots found right now. Stay tuned for upcoming deals!\n\n"
    message += f"🔗 [Join Our Channel](https://t.me/offers_live_24)\n"
    message += f"🚀 *Powered by Mintu Automation*"
    
    return message

def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    data = get_market_data()
    send_telegram_msg(data)
