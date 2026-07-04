import sqlite3
import os

DB_FILE = 'users.db'

def setup():
    """Create a fresh database for users."""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT, email TEXT)')
    conn.commit()
    conn.close()
    
    print("Database 'users.db' has been successfully initialized.")

if __name__ == "__main__":
    setup()


