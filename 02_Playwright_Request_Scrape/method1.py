import time
import random
import json
from playwright.sync_api import sync_playwright

base_url = "https://www.cricbuzz.com/api/mcenter/commentary-pagination/122687/"

api_urls = []

def handle_response(response):
    if "api" in response.url:
        responsesive_url = response.url       
        if responsesive_url.startswith(base_url):
            print("API: ", responsesive_url)
            api_urls.append(responsesive_url)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    page.on("response", handle_response)
    page.goto("https://www.cricbuzz.com/live-cricket-scores/122687/nz-vs-rsa-1st-t20i-south-africa-tour-of-new-zealand-2026")
    page.wait_for_timeout(3000)

    # Scroll multiple times
    for _ in range(65):
        scrool_amount = random.randint(200, 600)
        page.mouse.wheel(0, scrool_amount)
        time.sleep(random.uniform(0.5, 2))
    html = page.content()
    browser.close()

api_urls_json = {}
for i in range(0, len(api_urls)):
    api_urls_json[i] = api_urls[i]

with open("urls_links.json", "w") as f:
    json.dump(api_urls_json, f)


print(api_urls_json)

