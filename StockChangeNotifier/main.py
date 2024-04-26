import requests
import os
from dotenv import load_dotenv

load_dotenv()

# <--------------------CONSTANTS---------------------_>
# Add all stock that you want to check, will go in a list for these items.
SYMBOLS = ['GOOG', 'META', 'TSLA', 'NFLX']
SYMBOL_DICT = {
    'GOOG': 'Google',
    'META': 'Facebook',
    'TSLA': 'Tesla',
    'NFLX': 'Netflix',
}
# Replace 'YOUR_API_KEY' with your actual API key
stock_key = os.getenv('STOCK_KEY')
news_key = os.getenv('NEWS_KEY')

bot_token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

# The necessary percentage difference for it to be notable
NOTABLE = 3.0

news_params = {
    "apiKey": news_key,
    "sources": "bloomberg,cnbc,the-wall-street-journal,financial-times,reuters",
    "pageSize": 100,  # Adjust the page size as needed,
    'language': 'en',
    'qinTitle': ''
}


# <--------------------------LOGIC----------------------->
# Make the API request
def return_close_price(index: int, data) -> float:
    previous_date = list(data['Time Series (Daily)'].keys())[index]
    return float(data['Time Series (Daily)'][previous_date]['4. close'])


def return_difference(current: float, prev: float) -> float:
    ratio = (current / prev) - 1
    return ratio * 100


def get_news(company: str):
    base_url = "https://newsapi.org/v2/everything"
    news_params['q'] = company
    response = requests.get(base_url, params=news_params)
    response.raise_for_status()
    return response.json()['articles'][0]


def create_message(news, company: str, symbol: str) -> str:
    return f"{symbol}({company}) News\nTitle: {news['title']}\nURL: {news['url']}\nText: {news['content']}"


def send_message(percent_diff: float, message: str) -> None:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        'text': message
    }
    response = requests.post(url, json=payload)
    print(response.status_code)


def main():
    for symbol in SYMBOLS:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={stock_key}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        current_price = return_close_price(0, data)
        previous_price = return_close_price(1, data)
        percent_diff = return_difference(current_price, previous_price)

        if abs(percent_diff) >= NOTABLE:
            company = SYMBOL_DICT[symbol]
            recent_news = get_news(company)
            message = create_message(recent_news, company, symbol)
            send_message(message)


main()
