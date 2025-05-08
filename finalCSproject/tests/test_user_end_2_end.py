import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from tests.sample_user_data import sample_users
from models.User_Model import User_Model

BASE_URL = "http://localhost:5000/users"

@pytest.fixture(scope="module")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture(autouse=True)
def reset_database():
    User_Model.initialize_DB("closetappDB.db")
    for user in User_Model.get_all():
        User_Model.remove(user['username'])
    for u in sample_users:
        User_Model.create(u)

def test_user_index_page(browser):
    browser.get(BASE_URL)
    time.sleep(1)
    usernames = [elem.text for elem in browser.find_elements(By.TAG_NAME, "a") if elem.text]
    for u in sample_users:
        assert u['username'] in usernames

def test_create_user(browser):
    browser.get(f"{BASE_URL}/create")
    time.sleep(1)
    browser.find_element(By.NAME, "username").send_keys("selenium_user")
    browser.find_element(By.NAME, "email").send_keys("selenium@test.com")
    browser.find_element(By.NAME, "password").send_keys("pass1234")
    browser.find_element(By.TAG_NAME, "form").submit()
    time.sleep(1)
    assert "selenium_user" in browser.page_source

def test_view_user_details(browser):
    browser.get(BASE_URL)
    browser.find_element(By.LINK_TEXT, sample_users[0]['username']).click()
    time.sleep(1)
    assert sample_users[0]['email'] in browser.page_source

def test_edit_user(browser):
    browser.get(BASE_URL)
    edit_links = browser.find_elements(By.LINK_TEXT, "Edit")
    edit_links[0].click()
    time.sleep(1)
    username_input = browser.find_element(By.NAME, "username")
    username_input.clear()
    username_input.send_keys("updated_user")
    browser.find_element(By.TAG_NAME, "form").submit()
    time.sleep(1)
    assert "updated_user" in browser.page_source
