import scrapy
from urllib.parse import urljoin

class ScrapyPlaywrightJsScroll(scrapy.Spider):
    name = "spider"
    
    base_url = "https://ecstasybd.com/"
    start_urls = [
        "https://ecstasybd.com/?page=product-list&sid=18&p=1&type="
    ]
    

    def parse(self, response):
        all_page_links = response.css(".pagination-box a::attr(href)").getall()

        for page_link in all_page_links:
            full_page_link = urljoin(self.base_url, page_link)

            yield scrapy.Request(
                url = full_page_link,
                callback = self.extract_product_links
            )

        
    def extract_product_links(self, response):
        # Extract all partial URLs
        product_links = response.css("div.product-item a::attr(href)").getall()
        
        for link in product_links:
            
            # checking if the link is product link
            if "pid" in link:

                # convert relative url -> full url
                full_url = urljoin(self.base_url, link) 

                # send new request
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_product
                )

    def parse_product(self, response):
        # Extract data from each product page
        yield {
            "product_name" : response.css("h3.product-name::text").get(),
            "regular_price" : response.css(".price-regular.price-details::text").get(),
            "info_guide" : response.css("div#tab_oness div.tab-one p::text").getall(),
            "available_size" : response.css("div#tab_oness tr td:nth-child(2)::text").get(), 
            "availability" : response.css(".product-att.availability::text").get(),
            "sku" : response.css(".product-att.sku::text").get(),
            "PID" : response.css(".pid-container .product-att.sku::text").get()
        }