import os
import requests
import datetime
import yfinance as yf
import pandas as pd

# GitHub Secrets
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def get_fear_greed_index():
    """ক্রিপ্টো ফিয়ার অ্যান্ড গ্রিড ইনডেক্স সংগ্রহ"""
    try:
        r = requests.get("https://api.alternative.me/fng/", timeout=10)
        data = r.json()['data'][0]
        return f"{data['value']} ({data['value_classification']})"
    except:
        return "N/A"

def calculate_rsi(ticker, period=14):
    """টেকনিক্যাল RSI সিগন্যাল বের করা"""
    try:
        data = yf.download(ticker, period="1mo", interval="1d", progress=False)
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]
        
        signal = "⚖️ Neutral"
        if current_rsi > 70: signal = "⚠️ Overbought (মজুদ কমান)"
        elif current_rsi < 30: signal = "✅ Oversold (কেনার সুযোগ)"
        return f"{current_rsi:.2f} [{signal}]"
    except:
        return "N/A"

def get_market_data():
    tickers = {
        "BTC": "BTC-USD",
        "ETH": "ETH-USD",
        "NIFTY": "^NSEI",   # ইন্ডিয়ান নিফটি ৫০
        "GOLD": "GC=F",     # আন্তর্জাতিক গোল্ড
        "USD_INR": "INR=X"
    }
    market_results = {}
    for key, ticker in tickers.items():
        try:
            stock = yf.Ticker(ticker)
            price = stock.fast_info['last_price']
            hist = stock.history(period="2d")
            prev_close = hist['Close'].iloc[-2]
            change = ((price - prev_close) / prev_close) * 100
            emoji = "🟢" if change >= 0 else "🔴"
            market_results[key] = f"{price:,.2f} ({emoji} {change:+.2f}%)"
        except:
            market_results[key] = "Data Error"
    return market_results

def get_ai_analysis(market_info, fng, rsi):
    if not MISTRAL_API_KEY: return "ধৈর্য ও সঠিক পরিকল্পনাই সাফল্যের চাবিকাঠি।"
    try:
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
        prompt = f"Prices: {market_info}, FearGreed: {fng}, BTC-RSI: {rsi}. Give a professional market summary and 1 motivational tip in Bengali. Total 3 sentences max."
        data = {
            "model": "open-mistral-7b",
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(url, headers=headers, json=data, timeout=15)
        res_text = response.json()['choices'][0]['message']['content'].strip()
        return res_text.replace("<", "&lt;").replace(">", "&gt;")
    except:
        return "বাজারের ওপর নজর রাখুন এবং নিজের লক্ষ্যে অবিচল থাকুন।"

def get_final_report():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    market = get_market_data()
    fng = get_fear_greed_index()
    btc_rsi = calculate_rsi("BTC-USD")
    ai_analysis = get_ai_analysis(market, fng, btc_rsi)
    
    greet = "শুভ সকাল" if 5 <= now.hour < 12 else "শুভ দুপুর" if 12 <= now.hour < 17 else "শুভ সন্ধ্যা" if 17 <= now.hour < 20 else "শুভ রাত্রি"

    msg = f"<b>{greet}! 🏛️ Financial Dashboard</b>\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"📅 <b>Update:</b> {now.strftime('%d-%m-%Y %I:%M %p')}\n\n"
    
    msg += f"🌡 <b>MARKET SENTIMENT</b>\n"
    msg += f"• Fear &amp; Greed: <code>{fng}</code>\n"
    msg += f"• BTC RSI (14d): <code>{btc_rsi}</code>\n\n"
    
    msg += f"💰 <b>MAJOR ASSETS (LIVE)</b>\n"
    msg += f"• BTC: <code>${market['BTC']}</code>\n"
    msg += f"• ETH: <code>${market['ETH']}</code>\n"
    msg += f"• Gold: <code>${market['GOLD']}</code>\n"
    msg += f"• Nifty 50: <code>{market['NIFTY']}</code>\n\n"
    
    msg += f"💵 <b>CURRENCY</b>\n"
    msg += f"• USD/INR: <code>₹{market['USD_INR']}</code>\n\n"
    
    msg += f"💡 <b>AI Strategic Analysis:</b>\n"
    msg += f"<i>{ai_analysis}</i>\n\n"
    
    msg += f"🔗 <b>Join Community:</b> @OFFERS_LIVE_24\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"🚀 <b>Powered by Mintu Automation AI</b>"
    return msg

def send_telegram(text):
    if not TOKEN or not CHAT_ID: return
    img_url = "https://images.unsplash.com/photo-1611974714024-462cd92e3902?q=80&w=1000&auto=format"
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    payload = {"chat_id": CHAT_ID, "photo": img_url, "caption": text, "parse_mode": "HTML"}
    response = requests.post(url, json=payload)
    if not response.json().get("ok"):
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})

if __name__ == "__main__":
    report = get_final_report()
    send_telegram(report)
