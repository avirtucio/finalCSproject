import sqlite3
import os

class Clothes_Model:
    DB_PATH = "data/closetappDB.db"

    @classmethod
    def initialize_DB(cls, DB_name):
        cls.DB_PATH = DB_name
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS clothes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                photo BLOB
            )''')
            conn.commit()

    @classmethod
    def exists(cls, identifier):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            if isinstance(identifier, int):
                cursor.execute("SELECT 1 FROM clothes WHERE id=?", (identifier,))
            else:
                cursor.execute("SELECT 1 FROM clothes WHERE name=?", (identifier,))
            return cursor.fetchone() is not None

    @classmethod
    def create(cls, clothes_info):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO clothes (name, type, photo) VALUES (?, ?, ?)",
                (clothes_info["name"], clothes_info["type"], clothes_info.get("photo"))
            )
            conn.commit()
            clothes_info["id"] = cursor.lastrowid
            return clothes_info

    @classmethod
    def get(cls, id):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clothes WHERE id=?", (id,))
            row = cursor.fetchone()
            if row:
                return {"id": row[0], "name": row[1], "type": row[2], "photo": row[3]}
            return None

    @classmethod
    def get_all(cls):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clothes")
            rows = cursor.fetchall()
            return [
                {"id": row[0], "name": row[1], "type": row[2], "photo": row[3]}
                for row in rows
            ]

    @classmethod
    def update(cls, clothes_info):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE clothes SET name = ?, type = ?, photo = ? WHERE id = ?",
                (clothes_info["name"], clothes_info["type"], clothes_info.get("photo"), clothes_info["id"])
            )
            conn.commit()
            return cls.get(clothes_info["id"])

    @classmethod
    def remove(cls, id):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clothes WHERE id=?", (id,))
            conn.commit()
