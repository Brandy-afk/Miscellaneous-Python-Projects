from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome()
driver.get("https://www.python.org/")

def create_date_string(date : str) -> str:
    return date.split('T')[0]


def main():
    events = {}
    event_menu = driver.find_element(By.XPATH, '//*[@id="content"]/div/section/div[2]/div[2]/div/ul')
    l_items = event_menu.find_elements(By.TAG_NAME, 'li')

    counter = 0
    for l in l_items:
        new_event = {
            'name': l.find_element(By.TAG_NAME, 'a').text,
            'date': create_date_string(l.find_element(By.TAG_NAME, 'time').get_attribute('datetime'))
        }
        events[counter] = new_event
        counter += 1

    print(events)

if __name__ == '__main__':
    main()