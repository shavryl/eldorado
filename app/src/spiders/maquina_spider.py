import time
import json
from scrapy import Spider
from scrapy.selector import Selector

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.controller import click_button
from src.constants import (
    LINKS,
    ENTRANCE_MODAL,
    PRICES,
    LINKS_OLX
)



class MaquinaSpiderKK(Spider):
    name = "kk"
    allowed_domains = ["kuantokusta.pt"]
    start_urls = LINKS

    def __init__(self):
        service = webdriver.ChromeService(executable_path="/usr/bin/chromedriver")
        self.driver = webdriver.Chrome(service=service)

    def remove_modal(self):
        time.sleep(5)
        accept_xpath = ENTRANCE_MODAL
        click_button(self.driver, accept_xpath)
        
    def parse(self, response):
        target_price = float(PRICES[response.url])

        if response.url == LINKS[0]:
            self.driver.get(response.url)
            self.remove_modal()
     
        grid = response.xpath('.//div[@class="product-item"]')
        
        for item in grid:
            # here should be a separate controller with xpaths by domain
            big_price = item.xpath('.//span[@class="price-interval"]/text()').get()
            small_price = item.xpath('.//span[@class="small-price-interval"]/text()').get()
            price = small_price or big_price
            title = item.xpath('.//h2[@itemprop="name"]/text()').get()
            link = item.xpath('.//div[@class="product-item-inner"]/a/@href').get()
             
            price: str = price.split(" ")[1] if " " in price else price
            price = float(price.replace(",", ".").rstrip('€'))

            profit = round(target_price - price, 1)

            # # we should collect only relevant data, no need to save expensive items
            if target_price > price and link != "#":
                # and a separate class to standartize the output, maye it's one class
                yield {
                    "date": "2023-10-11",
                    "profit": profit,
                    "title": title,
                    "price": price,
                    "target_price": target_price,
                    "link": link,
                }
        


class MaquinaSpiderOlx(Spider):
    name = "olx"
    allowed_domains = ["olx.pt"]
    # start_urls = ["https://www.olx.pt/ads/q-cafe-maquina-Nespresso-Pixie/"]
    start_urls = LINKS_OLX
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

    def __init__(self):
        service = webdriver.ChromeService(executable_path="/usr/bin/chromedriver")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(options=chrome_options, service=service)

    def parse(self, response):

        self.driver.get(response.url)

        grid = self.driver.find_elements(By.CLASS_NAME, "css-rc5s2u")
        print(f"elements: {len(grid)}")

        # writing to file with: scrapy crawl olx -o olx.json
        for element in grid:
            print(element)

            data = element.find_element(By.CLASS_NAME, "css-1apmciz")
            price_element = data.find_element(By.TAG_NAME, "p")
            title_element = data.find_element(By.TAG_NAME, "h6")

            yield {
                "title": title_element.text.strip(),
                "price": price_element.text.strip(),
                "link": element.get_attribute("href")
            }
