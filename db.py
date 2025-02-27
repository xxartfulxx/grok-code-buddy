import sqlite3
from datetime import datetime
import json

DB_FILE = "grok_chat_history.db"

def initialize_db():
    """Set up the SQLite database and table, dropping old version if exists."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS chats")
    cursor.execute('''
        CREATE TABLE chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            messages TEXT NOT NULL,
            chat_id TEXT NOT NULL
        )
    ''')
    conn.commit()
    print("Database initialized with new schema")
    return conn

def save_session(conn, session, chat_id):
    """Save or update the current session by chat_id."""
    if not session:
        print("Session empty, not saving")
        return conn
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor = conn.cursor()
    print(f"Saving to DB: {session} with chat_id: {chat_id}")
    cursor.execute("SELECT id FROM chats WHERE chat_id = ?", (chat_id,))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("UPDATE chats SET messages = ?, timestamp = ? WHERE chat_id = ?",
                       (json.dumps(session), timestamp, chat_id))
        print(f"Updated existing chat with chat_id: {chat_id}")
    else:
        cursor.execute("INSERT INTO chats (timestamp, messages, chat_id) VALUES (?, ?, ?)",
                       (timestamp, json.dumps(session), chat_id))
        print(f"Inserted new chat with chat_id: {chat_id}")
    conn.commit()
    print("Saved to DB, committed")
    return conn

def load_chat(conn, timestamp):
    """Load a chat session by timestamp, return messages and chat_id."""
    cursor = conn.cursor()
    cursor.execute("SELECT messages, chat_id FROM chats WHERE timestamp = ?", (timestamp,))
    result = cursor.fetchone()
    return (json.loads(result[0]), result[1]) if result else ([], None)

def delete_chat(conn, timestamp):
    """Delete a chat session by timestamp."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chats WHERE timestamp = ?", (timestamp,))
    conn.commit()

def get_chat_history(conn):
    """Retrieve all chat history for display."""
    conn.commit()
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, messages, chat_id FROM chats ORDER BY timestamp DESC")
    history = cursor.fetchall()
    print(f"Fetched history: {history}")
    return history

def clear_all_chats(conn):
    """Clear all chat history."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chats")
    conn.commit()