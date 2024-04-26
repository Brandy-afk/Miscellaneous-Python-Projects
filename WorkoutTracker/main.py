import requests
import os
import gspread
from datetime import *
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv, dotenv_values



GOOGLE_SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# https://trackapi.nutritionix.com/v2/natural/exercise

nutrition_headers = {
    "x-app-id": os.getenv("NUTRITION_ID"),
    "x-app-key": os.getenv("NUTRITION_KEY"),
    "Content-Type": "application/json"
}

def load_environment_variables():
    load_dotenv()


def get_sheet():
    creds = Credentials.from_service_account_file('ServiceKey.json', scopes=GOOGLE_SCOPE)
    client = gspread.authorize(creds)
    return client.open_by_url(os.getenv('SHEET_URL')).sheet1


def main():
    load_environment_variables()
    sheet = get_sheet()
    person_input = input("Enter your exercises: ")
    data = {
        'query': person_input
    }
    response = requests.post(url=os.getenv('NUTRITION_ENDPOINT'), headers=nutrition_headers, json=data)
    response.raise_for_status()
    data = response.json()

    for exercise in data['exercises']:
        now = datetime.now()
        values = [now.strftime("%m/%d/%Y"), now.strftime("%H:%M:00"), exercise['name'].title(), f"{exercise['duration_min']} minutes", exercise['nf_calories']]
        sheet.append_row(values)

    print("Exercises completed and added.")


if __name__ == '__main__':
    main()
