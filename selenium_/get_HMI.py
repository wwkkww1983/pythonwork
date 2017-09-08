
# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from selenium import webdriver
import time
import base64
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions


def open_project(httppath):
    """打开工程网页"""
    ie_webdriver_server_path = r'C:\Python\Python34\IEDriverServer.exe'
    browser = webdriver.Ie(ie_webdriver_server_path)
    browser.get(httppath)
    return browser


def make_filelist(proj):
    elem = WebDriverWait(proj, 10).until(
        expected_conditions.presence_of_element_located((By.ID, "NODE_0DSPL_20")))

    # print(elem)
    svg = elem.get_attribute('src')
    #print('svg\n', svg)
    head = len('data:image/svg+xml;base64,')
    #print('attitude head len:\n', head)
    svgfile = svg[head:]
    #print('svgfile:\n', svgfile)
    svgg = base64.b64decode(svgfile)
    #print('svggg:\n', svgg)
    string = svgg.decode()
    #print('string\n', string)
    soup = BeautifulSoup(svgg, "html.parser")
    #print('soup\n', soup)
    gs = soup.find_all('text')
    print(gs)

if __name__ == "__main__":
    project = open_project(r"http://192.168.22.61/")
    time.sleep(3)
    make_filelist(project)
