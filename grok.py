import os
from dotenv import load_dotenv
import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox

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
            'https://api.x.ai/v1/chat/completions',
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

def ask_grok():
    prompt = input_field.get("1.0", tk.END).strip()
    if not prompt:
        messagebox.showwarning("Empty Input", "Please ask something!")
        return
    response_field.delete("1.0", tk.END)
    response_field.insert(tk.END, "Thinking...\n")
    response = fetch_grok_response(prompt)
    response_field.delete("1.0", tk.END)
    response_field.insert(tk.END, f"{response}\n\nRequests: {REQUEST_COUNT}/{REQUEST_LIMIT}")

root = tk.Tk()
root.title("Grok's Code Companion (Birthday Edition)")
root.geometry("400x500")

tk.Label(root, text="Ask Grok a Coding Question", font=("Arial", 14, "bold")).pack(pady=10)

input_field = scrolledtext.ScrolledText(root, height=5, width=40, wrap=tk.WORD)
input_field.pack(pady=5)

tk.Button(root, text="Ask", command=ask_grok).pack(pady=5)

response_field = scrolledtext.ScrolledText(root, height=15, width=40, wrap=tk.WORD)
response_field.pack(pady=5)

tk.Button(root, text="Quit", command=root.quit).pack(pady=5)

root.mainloop()