#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pywinauto import application
from time import sleep
from os import path, popen
from datetime import datetime
import serial


class Download(object):
    def __init__(self, exepath, filepath, iplist, filetype=u'工程文件', password=''):
        self.exepath = exepath
        self.app = None
        self.win = None
        self.filetype = filetype
        self.password = password
        self.filepath = filepath
        self.filesize = path.getsize(self.filepath)
        self.usb_ready = False
        self.set_ready = False
        self.ethernet_ready = False
        self.window_ready = False
        self.result = False
        # self.port = self.get_port()
        self.iplist = iplist
        self.ip_index = 0
        self.ip = None
        while self.ip_index < len(iplist):
            sleep(0.5)
            pingok = 'fail'
            if self.pingip() is True:
                pingok = 'success'
            else:
                pingok = 'fail'
            print('ping ', self.iplist[self.ip_index], pingok)
            self.ip_index += 1
            if self.ip_index >= len(iplist):
                self.ip_index = 0
                break

    # def getips(self, iplist=None):
    #     # ipl = []
    #     # if iplist:
    #     #     for i in iplist:
    #     #         ip = i.split('.')
    #     #         ipl.append(ip)
    #     #     return ipl
    #     return iplist[0]

    def pingip(self):
        result = False
        ipstr = self.iplist[self.ip_index]
        try:
            output = popen('ping -l 1 -n 1 ' + ipstr).readlines()
            sleep(0.2)
            for line in output:
                if str(line).upper().find('TTL') >= 0:
                    result = True
                    print('ip {} 连接正常'.format(ipstr))
                    self.ip = ipstr
                if str(line).find(u'找不到') >= 0:
                    result = False
                    print('无法连接ip {}'.format(ipstr))
        except Exception as e:
            print(e)
        return result

    def start(self):
        self.window_ready = False
        try:
            sleep(1)
            popen(r'taskkill /f /t /im Download.exe')
            print(u'正在关闭旧的Download窗口')
            sleep(1)
        except Exception:
            print(u'正在打开新的Download窗口')
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
        self.set_ready = False
        ip = self.iplist[self.ip_index].split('.')
        try:
            self.win[u'PC端口：ComboBox'].Select(u'Ethernet')
            self.win['IP:Edit1'].SetText(ip[-1])
            self.win['IP:Edit2'].SetText(ip[-2])
            self.win['IP:Edit3'].SetText(ip[-3])
            self.win['IP:Edit4'].SetText(ip[-4])
            self.win[u'文件类型：Combobox'].Select(self.filetype)
            # self.win[u'密码：Edit'].SetText(self.password)
            if self.win['IP:Edit4'].window_text() == ip[-4]:
                self.set_ready = True
            else:
                self.set_ready = False
        except Exception as e:
            print('下载工具打开或设置异常, {}'.format(e))
            self.set_ready = False

    def download(self):
        download_result = False
        self.result = download_result
        self.ethernet_ready = self.pingip()
        if not self.ethernet_ready:
            print('download, ethernet_ready false')
        else:
            for i in range(5):
                sleep(1)
                # print('正在检查可用性，第{}次'.format(i))
                try:
                    self.set()
                except Exception as e:
                    print('Download set fail: ', e)

            if not (self.ethernet_ready is True and self.window_ready is True and self.set_ready is True):
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '未检测到工程运行，停止下载')
            else:
                self.result = -1
                self.win['PC-->HMI(&D)Button'].Click()
                sleep(1)
                self.win[u'文件名(&N):Edit'].SetText(self.filepath)
                sleep(1)
                self.win['打开(&O)Button'].Click()
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '下载开始')
                sleep(3)
                if self.filetype == u'工程文件':
                    for i in range(5):
                        sleep(1)
                        txt = u'点击【确定】按钮升级'
                        try:
                            if txt in self.app.top_window()['Static'].window_text():
                                # 检测更新
                                self.app.top_window()['确定Button'].Click()
                                break
                            else:
                                continue

                        except Exception as e:
                            continue
                sleep(3)
                txt = u'传输成功!需要重新启动人机界面才能生效，点击‘确定’将重启人机界面，' \
                      u'\n如果机器正在运行组态，则数据有可能丢失。'
                for i in range(30):
                    sleep(1)
                    # print(u'查找传输成功标识 第{}次'.format(i))
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
    pth = r"D:\Program Files\WECONSOFT\HMIEditorP\20171108测试（颂华）\Download.exe"
    fpth = r"C:\Users\fan\Desktop\颂华pi3070上电卡logo文件系统问题修改验" \
           r"证\A8 161205恒温恒湿BD170929 VA.10.06优化版\3070 HMIProject170929 VA.10.06\HMIProject.wmt"
    # fpth = r'\\192.168.10.10\软件测试组\文件中转站\PI新版本\3000系列更新OS\script_PI3070_debug.osf2'
    ipl = ['192.168.22.47',
           '192.168.22.50',
           '192.168.22.52',
           '192.168.22.59',
           '192.168.22.60',
           '192.168.22.61']
    # ftype = u'镜像文件'
    download = Download(pth, fpth, ipl)
    download.start()
    sleep(1)
    download.set()
    # download.download()
    sucesstimes = 0
    for i in range(9999):
        print('--------------------', i, '--------------------')
        ip = download.iplist[download.ip_index]
        download.download()
        if download.result == 1:
            sucesstimes += 1
        else:
            print(u'下载失败', ip)
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ip,
              u'下载结果', download.result,  u'成功次数',sucesstimes)
        sleep(5)
        download.ip_index += 1
        if download.ip_index >= len(ipl):
            download.ip_index = 0

