import sqlite3
import json
import os

class Closets_Model:
    DB_PATH = None

    def __init__(self, db_name):
        self.DB_PATH = os.path.join(os.path.dirname(__file__), db_name)
        self.initialize_DB()

    def initialize_DB(self):
        with sqlite3.connect(self.DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS closets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    clothes_list TEXT DEFAULT '[]',
                    user_id INTEGER UNIQUE,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            conn.commit()

    def exists(self, *, user_id=None, closet_id=None):
        with sqlite3.connect(self.DB_PATH) as conn:
            c = conn.cursor()
            if user_id is not None:
                c.execute('SELECT 1 FROM closets WHERE user_id = ?', (user_id,))
            elif closet_id is not None:
                c.execute('SELECT 1 FROM closets WHERE id = ?', (closet_id,))
            else:
                return False
            return c.fetchone() is not None

    def add_item(self, user_id, clothes_id):
        with sqlite3.connect(self.DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT clothes_list FROM closets WHERE user_id = ?', (user_id,))
            row = c.fetchone()
            if not row:
                raise ValueError(f"No closet found for user_id {user_id}")

            clothes_list = json.loads(row[0])
            if clothes_id not in clothes_list:
                clothes_list.append(clothes_id)
                c.execute('UPDATE closets SET clothes_list = ? WHERE user_id = ?',
                          (json.dumps(clothes_list), user_id))
                conn.commit()
            return self.get_user_closet(user_id)

    def get_user_closet(self, user_id):
        with sqlite3.connect(self.DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT id, clothes_list, user_id FROM closets WHERE user_id = ?', (user_id,))
            row = c.fetchone()
            if row:
                return {
                    "id": row[0],
                    "clothes_list": json.loads(row[1]),
                    "user_id": row[2]
                }
            else:
                return None

    def get_all(self):
        with sqlite3.connect(self.DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT id, clothes_list, user_id FROM closets')
            rows = c.fetchall()
            closets = []
            for row in rows:
                closets.append({
                    "id": row[0],
                    "clothes_list": json.loads(row[1]),
                    "user_id": row[2]
                })
            return closets
