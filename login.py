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
from info_details import get_access_profiles, get_rights_profiles, get_user_ids
from extract_data import process_csv_users

class StormStudioBot:
    def __init__(self, driver_path=None):
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        options.add_argument("--log-level=3") 
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        service = Service(executable_path=driver_path, log_path=os.devnull) if driver_path else Service()
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 30)

    def login(self, url, organisation, username):
        self.driver.get(url)
        input_box = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#prefix_search input')))
        input_box.send_keys(organisation)
        input_box.send_keys(Keys.ENTER)
        for _ in range(10):
            try:
                dropdown = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'el-select')))
                dropdown.click()
                break
            except:
                time.sleep(1)
        else:
            raise Exception("User dropdown not clickable after multiple attempts")
        time.sleep(0.5)
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

    access_profiles = get_access_profiles(bot, token, base_url)
    rights_profiles = get_rights_profiles(bot, token, base_url)
    user_ids = get_user_ids(bot, token, base_url)

    def process_csv_and_assign():
        while True:
            csv_path = input("Enter the path to the CSV file with user data: ").strip()

            if (csv_path.startswith('"') and csv_path.endswith('"')) or (csv_path.startswith("'") and csv_path.endswith("'")):
                csv_path = csv_path[1:-1]

            data = process_csv_users(csv_path)

            for idx, row in enumerate(data, start=2):
                username = row.get("Username")
                access_profile = row.get("AccessProfile")
                rights_profile = row.get("RightsProfile")

                if not username or not rights_profile:
                    logging.warning(f"Row {idx}: Skipping due to missing data: {row}")
                    continue

                access_profile_id = next((pid for pid, name in access_profiles.items() if name == access_profile), None)
                rights_profile_id = next((pid for pid, info in rights_profiles.items() if info["name"] == rights_profile), None)
                user_name_id = user_ids.get(username)

                if not rights_profile_id or not user_name_id:
                    logging.warning(f"Row {idx}: Profile(s) not found for user {username}. Skipping.")
                    continue

                if not access_profile_id:
                    access_profile_id = 0 # All access profile
                    access_profile = "All"

                payload = {
                    "userId": str(user_name_id),
                    "profileId": str(rights_profile_id),
                    "objectProfileId": str(access_profile_id),
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

                if response.status_code == 200:
                    logging.info(f"Row {idx}: Successfully assigned {username} to {rights_profile} with access profile {access_profile}.")
                else:
                    logging.error(f"Row {idx}: Failed to assign {username}: {response.status_code} - {response.text}")

            again = input("Do you want to process another CSV file? (y/n): ").strip().lower()
            if again != "y":
                print("Finished processing CSV files.")
                break

    process_csv_and_assign()

   