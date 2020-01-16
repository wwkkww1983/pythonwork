#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: easy_use
# Author:    fan
# date:      2019/2/18 018
# -----------------------------------------------------------
from appium import webdriver
from time import sleep
from make_time_formated import *


def driver_init(appactivity, apppackage):
    desired_caps = dict()
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '6.0.1'
    desired_caps['deviceName'] = '127.0.0.1:7556'
    desired_caps['unicodeKeyboard'] = 'True'
    desired_caps['resetKeyBoard'] = 'True'
    desired_caps['appActivity'] = appactivity
    desired_caps['appPackage'] = apppackage
    desired_caps['noReset'] = 'True'
    dri = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    return dri


def qq_login(driver: webdriver):
    sleep(1)
    driver.find_element_by_id('com.tencent.mobileqq:id/btn_login').click()
    driver.find_element_by_name("QQ号/手机号/邮箱").clear()
    driver.find_element_by_name("QQ号/手机号/邮箱").send_keys("1780123846")
    driver.find_element_by_id("com.tencent.mobileqq:id/password").clear()
    driver.find_element_by_id("com.tencent.mobileqq:id/password").send_keys('wecon123')
    driver.find_element_by_id("com.tencent.mobileqq:id/login").click()


def vbox_login(driver: webdriver):
    sleep(1)
    # driver.find_element_by_id('com.weikong.vbox:id/user').send('test_fann')
    driver.find_elements_by_class_name('android.widget.EditText')[2].send('test_fann')


if __name__ == '__main__':
    # package = 'com.weikong.vbox'
    # activity = 'io.dcloud.PandoraEntry'
    package = 'com.tencent.mobileqq'
    activity = '.activity.SplashActivity'

    driver = driver_init(activity, package)

    qq_login(driver)
    # vbox_login(driver)
