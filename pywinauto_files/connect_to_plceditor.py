#! /usr/bin/env python
# coding=utf-8


import time
from pywinauto import application, findwindows


def open(apath):
    app = application.Application()
    app.start(apath)
    return app


def connect(title_name):
    app = application.Application()
    app.connect(title=title_name)
    return app


def getwindow(app):
    alive = False
    mwindow = app.window(title=r'Wecon PLC Editor - 软元件监视-1')
    if mwindow.exists(timeout=3):
        alive = True
        mwindow.print_control_identifiers()
    else:
        pass
    return alive


if __name__ == '__main__':
    # app_path = r'D:\Program Files\WECONSOFT\PLC Editor\1.3.3 3VM支持\PLCEditor.exe'
    # target_app = open(app_path)

    target_app = connect(r'Wecon PLC Editor - 软元件监视-1')
    time.sleep(3)
    flag = getwindow(target_app)
    print(flag)