import os
import requests

def test_telegram():
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    
    # এটি শুধু একটি সাধারণ টেক্সট মেসেজ পাঠাবে
    message = "🔔 Hello! This is a test from your GitHub Bot."
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    
    r = requests.post(url, data=payload)
    
    print(f"Status Code: {r.status_code}")
    print(f"Response: {r.text}")

if __name__ == "__main__":
    test_telegram()
