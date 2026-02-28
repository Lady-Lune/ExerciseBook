import scrapy
from scrapy import Selector


class PopflexReviewSpider(scrapy.Spider):
    name = "popflex-reviews"
    
    # url = "https://api.judge.me/reviews/reviews_for_widget?url=popflex.myshopify.com&shop_domain=popflex.myshopify.com&platform=shopify&page={PAGE}&per_page=6&product_id=7582857789523"

    custom_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Origin": "https://www.popflexactive.com",
        "Referer": "https://www.popflexactive.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "DNT": "1", 
        "Connection": "keep-alive",
    }

    def start_requests(self):

        url = f"https://api.judge.me/reviews/reviews_for_widget?url=popflex.myshopify.com&shop_domain=popflex.myshopify.com&platform=shopify&page=1&per_page=6&product_id=7582857789523"
        
        yield scrapy.Request(
            url=url,
            headers=self.custom_headers,
            callback=self.parse,
            meta={"page": 1}  # Track current page number
        )

    def parse(self, response):
        current_page = response.meta["page"]

        data = response.json()
        
        total_count = data.get("total_count", 0)
        html_content = data.get("html", "")
        self.logger.info(f"Page {current_page}: Found {total_count} total reviews")
        
        selector = Selector(text=html_content)
        
        reviews = selector.xpath("//div[@data-review-id]")
        
        for review in reviews:
            # Extract review details using XPath on the parsed HTML
            review_id = review.xpath("./@data-review-id").get()
            rating = review.xpath(".//span[@class='jdgm-rev__rating']/@data-score").get()
            timestamp = review.xpath(".//span[@class='jdgm-rev__timestamp']/@data-content").get()
            title = review.xpath(".//b[@class='jdgm-rev__title']/text()").get()
            body = review.xpath(".//div[@class='jdgm-rev__body']/p/text()").get()
            
            # Yield each review as a separate item
            yield {
                "review_id": review_id,
                "rating": int(rating) if rating else None,
                "timestamp": timestamp,
                "title": title.strip() if title else None,
                "body": body.strip() if body else None,
            }
        
        reviews_fetched_so_far = current_page * 6
        
        if reviews_fetched_so_far < total_count:
            next_page = current_page + 1
     
            next_url = f"https://api.judge.me/reviews/reviews_for_widget?url=popflex.myshopify.com&shop_domain=popflex.myshopify.com&platform=shopify&page={next_page}&per_page=6&product_id=7582857789523"
            yield scrapy.Request(
                url=next_url,
                headers=self.custom_headers,
                callback=self.parse,
                meta={"page": next_page}
            )
        else:
            self.logger.info(f"Finished! Scraped all {total_count} reviews.")

#   scrapy crawl popflex-reviews -O reviews.jl       # JSON Lines output
# To limit pages for testing, add: -s CLOSESPIDER_PAGECOUNT=10
