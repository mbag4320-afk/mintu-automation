import os
import requests
import random

# ১. ক্রিপ্টো প্রাইজ সংগ্রহের ফাংশন
def get_crypto_data():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        response = requests.get(url).json()
        btc = response['bitcoin']['usd']
        eth = response['ethereum']['usd']
        return f"🚀 *Crypto Market Update:*\n💰 BTC: ${btc} | 💎 ETH: ${eth}\n"
    except:
        return "🚀 *Crypto Update:* Data unavailable.\n"

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

# ৩. ডেইলি হেলথ টিপস (Bengali)
def get_health_tip():
    tips = [
        "💧 পর্যাপ্ত জল পান করুন, এটি শরীর সতেজ রাখে।",
        "🥗 খাবারে লবণের পরিমাণ কমান, রক্তচাপ নিয়ন্ত্রণে থাকবে।",
        "😴 রাতে অন্তত ৭-৮ ঘণ্টা ঘুমানোর অভ্যাস করুন।",
        "🍎 প্রতিদিন অন্তত একটি ঋতুভিত্তিক ফল খান।",
        "🚶‍♂️ দিনে অন্তত ২০ মিনিট দ্রুত হাঁটার অভ্যাস করুন।"
    ]
    return f"\n🍎 *Daily Health Tip:*\n_{random.choice(tips)}_\n"

# ৪. সব প্ল্যাটফর্মের ইনকাম লিঙ্ক (Amazon, Flipkart, Ajio, Myntra)
def get_all_deals():
    amazon_tag = "offerslive24-21"
    
    # আপনার দেওয়া প্রফিট লিঙ্কগুলো এখানে সেট করা হলো
    flipkart_link = "https://fktr.in/7WhPb8j"
    ajio_link = "https://ajiio.in/5eCLfL0"
    myntra_link = "https://myntr.it/b9SAtFm"
    budget_deals = "https://bitli.in/fCeVayZ"
    
    deals_text = "\n🔥 *Today's Best Shopping Deals:*\n"
    
    # আমাজন সেকশন
    deals_text += "\n📦 *Amazon Exclusive:*\n"
    deals_text += f"📱 [Mobiles & Gadgets](https://www.amazon.in/mobiles?tag={amazon_tag})\n"
    deals_text += f"💻 [Electronics & Laptops](https://www.amazon.in/electronics?tag={amazon_tag})\n"
    
    # অন্যান্য মেগা স্টোর সেকশন
    deals_text += "\n💰 *Mega Loot & Fashion:*\n"
    deals_text += f"🛍️ [Flipkart Big Bachat Deals]({flipkart_link})\n"
    deals_text += f"👟 [Ajio Trending Fashion]({ajio_link})\n"
    deals_text += f"👗 [Myntra Style Sale]({myntra_link})\n"
    deals_text += f"⚡ [Limited Time Loot Offers]({budget_deals})\n"
    
    deals_text += "\n🛍️ *Click and Shop to support our channel!*"
    return deals_text

# ৫. টেলিগ্রামে মেসেজ পাঠানোর ফাংশন
def send_telegram_message(message):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id, 
        "text": message, 
        "parse_mode": "Markdown", 
        "disable_web_page_preview": True 
    }
    requests.post(url, data=payload)

# মূল রানার
if __name__ == "__main__":
    final_message = get_crypto_data() + get_crypto_news() + get_health_tip() + get_all_deals()
    send_telegram_message(final_message)
    print("Full Income Automation Successful!")
