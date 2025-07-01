import os
import csv

REQUIRED_HEADERS = {"Username", "RightsProfile", "AccessProfile"}

def process_csv_users(path):
    if not os.path.exists(path):
        print("Error: File does not exist.")
        return None

    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        if not REQUIRED_HEADERS.issubset(reader.fieldnames):
            print("Error: Missing headers:", REQUIRED_HEADERS - set(reader.fieldnames))
            return None
        data = list(reader)
        return data
