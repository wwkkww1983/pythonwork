
# !/usr/bin/env python
# _*_ coding: utf-8 _*_

import time
import base64
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys


def open_browser():
    browser = webdriver.Firefox()
    return browser


def open_project(brsr, httppath):
    """打开工程网页"""
    brsr.get(httppath)
    return brsr

def check_hmi(proj):
    hmi_alive = False
    hmi_date = ''
    hmi_time = ''
    elem = None
    try:
        elem = WebDriverWait(proj, 20).until(
            expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div")))
    except Exception as e:
        print(e)
    if not elem:
        hmi_alive = False
    else:
        hmi_alive = True
        divs = proj.find_elements_by_xpath("/html/body/div")
        div_ids = {}
        div_scrnos = {}
        div_id = ''
        s = 1
        for i in range(len(divs)):
            try:
                div_ids[i] = divs[i].get_attribute('id')
                div_scrnos[i] = divs[i].get_attribute('scrno')
                if div_scrnos[i]:
                    div_id = div_ids[i]
                    break

                # print(i, div_ids[i], div_scrnos[i])
                s += 1
            except Exception as e:
                print(e)
        # print(div_id)
        span_ids = {}
        span_texts = {}

        spans = proj.find_elements_by_xpath("/html/body/div[{}]/span".format(s))
        for i in range(len(spans)):
            try:
                span_ids[i] = spans[i].get_attribute('id')
                span_texts[i] = spans[i].text
                # print(i, span_ids[i], span_texts[i])
            except Exception as e:
                print(e)

        for i in range(len(spans)):
            if 'DD' in span_ids[i]:
                hmi_date = span_texts[i]
                # print(hmi_date)
            else:
                pass
            if 'TIME' in span_ids[i]:
                hmi_time = span_texts[i]
                # print(hmi_time)
            else:
                pass
    # print('this hmi alive is {}, hmi current time: {} {}'.format(hmi_alive, hmi_date, hmi_time))
    return hmi_alive, hmi_date, hmi_time

    # for elem in elems:
    #     div_ids.append(elem.id)
    # print(div_ids)


    # if elem:
    #     date_elem = WebDriverWait(proj, 10).until(
    #         expected_conditions.presence_of_element_located((By.ID, 'SPAN_1DD_1_Comm')))
    #     print(date_elem.text)
    #     time_elem = WebDriverWait(proj, 10).until(
    #         expected_conditions.presence_of_element_located((By.ID, 'SPAN_2TIME_2_Comm')))
    #     print(time_elem.text)


    # # print(elem)
    # svg = elem.get_attribute('src')
    # # print('svg\n', svg)
    # head = len('data:image/svg+xml;base64,')
    # # print('attitude head len:\n', head)
    # svgfile = svg[head:]
    # # print('svgfile:\n', svgfile)
    # svgg = base64.b64decode(svgfile)
    # # print('svggg:\n', svgg)
    # string = svgg.decode()
    # # print('string\n', string)
    # soup = BeautifulSoup(svgg, "html.parser")
    # print('soup\n', soup)
    # gs = soup.find_all('text')
    # print(gs)
    # for i in gs:
    #     filelist.append(i.get_text())
    # print(filelist)
if __name__ == "__main__":
    # project = open_project(r"http://192.168.22.61/")
    hmiurl = r"http://d3bbfa1084f1a5eb107baf22a622a32e.hmi.we-con.com.cn:9999/"
    hmitempname = hmiurl[-28:-24]
    browser = open_browser()
    project = open_project(browser, hmiurl)
    time.sleep(3)
    hmialive, hmidate, hmitime = check_hmi(project)
    print('hmi:{} alive is {}, hmi current time: {} {}'.format(hmitempname, hmialive, hmidate, hmitime))
    time.sleep(1)
    project.quit()

