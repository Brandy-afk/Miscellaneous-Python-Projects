import smtplib
import random
import datetime as dt
import pandas

GMAIL_ADDRESS = "INSERT GMAIL HERE"
GMAIL_PASSWORD = "INSERT GMAL PASSSWORD"


def return_if_birthday(month, day):
    today = dt.datetime.today()
    return today.month == month and today.day == day


def return_random_letter(name):
    letter_int = random.randint(1, 3)
    with open(f'letter_templates/letter_{letter_int}.txt', 'r') as file:
        lines = ''.join(file.readlines())

    lines = lines.replace('[NAME]', name)
    return (f"Subject: Happy Birthday {name}!\n\n"
            f"{lines}")

def send_mail(to_addr, content):
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(GMAIL_ADDRESS, GMAIL_PASSWORD)
        connection.sendmail(GMAIL_ADDRESS, to_addr, msg=content)


def main():
    birthdays = pandas.read_csv('birthdays.csv')
    for (index, row) in birthdays.iterrows():
        if return_if_birthday(row.month, row.day):
            content = return_random_letter(row['name'])
            send_mail(row.email, content)
            print(f"Send Mail to {row['name']}")


main()
