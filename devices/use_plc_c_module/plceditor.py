#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: make_c_tree
# Author:    fan
# date:      2018/3/8
# -----------------------------------------------------------
import os
import shutil
import time
from toolbarmapping import get_x_y
from pywinauto import application, mouse, findbestmatch
import pymouse, pykeyboard
import unittest as unit


class PLCEDITOR(object):

    def __init__(self):
        self.app = None
        self.mwin = None
        self.ladder_name = ''
        self.processname = 'PLCEditor.exe'
        self.wintitle = ''

    def _get_wintitle(self, mode='编辑模式'):
        mode_dict = {'编辑模式': ' - 梯形图（写入）',
                     '监控模式': ' - 梯形图（监控 只读）',
                     '监控编辑': ' - 梯形图（监控 写入）'}
        self.wintitle = '  '.join(['Wecon PLC Editor', self.ladder_name, mode_dict[mode]])
        return self.wintitle

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

    def _click(self, txt_nm):
        mouse.click('left', get_x_y(txt_nm))

    def create_app(self):
        app = application.Application()

        app.connect(process=self._get_pid())
        self.app = app

    def get_mwin(self):
        mwin = self.app.top_window().Wait('ready', 3)
        time.sleep(.5)

        # time.sleep(.5)
        # print('222', mwin.Texts())
        # time.sleep(.5)
        self.ladder_name = r"C:\Users\fan\Desktop\PLC ID出错弹出输入框问题\测试梯形图客户工程.wcp"
        self.wintitle = self._get_wintitle('编辑模式')
        self.mwin = mwin

    def do_download(self):
        time.sleep(5)
        # 点击下载按钮
        app = self.app
        mouse.click('left', (681, 110))
        # time.sleep(5)
        app['在线操作'].wait('ready', 10)
        dialog_online = app['在线操作']
        dialog_online['参数+程序(&P)'].Click()
        dialog_online['执行(&E)'].Click()
        app['Wecon PLC Editor'].wait('ready', 10)
        app['Wecon PLC Editor']['是(&Y)'].Click()
        app['Wecon PLC Editor'].wait('ready', 100)
        app['Wecon PLC Editor']['是(&Y)'].Click()
        app['Wecon PLC Editor'].wait('ready', 10)
        app['Wecon PLC Editor']['确定'].Click()
        dialog_online['关闭'].Click()
        print('下载成功')

    def do_upload(self):
        time.sleep(5)
        # 点击上传按钮
        app = self.app
        mouse.click('left', (676, 89))
        # time.sleep(5)
        app['在线操作'].wait('ready', 10)
        dialog_online = app['在线操作']
        dialog_online['参数+程序(&P)'].Click()
        dialog_online['执行(&E)'].Click()
        app['Wecon PLC Editor'].wait('ready', 10)
        app['Wecon PLC Editor']['是(&Y)'].Click()
        app['Wecon PLC Editor'].wait('ready', 10)
        app['Wecon PLC Editor']['是(&Y)'].Click()
        app['Wecon PLC Editor'].wait('ready', 10)
        app['Wecon PLC Editor']['确定'].Click()
        dialog_online['关闭'].Click()
        print('上传成功')

    def do_online_check(self):
        time.sleep(3)
        # 点击校验按钮
        app = self.app
        mwin = self.mwin
        self._click('PLC校验')
        # time.sleep(5)
        app['在线操作'].wait('ready', 10)
        dialog_online = app['在线操作']
        dialog_online['参数+程序(&P)'].Click()
        dialog_online['执行(&E)'].Click()
        app['在线操作'].WaitNot('ready', 100)
        mwin['详细结果[参数]'].print_control_identifiers(2)
        s = mwin['Static8'].Texts()[0]
        if '存在0个不同内容。' == s:
            print('校准结果 =', '成功', s)
        else:
            print('校准结果 =', '失败')

    def go_online_monitor(self):
        app = self.app
        time.sleep(3)
        # 点击在线监控按钮
        self._click('监控模式')
        time.sleep(8)
        self.get_mwin()
        time.sleep(1)
        wintitle = self._get_wintitle('监控模式')
        time.sleep(1)
        temp = self.mwin.Texts()[0].split('  ')
        assert temp[-1] == ' - 梯形图（监控 只读）'
        print('正在监控模式')

    def go_online_write(self):
        app = self.app
        time.sleep(3)
        self._click('监控编辑')
        time.sleep(15)
        self.get_mwin()
        time.sleep(1)
        wintitle = self._get_wintitle('监控编辑')
        # app[wintitle].wait('ready', 100)
        time.sleep(1)
        temp = self.mwin.Texts()[0].split('  ')
        assert temp[-1] == ' - 梯形图（监控 写入）'
        print('正在监控编辑')

    def go_write_mode(self):
        app = self.app
        time.sleep(3)
        self._click('编辑模式')
        time.sleep(1)
        self.get_mwin()
        time.sleep(1)
        temp = self.mwin.Texts()[0].split('  ')
        assert temp[-1] == ' - 梯形图（写入）'
        print('正在编辑模式')

if __name__ == '__main__':
    editor = PLCEDITOR()
    editor.create_app()
    editor.get_mwin()
    # editor.do_download()
    # editor.do_upload()
    # editor.do_online_check()
    # editor.mwin.print_control_identifiers(2)
    editor.go_online_write()
    editor.go_online_monitor()
    editor.go_write_mode()



