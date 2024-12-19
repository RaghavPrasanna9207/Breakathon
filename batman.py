print("Aarambikkalaangala")
#https://github.com/builders-hut/dead-ideas

import sqlite3
import bcrypt

# Database Setup
def setup_database():
    """Sets up the SQLite database for user management."""
    conn = sqlite3.connect("medibolt_system.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK(role IN ('Patient', 'Doctor', 'Staff')) NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# User Registration
def register_user(username, password, role):
    """Registers a new user in the database."""
    conn = sqlite3.connect("medibolt_system.db")
    cursor = conn.cursor()

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       (username, hashed_password, role))
        conn.commit()
        print(f"User '{username}' registered successfully as {role}!")
    except sqlite3.IntegrityError:
        print(f"Error: Username '{username}' is already taken.")
    finally:
        conn.close()

# User Login
def login_user(username, password):
    """Validates user credentials and logs them in."""
    conn = sqlite3.connect("medibolt_system.db")
    cursor = conn.cursor()

    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_password, role = result
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            print(f"Login successful! Welcome, {username} ({role}).")
            return role
        else:
            print("Incorrect password. Please try again.")
    else:
        print(f"Username '{username}' not found.")

    return None

# Main Application Loop
def main():
    setup_database()  # Ensure the database is set up

    logged_in_user = None
    logged_in_role = None

    while True:
        if not logged_in_user:
            print("\nMedibolt User Management System")
            print("1. Register a new user")
            print("2. Login")
            print("3. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                # Register a new user
                username = input("Enter a new username: ")
                password = input("Enter a new password: ")
                print("Select role:")
                print("1. Patient")
                print("2. Doctor")
                print("3. Staff")
                role_choice = input("Choose a role (1/2/3): ")
                role_map = {"1": "Patient", "2": "Doctor", "3": "Staff"}
                role = role_map.get(role_choice)

                if role:
                    register_user(username, password, role)
                else:
                    print("Invalid role selection. Please try again.")

            elif choice == "2":
                # Login
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                role = login_user(username, password)

                if role:
                    logged_in_user = username
                    logged_in_role = role

            elif choice == "3":
                # Exit
                print("Exiting the system. Goodbye!")
                break

            else:
                print("Invalid option. Please try again.")

        else:
            print(f"\nWelcome, {logged_in_user} ({logged_in_role})")
            print("1. Sign out")
            print("2. Exit")
            action_choice = input("Choose an option: ")

            if action_choice == "1":
                print(f"Signing out {logged_in_user}...")
                logged_in_user = None
                logged_in_role = None

            elif action_choice == "2":
                print("Exiting the system. Goodbye!")
                break

            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
