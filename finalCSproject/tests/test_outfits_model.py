import os
import sqlite3
import pytest
from models.Outfits_Model import Outfits_Model
from tests.sample_outfits_data import sample_outfits

DB_NAME = "models/closetappDB.db"

def clear_and_seed():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS outfits")
    Outfits_Model.initialize_DB(DB_NAME)

    for outfit in sample_outfits:
        cursor.execute('''INSERT INTO outfits (id, name, user_id, clothes_list)
                          VALUES (?, ?, ?, ?)''',
                       (outfit["id"], outfit["name"], outfit["user_id"], outfit["clothes_list"]))

    conn.commit()
    conn.close()

@pytest.fixture(autouse=True)
def run_before_tests():
    clear_and_seed()

# Test exists
@pytest.mark.parametrize("query, expected", [
    (1, True),
    ("Summer Vibes", True),
    ("Nonexistent", False),
    (99, False)
])
def test_exists(query, expected):
    assert Outfits_Model.exists(query) == expected

# Test get_outfit
@pytest.mark.parametrize("query", [1, "Office Look"])
def test_get_outfit(query):
    outfit = Outfits_Model.get_outfit(query)
    assert outfit is not None
    assert "id" in outfit and "name" in outfit

# Test get_all
def test_get_all():
    all_outfits = Outfits_Model.get_all()
    assert len(all_outfits) == 5

# Test get_all_user_outfits
@pytest.mark.parametrize("user_query, expected_count", [(101, 2), (102, 2), (103, 1)])
def test_get_all_user_outfits(user_query, expected_count):
    outfits = Outfits_Model.get_all_user_outfits(user_query)
    assert len(outfits) == expected_count

# Test create
def test_create():
    new_outfit = {
        "name": "Chill Sunday",
        "user_id": 104,
        "clothes_list": "[15, 16]"
    }
    created = Outfits_Model.create(new_outfit)
    assert created is not None
    assert created["name"] == new_outfit["name"]

# Test remove
def test_remove():
    removed = Outfits_Model.remove(1)
    assert removed is not None
    assert removed["id"] == 1
    assert Outfits_Model.exists(1) is False