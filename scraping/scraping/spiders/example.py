import scrapy


class ExampleSpider(scrapy.Spider):
    name = "etsy-bitsy"
    allowed_domains = ["example..com"]
    start_urls = ["https://www.etsy.com/r/curated/etsys-best-vintage-finds?sections=1461029776888&narrow=best-vintage-finds"]

    def parse(self, response):
        grid_item = response.xpath('//li[@class="wt-list-unstyled wt-grid__item-xs-6 wt-grid__item-md-4 wt-grid__item-lg-3 wt-order-xs-0 wt-order-md-0 wt-order-lg-0 wt-show-xs wt-show-md wt-show-lg rlp-listing-grid__item"]')
        pass

