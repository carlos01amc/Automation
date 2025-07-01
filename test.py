from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

class StormStudioBot:
    def __init__(self, driver_path=None):
        service = Service(executable_path=driver_path) if driver_path else Service()
        self.driver = webdriver.Chrome(service=service)
        self.wait = WebDriverWait(self.driver, 30)

    def open_login_page(self, url):
        self.driver.get(url)

    def search_organisation(self, name):
        input_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#prefix_search input'))
        )
        input_field.send_keys(name)
        input_field.send_keys(Keys.ENTER)

    def select_user(self, username):
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'el-select'))).click()
        user_option = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//li[contains(@class, 'el-select-dropdown__item') and contains(., '{username}')]"))
        )
        user_option.click()

    def click_login(self):
        login_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "loginButton"))
        )
        login_button.click()

    def login(self, url, organisation, username):
        self.open_login_page(url)
        self.search_organisation(organisation)
        self.select_user(username)
        self.click_login()

    def quit(self, delay=5):
        time.sleep(delay)
        self.driver.quit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    bot = StormStudioBot()
    try:
        bot.login(
            url="https://www.timeforstorm.eu/stormstudio/login/content%20guru/8a46c4ac0c101da5#/login/content%20guru/8a46c4ac0c101da5%20storm%20STUDIO%E2%84%A2",
            organisation="Allianz Europe 01 Test",
            username="red01"
        )
        logging.info("Login successful!")
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        bot.quit()
