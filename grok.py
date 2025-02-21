import os
from dotenv import load_dotenv
import requests

load_dotenv()
XAI_API_KEY = os.getenv('XAI_API_KEY')
REQUEST_COUNT = 0
REQUEST_LIMIT = 100

def fetch_grok_response(prompt):
    global REQUEST_COUNT
    if REQUEST_COUNT >= REQUEST_LIMIT:
        return "Whoa, daily limit hit! Saving credits like your UK stash—wait ‘til tomorrow!"
    REQUEST_COUNT += 1
    try:
        response = requests.post(
            'https://api.x.ai/v1/chat/completions',  # Full, correct URL
            json={
                'model': 'grok-beta',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 120
            },
            headers={
                'Authorization': f'Bearer {XAI_API_KEY}',
                'Content-Type': 'application/json'
            }
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except requests.exceptions.RequestException as e:
        return f"Oops, something went wrong: {str(e)}"

def main():
    print("Welcome to Grok's Code Companion!")
    print(f"Daily limit: {REQUEST_LIMIT} requests—keeping it lean!")
    while True:
        prompt = input("Ask Grok a coding question (or 'quit' to exit): ")
        if prompt.lower() == 'quit':
            print("See ya, birthday star!")
            break
        if not prompt.strip():
            print("Please ask something!")
            continue
        print("Thinking...")
        response = fetch_grok_response(prompt)
        print(response)
        print(f"Requests used: {REQUEST_COUNT}/{REQUEST_LIMIT}")

if __name__ == "__main__":
    main()