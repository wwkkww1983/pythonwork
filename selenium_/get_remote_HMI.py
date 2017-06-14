
# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from selenium import webdriver
import time


def open_project(httppath, driver):
    """打开工程网页"""
    http_path = httppath
    browser = webdriver.Chrome(driver)
    browser.get(http_path)
    return browser


def button_click(hmi):
    elem = hmi.find_element_by_link_text("浏览")
    if elem is None:
        print('element not found' )
    else:
        elem.click()
        time.sleep(.5)


if __name__ == "__main__":
    # Iedriver = r'..\selenium_drivers\IEDriverServer.exe'
    Chromedriver = r'..\selenium_drivers\geckodriver.exe'
    hmi_ = open_project(r"http://weconcloud.com/main", Chromedriver)
    time.sleep(5)
    button_click(hmi_)
