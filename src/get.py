from chrome import get_chrome_driver
import json


def method_GET(event, context):
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
    driver = get_chrome_driver()
    driver.get(url_to_fetch)
    body = driver.page_source

    driver.close()
    driver.quit()

    response = {
        "statusCode": 200,
        "body": body,
        "headers": {
            "Content-Type": "text/html; charset=UTF-8"
        }
    }

    return response