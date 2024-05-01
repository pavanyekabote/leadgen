from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import os
import json

def main(event, context):
    print("Event is ", event)
    query_params = event.get("queryStringParameters", {}) or {}
    url_to_fetch = query_params.get("url")
    if not url_to_fetch and url_to_fetch == "":
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid url, can't be empty!"}),
            "headers": {
                "Content-Type": "application/json"
            }
        }
    print("Request for URL is ", url_to_fetch)
    print("OS PATH LS :: /opt :: ", os.listdir("/opt"))
    opts = Options()
    opts.binary_location = "/opt/headless-chromium"
    opts.add_argument("--headless")
    opts.add_argument("--no-zygote")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-setuid-sandbox")
    opts.add_argument("--start-maximized") 
    opts.add_argument("--start-fullscreen") 
    opts.add_argument("--single-process")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--ignore-certificate-errors")

    driver = Chrome(executable_path="/opt/chromedriver", options=opts)
    driver.get(url_to_fetch)
    body = driver.page_source

    driver.close()
    driver.quit()

    response = {
        "statusCode": 200,
        "body": body,
        "headers": {
            "Content-Type": "application/html"
        }
    }

    return response

