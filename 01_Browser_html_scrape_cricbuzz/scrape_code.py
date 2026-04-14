import random
import time

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.cricbuzz.com/live-cricket-scores/122687/nz-vs-rsa-1st-t20i-south-africa-tour-of-new-zealand-2026")
    page.wait_for_timeout(3000)
    
    previous_height = 0

    previous_height = 0


    for _ in range(70):
        scrool_amount = random.randint(200, 600)
        page.mouse.wheel(0, scrool_amount)
        time.sleep(random.uniform(0.5, 2))
    html = page.content()

    with open("page.html", "w", encoding="utf-8") as f:
        f.write(html)
    browser.close()