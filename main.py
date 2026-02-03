import os
import requests
import feedparser
import random
import time

# ১. ক্রিপ্টো প্রাইজ ও নিউজ
def get_crypto_update():
    try:
        price_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        res = requests.get(price_url).json()
        btc, eth = res['bitcoin']['usd'], res['ethereum']['usd']
        
        news_api = os.getenv("NEWS_API_KEY")
        news_url = f"https://newsapi.org/v2/everything?q=crypto&pageSize=2&apiKey={news_api}"
        n_res = requests.get(news_url).json()
        articles = n_res.get('articles', [])
        
        msg = f"📊 *Crypto Live:* BTC: ${btc} | ETH: ${eth}\n\n"
        for art in articles:
            msg += f"🔹 [{art['title'][:60]}...]({art['url']})\n"
        return msg + "\n"
    except:
        return "📊 *Crypto News:* Currently updating...\n\n"

# ২. ডাইনামিক ডিল হান্টার (MEGA Deals Style)
def post_mega_deals():
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    amazon_tag = "offerslive24-21"
    
    # জনপ্রিয় ডিল সাইটের ফিড
    feed_url = "https://indiafreestuff.in/feed"
    # ব্রাউজার হিসেবে পরিচয় দেওয়ার জন্য (যাতে ব্লক না করে)
    feed = feedparser.parse(feed_url, agent='Mozilla/5.0')
    
    if not feed.entries:
        # যদি ডিল না পায়, একটি সাধারণ মেসেজ দেবে
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      data={"chat_id": chat_id, "text": "🔎 *নতুন কোনো বড় ডিল এই মুহূর্তে নেই। আমাদের ক্যাটাগরি মেনু চেক করুন নিচে!*", "parse_mode": "Markdown"})
        return

    # সর্বশেষ ৩টি ডিল আলাদা আলাদা পোস্ট হবে (ভিডিওর মতো)
    for entry in feed.entries[:3]:
        title = entry.title.split('|')[0].strip()
        link = entry.link
        
        if "amazon.in" in link:
            link = f"{link}&tag={amazon_tag}" if "?" in link else f"{link}?tag={amazon_tag}"
        
        # ডিফল্ট ছবি
        img = "https://img.freepik.com/free-vector/special-offer-modern-sale-banner-template_1017-20667.jpg"
        
        caption = f"🛍️ *{title}*\n\n🔥 *Limited Time Deal! Grab it now!*\n\n👉 [Click Here to Buy]({link})"
        
        # ফটো পোস্ট করা
        payload = {"chat_id": chat_id, "photo": img, "caption": caption, "parse_mode": "Markdown"}
        requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", data=payload)
        time.sleep(3) # বিরতি

# ৩. হেলথ টিপস ও মেনু
def get_footer():
    tips = ["💧 পর্যাপ্ত জল পান করুন।", "🥗 লবণ কম খান।", "😴 ৭-৮ ঘণ্টা ঘুমান।", "🚶‍♂️ ২০ মিনিট হাঁটুন।"]
    tag = "offerslive24-21"
    
    footer = f"🍎 *Daily Health Tip:* _{random.choice(tips)}_\n\n"
    footer += "━━━ *SHOP BY CATEGORY* ━━━\n"
    footer += f"📱 [Smartphones](https://www.amazon.in/mobiles?tag={tag}) | 💻 [Laptops](https://www.amazon.in/electronics?tag={tag})\n"
    footer += f"👗 [Fashion](https://myntr.it/b9SAtFm) | 🎁 [Flipkart Loot](https://fktr.in/7WhPb8j)\n\n"
    footer += "✨ *Hurry! Prices may increase anytime!*"
    return footer

if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    
    # প্রথমে ক্রিপ্টো ও নিউজ পাঠাবে
    header_msg = get_crypto_update()
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": header_msg, "parse_mode": "Markdown", "disable_web_page_preview": True})
    
    # তারপর ৩টি ডিল আলাদা ফটো সহ পাঠাবে
    post_mega_deals()
    
    # সবশেষে হেলথ টিপস ও ক্যাটাগরি মেনু পাঠাবে
    footer_msg = get_footer()
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": footer_msg, "parse_mode": "Markdown", "disable_web_page_preview": True})

    print("MEGA Deals Automation Complete!")
