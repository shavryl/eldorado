import time

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException

from src.constants import LINKS, ENTRANCE_MODAL


def run():
    service = webdriver.ChromeService(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service)
    cities_milk = LINKS[0]
    driver.get(cities_milk)

    print(driver.title)
    time.sleep(10)
    # click accept
    modal = '//*[@id="didomi-notice-agree-button"]'
    accept_xpath = ENTRANCE_MODAL
    click_button(driver, modal)
    
    time.sleep(150)
    # driver.quit()


# driver should click on the button py x-path selector
def click_button(driver, xpath):
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        button.click()
    except TimeoutException:
        print("Timed out waiting for page to load")
    except NoSuchElementException:
        print("No such element")
    except ElementNotInteractableException:
        print("Element not interactable")



if __name__ == "__main__":
    run()
