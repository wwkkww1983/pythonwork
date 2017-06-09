# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from selenium import webdriver
import time


if __name__ == "__main__":

    browser = webdriver.Firefox()
    browser.get("https://www.baidu.com/")
    assert "百度" in browser.title

    elem = browser.find_element_by_id('kw')
    elem.send_keys("selenium")
    browser.find_element_by_id('su').click()
    time.sleep(2)

    browser.close()
    browser.quit()
