#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: operate_download
# Author:    fan
# date:      2018/7/26
# -----------------------------------------------------------
# 连接HMI串口，和PLC串口等待HMI正常发出数据后，通过PLC给HMI下电，按照设定的间隔上电或下电

from pywinauto import application, mouse
from time import sleep
import os
from datetime import datetime
import logging as log
from watchcom import *
# import serial

log.basicConfig(filename=os.path.join(os.getcwd(), 'log_levi_download.txt'),
                level=log.ERROR,
                format='%(asctime)s %(levelname)s: %(message)s')


class Download(object):
    def __init__(self, exepath, filepath, filetype=u'工程文件', password=''):
        self.exepath = exepath
        self.app = None
        self.win = None
        self.filetype = filetype
        self.password = password
        self.filepath = filepath
        self.filesize = os.path.getsize(self.filepath)
        self.usb_ready = False
        self.window_ready = False
        self.result = False
        # self.port = self.get_port()

    def start(self):
        self.window_ready = False
        try:
            sleep(1)
            os.popen(r'taskkill /f /t /im Download.exe')
            sleep(1)
        except Exception:
            pass
        self.app = application.Application()
        self.win = None
        self.app.start(self.exepath)
        sleep(1)
        self.win = self.app['Dialog']
        self.win.move_window(0, 0)
        self.window_ready = True

    def set(self):
        try:
            self.win[u'PC端口：ComboBox'].Select(u'USB:DownloadLink')
            self.win[u'文件类型：Combobox'].Select(self.filetype)
            self.win[u'密码：Edit'].SetText(self.password)
        except Exception:
            print('USB link not found.')
            log.error('USB link not found.')

    def download(self):
        download_result = False
        self.result = download_result
        port_hmi = set_port('com2', 115200, 7, 1, 'E')
        s = read_correct(port_hmi)
        if not s:
            print('hmi port error. process quited. please check if the problem happened.')
            quit()
        if s:
            print('hmi 串口检测正常，准备下载')
            sleep(1)
            i = 0
            while i <= 60:
                # 检查USB链接是否就绪
                i += 1
                sleep(1)
                try:
                    self.win[u'PC端口：ComboBox'].Select(u'USB:DownloadLink')
                    if u'USB:DownloadLink' in self.win[u'PC端口：ComboBox'].ItemTexts():
                        break
                except Exception:
                    print("USB link not found. ({})".format(i))
                    log.error("USB link not found. ({})".format(i))
            self.set()
            sleep(5)
            if self.win[u'PC端口：ComboBox'].is_enabled():
                self.win[u'PC-->HMI(&D)Button'].Click()
            # mouse.click(button='left', coords=(180, 370))    # 操作坐标，前提是窗口在顶层。
            sleep(2)
            self.app[u'打开Dialog'][u'文件名(&N):Edit'].SetText(self.filepath)
            sleep(.5)
            self.win['打开(&O)Button'].Click()
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '下载开始')
            log.info('{} {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '下载开始'))
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
                        sleep(2)
                        # 主对话框中已包含“名称”为'Static2'的控件，当文本变为txt时，说明该对话框被下载成功对话框覆盖
                        self.app.top_window()['确定Button'].Click()
                        download_result = True
                        break
                except Exception:
                    download_result = False
                    print('now downloding...')
                    continue
            if download_result is False:
                print('找不到下载成功确认窗口，无法完成下载')
                log.error('找不到下载成功确认窗口，无法完成下载')
            else:
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '下载完成')
                log.info('{} {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '下载完成'))
            self.result = download_result
            print('HMI软重启，等待看到LOGO')
            sleep(5)    # 等待看到LOGO
            port_plc = set_port('com6', 9600, 7, 1, 'E')
            switch(port_plc, 'Y0', 0)    # HMI下电
            print('出现LOGO，HMI下电，等待重新上电')
            time.sleep(5)
            port_plc.open()
            switch(port_plc, 'Y0', 1)  # HMI上电
            print('HMI 上电，等待重启完成')
            time.sleep(15)    # 等待重启

    # def get_port(self, port='com3', baudrate=9600):
    #     t = None
    #     try:
    #         t = serial.Serial(port, baudrate)
    #         t.bytesize = 7
    #         t.parity = 'E'
    #         t.stopbits = 1
    #         t.timeout = 3
    #         t.reset_input_buffer()
    #         print("""
    #               com       = %s
    #               baud_rate = %d
    #               data_size = %d
    #               parity    = %s
    #               stop_bits = %d""" % (t.port, t.baudrate, t.bytesize, t.parity, t.stopbits))
    #     except:
    #         print('串口打开失败')
    #
    #     if t.is_open:
    #         pass
    #     else:
    #         t.open()
    #     return t
    #
    # # 警告
    # # try:
    # #     warn = app['Warning']
    # #     print(warn['Static2'])
    # #     sleep(5)
    # #     warn['否(&N)'].click()
    # # except Exception as e:
    # #     print(e)

if __name__ == '__main__':
    # input("LEVI Download工程自动下载测试工具 V1.0\n输入任意字符开始测试：\n")
    n = 10000
    # while True:
    #     pth = input("请输入Download.exe完整路径：\n")
    #     fpth = input("请输入待下载.hmt工程文件完整路径：\n")
    #     if os.path.exists(pth) and os.path.exists(fpth):
    #         print("文件检查无误\n")
    #     else:
    #         print("文件检查失败！")
    #         continue
    #     n = input("请输入下载测试次数：")
    #     if n.isdigit() and int(n) > 0:
    #         print("确认下载次数为：{}".format(n))
    #         break
    #     else:
    #         print("次数输入有误，请重新输入(必须为正整数)！")
    #         continue
    pth = r"D:\Program Files\WECONSOFT\LeviStudio\20180809发布\Download.exe"
    fpth = r"E:\Redmine\700ML死机问题\卡logo下载测试\333.ehmt"
    download = Download(pth, fpth)
    download.start()
    download.set()
    sucesstimes = 0
    i = 0
    while i <= int(n)-1:
        i += 1
        print('尝试下载', i)
        download.download()
        if download.result == 1:
            sucesstimes += 1
            print('{} 本次({})下载结果: {}. 下载测试进度：成功次数/总次数: {}/{}'.format(
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            i,
                            download.result,
                            sucesstimes,
                            n
                            ))
            log.info('{} 本次({})下载结果: {}. 下载测试进度：成功次数/总次数: {}/{}'.format(
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                i,
                download.result,
                sucesstimes,
                n
            ))
        elif download.result == 0:
            log.error("下载失败")
            continue
    input("确认测试完成并已经保存数据，输入任意字符结束本程序:\n")
