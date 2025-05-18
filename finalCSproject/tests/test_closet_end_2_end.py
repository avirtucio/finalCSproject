import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import sqlite3
import json
from models.Closets_Model import Closets_Model
from tests.sample_closet_data import sample_closets

DB_PATH = os.path.join(os.path.dirname(__file__), '../closetappDB.db')

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in PATH
    yield driver
    driver.quit()

def reset_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    Closets_Model.initialize_DB(DB_PATH)
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        for closet in sample_closets:
            c.execute("INSERT INTO closets (id, clothes_list, user_id) VALUES (?, ?, ?)", 
                      (closet["id"], json.dumps(closet["clothes_list"]), closet["user_id"]))
        conn.commit()

@pytest.fixture(autouse=True)
def run_before_tests():
    reset_db()
    yield

def test_list_closets(driver):
    driver.get("http://localhost:5000/closets")
    time.sleep(1)
    rows = driver.find_elements(By.TAG_NAME, "tr")
    assert len(rows) >= 6  # 5 closets + header

def test_view_closet(driver):
    driver.get("http://localhost:5000/closets/1")
    time.sleep(1)
    heading = driver.find_element(By.TAG_NAME, "h2").text
    assert "User ID: 1" in heading

def test_add_item(driver):
    driver.get("http://localhost:5000/closets/1")
    time.sleep(1)
    input_box = driver.find_element(By.ID, "clothes_id")
    input_box.send_keys("99")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()
    time.sleep(1)
    # After redirect, check if new clothes id is shown
    page_source = driver.page_source
    assert "99" in page_source
