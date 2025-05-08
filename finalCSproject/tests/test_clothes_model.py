import pytest
import os
from models.Clothes_Model import Clothes_Model
from tests.sample_clothes_data import sample_clothes

DB_PATH = "data/closetappDB.db"

@pytest.fixture(autouse=True)
def setup_and_teardown():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    Clothes_Model.initialize_DB(DB_PATH)
    for item in sample_clothes:
        Clothes_Model.create(item)
    yield

def test_clothes_exists():
    assert Clothes_Model.exists("Red T-Shirt")
    assert not Clothes_Model.exists("Nonexistent Item")

def test_create_clothes():
    new_item = {"name": "Wool Scarf", "type": "Accessory", "photo": None}
    created = Clothes_Model.create(new_item)
    assert created["id"] is not None
    assert Clothes_Model.exists("Wool Scarf")

def test_get_clothes():
    item = Clothes_Model.get_all()[0]
    fetched = Clothes_Model.get(item["id"])
    assert fetched["name"] == item["name"]

def test_get_all_clothes():
    all_items = Clothes_Model.get_all()
    assert len(all_items) == 5

def test_update_clothes():
    item = Clothes_Model.get_all()[1]
    item["name"] = "Ripped Blue Jeans"
    updated = Clothes_Model.update(item)
    assert updated["name"] == "Ripped Blue Jeans"

def test_remove_clothes():
    item = Clothes_Model.get_all()[2]
    Clothes_Model.remove(item["id"])
    assert not Clothes_Model.exists(item["id"])
