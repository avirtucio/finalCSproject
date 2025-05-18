import os
import pytest
from models.Clothes_Model import Clothes_Model
from tests.sample_clothes_data_function import seed_db

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'closetappDB.db')

@pytest.fixture(autouse=True)
def setup_and_teardown():
    seed_db(DB_PATH)
    yield

def test_get_all():
    clothes = Clothes_Model.get_all()
    assert len(clothes) == 5

def test_create():
    new_clothes = {'name': 'Yellow Scarf', 'type': 'Accessory', 'photo': None}
    Clothes_Model.create(new_clothes)
    clothes = Clothes_Model.get_all()
    assert any(c['name'] == 'Yellow Scarf' for c in clothes)

def test_exists():
    assert Clothes_Model.exists('Blue Jeans') is True
    assert Clothes_Model.exists('Nonexistent') is False

def test_get():
    jeans = Clothes_Model.get(1)
    assert jeans['name'] == 'Blue Jeans'

def test_update():
    jeans = Clothes_Model.get(1)
    jeans['name'] = 'Blue Denim Jeans'
    Clothes_Model.update(jeans)
    updated = Clothes_Model.get(1)
    assert updated['name'] == 'Blue Denim Jeans'

def test_remove():
    Clothes_Model.remove(1)
    clothes = Clothes_Model.get_all()
    assert not any(c['id'] == 1 for c in clothes)
