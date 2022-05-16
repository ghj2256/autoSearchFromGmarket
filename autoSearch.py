from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

import re


def search():
    driver = webdriver.Chrome('./chromeDriver/chromedriver.exe')

    driver.get('http://minishop.gmarket.co.kr/organicmaru1004')
    driver.implicitly_wait(3)

    category = driver.find_element_by_xpath('//*[@id="ulCategory"]')
    category_list = re.compile('[가-힣]+').findall(category.text)

    product_code = []

    for c in category_list:
        print('new!')
        driver.find_element_by_partial_link_text(c).click()
        product = driver.find_element_by_xpath('//*[@id="ItemList"]/div[3]/ul')
        print(product.text)

    driver.quit()


if __name__ == "__main__":
    search()
