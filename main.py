import os
import requests
import datetime
import yfinance as yf

# GitHub Secrets
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def get_market_data():
    """লাইভ মার্কেট এবং গ্লোবাল ডাটা সংগ্রহ"""
    data = {}
    # আমরা এই সম্পদগুলোর ডাটা নেব
    tickers = {
        "BTC": "BTC-USD",
        "ETH": "ETH-USD",
        "SP500": "^GSPC",   # আমেরিকার বাজার
        "USD_INR": "INR=X"  # ডলার রেট
    }
    
    for key, ticker in tickers.items():
        try:
            stock = yf.Ticker(ticker)
            info = stock.fast_info
            price = info['last_price']
            # ২৪ ঘণ্টার পরিবর্তন বের করা
            prev_close = stock.history(period="2d")['Close'].iloc[-2]
            change_pct = ((price - prev_close) / prev_close) * 100
            
            emoji = "🟢" if change_pct >= 0 else "🔴"
            data[key] = f"${price:,.2f} ({emoji} {change_pct:+.2f}%)"
            
            if key == "USD_INR": # ডলারের জন্য শুধু রুপি সাইন
                 data[key] = f"₹{price:.2f} ({emoji} {change_pct:+.2f}%)"
        except:
            data[key] = "Data Unavailable"
    return data

def get_ai_analysis(market_info):
    """Mistral AI থেকে বাজারের মুড এবং টিপস নেওয়া"""
    if not MISTRAL_API_KEY:
        return "সাফল্য ধৈর্য এবং সঠিক পরিকল্পনার ফল।"
    try:
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
        prompt = f"Today's prices: {market_info}. Give a 1-sentence market mood and 1 motivational tip in Bengali. Total 2 sentences."
        data = {
            "model": "open-mistral-7b",
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(url, headers=headers, json=data, timeout=15)
        return response.json()['choices'][0]['message']['content'].strip()
    except:
        return "বাজারের ওপর নজর রাখুন এবং দীর্ঘমেয়াদী চিন্তা করুন।"

def get_final_message():
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30))
    formatted_time = now.strftime("%d-%m-%Y %I:%M %p")
    market = get_market_data()
    ai_thought = get_ai_analysis(market)
    
    # শুভেচ্ছা জানানো
    hour = now.hour
    greet = "শুভ সকাল" if 5 <= hour < 12 else "শুভ দুপুর" if 12 <= hour < 17 else "শুভ সন্ধ্যা" if 17 <= hour < 20 else "শুভ রাত্রি"

    msg = f"<b>{greet}! 🌟</b>\n"
    msg += f"📊 <b>Smart Market Report</b>\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"📅 <b>Update:</b> {formatted_time}\n\n"
    
    msg += f"💰 <b>CRYPTO ASSETS</b>\n"
    msg += f"• BTC: <code>{market['BTC']}</code>\n"
    msg += f"• ETH: <code>{market['ETH']}</code>\n\n"
    
    msg += f"🌎 <b>GLOBAL & FOREX</b>\n"
    msg += f"• S&P 500: <code>{market['SP500']}</code>\n"
    msg += f"• USD/INR: <code>{market['USD_INR']}</code>\n\n"
    
    msg += f"💡 <b>AI Market Analysis:</b>\n"
    msg += f"<i>{ai_thought}</i>\n\n"
    
    # এই লিঙ্কটি টেলিগ্রামে ক্লিক করা সহজ হবে
    msg += f"🔗 <b>Official Channel:</b> <a href='https://t.me/OFFERS_LIVE_24'>@OFFERS_LIVE_24</a>\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"🚀 <b>Powered by Mintu Automation AI</b>"
    return msg

def send_telegram(text):
    if not TOKEN or not CHAT_ID: return
    # একটি নতুন প্রফেশনাল টেকনিক্যাল চার্ট ছবি
    image_url = "https://images.unsplash.com/photo-1611974714024-462cd92e3902?auto=format&fit=crop&w=1000&q=80"
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    
    payload = {
        "chat_id": CHAT_ID,
        "photo": image_url,
        "caption": text,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

if __name__ == "__main__":
    content = get_final_message()
    send_telegram(content)
