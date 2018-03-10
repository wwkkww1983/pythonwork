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
from pywinauto import application, mouse, findbestmatch
import pymouse, pykeyboard
import unittest as unit


def make_c_file_tree():
    c_dir = r'E:\Redmine\_20180123 PLC CModule\提交\编译器\CBlock_测试代码\c_struc'
    pkg_dir = r'E:\Redmine\_20180123 PLC CModule\提交\编译器\CBlock_测试代码\topack'
    os.chdir(c_dir)
    fun_dirs = []
    for name in os.listdir(c_dir):
        if os.path.isfile(name) and (name[-2:] in ['.c']):
            tempdirname = os.path.splitext(name)[0]
            if tempdirname not in fun_dirs:
                fun_dirs.append(tempdirname)
                target_dir = os.path.join(pkg_dir, tempdirname)
                os.mkdir(target_dir)
                source_path = os.path.join(c_dir, name)
                shutil.copy(source_path, target_dir)


class PLCEDITOR(object):

    def __init__(self):
        self.app = None
        self.mwin = None
        self.ladder_name = ''
        self.processname = 'PLCEditor.exe'
        self.wintitle = ''

    def _get_wintitle(self, mode):
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

    def create_app(self):
        self.ladder_name = r"E:\Redmine\_20180123 PLC CModule\测试\测试工程\梯10-32000-0-0-100-10.pwcp"
        app = application.Application()
        # app.connect(title=win_title)
        # app.connect(handle=0x330E5A)
        app.connect(process=self._get_pid())
        self.app = app

    def get_mwin(self):
        rib_bar = 'Afx:RibbonBar:230000:8:10003:10'
        mwin = self.app.top_window()
        # self.ladder_name = mwin.Texts()
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
        mouse.click('left', (757, 65))
        # time.sleep(5)
        app['在线操作'].wait('ready', 10)
        dialog_online = app['在线操作']
        dialog_online['参数+程序(&P)'].Click()
        dialog_online['执行(&E)'].Click()
        mwin['详细结果[参数]'].wait('ready', 100)
        mwin['详细结果[参数]'].print_control_identifiers(2)
        s = mwin['Static8'].Texts()[0]
        if '存在0个不同内容。' == s:
            print('校准结果 =', '成功', s)
        else:
            print('校准结果 =', '失败')

    def online_monitor(self):
        app = self.app
        wintitle = self._get_wintitle('编辑模式')
        app[wintitle].wait('ready', 10)
        temp = self.mwin.Texts()[0].split('  ')
        assert temp[-1] == ' - 梯形图（写入）'
        time.sleep(3)
        # 点击在线监控按钮
        mouse.click('left', (580, 88))
        wintitle = self._get_wintitle('监控模式')
        app[wintitle].wait('ready', 10)
        temp = self.mwin.Texts()[0].split('  ')
        assert temp[-1] == ' - 梯形图（监控 只读）'
        print('正在监控模式')



if __name__ == '__main__':
    editor = PLCEDITOR()
    editor.create_app()
    editor.get_mwin()
    # editor.do_download()
    # editor.do_upload()
    # editor.do_online_check()
    editor.online_monitor()


