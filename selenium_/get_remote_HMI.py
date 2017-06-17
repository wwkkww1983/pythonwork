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
    elem = hmi.find_element_by_id("NODE_0FS_69")
    if elem is None:
        print('element not found')
    else:
        elem.click()

def get_datetime(hmi, id1, id2 ):
    elem_time = hmi.find_element_by_id(id1)
    elem_date = hmi.find_element_by_id(id2)
    if elem_time is None or elem_date is None:
        print('element not found')
    else:
        return elem_date.text+' '+elem_time.text

def timetologhmitime():
    pc_time = time.strftime('%Y.%m.%d %H:%M:%S', time.localtime())
    time_second = int(pc_time[-2:])
    if time_second%10 != 0:
        pass
    else:
        return pc_time

if __name__ == "__main__":
    # Iedriver = r'..\selenium_drivers\IEDriverServer.exe'
    # Chromedriver = r'..\selenium_drivers\geckodriver.exe'
    hmi_ = open_project(r"http://7f46ce7c04e3610da39e89793a2573e1.hmi.we-con.com.cn:9999/")
    time.sleep(5)
    # button_click(hmi_)
    id1 = 'SPAN_0TIME_63'
    id2 = 'SPAN_0DD_62'

    command = input('输入‘start’ 开始记录; 输入‘stop’停止记录')
    while command:
        if command == 'stop':
            break
        else:
            t = get_datetime(hmi_, id1, id2)
            d = timetologhmitime()
            if d is None:
                pass
            else:
                print('local time: ' + d + ' logged HMI time: ' + t, 'HMI is connected well')
                time.sleep(1.1)


