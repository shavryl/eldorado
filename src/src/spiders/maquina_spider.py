from scrapy import Spider
from scrapy.selector import Selector
from ..constants import LINKS


class MaquinaSpider(Spider):
    name = "maquina"
    allowed_domains = ["kuantokusta.pt"]
    start_urls = LINKS


    def parse(self, response):
        #//*[@id="didomi-notice-agree-button"]
        data = Selector(response).xpath('//*[@id="didomi-notice-agree-button"]')

        for item in data:
            yield item
