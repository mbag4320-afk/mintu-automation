import os
import requests
import datetime
import yfinance as yf

# GitHub Secrets
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def get_greeting():
    hour = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).hour
    if 5 <= hour < 12: return "শুভ সকাল ☀️"
    elif 12 <= hour < 17: return "শুভ দুপুর 🌤️"
    elif 17 <= hour < 20: return "শুভ সন্ধ্যা 🌆"
    else: return "শুভ রাত্রি 🌙"

def get_ai_insight():
    if not MISTRAL_API_KEY:
        return "সাফল্য মানে প্রতিদিনের ছোট ছোট প্রচেষ্টার সমষ্টি।"
    try:
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
        data = {
            "model": "open-mistral-7b",
            "messages": [{"role": "user", "content": "Write a 1-sentence motivational tip in Bengali. Avoid using special characters like <>."}]
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        res = response.json()
        return res['choices'][0]['message']['content'].strip().replace("<", "").replace(">", "")
    except:
        return "ধৈর্য ও সঠিক সিদ্ধান্তই বিনিয়োগের মূল চাবিকাঠি।"

def get_crypto_prices():
    prices = {}
    tickers = {"BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD"}
    for coin, ticker in tickers.items():
        try:
            val = yf.Ticker(ticker).fast_info['last_price']
            prices[coin] = f"${round(val, 2)}"
        except:
            prices[coin] = "Updating..."
    return prices

def get_final_message():
    greeting = get_greeting()
    prices = get_crypto_prices()
    ai_insight = get_ai_insight()
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).strftime("%d-%m-%Y %I:%M %p")
    
    # সহজ টেক্সট ফরম্যাট যাতে টেলিগ্রাম রিজেক্ট না করে
    msg = f"<b>{greeting}</b>\n"
    msg += f"📊 <b>Market Update</b>\n"
    msg += f"━━━━━━━━━━━━━━\n"
    msg += f"📅 <b>Date:</b> {now}\n\n"
    msg += f"💰 <b>CRYPTO PRICES</b>\n"
    msg += f"• BTC: {prices['BTC']}\n"
    msg += f"• ETH: {prices['ETH']}\n"
    msg += f"• SOL: {prices['SOL']}\n\n"
    msg += f"💡 <b>AI Insight:</b>\n"
    msg += f"<i>{ai_insight}</i>\n\n"
    msg += f"🔗 <b>Join:</b> https://t.me/OFFERS_LIVE_24\n"
    msg += f"━━━━━━━━━━━━━━\n"
    msg += f"🚀 Powered by Mintu Automation"
    return msg

def send_telegram(text):
    if not TOKEN or not CHAT_ID: return
    
    # প্রথমে ছবি ছাড়া সাধারণ মেসেজ পাঠিয়ে টেস্ট করি (এটি ১০০% কাজ করবে)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    
    response = requests.post(url, json=payload)
    print(f"Telegram Response: {response.text}") # এটি GitHub লগে এরর দেখতে সাহায্য করবে

if __name__ == "__main__":
    message_text = get_final_message()
    send_telegram(message_text)
