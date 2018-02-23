# !/usr/bin/env python3
# coding: utf-8
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

__author__ = 'fan'


class DoSomething(object):
    """
    open some web pages and search key words.
    Then return the index of these key words
    """

    def __init__(self):
        pass

    def setup(self, driver_path, web_url):
        self.driver_path = driver_path
        self.url = web_url
        self.driver = webdriver.Ie(driver_path)
        self.driver.get(self.url)

    def send_key_word(self, kw_id, keywords):
        self.keywords = keywords
        self.kw_id = kw_id
        self.search_id = self.driver.find_element_by_id(self.kw_id)
        self.search_id.send_keys(self.keywords)
        self.search_id.send_keys(Keys.ENTER)

    def find_index(self, message_, words='zTree', pages='page'):
        test_result = False
        keyword_index = -1
        self.words = words
        self.message = message_
        self.exp_condition = expected_conditions.presence_of_element_located((By.ID, pages))
        self.wait = WebDriverWait(self.driver, 10).until(self.exp_condition, self.message)
        for i in range (1, 11):
            content_div = self.driver.find_element_by_id(str(i))
            title = str(content_div.find_element_by_css_selector('.t a').text)
            print(title)

            if (self.keywords not in title.lower()):
                test_result = False
                print('Fail to find %s from page 1. Test case failed' % self.keywords)
                break

            if self.words not in title:
                continue

            else:
                keyword_index = i
                test_result = True

        print('==================================Test Report=====================================')

        if test_result:
            print("""\
            Test case pass
            Find keyword %s in index %d of searching pages
            Test case pass""" % (self.words, keyword_index))

        else:
            print('Test case failed')

    def close(self):
        self.driver.close()
        self.driver.quit()


if __name__ == '__main__':
    path = r'C:\Python34\IEDriverServer.exe'
    url = 'www.baidu.com'
    do_baidu = DoSomething()
    do_baidu.setup(path, url)

    time.sleep(1)
    do_baidu.send_key_word('kw', 'webdriver')

    time.sleep(1)
    message = 'Can not find div 1 at 10 seconds, case failure!'
    do_baidu.find_index(message)

    time.sleep(1)
#    do_baidu.close()




