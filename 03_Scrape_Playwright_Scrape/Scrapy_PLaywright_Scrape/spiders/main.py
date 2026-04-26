import scrapy
from urllib.parse import urljoin

class ScrapyPlaywrightJsScroll(scrapy.Spider):
    name = "spider"
    
    base_url = "https://ecstasybd.com/"
    start_urls = [
        "https://ecstasybd.com/?page=product-list&sid=18&p=1&type="
    ]
    

      
    def parse(self, response):
        #  Extract products from first page
        yield from self.extract_product_links(response)

        #  Handle pagination (remove duplicates)
        all_page_links = set(response.css(".pagination-box a::attr(href)").getall())

        for page_link in all_page_links:
            full_page_link = response.urljoin(page_link)

            yield scrapy.Request(
                url=full_page_link,
                callback=self.extract_product_links
            )

    def extract_product_links(self, response):
        product_links = response.css("div.product-item a::attr(href)").getall()
        
        for link in product_links:
            if "pid=" in link:
                full_url = response.urljoin(link)
                
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_product
                )

    def parse_product(self, response):
        # Extract data from each product page
        yield {
            "product_name": response.css("h3.product-name::text").get(default="").strip(),

            "regular_price": response.css(".price-regular.price-details::text").get(default="").strip(),

            "info_guide": [
                text.strip()
                for text in response.css("div#tab_oness div.tab-one p::text").getall()
                if text.strip()
            ],

            "available_size": response.css("div#tab_oness tr td:nth-child(2)::text").get(default="").strip(),

            "availability": response.css(".product-att.availability::text").get(default="").strip(),

            "sku": response.css(".product-att.sku::text").get(default="").strip(),

            "PID": response.css(".pid-container .product-att.sku::text").get(default="").strip()
        }