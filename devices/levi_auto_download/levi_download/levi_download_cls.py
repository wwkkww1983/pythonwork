#!/usr/bin/python3
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: levi_downlaod.py
# Author:    fan
# date:      2019/8/14
# -----------------------------------------------------------
# levi 下载模块基础类


from pywinauto import application
from time import sleep
import os
from mylog import mylog


class LeviDownload(object):
    def __init__(self):
        self.exepath = None
        self.app = None
        self.win = None
        self.filepath = None
        self.filetype = None
        self.password = None
        self.usb_ready = False
        self.win_opened = False
        self.project_downloaded_ok = False
        self.download_error = True
        self.downloading = False
        for l in os.popen(r"tasklist"):  # 获取进程列表
            if "Download.exe" in l:
                os.popen(r'taskkill /f /t /im Download.exe')  # 杀死Download.exe进程

    def open_download(self, exepath):
        """
        打开download窗口
        :return: None
        """
        sleep(1)
        self.exepath = exepath
        if self.win_opened:
            mylog("download window has been opened.")
        else:
            if not os.path.exists(self.exepath):
                mylog("file not found: {}".format(self.exepath))
            else:
                self.app = application.Application()
                self.app.start(self.exepath)
                sleep(1)
                self.win = self.app["Dialog"]
                self.win.move_window(0, 0)
                self.win_opened = True
                print("Download.exe opened")

    def config_download(self, filetype=u'工程文件', password=''):
        """
        配置下载类型、密码，确认USB状态
        :param filetype:
        :param password:
        :return:
        """
        self.filetype = filetype
        self.password = password
        try:
            self.win[u'PC端口：ComboBox'].select(u'USB:DownloadLink')
            self.win[u'文件类型：Combobox'].select(filetype)
            self.win[u'密码：Edit'].set_edit_text(password)
            self.usb_ready = True
        except Exception:
            mylog('a mistake append while configuring download.exe.')

    def download_project(self, filepath):
        """
        下载文件：打开文件、升级镜像、下载完成确认
        :param filepath:
        :return:
        """
        self.filepath = filepath
        self.project_downloaded_ok = False
        self.download_error = False
        if self.filetype == "工程文件":
            checkcount = 0
            topcount = 60  # 检查USB是否就绪，每秒检查一次，60秒
            while checkcount <= topcount:
                sleep(1)
                checkcount += 1
                try:
                    self.win[u'PC端口：ComboBox'].select(u'USB:DownloadLink')
                    break
                except Exception:
                    mylog(("USB link not found. ({}/{})".format(checkcount, topcount)))
            sleep(1)
            if self.win[u'PC端口：ComboBox'].is_enabled():
                self.win[u'PC-->HMI(&D)Button'].click()
            sleep(2)
            self.app[u'打开Dialog'][u'文件名(&N):Edit'].set_edit_text(self.filepath)
            sleep(.5)
            self.win['打开(&O)Button'].click()
            mylog('download started.')
            try:  # 检查是否有升级弹窗，每秒检查一次，10秒
                for i in range(10):
                    sleep(1)
                    if self.app['升级Dialog']['确定Button'].is_enabled():
                        # 检测更新
                        self.app['升级Dialog']['确定Button'].click()
                        self.app['升级Dialog']['确定Button'].click()
                        break
                    else:
                        print("checking update...")
            except Exception:
                pass
            """
            到这个步骤后，进入工程或镜像升级下载时间，这个过程一般会持续数十秒
            """
            self.downloading = True
            txt = u'传输成功!需要重新启动人机界面才能生效，点击‘确定’将重启人机界面，\n如果机器正在运行组态，则数据有可能丢失。'
            try:  # 检查下载是否完成，每秒检查一次，90秒
                for i in range(90):
                    sleep(1)
                    if self.app.top_window()['Static2'].window_text() == txt:
                        sleep(2)  # 主对话框中已包含“名称”为'Static2'的控件，当文本变为txt时，说明该对话框被下载成功对话框覆盖
                        self.app.top_window()['确定Button'].click()
                        self.project_downloaded_ok = True
                        self.downloading = False
                        break
                    elif self.app.top_window()['Static'].window_text() == '传输中出现错误!':
                        self.download_error = True
                        break
                    else:
                        # print("downloading or hmi is rebooting. {}/90".format(i))
                        continue
            except Exception:
                    self.project_downloaded_ok = False
                    self.downloading = False
            mylog("download finished, the result is {}".format(self.project_downloaded_ok))

    def close_error_tip_win(self):
        """
        关闭可能的异常弹出提示框，注意：需要时才调用
        :return:
        """
        for i in range(10):
            sleep(1)
            if self.app.top_window()['Static'].window_text() == '传输中出现错误!':
                self.app.top_window()["确定Button"].click()
                continue
            elif self.app.top_window()['Static'].window_text() == '更新文件失败！是否重试？':
                self.app.top_window()["取消Button"].click()
                continue
            elif "通讯测试超时，请确定下列问题：\n" in self.app.top_window()['Static2'].window_text():
                self.app.top_window()["否(&N)Button"].click()
                continue
            else:
                print(self.app.top_window().print_control_identifiers())
                continue


if __name__ == "__main__":
    exepth = r"D:\LeviStudio\Download.exe"
    fpth = r"D:\Levi下载测试\2070.ehmt"
    download = LeviDownload()
    download.open_download(exepth)
    download.config_download()
    download.download_project(fpth)
