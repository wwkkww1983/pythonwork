#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: click_compile
# Author:    fan
# date:      2019/6/19 019
# -----------------------------------------------------------
from pywinauto import application
import pyautogui
from time import sleep
from mylog import mylog
from make_time_formated import nowtimestr

click = pyautogui.click
CLICK_LOCATION = {
    "打开工程": (80, 15),
    "编译": (1045, 65)
}
# pi_path = r"D:\Program Files\WECONSOFT\PIStudio\20190313发布\HMIEditor.exe"
# project_path = r"E:\PROJECTS\HMIProject-编译崩溃自动测试\HMIProject-编译崩溃自动测试.pi"
# n = 5  # 点击编译次数
# interval = 5  # 编译等待时间

print("提示：文件路径可通过拖动文件到光标处快速输入文件路径（引号可不删除。"
      "在WINDOWS 10系统上，可能需要以管理员身份运行程序并手动输入参数。）")
pi_path = input("请输入PIStudio HMIEditor.exe文件路径\n:")
project_path = input("请输入工程.pi文件路径\n:")
n = input("请输入测试次数\n:")
n = int(n)
interval = input("请输入编译等待时间（秒）\n:")
interval = int(interval)

if pi_path[0] == '"' and pi_path[-1] == '"':
    pi_path = pi_path[1:-1]
if project_path[0] == '"' and project_path[-1] == '"':
    project_path = project_path[1:-1]

mylog("{}, 开始测试".format(nowtimestr()))

app = application.Application()
app.start(pi_path)
win = app.top_window()
win.maximize()  # 窗口最大化
# win.minimize()  # 窗口最小化
sleep(5)
click(*CLICK_LOCATION["打开工程"])
win_open = app["打开"]
win_open[u'文件名(&N):Edit'].SetText(project_path)
win_open['打开(&O)Button'].Click()
sleep(3)
win = app.top_window()
i = 1
while i <= n:
    click(*CLICK_LOCATION["编译"])
    sleep(interval)
    mylog("{}, 编译点击次数{}/{}".format(nowtimestr(), i, n))
    i += 1
input("测试结束, 输入任意键退出。")
if __name__ == '__main__':
    pass
