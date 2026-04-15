# Fetching Headers & Cookies using Playwright and Collect data using request passing url fetched by Playwright.
import time
import random
from playwright.sync_api import sync_playwright

base_url = "https://www.cricbuzz.com/api/mcenter/commentary-pagination/122687/"

def handle_request(response):
    if "api" in response.url:
        responsesive_url = response.url       
        if responsesive_url.startswith(base_url):
            print("Headers: ", response.headers)
            


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.on("request", handle_request)
    page.goto("https://www.cricbuzz.com/live-cricket-scores/122687/nz-vs-rsa-1st-t20i-south-africa-tour-of-new-zealand-2026")
    page.wait_for_timeout(3000)

    for _ in range(20):
        scrool_amount = random.randint(200, 600)
        page.mouse.wheel(0, scrool_amount)
        time.sleep(random.uniform(0.5, 2))

    cookies = context.cookies()
    print("cookies :")

    for c in cookies:
        print(c)


# From the output we get
headers = {
    'user-agent' : "'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'",
    'content-type' : "application/json',"
}

cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}

# # apply to 
# import requests
# response = requests.get(url, headers=headers, cookies=cookies_dict)
# response.json()