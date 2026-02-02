import os
import requests

# ১. ক্রিপ্টো প্রাইজ সংগ্রহের ফাংশন
def get_crypto_data():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        response = requests.get(url).json()
        btc = response['bitcoin']['usd']
        eth = response['ethereum']['usd']
        return f"🚀 *Crypto Market Update:*\n💰 BTC: ${btc}\n💎 ETH: ${eth}\n"
    except:
        return "🚀 *Crypto Update:* Data temporarily unavailable.\n"

# ২. ক্রিপ্টো নিউজ সংগ্রহের ফাংশন
def get_crypto_news():
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/everything?q=crypto&pageSize=3&apiKey={api_key}"
    try:
        response = requests.get(url).json()
        articles = response.get('articles', [])
        news_text = "\n📰 *Latest Crypto News:*\n"
        for art in articles:
            news_text += f"🔹 [{art['title']}]({art['url']})\n"
        return news_text
    except:
        return ""

# ৩. সব ক্যাটাগরির অ্যামাজন ডিল লিঙ্ক তৈরির ফাংশন
def get_amazon_deals():
    tag = "offerslive24-21" # আপনার ইউনিক অ্যামাজন আইডি
    base_url = "https://www.amazon.in"
    
    deals_text = "\n🔥 *Today's Best Amazon Deals (Categorized):*\n\n"
    deals_text += f"📱 [Mobiles & Accessories]({base_url}/mobiles?tag={tag})\n"
    deals_text += f"💻 [Electronics & Laptops]({base_url}/electronics?tag={tag})\n"
    deals_text += f"👕 [Fashion & Clothing]({base_url}/fashion?tag={tag})\n"
    deals_text += f"🏠 [Home & Kitchen]({base_url}/home-improvement?tag={tag})\n"
    deals_text += f"⚡ [Daily Lightning Deals]({base_url}/deals?tag={tag})\n"
    
    deals_text += "\n🛍️ *Click any link above to shop and support us!*"
    return deals_text

# ৪. টেলিগ্রামে মেসেজ পাঠানোর ফাংশন
def send_telegram_message(message):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id, 
        "text": message, 
        "parse_mode": "Markdown", 
        "disable_web_page_preview": False
    }
    requests.post(url, data=payload)

# মূল রানার ফাংশন
if __name__ == "__main__":
    final_message = get_crypto_data() + get_crypto_news() + get_amazon_deals()
    send_telegram_message(final_message)
    print("Full Automation Successful!")
