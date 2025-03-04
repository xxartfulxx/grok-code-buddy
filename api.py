import os
import requests
from dotenv import load_dotenv
import threading
from db import save_session
import sqlite3

load_dotenv()
XAI_API_KEY = os.getenv('XAI_API_KEY')
REQUEST_COUNT = 0
REQUEST_LIMIT = 100

def fetch_grok_response(prompt, session, gui):
    global REQUEST_COUNT
    print(f"Prompt: {prompt}")
    print(f"Prompt length (chars): {len(prompt)}")  # Log input size
    
    if REQUEST_COUNT >= REQUEST_LIMIT:
        print("Hit request limit")
        return "Hit the limit—chill for now, back soon!"
    
    REQUEST_COUNT += 1
    gui.increment_request_count()
    print(f"Request count: {REQUEST_COUNT}/{REQUEST_LIMIT}")

    session.append({'role': 'user', 'content': prompt})
    api_url = "https://api.x.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {XAI_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "grok-beta", "messages": session, "max_tokens": 4000}  # Upped to 4000

    def make_api_call():
        temp_conn = sqlite3.connect("grok_chat_history.db")
        try:
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            answer = data['choices'][0]['message']['content']
            print(f"Response: {answer[:50]}...")
            print(f"Response length (chars): {len(answer)}")  # Log output size
            session.append({'role': 'assistant', 'content': answer})
            save_session(temp_conn, session, gui.current_chat_id)
            gui.root.after(0, lambda: gui.display_session())
        except requests.RequestException as e:
            error_msg = f"Error: {str(e)}"
            print(error_msg)
            session.append({'role': 'assistant', 'content': error_msg})
            save_session(temp_conn, session, gui.current_chat_id)
            gui.root.after(0, lambda: gui.display_session())
        finally:
            temp_conn.close()

    threading.Thread(target=make_api_call).start()
    return "Processing your request..."