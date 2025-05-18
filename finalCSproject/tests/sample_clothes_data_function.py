import sqlite3

def seed_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS clothes')
    c.execute('''
        CREATE TABLE clothes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            photo BLOB
        )
    ''')
    sample_clothes = [
        ('Blue Jeans', 'Pants', None),
        ('Red T-Shirt', 'Shirt', None),
        ('Black Jacket', 'Jacket', None),
        ('White Sneakers', 'Shoes', None),
        ('Green Hat', 'Hat', None)
    ]
    c.executemany('INSERT INTO clothes (name, type, photo) VALUES (?, ?, ?)', sample_clothes)
    conn.commit()
    conn.close()
