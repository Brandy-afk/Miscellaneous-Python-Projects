from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def main():
    chrome_settings = webdriver.ChromeOptions()
    chrome_settings.add_experimental_option('detach', True)

    driver = webdriver.Chrome(options=chrome_settings)
    driver.maximize_window()

    # ----------Sign up website----------#
    driver.get("https://secure-retreat-92358.herokuapp.com/")

    name_ele = driver.find_element(By.NAME, 'fName')
    last_ele = driver.find_element(By.NAME, 'lName')
    email_ele = driver.find_element(By.NAME, 'email')

    name_ele.send_keys("Brandon")
    last_ele.send_keys("D")
    email_ele.send_keys('wenwaad@awkda.com')

    sign_up = driver.find_element(By.CSS_SELECTOR, '.form-signin button')
    sign_up.click()


    # ---------------WIKI-----------------#
    # driver.get('https://en.wikipedia.org/wiki/Main_Page')
    #
    # articles_count = driver.find_element(By.CSS_SELECTOR, '#articlecount a')
    # print(f'Number of articles: {articles_count.text}')
    # #
    # # all_portals = driver.find_element(By.LINK_TEXT, 'Content portals')
    # # all_portals.click()
    #
    # search_bar = driver.find_element(By.NAME, 'search')
    # search_bar.send_keys('Python')
    # search_bar.send_keys(Keys.ENTER)


if __name__ == '__main__':
    main()
