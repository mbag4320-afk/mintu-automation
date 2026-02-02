import os
import requests

def get_crypto_data():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        response = requests.get(url).json()
        btc = response['bitcoin']['usd']
        eth = response['ethereum']['usd']
        return f"🚀 *Crypto Price Update:*\n\n💰 Bitcoin: ${btc}\n💎 Ethereum: ${eth}"
    except:
        return "🚀 *Crypto Price Update:* (Data unavailable)"

def get_crypto_news():
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/everything?q=crypto&pageSize=3&apiKey={api_key}"
    try:
        response = requests.get(url).json()
        articles = response.get('articles', [])
        news_text = "\n\n📰 *Latest Crypto News:*\n"
        for art in articles:
            news_text += f"🔹 [{art['title']}]({art['url']})\n\n"
        return news_text
    except:
        return "\n\n📰 *News currently unavailable.*"

def send_telegram_message(message):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown", "disable_web_page_preview": False}
    requests.post(url, data=payload)

if __name__ == "__main__":
    content = get_crypto_data() + get_crypto_news()
    content += "\n\n🔥 Join for more updates!" # এখানে পরে আপনার রেফারেল লিঙ্ক দিতে পারবেন
    send_telegram_message(content)
    print("Update sent successfully!")
