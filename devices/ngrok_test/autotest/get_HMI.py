
# !/usr/bin/env python
# _*_ coding: utf-8 _*_

import time
# import base64
# from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import logging as log
# from selenium.webdriver.common.keys import Keys

log.basicConfig(filename=os.path.join(os.getcwd(), 'log.txt'),
                level=log.INFO,
                format='%(asctime)s %(levelname)s: %(message)s')
NUM_KEYB = {'0': 'SPAN_1000KY_3_1000',
            '1': 'SPAN_1000KY_5_1000',
            'CLR': 'SPAN_1000KY_12_1000',
            'ESC': 'SPAN_1000KY_13_1000',
            'ENTER': 'SPAN_1000KY_23_1000'}


def open_browser():
    browser = webdriver.Firefox()
    # browser.set_window_size(400, 300)
    return browser


def open_project(brsr: webdriver, httppath):
    """打开工程网页"""
    try:
        for i in range(3):
            brsr.get(httppath)
            time.sleep(3)
            try:
                text = brsr.find_element_by_xpath("/html/body/pre")
                if 'not found' not in text.text:
                    break
                else:
                   pass
            except:
                break
    except Exception as e:
        log.error('open remote hmi webpage fail: {}, {}'.format(httppath, e))
        return None
    return brsr


def check_hmi(proj: webdriver):
    # 尝试查找页面元素并返回用于判断页面存在的信息
    hmi_alive = False
    hmi_date = '-'
    hmi_time = '-'
    check_info = '-'
    if not proj:
        # 无法获取目标页面
        check_info = 'fail to open the url'
        log.info(check_info)
        print(proj)
        return hmi_alive, hmi_date, hmi_time, check_info
    else:
        try:
            elem = WebDriverWait(proj, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div")))
            if not elem:
                pass
            else:
                hmi_alive = True
                try:
                    divs = proj.find_elements_by_xpath("/html/body/div")
                    if divs:
                        div_ids = {}
                        div_scrnos = {}
                        span_ids = {}
                        span_texts = {}
                        # div_id = ''
                        s = 1
                        for i in range(len(divs)):
                            div_ids[i] = divs[i].get_attribute('id')
                            div_scrnos[i] = divs[i].get_attribute('scrno')
                            if div_scrnos[i]:
                                # div_id = div_ids[i]
                                break
                            # print(i, div_ids[i], div_scrnos[i])
                            s += 1
                        # print(div_id)
                        spans = proj.find_elements_by_xpath("/html/body/div[{}]/span".format(s))
                        for i in range(len(spans)):
                            span_ids[i] = spans[i].get_attribute('id')
                            span_texts[i] = spans[i].text
                            if 'DD' in span_ids[i]:
                                hmi_date = span_texts[i]
                            if 'TIME' in span_ids[i]:
                                hmi_time = span_texts[i]
                            # print(i, span_ids[i], span_texts[i])
                except Exception as e:
                    # 查找第一个div元素失败 = HMI未在线
                    check_info = 'date part not found'
                    # log.error(check_info)
        except Exception as e:
            # 无法获得对应HMI的网页，退出当前连接
            check_info = 'div not found'
            # log.error(check_info)
            return hmi_alive, hmi_date, hmi_time, check_info
    return hmi_alive, hmi_date, hmi_time, check_info


def click_button(proj: webdriver, y):
    button = {0: 'SPAN_0BS_0_0',
              1: 'SPAN_0BS_1_0',
              2: 'SPAN_0BS_2_0',
              3: 'SPAN_0BS_3_0',
              4: 'SPAN_0BS_4_0',
              5: 'SPAN_0BS_5_0',
              6: 'SPAN_0BS_6_0',
              7: 'SPAN_0BS_0_0', }
    div = proj.find_element_by_xpath('/html/body/div[@id="divfrm0"]/span[@id="{}"]'.format(button[0]))
    div.click()
    # print(div.get_attribute('src'), div.get_attribute('id'))


def type_num(proj: webdriver, num_str):
    proj.find_element_by_id(NUM_KEYB['CLR'])
    time.sleep(0.5)
    for i in list(num_str):
        proj.find_element_by_id(NUM_KEYB[i]).click()
        time.sleep(0.5)
    time.sleep(0.5)
    proj.find_element_by_id(NUM_KEYB['ENTER']).click()


def set_num_value(proj: webdriver, num_str: str):
    y = list(num_str)
    num_str_new = ''.join([y.pop() for i in range(8)])
    type_num(proj, num_str_new)


if __name__ == "__main__":
    # log.info('hmi checking format: [hmi name] [alive] [date str] [time str] [info]')
    # hmiurl = r"http://d3bbfa1084f1a5eb107baf22a622a32e.hmi.we-con.com.cn:9999/"
    # hmitempname = hmiurl[-28:-24]
    hmiurl = 'http://192.168.39.23'
    browser = open_browser()
    project = open_project(browser, hmiurl)
    time.sleep(2)
    # time.sleep(3)
    # hmialive, hmidate, hmitime, checkinfo = check_hmi(project)
    # log.info('[{}], [{}], [{}], [{}], [{}]'.format(hmitempname, hmialive, hmidate, hmitime, checkinfo))
    # time.sleep(1)
    # try:
    #     project.quit()
    #     log.info('browser closed safely.')
    # except:
    #     log.error('broser closed ERROR.')
    set_num_value(project, '01111101')
