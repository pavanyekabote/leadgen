from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time 
import json
import re
from urllib.parse import quote
import db

def login_linkedin(data, driver):
    print("Initializing login with usn and pwd")
    usn = data.get("username")
    pwd = data.get("password")
    print(f"Logging in user {usn}")
    input_usn = driver.find_element(By.ID, "username")
    input_pwd = driver.find_element(By.ID, "password")
    form_button = driver.find_element(By.CSS_SELECTOR, ".login__form .login__form_action_container button.from__button--floating")

    time.sleep(2)
    input_usn.send_keys(usn)
    input_pwd.send_keys(pwd)
    form_button.click()
    print(f"Login seems to be successfull, saving cookies of user ...{usn}")
    time.sleep(3)

    db.save_login_details({"user": usn, "login_with": "username_password", "platform": "linkedin"})
    save_cookies(usn, driver.get_cookies())


def save_cookies(user, driver):
    print("Saving cookies to disk...")
    cookies = driver.get_cookies()
    data = {"user": user, "cookies": cookies}
    db.save_cookies(data)

# browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")


def refresh_homepage(driver):
    print("Refresh homepage ...")
    driver.get("https://www.linkedin.com/feed/")

def is_this_login_page(driver):
    print("Checkin login page ...")
    current_url = driver.execute_script("return window.location.href")
    if 'login' in current_url:
        print("Login required")
        return True
    print("No need of login")
    return False

def load_cookies(cookies, driver):
    print("Loading cookies...")
    for cookie in cookies:
        driver.add_cookie(cookie)

def search_keywords(keywords, driver: webdriver.Chrome):
    print("Searching for keywords :: " + keywords + "")
    search_input = find_element(driver, By.CSS_SELECTOR, "#global-nav #global-nav-typeahead input.search-global-typeahead__input")
    search_input.send_keys(keywords)
    search_input.send_keys(Keys.ENTER)
    time.sleep(10)

class ReplacerObject:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def find_element(element, by, selector):
    try:
        return element.find_element(by, selector)
    except Exception as e:
        pass
    replacer = ReplacerObject(**{'text': None, 'get_attribute': lambda x: None})
    return replacer

def find_elements(element, by, selector):
    try:
        return element.find_elements(by, selector)
    except Exception as e:
        pass
    return []
