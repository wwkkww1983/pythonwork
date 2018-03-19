#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: bushound.py
# Author:    fan
# date:      2018/3/14
# -----------------------------------------------------------
import os
import shutil
import time
from toolbarmapping import get_x_y
from pywinauto import application, mouse, findbestmatch

class BUSHOUND(object):

    def __init__(self):
        self.app = None
        self.mwin = None
        self.ladder_name = ''
        self.processname = 'bushound.exe'
        self.wintitle = ''

    def _get_pid(self):
        f = os.popen('tasklist')
        try:
            for line in f:
                if line != '\n':
                    line = line[:-1]
                    if self.processname in line:
                        for word in line.split(' '):
                            if word.isdigit():
                                return int(word)
        except Exception as e:
            print(e)
            return None

    def create_app(self):
        app = application.Application()
        app.connect(process=self._get_pid())
        self.app = app

    def get_mwin(self):
        mwin = self.app['Bus Hound']
        self.mwin = mwin
        return mwin

    def get_toolbar(self):
        mwin = self.app['Bus Hound']
        toolbar = mwin['Toolbar']
        self.toolbar = toolbar
        return toolbar

    def toolbar_click(self, buttname):
        buttmap = {'capture': 0,
                   'save': 1,
                   'setting': 2,
                   'device': 3,
                   'help': 4,
                   'exit': 5,
                   'persoft': 7}
        self.toolbar.Button(buttmap[buttname]).Click()

    def save_log(self):
        time.sleep(2)
        if self.toolbar:
            self.toolbar_click('save')
            self.mwin['Edit'].SetText('BUSHoundlog')
            self.mwin['&SaveButton'].Click()
            time.sleep(0.5)
            self.app['Save Captured Data'].Wait('ready', 3)
            self.app['Save Captured Data']['Edit1'].SetText(r'C:\Users\fan\Desktop\PLC ID出错弹出输入框问题\bushoundlog.txt')
            self.app['Save Captured Data'].Wait('ready', 3)
            # self.app['Save Captured Data']['保存(&S)Button'].Click()
            try:
                time.sleep(1)
                self.app['Save Captured Data']['保存(&S)Button'].Click()
                bus.app['确认另存为']['是&Y'].Wait('ready', 5)
                bus.app['确认另存为']['是&Y'].Click()
                bus.app['确认另存为']['是&Y'].Click()
            except Exception as e:
                print('无需覆盖', e)

    def run_monitor(self):
        time.sleep(2)
        if self.toolbar:
            self.toolbar_click('capture')
            self.mwin['&RUN'].Click()


if __name__ == '__main__':
    bus = BUSHOUND()
    bus.create_app()
    bus.get_mwin()
    bus.get_toolbar()
    # bus.mwin['&Send Commands'].Click()
    # c = bus.mwin['Toolbar'].ButtonCount()
    # for i in range(c):
    #     print(bus.mwin['Toolbar'].GetButton(i))
    # bus.toolbar_click('save')
    # bus.save_log()
    bus.run_monitor()
