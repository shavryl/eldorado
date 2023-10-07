import time
import json
from scrapy import Spider
from scrapy.selector import Selector

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.controller import click_button
from src.constants import LINKS, ENTRANCE_MODAL


class MaquinaSpider(Spider):
    name = "maquina"
    allowed_domains = ["kuantokusta.pt"]
    start_urls = [
        f"https://www.kuantokusta.pt/search?q=cafe+maquina&pag={page}"
          for page in range(1, 5)
    ]

    def __init__(self):
        service = webdriver.ChromeService(executable_path="/usr/bin/chromedriver")
        self.driver = webdriver.Chrome(service=service)

    def remove_modal(self):
        time.sleep(5)
        accept_xpath = ENTRANCE_MODAL
        click_button(self.driver, accept_xpath)
        
    def parse(self, response):
        time.sleep(2)

        if response.url == LINKS[0]:
            self.driver.get(response.url)
            self.remove_modal()
     
        grid = response.xpath('.//div[@class="product-item"]')
        num = 1
        for item in grid:
            # here should be a separate controller with xpaths by domain

            print(num)
            big_price = item.xpath('.//span[@class="price-interval"]/text()').get()
            small_price = item.xpath('.//span[@class="small-price-interval"]/text()').get()
            price = small_price or big_price
            print(f"price: {price}")
            title = item.xpath('.//h2[@itemprop="name"]/text()').get()
            print(f"title: {title}")
            link = item.xpath('.//div[@class="product-item-inner"]/a/@href').get()
            print(f"link: {link}")
            num += 1

            # and a separate class to standartize the output, maye it's one class
            yield {
                "date": "2023-10-06",
                "title": title,
                "price": price,
                "link": link,
            }
        