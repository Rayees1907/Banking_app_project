import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

DATABASE = 'data/bank.db' # Path relative to the project root

def get_db_connection():
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            balance REAL DEFAULT 0.0
        )
    ''')
    conn.commit()
    conn.close()

def create_user(username, password):
    hashed_password = generate_password_hash(password)
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO users (username, password, balance) VALUES (?, ?, ?)",
                       (username, hashed_password, 0.0))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # Username already exists
    finally:
        conn.close()

def get_user_by_username(username):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return user

def update_user_balance(user_id, amount):
    conn = get_db_connection()
    conn.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, user_id))
    conn.commit()
    conn.close()

def check_password(hashed_password, password):
    return check_password_hash(hashed_password, password)