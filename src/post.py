from linkedin_login import login_linkedin, search_keywords
from chrome import get_chrome_driver
import time
import json

def method_POST(event, context):

    body = event.get("body", {}) or {}
    platform = body.get("platform")
    user = body.get("username")
    password = body.get("password")
    keywords = body.get("keywords")

    driver = get_chrome_driver()

    login_linkedin({
        "username": user,
        "password": password,
        "keywords": keywords,
        "platform": platform
    }, driver)

    search_keywords(keywords, driver)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)
    page_source = driver.page_source

    return {
        "statusCode": 200,
        "body": json.dumps({"data": page_source}),
        "headers": {
            "Content-Type": "application/json"
        }
    }


    
