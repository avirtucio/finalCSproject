import sqlite3
from datetime import datetime
import os
import base64

def seed_sample_posts(DB_NAME="models/closetappDB.db"):
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS Posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            text_content TEXT,
            image BLOB,
            created_at TEXT,
            updated_at TEXT,
            visibility TEXT
        )
    ''')

    sample_posts = [
        (1, "First post!", b"", datetime.now().isoformat(), datetime.now().isoformat(), "public"),
        (2, "Another stylish day.", b"", datetime.now().isoformat(), datetime.now().isoformat(), "friends-only"),
        (1, "Loving this new fit!", b"", datetime.now().isoformat(), datetime.now().isoformat(), "private"),
        (3, "Throwback outfit.", b"", datetime.now().isoformat(), datetime.now().isoformat(), "public"),
        (2, "Wardrobe goals.", b"", datetime.now().isoformat(), datetime.now().isoformat(), "public"),
    ]

    c.executemany('''
        INSERT INTO Posts (user_id, text_content, image, created_at, updated_at, visibility)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', sample_posts)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed_sample_posts()
