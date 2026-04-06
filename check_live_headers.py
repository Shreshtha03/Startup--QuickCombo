import requests

def check_headers():
    try:
        # Hit the DJANGO API specifically
        url = 'https://quickcombo.alwaysdata.net/api/menu/'
        print(f"Checking URL: {url}")
        r = requests.get(url)
        print(f"Status: {r.status_code}")
        print("--- Headers ---")
        for k, v in r.headers.items():
            print(f"{k}: {v}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_headers()
