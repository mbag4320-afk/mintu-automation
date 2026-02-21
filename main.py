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
    try:
        r = requests.get("https://api.alternative.me/fng/", timeout=10)
        data = r.json()['data'][0]
        return f"{data['value']} ({data['value_classification']})"
    except:
        return "Stable"

def calculate_rsi(ticker):
    try:
        # ডাটা ডাউনলোডে কিছুটা পরিবর্তন যাতে N/A না আসে
        data = yf.download(ticker, period="1mo", interval="1d", progress=False)
        if data.empty: return "Analyzing..."
        
        close = data['Close']
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        val = rsi.iloc[-1]
        
        if isinstance(val, pd.Series): val = val.iloc[0] # Handle multi-index
        
        signal = "⚖️ Neutral"
        if val > 70: signal = "⚠️ Overbought"
        elif val < 30: signal = "✅ Oversold"
        return f"{val:.2f} [{signal}]"
    except:
        return "Market Stability"

def get_market_data():
    tickers = {
        "BTC": "BTC-USD",
        "ETH": "ETH-USD",
        "NIFTY": "^NSEI",
        "GOLD": "GC=F",
        "USD_INR": "INR=X"
    }
    results = {}
    for key, ticker in tickers.items():
        try:
            stock = yf.Ticker(ticker)
            price = stock.fast_info['last_price']
            hist = stock.history(period="2d")
            prev_close = hist['Close'].iloc[-2]
            change = ((price - prev_close) / prev_close) * 100
            emoji = "🟢" if change >= 0 else "🔴"
            results[key] = f"{price:,.2f} ({emoji} {change:+.2f}%)"
        except:
            results[key] = "Data Live"
    return results

def get_ai_analysis(market, fng, rsi):
    if not MISTRAL_API_KEY: return "ধৈর্যই সফল বিনিয়োগের চাবিকাঠি।"
    try:
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
        # প্রম্পট আরও সুনির্দিষ্ট করা হয়েছে
        prompt = f"Prices: {market}, Sentiment: {fng}, RSI: {rsi}. Write a short professional market analysis and a motivational tip strictly in Bengali. No English translation."
        data = {
            "model": "open-mistral-7b",
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(url, headers=headers, json=data, timeout=15)
        return response.json()['choices'][0]['message']['content'].strip()
    except:
        return "বাজারের গতিবিধি পর্যবেক্ষণ করুন এবং শান্ত থাকুন।"

def get_final_report():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    market = get_market_data()
    fng = get_fear_greed_index()
    btc_rsi = calculate_rsi("BTC-USD")
    ai_msg = get_ai_analysis(market, fng, btc_rsi)
    
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
    msg += f"<i>{ai_msg}</i>\n\n"
    
    msg += f"🔗 <b>Join Community:</b> @OFFERS_LIVE_24\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━"
    return msg

def send_telegram(text):
    if not TOKEN or not CHAT_ID: return
    img_url = "https://images.unsplash.com/photo-1611974714024-462cd92e3902?q=80&w=1000&auto=format"
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    payload = {"chat_id": CHAT_ID, "photo": img_url, "caption": text, "parse_mode": "HTML"}
    r = requests.post(url, json=payload)
    if not r.json().get("ok"):
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})

if __name__ == "__main__":
    report = get_final_report()
    send_telegram(report)
