import tkinter as tk
from tkinter import messagebox, ttk
import api
from utils import format_code_block
from db import load_chat, delete_chat, get_chat_history
import json 
import uuid

class GrokGUI:
    def __init__(self, root, conn, session, send_callback, new_chat_callback, clear_all_callback):
        self.root = root
        self.conn = conn
        self.session = session
        self.send_callback = send_callback
        self.new_chat_callback = new_chat_callback
        self.clear_all_callback = clear_all_callback
        self.request_count = 0
        self.current_chat_id = str(uuid.uuid4())
        self.setup_gui()

    def setup_gui(self):
        self.root.title("Grok Chat by debPii")
        self.root.geometry("700x600")
        self.root.configure(bg="#000000")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", font=("Helvetica", 10, "bold"), padding=8, background="#ff0000", foreground="#ffffff")
        style.map("TButton", background=[('active', '#cc0000')])
        style.configure("Clear.TButton", background="#ff3333", foreground="#ffffff")
        style.map("Clear.TButton", background=[('active', '#cc3333')])

        main_frame = tk.Frame(self.root, bg="#000000")
        main_frame.pack(fill="both", expand=True)

        self.history_frame = tk.Frame(main_frame, bg="#1a1a1a", width=300)
        self.history_frame.pack(side=tk.LEFT, fill="y", padx=(10, 0), pady=10)
        tk.Label(self.history_frame, text="Chat History", font=("Helvetica", 12, "bold"), fg="#ff0000", bg="#1a1a1a").pack(pady=5)
        self.history_listbox = tk.Listbox(self.history_frame, bg="#1a1a1a", fg="#ffffff", font=("Helvetica", 10), bd=0, highlightthickness=0)
        self.history_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.history_listbox.bind("<<ListboxSelect>>", self.load_chat)
        self.history_listbox.bind("<Double-Button-1>", self.delete_chat)

        chat_frame = tk.Frame(main_frame, bg="#000000")
        chat_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)

        tk.Label(chat_frame, text="Grok Chat by debPii", font=("Helvetica", 20, "bold"), fg="#ffffff", bg="#000000").pack(pady=5)

        # Answer field with scrollbar
        answer_container = tk.Frame(chat_frame, bg="#000000")
        answer_container.pack(fill="both", expand=True)
        self.answer_field = tk.Text(answer_container, height=20, width=50, wrap=tk.WORD, bg="#1a1a1a", fg="#ffffff", font=("Courier", 10), bd=0, relief="flat")
        self.answer_field.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar = tk.Scrollbar(answer_container, command=self.answer_field.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.answer_field.config(yscrollcommand=scrollbar.set)
        self.answer_field.insert(tk.END, "Hey, I’m Grok! Start a new chat or pick one from the left.\n")
        self.answer_field.bind("<Button-3>", self.show_context_menu)
        self.answer_field.tag_configure("keyword", foreground="#ff5555")  # Red
        self.answer_field.tag_configure("string", foreground="#55ff55")   # Green
        self.answer_field.tag_configure("comment", foreground="#888888")  # Grey
        self.answer_field.tag_configure("normal", foreground="#ffffff")   # White

        # Input field with scrollbar
        input_frame = tk.Frame(chat_frame, bg="#000000")
        input_frame.pack(fill="x", pady=(5, 0))
        self.input_field = tk.Text(input_frame, height=3, width=50, wrap=tk.WORD, bg="#1a1a1a", fg="#ffffff", font=("Helvetica", 10), bd=0, relief="flat", insertbackground="#ff0000")
        self.input_field.pack(side=tk.LEFT, fill="x", expand=True)
        input_scrollbar = tk.Scrollbar(input_frame, command=self.input_field.yview)
        input_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.input_field.config(yscrollcommand=input_scrollbar.set)
        self.input_field.bind("<Return>", self.send_prompt)
        self.input_field.bind("<Control-v>", self.paste_text)
        self.input_field.bind("<Button-3>", self.show_context_menu)

        self.context_menu = tk.Menu(self.root, tearoff=0, bg="#1a1a1a", fg="#ffffff")
        self.context_menu.add_command(label="Paste", command=self.paste_text, background="#1a1a1a", foreground="#ffffff")
        self.context_menu.add_command(label="Copy", command=self.copy_text, background="#1a1a1a", foreground="#ffffff")

        button_frame = tk.Frame(chat_frame, bg="#000000")
        button_frame.pack(fill="x", pady=(5, 0))
        ttk.Button(button_frame, text="Send", command=self.send_prompt, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="New Chat", command=self.new_chat_callback, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_all_callback, style="Clear.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit, style="TButton").pack(side=tk.LEFT, padx=5)

        self.update_history_list()

    def send_prompt(self, event=None):
        prompt = self.input_field.get("1.0", tk.END).strip()
        if not prompt:
            messagebox.showinfo("Hey!", "Got a question? Throw it my way!")
            return "break"
        self.input_field.delete("1.0", tk.END)
        self.answer_field.delete("1.0", tk.END)
        self.answer_field.insert(tk.END, "Processing your cosmic query...\n")
        self.answer_field.see(tk.END)
        self.root.update()
        print("Calling send_callback...")
        self.send_callback(prompt)
        return "break"

    def display_session(self):
        self.answer_field.delete("1.0", tk.END)
        if not self.session:
            self.answer_field.insert(tk.END, "Start typing to chat!\n")
            return
        for entry in self.session:
            if entry['role'] == 'user':
                self.answer_field.insert(tk.END, f"You: {entry['content']}\n")
            else:
                formatted_content = format_code_block(entry['content'])
                self.answer_field.insert(tk.END, "Grok: ")
                for text, tag in formatted_content:
                    self.answer_field.insert(tk.END, text, tag)
        self.answer_field.insert(tk.END, f"\n[Requests: {self.request_count}/{api.REQUEST_LIMIT}]")
        self.answer_field.see(tk.END)
        print(f"Displayed session, chat request count: {self.request_count}, global count: {api.REQUEST_COUNT}")

    def load_chat(self, event):
        selected = self.history_listbox.get(self.history_listbox.curselection())
        if selected:
            timestamp = selected.split(" [X]")[0]
            messages, chat_id = load_chat(self.conn, timestamp)
            self.session[:] = messages
            self.current_chat_id = chat_id if chat_id else str(uuid.uuid4())
            self.request_count = len(messages) // 2
            print(f"Loaded chat with chat_id: {self.current_chat_id}, messages: {messages}")
            self.display_session()

    def delete_chat(self, event):
        selected = self.history_listbox.get(self.history_listbox.curselection())
        if selected:
            timestamp = selected.split(" [X]")[0]
            delete_chat(self.conn, timestamp)
            self.update_history_list()
            if self.session == load_chat(self.conn, timestamp)[0]:
                self.session.clear()
                self.answer_field.delete("1.0", tk.END)
                self.answer_field.insert(tk.END, "Chat deleted! Start a new one?\n")

    def update_history_list(self):
        print("Updating history listbox...")
        self.history_listbox.delete(0, tk.END)
        history = get_chat_history(self.conn)
        print(f"History to display: {history}")
        for timestamp, messages, chat_id in history:
            messages_list = json.loads(messages)
            preview = messages_list[0]['content'][:20] + "..." if messages_list else "Empty chat"
            print(f"Adding entry: {timestamp} [X] - {preview} (chat_id: {chat_id})")
            self.history_listbox.insert(tk.END, f"{timestamp} [X] - {preview}")
        print(f"History listbox updated with {len(history)} entries")
        self.history_listbox.update()
        self.root.update()

    def paste_text(self, event=None):
        try:
            self.input_field.delete("1.0", tk.END)
            self.input_field.insert(tk.END, self.root.clipboard_get())
        except tk.TclError:
            pass

    def copy_text(self, event=None):
        self.root.clipboard_clear()
        text_to_copy = self.answer_field.get("1.0", tk.END).strip()
        self.root.clipboard_append(text_to_copy)
        messagebox.showinfo("Copied!", "Chat text copied to clipboard!")

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def increment_request_count(self):
        self.request_count += 1

    def reset_request_count(self):
        self.request_count = 0

    def new_chat_id(self):
        self.current_chat_id = str(uuid.uuid4())
        print(f"New chat ID generated: {self.current_chat_id}")