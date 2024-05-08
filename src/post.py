from linkedin_login import login_linkedin, search_keywords, search_keywords_with_url, load_cookies
from chrome import get_chrome_driver
import time
import json
from multiprocessing import Process
from concurrent.futures import ProcessPoolExecutor, as_completed
from db import get_user_cookies

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
    # login_linkedin({
    #     "username": user,
    #     "password": password,
    #     "keywords": keywords,
    #     "platform": platform
    # }, driver)

    n_pages = 10
    n_items_per_page = 10
    cookies = (get_user_cookies({"user": "yekabotep@gmail.com"}) or {}).get("cookies", [])
    print("Cokies ", cookies)
    load_cookies(cookies, driver)

    posts = search_keywords_with_url(keywords, driver, page=page_number)
    # search_keywords(keywords, driver)
    # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    # time.sleep(5)
    print("POSTS ", posts)
    page_source = driver.page_source
    # page_source = ""
    print("PAGE SOURCE :: ", page_source)
    driver.close()
    driver.quit()

    return {
        "statusCode": 200,
        "body": page_source, # json.dumps({"data": page_source}),
        "headers": {
            "Content-Type": "text/html"
        }
    }


    
