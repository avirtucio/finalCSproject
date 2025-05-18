import os
import pytest
import sqlite3
import json
from models.Closets_Model import Closets_Model

DB_NAME = "closetappDB.db"

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    # Remove old DB file if exists
    if os.path.exists(os.path.join("models", DB_NAME)):
        os.remove(os.path.join("models", DB_NAME))

    # Initialize and seed closets table with sample data
    closets_model = Closets_Model(DB_NAME)
    conn = sqlite3.connect(os.path.join("models", DB_NAME))
    c = conn.cursor()

    # Create users table (minimal for FK)
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT,
            password TEXT
        )
    ''')

    # Seed users to match closet user_ids
    c.executemany('INSERT INTO users (id, username, email, password) VALUES (?, ?, ?, ?)', [
        (1, 'user1', 'user1@example.com', 'pass1'),
        (2, 'user2', 'user2@example.com', 'pass2'),
        (3, 'user3', 'user3@example.com', 'pass3'),
        (4, 'user4', 'user4@example.com', 'pass4'),
        (5, 'user5', 'user5@example.com', 'pass5'),
    ])

    # Seed closets table
    from tests.sample_closet_data import sample_closets
    c.executemany('INSERT INTO closets (id, clothes_list, user_id) VALUES (?, ?, ?)',
                  [(c["id"], c["clothes_list"], c["user_id"]) for c in sample_closets])

    conn.commit()
    yield
    conn.close()
    if os.path.exists(os.path.join("models", DB_NAME)):
        os.remove(os.path.join("models", DB_NAME))

def test_exists():
    cm = Closets_Model(DB_NAME)
    assert cm.exists(user_id=1) is True
    assert cm.exists(closet_id=2) is True
    assert cm.exists(user_id=999) is False

def test_get_user_closet():
    cm = Closets_Model(DB_NAME)
    closet = cm.get_user_closet(1)
    assert closet["user_id"] == 1
    assert isinstance(closet["clothes_list"], list)

def test_add_item():
    cm = Closets_Model(DB_NAME)
    closet_before = cm.get_user_closet(2)
    assert closet_before["clothes_list"] == []

    updated_closet = cm.add_item(2, 42)
    assert 42 in updated_closet["clothes_list"]

def test_get_all():
    cm = Closets_Model(DB_NAME)
    closets = cm.get_all()
    assert len(closets) == 5
