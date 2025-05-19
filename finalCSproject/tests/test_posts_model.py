import pytest
import sqlite3
from datetime import datetime
from models.Posts_Model import Posts_Model
from tests.sample_posts_data import seed_sample_posts

DB_NAME = "models/closetappDB.db"

@pytest.fixture(autouse=True)
def run_before_tests():
    seed_sample_posts()
    Posts_Model.initialize_DB(DB_NAME)

class TestPostsModel:
    def test_exists_true(self):
        assert Posts_Model.exists(1) == True

    def test_exists_false(self):
        assert Posts_Model.exists(999) == False

    def test_create_post(self):
        new_post = {
            "user_id": 4,
            "text_content": "New vibes.",
            "image": b"",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "visibility": "public"
        }
        created = Posts_Model.create(new_post)
        assert created["user_id"] == 4
        assert created["text_content"] == "New vibes."
        assert Posts_Model.exists(created["id"]) == True

    def test_get_post(self):
        post = Posts_Model.get_post(2)
        assert post["id"] == 2
        assert post["text_content"] == "Another stylish day."

    def test_get_post_not_found(self):
        assert Posts_Model.get_post(999) == None

    def test_get_all(self):
        posts = Posts_Model.get_all()
        assert len(posts) == 5

    def test_delete_post(self):
        deleted = Posts_Model.delete(3)
        assert deleted["id"] == 3
        assert Posts_Model.exists(3) == False
