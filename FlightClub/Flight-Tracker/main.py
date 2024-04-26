import requests
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta
from google.oauth2.service_account import Credentials
from flightdata import *
import smtplib
import gspread
import os

GOOGLE_SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
FLIGHT_ENDPOINT = 'https://api.tequila.kiwi.com/v2/search'
ORGIN_CITY = 'MIA'
TARGET_CITIES = ['TYO', 'HKG', 'ROM', 'MIL', 'LON', 'BCN', 'MOW']
# Months
TIME_RANGE = 6

flight_headers = {}


def load_variables() -> None:
    load_dotenv()
    global flight_headers
    flight_headers = {'apikey': os.getenv('FLIGHT_TOKEN')}


def get_sheet(sheet: str):
    creds = Credentials.from_service_account_file(filename='sa.json', scopes=GOOGLE_SCOPE)
    client = gspread.authorize(creds)
    return client.open_by_url(os.getenv("SHEET_URL")).worksheet(sheet)


def get_cheap_flights() -> list[FlightData]:
    format = '%d/%m/%Y'
    future_date = (datetime.now() + relativedelta(months=TIME_RANGE)).strftime(format)
    today_date = datetime.now().strftime(format)

    cheapest_flights = []
    for city in TARGET_CITIES:
        params = {
            'fly_from': ORGIN_CITY,
            'fly_to': city,
            'date_from': today_date,
            'date_to': future_date,
            "nights_in_dst_from": 7,  # Minimum number of nights in the destination
            "nights_in_dst_to": 14,  # Maximum number of nights in the destination
            'max_stopovers': 2,
            'curr': 'USD'
        }

        response = requests.get(FLIGHT_ENDPOINT, headers=flight_headers, params=params)
        response.raise_for_status()
        flights = response.json()

        if len(flights) == 0:
            continue
        else:
            cf = return_cheapest_flight(flights['data'])
            if cf is None:
                continue
            else:
                cheapest_flights.append(cf)

    return cheapest_flights


def return_cheapest_flight(flights):
    try:
        sorted_flights = sorted(flights, key=lambda flight: float(flight['price']))
        return create_flight_date(sorted_flights[0])
    except IndexError:
        print("Error: No flight found")
        return None


def create_flight_date(flight):
    depart_date = '/'.join(flight['route'][0]['local_departure'].split('T')[0].split('-'))
    return_date = '/'.join(flight['route'][len(flight['route']) - 1]['local_departure'].split('T')[0].split('-'))

    return FlightData(flight['price'], depart_date, return_date, flight['cityTo'], flight['cityCodeTo'])


def create_alerts(cheap_flights):
    sheet = get_sheet('FlightInfo')
    current_records = {entry['City']: entry for entry in sheet.get_all_records()}

    messages = []
    for data in cheap_flights:
        if data.city not in current_records:
            sheet.append_row(data.return_list())
            messages.append(data.print_data())
        elif float(current_records[data.city]['Price']) > float(data.price):
            sheet.insert_row(data.print_data(), index=sheet.find(data.city).row)
            messages.append(data.print_data())
    return messages


def send_emails(messages: list[str]):
    sheet = get_sheet("PersonInfo")
    records = sheet.get_all_records()
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(os.getenv("GMAIL_ADDRESS"), os.getenv("GMAIL_PASSWORD"))
        for message in messages:
            for record in records:
                connection.sendmail(from_addr=os.getenv("GMAIL_ADDRESS"), to_addrs=record['Email'],
                                    msg=f'Subject: Low Price Alter {record['First']}!\n\n'
                                        f'{message}')


def main():
    load_variables()
    cheap_flights = get_cheap_flights()
    messages = create_alerts(cheap_flights)
    send_emails(messages)


# TEXTING (Telegram)
# def send_message(message: str) -> None:
#     url = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/sendMessage"
#     payload = {
#         "chat_id": os.getenv('CHAT_ID'),
#         'text': message
#     }
#     response = requests.post(url, json=payload)


if __name__ == '__main__':
    main()
