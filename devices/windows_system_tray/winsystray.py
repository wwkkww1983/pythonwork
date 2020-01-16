#!usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: winsystray
# Author:    fan
# date:      2019/12/26
# -----------------------------------------------------------
from PyQt5.QtWidgets import QSystemTrayIcon, QApplication
from PyQt5.QtGui import QIcon
import sys
from make_time_formated import *
from datetime import datetime
from pytz import timezone


def set_systray():
    systray = QSystemTrayIcon()
    systray.setIcon(QIcon("E:\MyWorkPlace\pythonwork\devices\windows_system_tray\systray.png"))
    # systray.setToolTip("Warframe")
    while True:
        systray.setToolTip("""
    本地时间：{}
    地球平原时间：{}，倒计时：{}
    金星平原天气：{}，倒计时：{}
    """.format(1,2,3,4,5))
        systray.show()
        time.sleep(1)


def update_info():
    _fmt = '%Y-%m-%d %H:%M:%S'
    nowtime = nowtimestr(fmt=_fmt)
    tz_useastern = timezone("US/Eastern")
    dt_useastern = datetime.now(tz=tz_useastern)
    print(nowtime)
    print(dt_useastern.strftime(_fmt))

if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # set_systray()
    # sys.exit(app.exec_())
    update_info()
