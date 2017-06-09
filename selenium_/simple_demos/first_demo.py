# coding: utf-8
__author__ = 'Chris Wang'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


if __name__ == "__main__":
    test_result = False
    ie_webdriver_server_path = \
        r'C:\Users\fan\OneDrive\pythonwork\selenium_\selenium_drivers\IEDriverServer.exe'
    driver = webdriver.Ie(ie_webdriver_server_path)
    driver.get("http://www.baidu.com")
    search_input_element = driver.find_element_by_id('kw')
    search_input_element.send_keys("WebDriver")
    search_input_element.send_keys(Keys.ENTER)

    search_content_element = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.ID, "content_left"))
    )

    for i in range(1, 11):
        content_div = driver.find_element_by_id(str(i))
        title = str(content_div.find_element_by_css_selector(".t a").text.encode('utf8'))

        if 'Watir' not in title:
            continue
        else:
            print('Find keyword watir, it was in index %d search result! Test case pass!' % i)
            test_result = True

    if test_result is False:
        raise Exception("Test fail! Can not find keyword from search page!")
    else:
        driver.close()
        driver.quit()