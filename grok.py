import tkinter as tk
from db import initialize_db, save_session
from api import fetch_grok_response
from gui import GrokGUI

def main():
    root = tk.Tk()
    conn = initialize_db()
    current_session = []

    def send_prompt(prompt):
        nonlocal gui
        print(f"Sending prompt: {prompt}")
        response = fetch_grok_response(prompt, current_session, gui)
        print(f"Got initial response: {response}")
        gui.answer_field.delete("1.0", tk.END)
        gui.answer_field.insert(tk.END, response + "\n")
        # Save moved to api.py thread to include API response
        gui.update_history_list()
        print("GUI update called—history should refresh")

    def new_chat():
        nonlocal gui
        if current_session:
            save_session(conn, current_session, gui.current_chat_id)
            print("Saved current chat as a unique session")
            current_session.clear()
        gui.new_chat_id()
        gui.reset_request_count()
        gui.answer_field.delete("1.0", tk.END)
        gui.answer_field.insert(tk.END, "New chat started! What’s on your mind?\n")
        gui.update_history_list()
        print("New chat started, history refreshed")

    def clear_all_chats():
        nonlocal gui
        from db import clear_all_chats
        clear_all_chats(conn)
        current_session.clear()
        gui.new_chat_id()
        gui.reset_request_count()
        gui.update_history_list()
        gui.answer_field.delete("1.0", tk.END)
        gui.answer_field.insert(tk.END, "All chats cleared! Fresh start—ask away.\n")

    gui = GrokGUI(root, conn, current_session, send_prompt, new_chat, clear_all_chats)
    root.mainloop()

if __name__ == "__main__":
    main()