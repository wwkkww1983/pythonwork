
# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from selenium import webdriver
import time


def open_project(httppath):
    """打开工程网页"""
    http_path = httppath
    browser = webdriver.Firefox()
    browser.get(http_path)
    return browser


def button_click(hmi):
    elem = hmi.find_element_by_id("NODE_0BS_109")
    for i in range(100):
        elem.click()
        time.sleep(.5)


if __name__ == "__main__":
    hmi_ = open_project(r"http://192.168.10.228/")
    time.sleep(3)
    button_click(hmi_)
