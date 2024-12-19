print("Aarambikkalaangala")
#https://github.com/builders-hut/dead-ideas

import sqlite3
import bcrypt
import json
import os

# File constants
SAVE_FOLDER = "saves"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)


# ========== User Management ==========
def setup_database():
    """Sets up the SQLite database for user management."""
    conn = sqlite3.connect("user_system.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def register_user(username, password):
    """Registers a new user in the database."""
    conn = sqlite3.connect("user_system.db")
    cursor = conn.cursor()

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print(f"User '{username}' registered successfully!")
    except sqlite3.IntegrityError:
        print(f"Error: Username '{username}' is already taken.")
    finally:
        conn.close()


def login_user(username, password):
    """Validates user credentials and logs them in."""
    conn = sqlite3.connect("user_system.db")
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    conn.close()

    if result:
        stored_password = result[0]
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            print(f"Login successful! Welcome, {username}.")
            return True
        else:
            print("Incorrect password. Please try again.")
    else:
        print(f"Username '{username}' not found.")

    return False
