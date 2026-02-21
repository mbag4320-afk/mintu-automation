import os
import requests
import datetime
import yfinance as yf

# GitHub Secrets
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def get_market_data():
    tickers = {"BTC": "BTC-USD", "ETH": "ETH-USD", "SP500": "^GSPC", "USD_INR": "INR=X"}
    data = {}
    for key, ticker in tickers.items():
        try:
            stock = yf.Ticker(ticker)
            price = stock.fast_info['last_price']
            hist = stock.history(period="2d")
            prev_close = hist['Close'].iloc[-2]
            change = ((price - prev_close) / prev_close) * 100
            emoji = "🟢" if change >= 0 else "🔴"
            data[key] = f"{price:,.2f} ({emoji} {change:+.2f}%)"
        except:
            data[key] = "N/A"
    return data

def get_ai_analysis(market_info):
    if not MISTRAL_API_KEY: return "সাফল্য ধৈর্য এবং সঠিক পরিকল্পনার ফল।"
    try:
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
        prompt = f"Market: {market_info}. Give a 1-sentence Bengali market mood and 1 motivational tip. Avoid HTML tags."
        data = {
            "model": "open-mistral-7b",
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(url, headers=headers, json=data, timeout=15)
        # HTML এরর এড়াতে বিশেষ চিহ্নগুলো বদলে দেওয়া
        res_text = response.json()['choices'][0]['message']['content'].strip()
        return res_text.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
    except:
        return "বাজারের ওপর নজর রাখুন এবং দীর্ঘমেয়াদী চিন্তা করুন।"

def get_final_message():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    market = get_market_data()
    ai_thought = get_ai_analysis(market)
    
    # সময় অনুযায়ী শুভেচ্ছা
    greet = "শুভ সকাল" if 5 <= now.hour < 12 else "শুভ দুপুর" if 12 <= now.hour < 17 else "শুভ সন্ধ্যা" if 17 <= now.hour < 20 else "শুভ রাত্রি"

    msg = f"<b>{greet}! 🌟</b>\n"
    msg += f"📊 <b>Smart Market Report</b>\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"📅 <b>Update:</b> {now.strftime('%d-%m-%Y %I:%M %p')}\n\n"
    msg += f"💰 <b>CRYPTO ASSETS</b>\n"
    msg += f"• BTC: <code>${market['BTC']}</code>\n"
    msg += f"• ETH: <code>${market['ETH']}</code>\n\n"
    msg += f"🌎 <b>GLOBAL & FOREX</b>\n"
    msg += f"• S&P 500: <code>{market['SP500']}</code>\n"
    msg += f"• USD/INR: <code>₹{market['USD_INR']}</code>\n\n"
    msg += f"💡 <b>AI Analysis:</b>\n"
    msg += f"<i>{ai_thought}</i>\n\n"
    msg += f"🔗 <b>Join:</b> @OFFERS_LIVE_24\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"🚀 <b>Powered by Mintu Automation</b>"
    return msg

def send_telegram(text):
    if not TOKEN or not CHAT_ID: 
        print("Missing TOKEN or CHAT_ID")
        return
        
    # ছবি সহ পাঠানোর চেষ্টা
    img_url = "https://images.unsplash.com/photo-1611974714024-462cd92e3902?q=80&w=1000&auto=format"
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHAT_ID,
        "photo": img_url,
        "caption": text,
        "parse_mode": "HTML"
    }
    
    response = requests.post(url, json=payload)
    
    # যদি ছবি সহ মেসেজ এরর দেয়, তবে শুধু টেক্সট পাঠাবে
    if not response.json().get("ok"):
        print(f"Photo failed: {response.text}. Trying text only...")
        url_text = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload_text = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
        response = requests.post(url_text, json=payload_text)
        
    print(f"Final Telegram Response: {response.text}")

if __name__ == "__main__":
    content = get_final_message()
    send_telegram(content)
