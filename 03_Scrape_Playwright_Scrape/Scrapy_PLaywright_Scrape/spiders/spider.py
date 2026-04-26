import scrapy
import random
import asyncio

class ScrapyPlaywrightJsScroll(scrapy.Spider):
    name = "spider1"

    def start_requests(self):
        yield scrapy.Request(
            "https://www.cricbuzz.com/live-cricket-scores/122687/nz-vs-rsa-1st-t20i-south-africa-tour-of-new-zealand-2026",
            meta={
                "playwright": True,
                "playwright_include_page": True
            },
            callback=self.parse
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        # wait for page load
        await page.wait_for_timeout(3000)

        # scrolling
        for _ in range(65):  # reduced
            scroll_amount = random.randint(200, 600)
            await page.mouse.wheel(0, scroll_amount)
            await asyncio.sleep(random.uniform(0.5, 2))

        html = await page.content()

        with open("cricbuzz.html", "w", encoding="utf-8") as f:
            f.write(html)

        await page.close()

        yield {"html": html}