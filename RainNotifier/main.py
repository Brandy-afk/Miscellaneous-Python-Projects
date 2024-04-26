import requests
import smtplib

#Using email right now, but use twilio to set up SMS text messages

GMAIL_ADDRESS = "**********"
GMAIL_PASSWORD = "*********"

LINK = "https://api.openweathermap.org/data/2.5/forecast"
MY_LAT = 39.739235
MY_LNG = -104.990250
CITY = "Denver,US"
WEATHER_API_KEY = "****************"
para = {
    'lat': MY_LAT,
    'lon': MY_LNG,
    'appid' : WEATHER_API_KEY,
    'cnt' : 3
}

def return_if_rain(weather):
    for hour_data in weather:
        for forcast in hour_data:
            print(forcast)
            if int(forcast['id']) < 700:
                return True
    return False


def send_mail():
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(GMAIL_ADDRESS, GMAIL_PASSWORD)
        connection.sendmail(GMAIL_ADDRESS, to_addrs="brandondmesch@gmail.com", msg=f"Subject: Weather Forecast\n\n"
                                                                                             f"Its going to rain, bring an umbrella!")

response = requests.get(LINK, params=para)
response.raise_for_status()

forecast_data = response.json()
weather_data = [forecast['weather'] for forecast in forecast_data['list']]

if return_if_rain(weather_data):
    send_mail()

send_mail()


