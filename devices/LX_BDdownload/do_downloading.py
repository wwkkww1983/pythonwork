#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: do_downloading
# Author:    fan
# date:      2018/5/3
# -----------------------------------------------------------
from serial import Serial
import serial.tools.list_ports
from stm32bl import download as bin_download
from ui_download_ui import Ui_Dialog as UI
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QFont, QPalette, QColor


class ThreadDoanloading(QThread):
    downlodSignal = pyqtSignal(list)    # 定义返回主线程的信号（list把标识和信息回传）

    def __init__(self, parent=None):
        super(ThreadDoanloading, self).__init__(parent)
        self.flag = None
        self.word = ''
        self.wordColor = 'white'

    def get_para(self, pt, pth, bd):
        """
        获取下载参数
        :param pt:
        :param pth:
        :param bd:
        :return:
        """
        self.pt = pt
        self.pth = pth
        self.bd = bd

    def run(self):
        """
        执行下载，下载前更新状态，按照返回值整理应回传主线程的信息，放到list中
        :return:
        """
        self.flag = -1
        self.word = '正在下载'
        self.wordColor = 'yellow'
        self.downlodSignal.emit([self.flag, self.word, self.wordColor])
        flag = do_downloading(self.pt, self.pth, self.bd)
        if flag:
            if flag == "串口打开失败\n":
                self.flag = 0
                self.word = '下载失败（串口打开失败）'
                self.wordColor = 'red'
            elif flag == "无连接到 boot-loader\n":
                self.flag = 0
                self.word = '下载失败（无法连接boot-loader）'
                self.wordColor = 'red'
            else:
                self.flag = 1
                self.word = '下载成功'
                self.wordColor = 'green'
        else:
            # 原函数没有定义返回False情况，这里处理一下，避免未知错误
            self.flag = 0
            self.word = '下载失败（未知错误）'
            self.wordColor = 'red'
        # 下载结果传回主线程
        self.downlodSignal.emit([self.flag, self.word, self.wordColor])


class DOWNLOAD(QWidget, UI):
    """
    定义下载类
    """
    def __init__(self):
        super(DOWNLOAD, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(self.label_4.text())
        self.label_3.setText('准备就绪')
        # 设置下载状态字体
        self.label_3.setFont(QFont('Microsoft YaHei UI', 20, QFont.Bold))
        # 获取COM列表、创建波特率列表
        port_list = scan_ser_ports()
        baud_list = [187500, 115200, 38400, 19200, 9600, 4800, 2400]

        # 预留，用来读取上次有效参数用，注意当串口变更时需进行处理
        # 参数顺序：0-串口，1-bin路径，2-波特率
        with open('defaultconfig.ini', 'r', encoding='utf-8', errors='ignore') as f:
            last_defaultconfig = f.readlines()

        for port_text in port_list:
            self.comboBox.addItem(port_text)
        for baud in baud_list:
            self.comboBox_2.addItem(str(baud))
        if last_defaultconfig[0][:-1] in port_list:
            self.comboBox.setCurrentText(last_defaultconfig[0][:-1])
        self.lineEdit.setText(last_defaultconfig[1][:-1])
        if int(last_defaultconfig[2][:-1]) in baud_list:
            self.comboBox_2.setCurrentText(last_defaultconfig[2][:-1])


def scan_ser_ports():
    """
    检测系统可用串口列表，返回串口名（str）的列表
    :return: ports_list 串口名（str）列表
    """
    port_text_list = []
    port_list = serial.tools.list_ports.comports()
    if len(port_list) < 1:
        port_text = '找不到串口'
        port_text_list.append(port_text)
    else:
        for port in port_list:
            port_text = '{0} > {1}'.format(port[0], port[1])
            port_text_list.append(port_text)
    return port_text_list


def do_downloading(port='', bin_path='', baud=115200):
    """
    通过串口下载BD板固件
    :param port:串口名称(str),
    :param bin_path:固件路径
    :param baud:波特率
    :return: 下载成功=1，下载失败=原因（串口错误、连接错误）
    """
    flag = bin_download(port, bin_path, baud)
    return flag


def main_logic():
    """
    执行下载
    :return:
    """
    thread = ThreadDoanloading()
    import sys
    app = QApplication(sys.argv)
    download = DOWNLOAD()
    download.show()

    def click_select_path():
        dialog = QFileDialog()
        path, t = dialog.getOpenFileName(download, "选择BD板固件.bin",
                                         r'G:\C盘系统文档备份\我的文档',
                                         'BD固件 (*.bin);;所有文件 (*.*)')
        download.lineEdit.setText(path)

    def flag_todo(flag_list):
        # 处理下载线程返回标识
        download.label_3.setText(flag_list[1])
        # 按照不同情况设置标签颜色，注意先设置setAutoFillBackgound设置True
        download.label_3.setAutoFillBackground(True)
        pale = QPalette()
        pale.setColor(QPalette.Window, QColor(flag_list[2]))
        download.label_3.setPalette(pale)

        if flag_list[0] == 1:
            download.pushButton.setDisabled(False)
            # 如果下载成功，则把当前参数存放，作为下次打开文件的默认参数
            defaultconfig = [download.comboBox.currentText()+'\n',
                             download.lineEdit.text()+'\n',
                             download.comboBox_2.currentText()+'\n']
            with open('defaultconfig.ini', 'w', encoding='utf-8', errors='ignore') as f:
                f.writelines(defaultconfig)

        elif flag_list[0] == -1:
            download.pushButton.setDisabled(True)
        elif flag_list[0] == 0:
            download.pushButton.setDisabled(False)

    def click_download():

        current_port = download.comboBox.currentText().split(' ')[0]    # 选中当前串口
        current_baud = int(download.comboBox_2.currentText())    # 选中当前波特率，注意转为整型
        current_path = download.lineEdit.text()    # 选择路径
        thread.get_para(current_port, current_path, current_baud)
        thread.downlodSignal.connect(flag_todo)
        thread.start()

    download.pushButton_2.clicked.connect(click_select_path)
    download.pushButton.clicked.connect(click_download)
    # download.destroyed.connect(thread.quit)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main_logic()
