import requests
import os
from decouple import config

api_key = "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"
sender_email = "ayushtomar061004@gmail.com"
to_email = "shreshtha0311@gmail.com"

url = "https://api.brevo.com/v3/smtp/email"
headers = {
    "accept": "application/json",
    "api-key": api_key,
    "content-type": "application/json"
}

data = {
    "sender": {"name": "QuickCombo Test", "email": sender_email},
    "to": [{"email": to_email, "name": "Shreshtha"}],
    "subject": "QuickCombo Brevo API Test",
    "htmlContent": "<html><body><h1>It works!</h1><p>This is a test from Brevo API.</p></body></html>"
}

response = requests.post(url, headers=headers, json=data)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
