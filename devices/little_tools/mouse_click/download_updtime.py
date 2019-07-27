#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: download_updtime
# Author:    fan
# date:      2019/7/13 013
# -----------------------------------------------------------

from pywinauto import application
from time import sleep
from mylog import mylog
from make_time_formated import nowtimestr

with open("log.txt", "w", encoding="utf-8") as f:
    f.write("测试记录\n")
downloadexepath = input("请输入download.exe完整路径\n>")
if downloadexepath[0] == '"' and downloadexepath[-1] == '"':
    pi_path = downloadexepath[1:-1]
app = application.Application()
app_plceditor = app.connect(title="Wecon PLC Editor - 软元件监视-1")
win = app_plceditor["修改软元件值"]
app_download = app.start(downloadexepath)
mylog("{}, 测试开始".format(nowtimestr()))


def start():
    win["ON"].click()
    sleep(20)
    app_download.top_window()[r"更新HMI时间(&T)"].click()
    sleep(1)
    app_download.top_window()["是"].click()
    sleep(1)
    app_download.top_window()["确定"].click()
    sleep(3)
    win["OFF"].click()
    sleep(2)

if __name__ == '__main__':
    i = 1
    while i < 20000:
        start()
        mylog("{}, count:{}/20000".format(nowtimestr(), i))
        i += 1
    input("输入任意键退出")
