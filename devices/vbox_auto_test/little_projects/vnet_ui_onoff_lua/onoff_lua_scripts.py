#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: onoff_lua_scripts
# Author:    fan
# date:      2019/7/13 013
# -----------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class VnetWebUi(object):
    def __init__(self):
        self.driver = webdriver.Firefox()

    def open_page(self):
        driver = self.driver
        driver.get("http://rc.v-box.net:8080/box-web/web/html/user/login.html")
        driver.find_element_by_id("alias").click()
        driver.find_element_by_id("alias").clear()
        driver.find_element_by_id("alias").send_keys("test_fan")
        driver.find_element_by_id("password").click()
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("123456")
        driver.find_element_by_id("login").click()
        WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, u"(.//*[normalize-space(text()) and normalize-space(.)='添加V-BOX'])[2]/following::span[1]")
            )
        ).click()
        time.sleep(5)
        driver.find_element_by_id("spanid_842").click()

        time.sleep(1)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='默认组'])[1]/following::span[6]"
        ).click()

        time.sleep(10)
        driver.switch_to.frame(0)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='历史数据'])[1]/following::div[2]"
        ).click()

        # elem = WebDriverWait(driver, 10).until(
        #     expected_conditions.presence_of_element_located(
        #         (By.XPATH, u"(.//*[normalize-space(text()) and normalize-space(.)='历史数据'])[1]/following::div[2]")))
        # elem.click()

        # driver.find_element_by_xpath(
        #     u"(.//*[normalize-space(text()) and normalize-space(.)='添加V-BOX'])[2]/following::span[1]").click()
        # driver.find_element_by_id("spanid_842").click()
        # driver.find_element_by_xpath(
        #     u"(.//*[normalize-space(text()) and normalize-space(.)='默认组'])[1]/following::span[6]").click()
        # # ERROR: Caught exception [ERROR: Unsupported command [selectFrame | index=0 | ]]
        # driver.find_element_by_xpath(
        #     u"(.//*[normalize-space(text()) and normalize-space(.)='历史数据'])[1]/following::div[2]").click()
        # time.sleep(5)
        # driver.find_element_by_xpath(
        #     u"(.//*[normalize-space(text()) and normalize-space(.)='定时执行'])[1]/following::span[1]").click()
        # time.sleep(5)
        # driver.find_element_by_xpath(
        #     u"(.//*[normalize-space(text()) and normalize-space(.)='定时执行'])[1]/following::span[1]").click()

        driver.switch_to.frame(0)
        WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, u"(.//*[normalize-space(text()) and normalize-space(.)='定时执行'])[1]/following::span[1]")
            )
        ).click()
        WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH,u"(.//*[normalize-space(text()) and normalize-space(.)='定时执行'])[1]/following::span[1]")
            )
        ).click()

    def onoff_scripts(self):
        driver = self.driver
        time.sleep(5)
        driver.switch_to.frame(0)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='定时执行'])[1]/following::span[1]").click()
        time.sleep(5)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='定时执行'])[1]/following::span[1]").click()


if __name__ == '__main__':
    ui = VnetWebUi()
    ui.open_page()
    # ui.onoff_scripts()

