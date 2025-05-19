import sqlite3
import json
from datetime import datetime

class Posts_Model:
    DB_PATH = "models/closetappDB.db"

    @classmethod
    def initialize_DB(cls, DB_NAME):
        cls.DB_PATH = DB_NAME
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    text_content TEXT,
                    image BLOB,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    visibility TEXT CHECK(visibility IN ('public', 'private', 'friends-only')) NOT NULL DEFAULT 'public',
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')
            conn.commit()

    @classmethod
    def exists(cls, id):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM posts WHERE id = ?", (id,))
            return cursor.fetchone() is not None

    @classmethod
    def create(cls, post_info):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO posts (user_id, text_content, image, created_at, updated_at, visibility)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                post_info['user_id'],
                post_info.get('text_content', ''),
                post_info.get('image'),
                post_info.get('created_at', datetime.now().isoformat()),
                post_info.get('updated_at', datetime.now().isoformat()),
                post_info.get('visibility', 'public')
            ))
            conn.commit()
            post_info['id'] = cursor.lastrowid
            return post_info

    @classmethod
    def get_post(cls, id):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM posts WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'user_id': row[1],
                    'text_content': row[2],
                    'image': row[3],
                    'created_at': row[4],
                    'updated_at': row[5],
                    'visibility': row[6]
                }
            return None

    @classmethod
    def get_all(cls):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM posts")
            rows = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'user_id': row[1],
                    'text_content': row[2],
                    'image': row[3],
                    'created_at': row[4],
                    'updated_at': row[5],
                    'visibility': row[6]
                }
                for row in rows
            ]
        
    @classmethod
    def update(cls, updated_post_info):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE posts
                SET text_content = ?, image = ?, visibility = ?
                WHERE id = ?
            """, (updated_post_info["text_content"], updated_post_info["image"], updated_post_info["visibility"], updated_post_info["id"]))
            conn.commit()
            return cls.get_post(updated_post_info["id"])

    @classmethod
    def delete(cls, id):
        post = cls.get_post(id)
        if not post:
            return None
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM posts WHERE id = ?", (id,))
            conn.commit()
        return post
