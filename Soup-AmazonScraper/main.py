import requests
import smtplib
from bs4 import BeautifulSoup
import dotenv
import os

dotenv.load_dotenv()

url = ("https://www.amazon.com/Kozyard-Polypropylene-Reclinging-Sunbathing-Textilence/dp/B0867C6CMJ/ref=sxin_12_pa_sp_"
       "search_thematic_sspa?content-id=amzn1.sym.c5752f79-8747-4816-9200-c3f3add2f27d%3Aamzn1.sym.c5752f79-8747-4816-9200-"
       "c3f3add2f27d&crid=16N4WN3LBJKWQ&cv_ct_cx=tanning%2Bchair&dib=eyJ2IjoiMSJ9.CPB49eTHaf6TuQh2-gQ9hzkGtmKroInIBJmx-"
       "DrJ1yZUzC38jKAyxON3Hpqw9NWKvqPb9Rlmpk5C3NajeRGwIw.OsQonLfdPRZS32ZXgRd7CC_rmCPHSi7M6u2J4V0CRpU&dib_tag=se&keywords="
       "tanning%2Bchair&pd_rd_i=B0867C6CMJ&pd_rd_r=550d9bd5-894e-442c-b7bb-270266492b2a&pd_rd_w=1IB61&pd_rd_wg=gzuGw&pf_rd_"
       "p=c5752f79-8747-4816-9200-c3f3add2f27d&pf_rd_r=EK9N0W53EV0W3MKQ4PKV&qid=1712081938&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA"
       "%3D%3D&sprefix=tanning%2Bchair%2Caps%2C134&sr=1-4-9"
       "428117c-b940-4daa-97e9-ad363ada7940-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9zZWFyY2hfdGhlbWF0aWM&th=1")

headers = {
    "User-Agent": "Defined",
    "Accept-Language": "en-ZA,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6",
}

gmail_user = os.getenv('GMAIL_USER')
gmail_password = os.getenv('GMAIL_PASSWORD')
send_user = '**********'
DESIRED_PRICE = 100


def send_mail(product_name):
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(gmail_user, gmail_password)
        connection.sendmail(from_addr=gmail_user, to_addrs=send_user, msg='Subject: Low Product Price\n\n'
                                                                          f'{product_name} is currently below your '
                                                                          f'desired price.\n'
                                                                          f'URL:{url}')

def get_price(soup):
    soup_price = soup.find(name='span', class_='a-price-whole')
    price = float(soup_price.getText())
    return price


def main():
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    price = get_price(soup)
    if price <= DESIRED_PRICE:
        send_mail("Patio Chair")


if __name__ == '__main__':
    main()
