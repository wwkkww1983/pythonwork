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


class DOWNLOAD(QWidget, UI):
    def __init__(self):
        super(DOWNLOAD, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(self.label_4.text())
        self.label_3.setText('准备就绪')
        port_list = scan_ser_ports()
        baud_list = [187500, 115200, 38400, 19200, 9600, 4800, 2400]
        # 预留，用来读取上次有效参数用，注意当串口变更时需进行处理
        with open('defaultconfig.ini', 'r', encoding='utf-8', errors='ignore') as f:
            info = f.readlines()
        print(info)
        for port_text in port_list:
            self.comboBox.addItem(port_text)
        for baud in baud_list:
            self.comboBox_2.addItem(str(baud))

        if info[0][:-1] in port_list:
            self.comboBox.setCurrentText(info[0][:-1])
        self.lineEdit.setText(info[1][:-1])
        if info[2][:-1] in baud_list:
            self.comboBox_2.setCurrentText(info[2][:-1])


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


def do_downloading(port, bin_path, baud):
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
    import sys
    app = QApplication(sys.argv)
    download = DOWNLOAD()
    download.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    # 获取串口列表
    p = scan_ser_ports()
    for a in p:
        print(a)

    main_logic()
