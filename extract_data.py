import os
import csv

REQUIRED_HEADERS = {"Username", "RightsProfile", "AccessProfile"}

def process_csv_users(path):
    while True:
        if not os.path.exists(path):
            os.system('clear' if os.name == 'posix' else 'cls')
            print("Error: File does not exist.")
            path = input("Enter the CSV file path to retry: ")
            continue

        if not path.lower().endswith('.csv'):
            os.system('clear' if os.name == 'posix' else 'cls')
            print("Error: File is not a CSV.")
            path = input("Enter the CSV file path to retry: ")
            continue

        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            if reader.fieldnames is None or not REQUIRED_HEADERS.issubset(reader.fieldnames):
                os.system('clear' if os.name == 'posix' else 'cls')
                missing = REQUIRED_HEADERS - set(reader.fieldnames or [])
                print("Error: Missing headers:", missing)
                path = input("Enter the CSV file path to retry: ")
                continue
            data = list(reader)
            if not data:
                os.system('clear' if os.name == 'posix' else 'cls')
                print("Error: CSV file is empty.")
                path = input("Enter the CSV file path to retry: ")
                continue
            return data
