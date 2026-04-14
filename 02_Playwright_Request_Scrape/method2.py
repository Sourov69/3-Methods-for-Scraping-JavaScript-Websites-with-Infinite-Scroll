# Direct Fetching & Saving Json Response Data
import time
import random
import json
from playwright.sync_api import sync_playwright


base_url = "https://www.cricbuzz.com/api/mcenter/commentary-pagination/122687/"

all_data = {}   #  this will store everything

def handle_response(response):
    global all_data

    if "api" in response.url:
        responsive_url = response.url

        if responsive_url.startswith(base_url):
            try:
                if response.status == 200:
                    data = response.json()

                    # 🔥 create index automatically
                    index = len(all_data)

                    all_data[index] = {
                        "url": response.url,
                        "data": data
                    }

                    print(f"Stored: {index} -> {response.url}")

            except Exception as e:
                print("Error:", e)

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

with open("playwright_direct_json_fetch.json", "w") as f:
    json.dump(all_data, f)