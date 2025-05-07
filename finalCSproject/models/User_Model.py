import sqlite3

class User_Model: #tetstees
    DB_PATH = "models/closetappDB.db"

    @classmethod
    def initialize_DB(cls, DB_name):
        cls.DB_PATH = DB_name
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )''')
            conn.commit()

    @classmethod
    def exists(cls, identifier):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            if isinstance(identifier, int):
                cursor.execute("SELECT 1 FROM users WHERE id=?", (identifier,))
            else:
                cursor.execute("SELECT 1 FROM users WHERE username=?", (identifier,))
            return cursor.fetchone() is not None

    @classmethod
    def create(cls, user_info):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
            """, (user_info["username"], user_info["email"], user_info["password"]))
            conn.commit()
            user_info["id"] = cursor.lastrowid
            return user_info

    @classmethod
    def get(cls, identifier):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            if isinstance(identifier, int):
                cursor.execute("SELECT * FROM users WHERE id=?", (identifier,))
            else:
                cursor.execute("SELECT * FROM users WHERE username=?", (identifier,))
            row = cursor.fetchone()
            if row:
                return {"id": row[0], "username": row[1], "email": row[2], "password": row[3]}
            return None

    @classmethod
    def get_all(cls):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            return [
                {"id": row[0], "username": row[1], "email": row[2], "password": row[3]}
                for row in rows
            ]

    @classmethod
    def update(cls, user_info):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users
                SET username = ?, email = ?, password = ?
                WHERE id = ?
            """, (user_info["username"], user_info["email"], user_info["password"], user_info["id"]))
            conn.commit()
            return cls.get(user_info["id"])

    @classmethod
    def remove(cls, username):
        with sqlite3.connect(cls.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE username=?", (username,))
            conn.commit()
