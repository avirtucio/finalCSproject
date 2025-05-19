import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import sqlite3
import time
import json

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'closetappDB.db')
SEED_DATA_PATH = os.path.join(os.path.dirname(__file__), 'sample_outfits_data.py')
BASE_URL = "http://localhost:5000"

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run headless Chrome
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def reset_database():
    # Clear and reseed the database with sample data before tests
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Clear outfits table
    c.execute("DELETE FROM outfits;")
    conn.commit()
    # Insert sample outfits from sample_outfits_data.py
    from tests.sample_outfits_data import sample_outfits
    for outfit in sample_outfits:
        clothes_list_json = json.dumps(outfit['clothes_list'])
        c.execute(
            "INSERT INTO outfits (id, name, user_id, clothes_list) VALUES (?, ?, ?, ?);",
            (outfit['id'], outfit['name'], outfit['user_id'], clothes_list_json)
        )
    conn.commit()
    conn.close()

@pytest.fixture(autouse=True)
def setup_and_teardown():
    reset_database()
    yield
    # Optionally reset or cleanup after test

def test_outfits_index_page(driver):
    driver.get(f"{BASE_URL}/outfits")
    assert "Outfits" in driver.title or "Outfits" in driver.page_source
    # Check that at least one outfit is listed
    outfits = driver.find_elements(By.CSS_SELECTOR, ".outfit-item")
    assert len(outfits) >= 1

def test_create_new_outfit(driver):
    driver.get(f"{BASE_URL}/outfits/create")
    # Fill in form
    name_input = driver.find_element(By.NAME, "name")
    user_id_input = driver.find_element(By.NAME, "user_id")
    clothes_list_input = driver.find_element(By.NAME, "clothes_list")
    
    name_input.send_keys("Test Outfit")
    user_id_input.send_keys("1")
    # Example clothes ids json list
    clothes_list_input.send_keys('[1,2,3]')
    
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    
    # Wait for redirect
    WebDriverWait(driver, 5).until(EC.url_contains("/outfits"))
    # Check new outfit in list
    page_source = driver.page_source
    assert "Test Outfit" in page_source

def test_view_outfit_details(driver):
    # Assume outfit with id=1 exists (from seeded data)
    driver.get(f"{BASE_URL}/outfits/1")
    assert "Outfit Details" in driver.page_source or "1" in driver.page_source
    assert "Clothes List" in driver.page_source

def test_edit_outfit(driver):
    # Navigate to edit page for outfit with id=1
    driver.get(f"{BASE_URL}/outfits/1/edit")
    
    name_input = driver.find_element(By.NAME, "name")
    name_input.clear()
    name_input.send_keys("Updated Outfit Name")
    
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    
    WebDriverWait(driver, 5).until(EC.url_contains("/outfits/1"))
    assert "Updated Outfit Name" in driver.page_source

def test_delete_outfit(driver):
    # Navigate to outfits list page
    driver.get(f"{BASE_URL}/outfits")
    
    # Find delete button/link for outfit with id=1 - assuming it has data-id or similar attribute
    delete_button = driver.find_element(By.CSS_SELECTOR, "button.delete-outfit[data-id='1']")
    delete_button.click()
    
    # Confirm alert if any (handle JS alert)
    try:
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass
    
    time.sleep(1)  # Wait for deletion
    
    # Refresh outfits page
    driver.get(f"{BASE_URL}/outfits")
    page_source = driver.page_source
    assert "Updated Outfit Name" not in page_source
