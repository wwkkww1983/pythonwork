#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pywinauto import application
from time import sleep
from os import path, popen
from datetime import datetime
import serial


class Download(object):
    def __init__(self, exepath, filepath, filetype=u'工程文件', password=''):
        self.exepath = exepath
        self.app = None
        self.win = None
        self.filetype = filetype
        self.password = password
        self.filepath = filepath
        self.filesize = path.getsize(self.filepath)
        self.usb_ready = False
        self.window_ready = False
        self.result = False
        self.port = self.get_port()

    def start(self):
        self.window_ready = False
        try:
            sleep(1)
            popen(r'taskkill /f /t /im Download.exe')
            sleep(1)
        except Exception:
            pass
        self.app = application.Application()
        self.win = None
        self.app.start(self.exepath)
        sleep(1)
        # if self.app.top_window()[u'程序已经运行Static'].is_enabled():
        #     if self.app.top_window()['确定Button'].is_enabled():
        #         self.app.top_window()['确定Button'].Click()
        #
        #         self.app.start(self.exepath)
        #         sleep(1)
        #     else:
        #         pass
        #     self.win = self.app['Dialog']
        # else:
        #     pass
        self.win = self.app['Dialog']
        self.window_ready = True

    def set(self):
        self.usb_ready = False
        try:
            self.win[u'PC端口：ComboBox'].Select(u'USB:DownloadLink')
            self.win[u'文件类型：Combobox'].Select(self.filetype)
            self.win[u'密码：Edit'].SetText(self.password)
            self.usb_ready = True
        except Exception:
            print('未找到"USB:DownloadLink"连接')
            self.usb_ready = False

    def download(self):
        download_result = False
        self.result = download_result
        s = b''
        self.port.reset_input_buffer()
        for i in range(60):
            sleep(1.1)
            try:
                s = self.port.read(size=6)
                print(s)
                if s == b'aabbcc':
                    sleep(2)

                    break
                else:
                    self.port.reset_input_buffer()
                    continue
            except Exception:
                continue
        sleep(1)
        for i in range(60):
            sleep(1)
            try:
                self.win[u'PC端口：ComboBox'].Select(u'USB:DownloadLink')
                if u'USB:DownloadLink' in self.win[u'PC端口：ComboBox'].ItemTexts():
                    break
            except Exception:
                continue
        sleep(1)
        # if not (self.ready == True or s == b'aabbcc'):
        if not (self.usb_ready is True and self.window_ready is True and s == b'aabbcc'):
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '未检测到工程运行，停止下载')
            self.result = -1
            return
        else:
            sleep(5)
            self.set()
            sleep(.5)
            self.win['PC-->HMI(&D)Button'].Click()
            sleep(1)
            self.win[u'文件名(&N):Edit'].SetText(self.filepath)
            sleep(.5)
            self.win['打开(&O)Button'].Click()
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '下载开始')
            for i in range(10):
                sleep(1)
                try:
                    if self.app['升级Dialog']['确定Button'].is_enabled():
                        # 检测更新
                        self.app['升级Dialog']['确定Button'].Click()
                        self.app['升级Dialog']['确定Button'].Click()
                        break
                    else:
                        continue
                except Exception:
                    continue
            sleep(10)
            txt = u'传输成功!需要重新启动人机界面才能生效，点击‘确定’将重启人机界面，\n如果机器正在运行组态，则数据有可能丢失。'
            for i in range(90):
                sleep(1)
                try:
                    if self.app.top_window()['Static2'].window_text() == txt:
                        # 主对话框中已包含“名称”为'Static2'的控件，当文本变为txt时，说明该对话框被下载成功对话框覆盖
                        self.app.top_window()['确定Button'].Click()
                        download_result = True
                        break
                    else:
                        download_result = False
                        continue
                except Exception:
                    continue
            if download_result is False:
                print('找不到下载成功确认窗口，无法完成下载')
            else:
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '下载完成')
            self.result = download_result

    def get_port(self, port='com3', baudrate=9600):
        t = None
        try:
            t = serial.Serial(port, baudrate)
            t.bytesize = 7
            t.parity = 'E'
            t.stopbits = 1
            t.timeout = 3
            t.reset_input_buffer()
            print("""
                  com       = %s
                  baud_rate = %d
                  data_size = %d
                  parity    = %s
                  stop_bits = %d""" % (t.port, t.baudrate, t.bytesize, t.parity, t.stopbits))
        except:
            print('串口打开失败')

        if t.is_open:
            pass
        else:
            t.open()
        return t

    # 警告
    # try:
    #     warn = app['Warning']
    #     print(warn['Static2'])
    #     sleep(5)
    #     warn['否(&N)'].click()
    # except Exception as e:
    #     print(e)

if __name__ == '__main__':
    pth = r'D:\Program Files\WECONSOFT\LeviStudio\20170120 发布\Download.exe'
    fpth = r'C:\Users\fan\Desktop\NewProject\NewProject.hmt'
    download = Download(pth, fpth)
    download.start()
    download.set()
    sucesstimes = 0
    for i in range(9999999):
        print('尝试下载', i)
        download.download()
        if download.result == 1:
            sucesstimes += 1
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '下载结果', '次数', sucesstimes, download.result)
        elif download.result == 0:
            break
