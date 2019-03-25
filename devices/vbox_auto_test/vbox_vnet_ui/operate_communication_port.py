#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: operate_communication_port
# Author:    fan
# date:      2019/3/25 025
# 通讯口增删改部分UI识别复杂，不继续进行
# -----------------------------------------------------------
import time
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select  # 处理下拉列表


browser = webdriver.Firefox()
# browser.set_window_size(400, 300)

browser.get(r"http://rc.v-box.net:8080/box-web200/index.html#")
time.sleep(5)
browser.find_element_by_id("alias").send_keys("test_fan")
browser.find_element_by_id("password").send_keys("123456")
browser.find_element_by_id("login").click()
time.sleep(5)
browser.find_element_by_id("dir_a_842").click()
browser.find_element_by_id("box_148").click()
browser.switch_to_frame(0)
time.sleep(5)
browser.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='远程下载'])[1]/following::i[1]").click()
time.sleep(5)
browser.switch_to_frame(0)
browser.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='基本信息'])[1]/following::font[1]").click()
time.sleep(5)
browser.find_element_by_xpath(
    "(.//*[normalize-space(text()) and normalize-space(.)='您配置"
    "与V-BOX与相连通的设备（比如：PLC品牌及型号，数据采集模块，PID"
    "控制表或MODBUS标准协议等）'])[1]/following::font[1]"
).click()  # 添加按钮
time.sleep(2)
browser.find_element_by_id("select2-chosen-1").click()  # 选择通讯口
browser.find_element_by_id("select2-result-label-3").click()
  # 选择通讯口-选中
browser.find_element_by_id("select2-chosen-2").click()  # 设备类型
browser.find_element_by_id("select2-result-label-11").click()  # 设备类型-选中
browser.find_element_by_id("type").click()  # 驱动名称




# 添加串口操作


if __name__ == '__main__':
    pass
