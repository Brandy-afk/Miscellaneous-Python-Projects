import selenium.webdriver.remote.webelement
from selenium import webdriver
from selenium.webdriver.common.by import By
import threading
import time

UPGRADE_INTERVAL = 1

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")
driver.maximize_window()


def click_cookie(ID):
    cookie_element = driver.find_element(By.ID, 'cookie')
    while True:
        cookie_element.click()

def choose_upgrade():
    store_element = driver.find_element(By.ID, 'store')
    upgrades = store_element.find_elements(By.XPATH, './*')
    current_cookies = driver.find_element(By.ID, 'money')

    money = float(current_cookies.text.replace(',', ''))
    for index in range(len(upgrades) - 1, 0, -1):
        split_text = upgrades[index].find_element(By.TAG_NAME, "b").text.split(' ')
        try:
            cost_text = split_text[len(split_text) - 1].replace(',', '')
            cost = float(cost_text)
            if cost < money:
                upgrades[index].click()
                break
        except ValueError:
            continue



def main():
    threads = []
    for i in range(4):
        t = threading.Thread(target=click_cookie, args=(i,))
        threads.append(t)
        t.start()

    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= UPGRADE_INTERVAL:
            choose_upgrade()
            start_time = time.time()


if __name__ == '__main__':
    main()
