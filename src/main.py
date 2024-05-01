from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import os

def main(event, context):
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

    driver = Chrome("/opt/chromedriver", options=opts)
    driver.get("www.google.com")
    title = driver.title

    driver.close()
    driver.quit()

    response = {
        "statusCode": 200,
        "body": title
    }

    return response

