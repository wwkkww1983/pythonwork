
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
from datetime import datetime as dt
import logging as log
# from selenium.webdriver.common.keys import Keys

log.basicConfig(filename=os.path.join(os.getcwd(), 'log.txt'),
                level=log.INFO,
                format='%(asctime)s %(levelname)s: %(message)s')


def open_browser():
    browser = webdriver.Firefox()
    # browser.set_window_size(400, 300)
    return browser


def open_project(brsr, httppath):
    """打开工程网页"""
    try:
        for i in range(10):
            brsr.get(httppath)
            try:
                text = brsr.find_element_by_xpath("/html/body/pre")
                if 'not found' not in text.text:
                    break
                else:
                   pass
            except:
                break
            time.sleep(1)
    except Exception as e:
        log.error('open remote hmi webpage fail: {}'.format(httppath))
        print(e)
        return None
    return brsr


def check_hmi(proj):
    hmi_alive = False
    hmi_date = 'None'
    hmi_time = 'None'
    check_info = '-'
    elem = None
    if not proj:
        check_info = '打开连接失败'
        log.info(check_info)
        print(proj)
        # 无法获取目标页面
        return hmi_alive, hmi_date, hmi_time, check_info
    else:
        try:
            elem = WebDriverWait(proj, 5).until(
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
                        div_id = ''
                        s = 1
                        for i in range(len(divs)):
                            div_ids[i] = divs[i].get_attribute('id')
                            div_scrnos[i] = divs[i].get_attribute('scrno')
                            if div_scrnos[i]:
                                div_id = div_ids[i]
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
                    check_info = '查找date/time部件失败'
                    # log.info(check_info)
                    print(e)
        except Exception as e:
            # 无法获得对应HMI的网页，退出当前连接
            check_info = '查找网页div元素失败， 连接失败'
            print(e)
            # log.error(check_info)
            return hmi_alive, hmi_date, hmi_time, check_info
    return hmi_alive, hmi_date, hmi_time, check_info

if __name__ == "__main__":
    log.info('hmi checking format: [hmi name] [alive] [date str] [time str] [info]')
    hmiurl = r"http://d3bbfa1084f1a5eb107baf22a622a32e.hmi.we-con.com.cn:9999/"
    hmitempname = hmiurl[-28:-24]
    browser = open_browser()
    project = open_project(browser, hmiurl)
    time.sleep(3)
    hmialive, hmidate, hmitime, checkinfo = check_hmi(project)
    log.info('[{}], [{}], [{}], [{}], [{}]'.format(hmitempname, hmialive, hmidate, hmitime, checkinfo))
    time.sleep(1)
    try:
        project.quit()
        log.info('浏览器已关闭')
    except:
        log.error('浏览器异常关闭')

