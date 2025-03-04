import os
import requests
from dotenv import load_dotenv
import threading

load_dotenv()
XAI_API_KEY = os.getenv('XAI_API_KEY')
REQUEST_COUNT = 0
REQUEST_LIMIT = 100  # Adjust if xAI specifies a real limit

def fetch_grok_response(prompt, session, gui):
    global REQUEST_COUNT
    print(f"Entering fetch_grok_response with prompt: {prompt}")
    
    if REQUEST_COUNT >= REQUEST_LIMIT:
        print("Hit local request limit")
        return "Whoa, we’ve hit the limit! Time to chill—back later, yeah?"
    
    REQUEST_COUNT += 1
    gui.increment_request_count()
    print(f"Global request count incremented to: {REQUEST_COUNT}")

    session.append({'role': 'user', 'content': prompt})
    print(f"Session updated: {session}")

    api_url = "https://api.x.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {XAI_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "grok-beta",
        "messages": session,  # Full session history
        "max_tokens": 500  # Increased for longer responses
    }

    def make_api_call():
        try:
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            answer = data['choices'][0]['message']['content']  # Adjust if response structure differs
            print(f"API response received: {answer[:50]}...")
            session.append({'role': 'assistant', 'content': answer})
            gui.root.after(0, lambda: gui.display_session())  # Update GUI safely
        except requests.exceptions.RequestException as e:
            error_msg = f"Oops, something went wrong: {str(e)}"
            print(error_msg)
            session.append({'role': 'assistant', 'content': error_msg})
            gui.root.after(0, lambda: gui.display_session())

    threading.Thread(target=make_api_call).start()
    return "Processing... check back soon!"  # Immediate feedback