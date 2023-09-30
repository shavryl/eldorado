from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException




# driver should get the url
def get_url(driver, url):
    driver.get(url)


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

