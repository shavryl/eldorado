import time
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
    start_urls = LINKS

    def __init__(self):
        service = webdriver.ChromeService(executable_path="/usr/bin/chromedriver")
        self.driver = webdriver.Chrome(service=service)

    def remove_modal(self):
        time.sleep(10)
        accept_xpath = ENTRANCE_MODAL
        click_button(self.driver, accept_xpath)
        
    def parse(self, response):
        self.driver.get(response.url)
        self.remove_modal()

        items_grid = '//*[@id="searchForm"]/div/div[3]/div[3]'
        data = Selector(response).xpath(items_grid)

        for item in data:
            print(item)

        # while True:
        #     next = self.driver.find_element_by_xpath('//td[@class="pagn-next"]/a')

        #     try:
        #         next.click()

        #         # get the data and write it to scrapy items
        #     except:
        #         break

        self.driver.close()
