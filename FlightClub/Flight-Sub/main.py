import dotenv
import os
import gspread
from google.oauth2.service_account import Credentials
from email.utils import parseaddr

GOOGLE_SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
def on_start():
    dotenv.load_dotenv()

def get_sheet():
    creds = Credentials.from_service_account_file('sa.json', scopes=GOOGLE_SCOPE)
    client = gspread.authorize(creds)
    return client.open_by_url(os.getenv('SHEET_URL')).worksheet('PersonInfo')

def user_input(check, message) -> str:
    u_i = ""
    while check(u_i) is False:
        u_i = input(message)
        if check(u_i) is False:
            print("Bad input, try again!")
    return u_i


def valid_email(email) -> bool:
    name, addr = parseaddr(email)
    return '@' in addr


def check_for_alpha(i):
    return i.isalpha() and i != ""

def get_emails():
    email = user_input(valid_email, "What is your email?\n")
    validated_email = user_input(valid_email, "-Please validate your email-\n")
    return (validated_email , email)

def main():
    on_start()
    sheet = get_sheet()
    records = sheet.get_all_records()
    record_map = {(record['First'], record['Last']): record for record in records}

    print("Welcome to Brandon's flight club!")
    print("We find the best deals and email you.")
    while True:
        first = user_input(check_for_alpha, "What is your first name? ")
        last = user_input(check_for_alpha, "What is your last name? ")

        (confirm_email, email) = get_emails()
        while email != confirm_email:
            print("Bad email, try again!")
            (confirm_email, email) = get_emails()

        if (first, last) in record_map:
            print("You are already in the flight club!\n")
            continue
        else:
            print(f"Welcome to the club {first}!\n")
            sheet.append_row([first, last, email])





if __name__ == '__main__':
    main()
