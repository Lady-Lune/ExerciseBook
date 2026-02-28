from datetime import date, datetime, timezone
import scrapy


class EtsySpider(scrapy.Spider):
    name = "etsy-bitsy"
    start_urls = ["https://www.etsy.com/r/curated/etsys-best-vintage-finds?sections=1461029776888&narrow=best-vintage-finds"]

    def parse(self, response):
        grid_item = response.xpath('//li[@class="wt-list-unstyled wt-grid__item-xs-6 wt-grid__item-md-4 wt-grid__item-lg-3 wt-order-xs-0 wt-order-md-0 wt-order-lg-0 wt-show-xs wt-show-md wt-show-lg rlp-listing-grid__item"]')
        card_info = grid_item.xpath(".//div[contains(@class, 'v2-listing-card__info') and contains(@class, 'wt-pt-xs-0')]")
        for card in card_info:
            id = id = card.xpath(".//h3/@id").re(r"\d+$")[0]
            name = response.xpath(f'.//h3[contains(@id, "listing-title-{id}")]/text()').get().strip()
            price = card.xpath('.//span[contains(@class, "currency-value")]/text()').get()
            date = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
            self.logger.info(f"ID: {id}, Name: {name}")
            yield {"timestamp":date,"id": id, "name": name, "price": price}

# run " scrapy crawl etsy-bitsy -O listings.csv " to generate a csv file with the scraped data.
