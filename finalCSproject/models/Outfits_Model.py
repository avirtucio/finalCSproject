import sqlite3
import json

class Outfits_Model:
    DB_PATH = "models/closetappDB.db"

    @classmethod
    def initialize_DB(cls, DB_NAME):
        cls.DB_PATH = DB_NAME
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS outfits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    clothes_list TEXT NOT NULL
                )
            ''')
            conn.commit()

    @classmethod
    def exists(cls, outfit_name=None, id=None):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            if id is not None:
                cursor.execute("SELECT 1 FROM outfits WHERE id = ?", (id,))
            elif outfit_name is not None:
                cursor.execute("SELECT 1 FROM outfits WHERE name = ?", (outfit_name,))
            else:
                return False
            return cursor.fetchone() is not None

    @classmethod
    def create(cls, outfit_info):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO outfits (name, user_id, clothes_list)
                VALUES (?, ?, ?)
            ''', (
                outfit_info['name'],
                outfit_info['user_id'],
                json.dumps(outfit_info['clothes_list'])
            ))
            conn.commit()
            outfit_info['id'] = cursor.lastrowid
            return outfit_info

    @classmethod
    def get_outfit(cls, outfit_name=None, id=None):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            if id is not None:
                cursor.execute("SELECT * FROM outfits WHERE id = ?", (id,))
            elif outfit_name is not None:
                cursor.execute("SELECT * FROM outfits WHERE name = ?", (outfit_name,))
            else:
                return None
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'name': row[1],
                    'user_id': row[2],
                    'clothes_list': json.loads(row[3])
                }
            return None

    @classmethod
    def get_all(cls):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM outfits")
            rows = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'name': row[1],
                    'user_id': row[2],
                    'clothes_list': json.loads(row[3])
                } for row in rows
            ]

    @classmethod
    def get_all_user_outfits(cls, username=None, user_id=None):
        if user_id is None:
            raise ValueError("user_id is required")
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM outfits WHERE user_id = ?", (user_id,))
            rows = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'name': row[1],
                    'user_id': row[2],
                    'clothes_list': json.loads(row[3])
                } for row in rows
            ]

    @classmethod
    def remove(cls, id):
        outfit = cls.get_outfit(id=id)
        if not outfit:
            return None
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM outfits WHERE id = ?", (id,))
            conn.commit()
        return outfit
