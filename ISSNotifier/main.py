import requests as rq
import datetime as dt
import smtplib

GMAIL_ADDRESS = "********"
GMAIL_PASSWORD = "********"
PERSONAL_EMAIL = "********"

MY_LAT = 39.739235
MY_LNG = -104.990250


def is_within_distance(num, target, distance):
    return abs(num - target) <= distance


def return_if_nearby():
    station_response = rq.get('http://api.open-notify.org/iss-now.json')
    station_response.raise_for_status()
    station_data = station_response.json()

    station_latitude = float(station_data['iss_position']['latitude'])
    station_longitude = float(station_data['iss_position']['longitude'])

    return (is_within_distance(MY_LNG, station_longitude, 5)
            and is_within_distance(MY_LAT, station_latitude, 5))


def return_if_night():
    now = dt.datetime.now()

    parameters = {
        'lat': MY_LAT,
        'lng': MY_LNG,
        'formatted': 0
    }

    response = rq.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    data = response.json()
    sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])

    return now.hour >= sunset or now.hour < sunrise


def send_mail():
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(GMAIL_ADDRESS, GMAIL_PASSWORD)
        connection.sendmail(GMAIL_ADDRESS, PERSONAL_EMAIL, f'Subject:ISS Location Alert\n\n'
                                                           f'Hey!\nLook up at the sky to see the ISS right now!')


def main():
    if return_if_night():
        if return_if_nearby():
            send_mail()


main()
