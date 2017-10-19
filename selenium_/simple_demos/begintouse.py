# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time


if __name__ == "__main__":

    # browser = webdriver.Firefox(r'C:\Python34\geckodriver.exe')
    browser = webdriver.Firefox()
    browser.maximize_window()

    action = ActionChains(browser)
    browser.get("https://www.baidu.com/")
    assert "百度" in browser.title

    keyword = browser.find_element_by_id('kw')
    locate1 = keyword.location

    dosearch = browser.find_element_by_id('su')

    locate2 = dosearch.location
    print('kw', locate1, 'su', locate2)
    time.sleep(1)
    # action.move_to_element(keyword)
    # action.send_keys('abcd')
    action.move_to_element(dosearch)
    # action.move_by_offset(locate1['x'], locate1['y'])
    # action.move_by_offset(locate2['x'], locate2['y'])
    # action.click()
    # action.perform()

    # keyword.send_keys('webdriver')
    # action = ActionChains(browser)
    # action.move_to_element(keyword)
    action.click_and_hold(dosearch)
    action.perform()
    time.sleep(10)
    action.reset_actions()
    action.release(dosearch)
    action.perform()

    time.sleep(2)
    browser.close()
    browser.quit()
