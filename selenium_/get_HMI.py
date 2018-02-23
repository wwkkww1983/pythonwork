
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


def open_project(httppath):
    """打开工程网页"""
    browser = webdriver.Firefox()
    browser.get(httppath)
    return browser


def make_filelist(proj):
    filelist = []
    elem = WebDriverWait(proj, 10).until(
        expected_conditions.presence_of_element_located((By.ID, "NODE_0DSPL_19")))

    # print(elem)
    svg = elem.get_attribute('src')
    # print('svg\n', svg)
    head = len('data:image/svg+xml;base64,')
    # print('attitude head len:\n', head)
    svgfile = svg[head:]
    # print('svgfile:\n', svgfile)
    svgg = base64.b64decode(svgfile)
    # print('svggg:\n', svgg)
    string = svgg.decode()
    # print('string\n', string)
    soup = BeautifulSoup(svgg, "html.parser")
    print('soup\n', soup)
    gs = soup.find_all('text')
    print(gs)
    for i in gs:
        filelist.append(i.get_text())
    print(filelist)
if __name__ == "__main__":
    # project = open_project(r"http://192.168.22.61/")
    project = open_project(r"http://35702dcc66ee7e0132ee71c7b21e256f.hmi.we-con.com.cn:9999/")
    time.sleep(3)
    make_filelist(project)
