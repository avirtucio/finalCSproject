import pytest
import os
from models.User_Model import User_Model
from tests.sample_user_data import sample_users

DB_PATH = "models/closetappDB.db"

@pytest.fixture(autouse=True)
def setup_and_teardown():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    User_Model.initialize_DB(DB_PATH)
    for user in sample_users:
        User_Model.create(user)
    yield

def test_user_exists():
    assert User_Model.exists("alice")
    assert not User_Model.exists("nonexistent")

def test_create_user():
    new_user = {"username": "frank", "email": "frank@example.com", "password": "frank123"}
    created_user = User_Model.create(new_user)
    assert created_user["id"] is not None
    assert User_Model.exists("frank")

def test_get_user():
    user = User_Model.get("bob")
    assert user["username"] == "bob"
    user_by_id = User_Model.get(user["id"])
    assert user_by_id["username"] == "bob"

def test_get_all():
    users = User_Model.get_all()
    assert len(users) == 5

def test_update_user():
    user = User_Model.get("charlie")
    user["email"] = "newcharlie@example.com"
    updated_user = User_Model.update(user)
    assert updated_user["email"] == "newcharlie@example.com"

def test_remove_user():
    User_Model.remove("diana")
    assert not User_Model.exists("diana")
