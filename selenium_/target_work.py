# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

__author__ = 'Chris Wang'

if __name__ == "__main__":
    test_result = False
    keyword_index = -1
    error_msg = ''

    ie_webdriver_server_path = \
        r'C:\Python\Python34\IEDriverServer.exe'
    driver = webdriver.Ie(ie_webdriver_server_path)
    # ff_webdriver_server_path = \
    #     r'C:\Python\Python34\geckodriver.exe'
    # driver = webdriver.Firefox(ff_webdriver_server_path)

    driver.get("http://www.baidu.com")
    search_input_element = driver.find_element_by_id('kw')
    search_input_element.send_keys("WebDriver")
    search_input_element.send_keys(Keys.ENTER)

    page_element = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.ID, "page"))
    )

    second_page_element = driver.find_element_by_css_selector("#page a")
    second_page_element = driver.find_element_by_class_name("n")
    second_page_element.click()

    search_content_element = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.ID, "11")),
        message='Can not find div 11 at 10 seconds, case failure!'
    )

    for i in range(11, 21):
        content_div = driver.find_element_by_id(str(i))
        title = str(content_div.find_element_by_css_selector(".t a").text)
        print (title)

        if ('webdriver' not in title.lower()) and ('selenium' not in title.lower()):
            test_result = False
            print ('Can not find webdriver or selenium keyword from title! Test case will failure!')
            break

        if 'WebDriver - Mozilla | MDN' not in title:
            continue
        else:
            keyword_index = i - 10
            test_result = True

    print ('=======================Test Result=======================')

    if test_result:
        print ('Test case pass!')
        print ('Find keyword "WebDriver - Mozilla | MDN", ' \
              'it was in index %d search result! Test case pass!' % keyword_index)
    else:
        print ('Test case fail!')

    driver.close()
    driver.quit()
