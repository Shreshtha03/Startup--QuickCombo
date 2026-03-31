import os
import time
import requests

# This script is meant to be run by AlwaysData Scheduled Tasks every 5 minutes
# to prevent the backend from spinning down due to inactivity.

# Replace with your actual deployed AlwaysData backend URL if different
API_URL = os.environ.get("QUICKCOMBO_API_URL", "https://quickcombo.alwaysdata.net/api/restaurants/")

def ping_server():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Pinging {API_URL} to keep server awake...")
    try:
        response = requests.get(API_URL, timeout=10)
        if response.status_code == 200:
            print(f"✅ Success! Server is awake. Response time: {response.elapsed.total_seconds()}s")
        else:
            print(f"⚠️ Warning: Server responded with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error pinging server: {e}")

if __name__ == "__main__":
    ping_server()
