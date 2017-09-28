#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name：     connect_to_topwin.py
# Description :
#   Author:      fan
#   date:        2017/9/28
#   IDE:         PyCharm Community Edition
# -----------------------------------------------------------

from pywinauto import application
from time import sleep

app = application.Application()
win = None


def connectapp(app_handle):
    global app
    app = application.Application()
    app.connect(handle=app_handle)
    print(app)


def getwin(win_title, win_class_name):
    global win
    wintitle = win_title
    winclassname = win_class_name
    win = app.window(title=wintitle, class_name=winclassname)
    print(win)
    print(win.print_control_identifiers())
    print(win['ListBox1'].ItemTexts(), '\n', win['ListBox2'].ItemTexts(), '\n', win['ListBox3'].ItemTexts())


def runelem(list_type_element):
    elem = list_type_element
    pics = win[elem].ItemTexts()
    count = 1
    pics.append('end')
    for i in pics:
        sleep(.1)
        if i == '':
            print('start')
        if i == 'end':
            count = 0
            print('end')
        else:
            win[elem].Select(i)
            print(count)
            count += 1

if __name__ == '__main__':
    levihandle = 0x002D0AAA
    tukutitle = u'工程位图图库'
    tukuclassname = u'#32770'
    connectapp(levihandle)
    getwin(tukutitle, tukuclassname)
    runelem('ListBox1')
