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

    driver.close()
    driver.quit()

    future_data = {}
    with ProcessPoolExecutor(max_workers=10) as executor: 
        
        for page in range(1, n_pages + 1):
            driver = get_chrome_driver()
            driver.get("https://linkedin.com/feed")
            for cookie in cookies:
                print("Addugb cookie ...", cookie)
                driver.add_cookie(cookie)
            fut = executor.submit(search_keywords_with_url, (keywords, driver, page), )
            future_data[fut] = page
            
        for future in as_completed(future_data):
            page_number = future_data[future]
            try:
                data = future.result()
                print("Page numebr ", page_number, " => ", data)
            except Exception as e:
                print('%r generated an exception: %s' % (page_number, e))
            


    # search_keywords(keywords, driver)
    # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    # time.sleep(5)
    # page_source = driver.page_source
    page_source = ""

    return {
        "statusCode": 200,
        "body": json.dumps({"data": page_source}),
        "headers": {
            "Content-Type": "application/json"
        }
    }


    
