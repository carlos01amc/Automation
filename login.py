import json
import time
import os
import logging
import requests
from enum import Enum
from urllib.parse import parse_qs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class StormStudioBot:
    def __init__(self, driver_path=None):
        options = Options()
        options.add_argument("--start-maximized")
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        service = Service(executable_path=driver_path) if driver_path else Service()
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 30)

    def login(self, url, organisation, username):
        self.driver.get(url)
        input_box = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#prefix_search input')))
        input_box.send_keys(organisation)
        input_box.send_keys(Keys.ENTER)
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'el-select'))).click()
        self.wait.until(EC.element_to_be_clickable((
            By.XPATH, f"//li[contains(@class, 'el-select-dropdown__item') and contains(., '{username}')]"
        ))).click()
        self.wait.until(EC.element_to_be_clickable((By.ID, "loginButton"))).click()

    def navigate_to_user_profiles(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "ProductImage_NGServiceSettings"))).click()
        self.wait.until(EC.element_to_be_clickable((By.ID, "ProductImage_UserProfiles"))).click()

    def extract_assignment_payload(self):
        logs = self.driver.get_log("performance")
        for entry in logs:
            try:
                msg = json.loads(entry["message"])["message"]
                req = msg.get("params", {}).get("request", {})
                if msg.get("method") == "Network.requestWillBeSent" and "assignments" in req.get("url", ""):
                    return req.get("postData")
            except:
                continue
        return None

    def quit(self, delay=5):
        time.sleep(delay)
        self.driver.quit()

class Region(Enum):
    EU = 1
    UK = 2

def get_region_url(region):
    return {
        Region.EU: "https://www.timeforstorm.eu/stormstudio/login/content%20guru/8a46c4ac0c101da5#/login/content%20guru/8a46c4ac0c101da5%20storm%20STUDIO%E2%84%A2",
        Region.UK: "https://www.timeforstorm.com/stormstudio/login/content%20guru/8a46c4ac0c101da5"
    }[region]

def ask_region():
    print("Select region:\n1. EU\n2. UK")
    while True:
        choice = input("Enter 1 for EU or 2 for UK: ").strip()
        if choice == "1":
            return Region.EU
        elif choice == "2":
            return Region.UK
        print("Invalid input. Try again.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    region = ask_region()
    bot = StormStudioBot()
    try:
        bot.login(
            url=get_region_url(region),
            organisation=input("Enter organisation name: ").strip(),
            username="red01"
        )
        os.system('cls' if os.name == 'nt' else 'clear')
        logging.info("Login successful!")
        bot.navigate_to_user_profiles()
        time.sleep(3)
        raw_payload = bot.extract_assignment_payload()
        if raw_payload:
            parsed = {k: v[0] for k, v in parse_qs(raw_payload).items()}
            token = parsed.get("szSecurityToken")
    finally:
        logging.info("Token Extracted")

    base_url = "https://www.timeforstorm.eu/stormstudio"
    post_url = f"{base_url}/userprofiles/addassignment"

    session = requests.Session()
    for cookie in bot.driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])

    payload = {
        "userId": "82831",
        "profileId": "1808",
        "objectProfileId": "0",
        "szSecurityToken": token,
        "securityToken": token,
        "lang": "en",
        "appUrl": base_url
    }

    headers_post = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Referer": f"{base_url}/userprofiles",
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = session.post(post_url, headers=headers_post, data=payload)

    print("Status Code:", response.status_code)
    print("Response:", response.text or "[Resposta vazia]")