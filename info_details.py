import requests

def get_access_profiles(bot, token, base_url="https://www.timeforstorm.eu/stormstudio"):
    url = f"{base_url}/objectprofiles/get"
    session = requests.Session()
    
    for cookie in bot.driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])

    payload = {
        "szSecurityToken": token,
        "securityToken": token,
        "lang": "en",
        "appUrl": base_url
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Referer": f"{base_url}/userprofiles",
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = session.post(url, headers=headers, data=payload)
    profiles = {}
    print("Fetching rights profiles...")

    if response.status_code == 200:
        try:
            data = response.json()
            for profile in data.get("profiles", []):
                profiles[profile["profileId"]] = profile["name"]
        except Exception as e:
            print("Error parsing response:", e)
    else:
        print("Request failed:", response.status_code, response.text)

    return profiles

def get_rights_profiles(bot, token, base_url="https://www.timeforstorm.eu/stormstudio"):
    url = f"{base_url}/rightsprofiles/user"
    session = requests.Session()

    for cookie in bot.driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])

    payload = {
        "szSecurityToken": token,
        "securityToken": token,
        "lang": "en",
        "appUrl": base_url
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Referer": f"{base_url}/userprofiles",
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = session.post(url, headers=headers, data=payload)
    rights_profiles = {}

    if response.status_code == 200:
        try:
            data = response.json()
            for profile in data.get("profiles", []):
                profile_id = profile.get("profileId")
                org_id = profile.get("orgId")
                name = profile.get("name")
                rights_profiles[profile_id] = {
                    "name": name,
                    "orgId": org_id
                }
        except Exception as e:
            print("Error parsing rights profiles:", e)
    else:
        print("Failed request:", response.status_code, response.text)

    return rights_profiles

def get_user_ids(bot, token, base_url="https://www.timeforstorm.eu/stormstudio"):
    url = f"{base_url}/rightsprofiles/assignments"
    session = requests.Session()

    for cookie in bot.driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])

    payload = {
        "szSecurityToken": token,
        "securityToken": token,
        "lang": "en",
        "appUrl": base_url
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Referer": f"{base_url}/userprofiles",
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = session.post(url, headers=headers, data=payload)
    user_map = {}

    if response.status_code == 200:
        try:
            data = response.json()
            for user in data.get("users", []):
                user_name = user.get("name")
                user_id = user.get("userId")
                if user_name and user_id:
                    user_map[user_name] = user_id
        except Exception as e:
            print("Error parsing user list:", e)
    else:
        print("Failed request:", response.status_code, response.text)

    return user_map