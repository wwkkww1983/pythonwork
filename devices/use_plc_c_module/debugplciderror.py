#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: debugplciderror
# Author:    fan
# date:      2018/3/14
# -----------------------------------------------------------
from bushound import BUSHOUND
from plceditor import PLCEDITOR
from time import sleep

if __name__ == '__main__':
    bus = BUSHOUND()
    bus.create_app()
    bus.get_mwin()
    bus.get_toolbar()
    bus.run_monitor()
    sleep(3)

    editor = PLCEDITOR()
    editor.create_app()
    editor.get_mwin()
    # editor.go_online_write()
    # editor.get_mwin()
    i = 0
    while i < 1:
        editor.app['梯形图（监控写入）'].Wait('ready', 5)
        editor.app['梯形图（监控写入）'].SendKeys('666')
        # if i % 2 == 0:
        #     bus.save_log()
        sleep(5)
        i += 1
