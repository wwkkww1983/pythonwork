#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: do_visiting_vbox
# Author:    fan
# date:      2018/5/15
# -----------------------------------------------------------
import time
# import base64
# from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from datetime import datetime as dt
import logging as log
# from selenium.webdriver.common.keys import Keys

log.basicConfig(filename=os.path.join(os.getcwd(), 'log.txt'),
                level=log.INFO,
                format='%(asctime)s %(levelname)s: %(message)s')


class VboxVist(object):
    def __init__(self):
        self.browser = None
        self.login_page = "http://www.v-box.net/web/html/user/login.html"
        self.index_page = "http://www.v-box.net/index.html"

    def open_browser(self):
        browser = webdriver.Firefox()
        # browser.set_window_size(400, 300)
        self.browser = browser
        return browser

    def open_page(self, page_address):
        """打开工程网页"""
        brsr = self.browser
        if page_address == "login":
            page_address = self.login_page
        if page_address == "index":
            page_address = self.index_page
        try:
            for i in range(1):
                brsr.get(page_address)
                time.sleep(3)
        except Exception as e:
            log.error('open v-box home address fail: {}, {}'.format(page_address, e))
            return None
        self.browser = brsr
        return brsr

    def do_login(self):
        self.open_page("login")
        brsr = self.browser
        time.sleep(5)
        ele_username = brsr.find_element_by_id("alias")
        ele_username.send_keys("test_fan")
        ele_username = brsr.find_element_by_id("password")
        ele_username.send_keys("123456")
        ele_username = brsr.find_element_by_id("login")
        ele_username.click()

    def do_quit(self):
        time.sleep(10)
        self.open_page("index")
        brsr = self.browser


if __name__ == '__main__':
    box = VboxVist()
    box.open_browser()
    # box.open_page("login")

    box.do_login()
    box.do_quit()

    # box.open_browser().find_element_by_id("").send_keys()