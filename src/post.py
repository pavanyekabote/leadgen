from linkedin_login import login_linkedin, search_keywords, search_keywords_with_url
from chrome import get_chrome_driver
import time
import json
from multiprocessing import Process
from concurrent.futures import ProcessPoolExecutor, as_completed


def method_POST(event, context):

    body = json.loads(event.get("body", "{}") or "{}")
    platform = body.get("platform")
    user = body.get("username")
    password = body.get("password")
    keywords = body.get("keywords")
    page_number = int(body.get("pageNumber", 1))

    driver = get_chrome_driver()

    driver.get("https://www.linkedin.com/uas/login")
    time.sleep(2)
    login_linkedin({
        "username": user,
        "password": password,
        "keywords": keywords,
        "platform": platform
    }, driver)

    n_pages = 10
    n_items_per_page = 10
    cookies = driver.get_cookies()
    print("Cokies ", cookies)
    posts = search_keywords_with_url(keywords, driver, page=page_number)
    time.sleep(3)
    # search_keywords(keywords, driver)
    # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    # time.sleep(5)
    page_source = driver.page_source
    # page_source = ""
    driver.close()
    driver.quit()

    return {
        "statusCode": 200,
        "body": page_source, # json.dumps({"data": page_source}),
        "headers": {
            "Content-Type": "text/html"
        }
    }


    
