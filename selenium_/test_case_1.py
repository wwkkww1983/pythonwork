# !/usr/bin/env python3
# coding: utf-8

import  target_work_via_class
import time


path = r'C:\Users\fan\OneDrive\pythonwork\selenium_\selenium_drivers\IEDriverServer.exe'
url = 'www.baidu.com'
test = target_work_via_class.DoSomething()
test.setup(path, url)
time.sleep(5)
test.close()