import os
import time
from dotenv import load_dotenv
import requests

# Load ENV vars
load_dotenv()
XAI_API_KEY = os.getenv('XAI_API_KEY')

def fetch_grok_response(prompt):
    # Mock API until credits land
    time.sleep(0.5)  # Fake delay
    return f"🎉 Happy birthday, Jamaican coder! Mock reply to: '{prompt}'"

def main():
    print("Welcome to Grok's Code Companion!")
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

if __name__ == "__main__":
    main()