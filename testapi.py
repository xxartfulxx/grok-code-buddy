import os
import requests
from dotenv import load_dotenv

load_dotenv()
XAI_API_KEY = os.getenv('XAI_API_KEY')
api_url = "https://api.x.ai/v1/chat/completions"  # Replace with YOUR endpoint

headers = {
    "Authorization": f"Bearer {XAI_API_KEY}",
    "Content-Type": "application/json"
}
payload = {
    "model": "grok-beta",
    "messages": [{"role": "user", "content": "Hello, test!"}],
    "max_tokens": 50
}

response = requests.post(api_url, json=payload, headers=headers)
print("URL Tested:", api_url)
print("Status Code:", response.status_code)
print("Headers:", response.headers)
print("Raw Response:", response.text.encode().decode('utf-8', errors='replace'))
print("API Key (masked):", XAI_API_KEY[:5] + "..." + XAI_API_KEY[-5:])