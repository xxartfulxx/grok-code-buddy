import os
import sqlite3
import json
from datetime import datetime
from dotenv import load_dotenv
import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk

# Load API key
load_dotenv()
XAI_API_KEY = os.getenv('XAI_API_KEY')
REQUEST_COUNT = 0
REQUEST_LIMIT = 100
DB_FILE = "grok_chat_history.db"

# SQLite setup
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        messages TEXT NOT NULL
    )
''')
conn.commit()

# Store current session
current_session = []

def fetch_grok_response(prompt):
    global REQUEST_COUNT, current_session
    if REQUEST_COUNT >= REQUEST_LIMIT:
        return "Whoa, we’ve hit the limit! Time to chill—back tomorrow, yeah?"
    REQUEST_COUNT += 1
    
    current_session.append({'role': 'user', 'content': prompt})
    
    try:
        response = requests.post(
            'https://api.x.ai/v1/chat/completions',
            json={
                'model': 'grok-beta',
                'messages': current_session,
                'max_tokens': 150
            },
            headers={
                'Authorization': f'Bearer {XAI_API_KEY}',
                'Content-Type': 'application/json'
            }
        )
        response.raise_for_status()
        answer = response.json()['choices'][0]['message']['content'].strip()
        current_session.append({'role': 'assistant', 'content': answer})
        return answer
    except requests.exceptions.RequestException as e:
        return f"Oof, something’s glitchy: {str(e)}"

def send_prompt(event=None):
    prompt = input_field.get("1.0", tk.END).strip()
    if not prompt:
        messagebox.showinfo("Hey!", "Got a question? Throw it my way!")
        return
    answer_field.delete("1.0", tk.END)
    answer_field.insert(tk.END, "Processing your cosmic query...\n")
    response = fetch_grok_response(prompt)
    display_current_session()
    input_field.delete("1.0", tk.END)

def new_chat():
    global current_session
    if current_session:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO chats (timestamp, messages) VALUES (?, ?)", 
                       (timestamp, json.dumps(current_session)))
        conn.commit()
        update_history_list()
    current_session = []
    answer_field.delete("1.0", tk.END)
    answer_field.insert(tk.END, "New chat started! What’s on your mind?\n")

def clear_all_chats():
    global current_session
    cursor.execute("DELETE FROM chats")
    conn.commit()
    current_session = []
    update_history_list()
    answer_field.delete("1.0", tk.END)
    answer_field.insert(tk.END, "All chats cleared! Fresh start—ask away.\n")
    input_field.delete("1.0", tk.END)

def display_current_session():
    answer_field.delete("1.0", tk.END)
    if not current_session:
        answer_field.insert(tk.END, "Start typing to chat!\n")
        return
    for entry in current_session:
        if entry['role'] == 'user':
            answer_field.insert(tk.END, f"You: {entry['content']}\n")
        else:
            answer_field.insert(tk.END, f"Grok: {entry['content']}\n")
    answer_field.insert(tk.END, f"\n[Requests: {REQUEST_COUNT}/{REQUEST_LIMIT}]")

def load_chat(event):
    global current_session
    selected = history_listbox.get(history_listbox.curselection())
    if selected:
        timestamp = selected.split(" - ")[0]
        cursor.execute("SELECT messages FROM chats WHERE timestamp = ?", (timestamp,))
        result = cursor.fetchone()
        if result:
            current_session = json.loads(result[0])
            display_current_session()

def update_history_list():
    history_listbox.delete(0, tk.END)
    cursor.execute("SELECT timestamp, messages FROM chats ORDER BY timestamp DESC")
    for row in cursor.fetchall():
        timestamp, messages = row
        messages_list = json.loads(messages)
        preview = messages_list[0]['content'][:20] + "..." if messages_list else "Empty chat"
        history_listbox.insert(tk.END, f"{timestamp} - {preview}")

def paste_text(event=None):
    try:
        input_field.delete("1.0", tk.END)
        input_field.insert(tk.END, root.clipboard_get())
    except tk.TclError:
        pass

def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)

# Set up the GUI
root = tk.Tk()
root.title("Grok Chat by debPii")
root.geometry("700x600")
root.configure(bg="#000000")  # Black background

# Style configuration
style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", font=("Helvetica", 10, "bold"), padding=8, background="#ff0000", foreground="#ffffff")  # Red buttons, white text
style.map("TButton", background=[('active', '#cc0000')])  # Darker red on hover
style.configure("Clear.TButton", background="#ff3333", foreground="#ffffff")  # Slightly lighter red for Clear
style.map("Clear.TButton", background=[('active', '#cc3333')])

# Main frame
main_frame = tk.Frame(root, bg="#000000")
main_frame.pack(fill="both", expand=True)

# History panel
history_frame = tk.Frame(main_frame, bg="#1a1a1a", width=200)  # Dark gray (near black)
history_frame.pack(side=tk.LEFT, fill="y", padx=(10, 0), pady=10)
tk.Label(history_frame, text="Chat History", font=("Helvetica", 12, "bold"), fg="#ff0000", bg="#1a1a1a").pack(pady=5)  # Red text
history_listbox = tk.Listbox(history_frame, bg="#1a1a1a", fg="#ffffff", font=("Helvetica", 10), bd=0, highlightthickness=0)  # White text
history_listbox.pack(fill="both", expand=True, padx=5, pady=5)
history_listbox.bind("<<ListboxSelect>>", load_chat)

# Chat area
chat_frame = tk.Frame(main_frame, bg="#000000")
chat_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)

# Header
header_frame = tk.Frame(chat_frame, bg="#000000")
header_frame.pack(pady=5)
tk.Label(header_frame, text="Grok Chat by debPii", font=("Helvetica", 20, "bold"), fg="#ffffff", bg="#000000").pack()  # White title, bold Helvetica

# Answer area
answer_frame = tk.Frame(chat_frame, bg="#000000")
answer_frame.pack(fill="both", expand=True)
answer_field = scrolledtext.ScrolledText(
    answer_frame, height=20, width=50, wrap=tk.WORD, bg="#1a1a1a", fg="#ffffff",  # Dark gray bg, white text
    font=("Helvetica", 10), bd=0, relief="flat"
)
answer_field.pack(fill="both", expand=True)
answer_field.insert(tk.END, "Hey, I’m Grok! Start a new chat or pick one from the left.\n")

# Input area
input_frame = tk.Frame(chat_frame, bg="#000000")
input_frame.pack(fill="x", pady=5)
input_field = scrolledtext.ScrolledText(
    input_frame, height=3, width=50, wrap=tk.WORD, bg="#1a1a1a", fg="#ffffff",  # Dark gray bg, white text
    font=("Helvetica", 10), bd=0, relief="flat", insertbackground="#ff0000"  # Red cursor
)
input_field.pack(side=tk.LEFT, fill="x", expand=True)
input_field.bind("<Return>", send_prompt)
input_field.bind("<Control-v>", paste_text)

# Context menu
context_menu = tk.Menu(root, tearoff=0, bg="#1a1a1a", fg="#ffffff")  # Dark gray bg, white text
context_menu.add_command(label="Paste", command=paste_text, background="#1a1a1a", foreground="#ffffff")
input_field.bind("<Button-3>", show_context_menu)

# Buttons
button_frame = tk.Frame(chat_frame, bg="#000000")
button_frame.pack(pady=5)
send_button = ttk.Button(button_frame, text="Send", command=send_prompt, style="TButton")
send_button.pack(side=tk.LEFT, padx=5)
new_button = ttk.Button(button_frame, text="New Chat", command=new_chat, style="TButton")
new_button.pack(side=tk.LEFT, padx=5)
clear_button = ttk.Button(button_frame, text="Clear All", command=clear_all_chats, style="Clear.TButton")
clear_button.pack(side=tk.LEFT, padx=5)
exit_button = ttk.Button(button_frame, text="Exit", command=root.quit, style="TButton")
exit_button.pack(side=tk.LEFT, padx=5)

# Load initial history
update_history_list()

root.mainloop()

# Close database connection
conn.close()