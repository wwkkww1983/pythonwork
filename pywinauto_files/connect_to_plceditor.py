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


def getwindow(app, window_title=r'Wecon PLC Editor'):
    result = False
    mwindow = app.window(title=window_title)
    if mwindow.exists(timeout=3):
        result = True
        mwindow.print_control_identifiers()
    else:
        pass
    return 'return {1} while trying to find window or dialog: "{1}" '.format(result, window_title)


def modifydata():
    modi_window = findwindows.find_window(title=r'修改软元件值')
    print(modi_window)


if __name__ == '__main__':
    # app_path = r'D:\Program Files\WECONSOFT\PLC Editor\1.3.3 3VM支持\PLCEditor.exe'
    # target_app = open(app_path)
    target_app = connect(r'Wecon PLC Editor - 软元件监视-1')
    time.sleep(3)
    flag = getwindow(target_app, r'修改软元件值')
    print(flag)