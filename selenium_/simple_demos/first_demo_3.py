# coding: utf-8
__author__ = "Chris Wang"


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


if __name__ == "__main__":

    test_result = False

    ie_webdriver_server_path = \
        r"C:\\Users\\fan\OneDrive\pythonwork\selenium_\selenium_drivers\IEDriverServer.exe"

    driver = webdriver.Ie(ie_webdriver_server_path)
    driver.get("http://www.baidu.com")

    search_input_element = driver.find_element_by_id('kw')
    search_input_element.send_keys('WebDriver')
    search_input_element.send_keys(Keys.ENTER)


    search_input_element = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_all_elements_located((By.ID, "content_left"))
    )
    # 等待driver 执行至少10s, 直到所有元素已加载

    driver.find_element_by_id('page').find_element_by_css_selector('a').send_keys(Keys.ENTER)
    # 找到id=page,找到第一个a标签--点击第二页

    search_input_element = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_all_elements_located((By.ID, "20"))
    )

    for i in range(11, 21):
        content_div = driver.find_element_by_id(str(i))
        title = str(content_div.find_element_by_css_selector(".t a").text.encode('utf8'))

        if "WebdriverIO - API Docs" not in title:
            continue
        else:
            print(r'Find keyword "WebDriver - Mozilla | MDN", it was in index %d search result! Test case pass!' % i)
            test_result = True

    if test_result == False:
        raise Exception("Test fail! Can not find keyword from search page!")
    else:
        driver.close()
        driver.quit()

