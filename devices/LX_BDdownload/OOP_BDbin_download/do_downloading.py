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
from PyQt5.QtCore import pyqtSignal, QThread, QDir
from PyQt5.QtGui import QFont, QPalette, QColor
import json


class ThreadDoanloading(QThread):
    downlodSignal = pyqtSignal(list)    # 定义返回主线程的信号（list把标识和信息回传）

    def __init__(self, parent=None):
        super(ThreadDoanloading, self).__init__(parent)
        self.flag = None
        self.word = ''
        self.wordColor = 'white'

    def get_para(self, download):
        """
        获取下载参数
        :param pt:
        :param pth:
        :param bd:
        :return:
        """
        self.pt = download.port
        self.pth = download.path
        self.bd = download.baud
        self.dodoadload = download.do_downloading

    def run(self):
        """
        执行下载，下载前更新状态，按照返回值整理应回传主线程的信息，放到list中
        :return:
        """
        self.flag = -1
        self.word = '正在下载'
        self.wordColor = 'yellow'
        self.downlodSignal.emit([self.flag, self.word, self.wordColor])
        flag = self.dodoadload(self.pt, self.pth, self.bd)
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


class Downloading(object):
    def __init__(self, port, path, baud):
        self.download_flag = None
        # 获取COM列表、创建波特率列表
        self.port = port
        self.path = path
        self.baud = baud

    def do_downloading(self, port, bin_path, baud):
        """
        通过串口下载BD板固件
        :param port:串口名称(str),
        :param bin_path:固件路径
        :param baud:波特率
        :return: 下载成功=1，下载失败=原因（串口错误、连接错误）
        """
        flag = bin_download(port, bin_path, baud)
        self.download_flag = flag
        return flag


class DownloadUi(QWidget, UI):
    """
    定义下载界面
    """
    def __init__(self):
        super(DownloadUi, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(self.label_4.text())
        # 设置'下载状态'文本和字体
        self.label_3.setText('准备就绪')
        self.label_3.setFont(QFont('Microsoft YaHei UI', 20, QFont.Bold))
        # 设置一个默认路径存放实例
        self.direc = QDir()

        self.download = None

        self.baud_list = [187500, 115200, 38400, 19200, 9600, 4800, 2400]
        self.port_list = self.scan_ser_ports()

        for port_text in self.port_list:
            self.comboBox.addItem(port_text)
        for baud in self.baud_list:
            self.comboBox_2.addItem(str(baud))


        with open('downloadpara.json', 'r') as f:
            s = f.read()
            print()
            d = json.loads(s, object_hook=JSONObject)    # 对象钩子，确定loads的数据应转换成何种对象（字典->实例对象）
        for port_full_name in self.port_list:
            if d.port in port_full_name:
                self.comboBox.setCurrentText(port_full_name)
        self.lineEdit.setText(d.path)
        if d.baud in self.baud_list:
            self.comboBox_2.setCurrentText(str(d.baud))

    def scan_ser_ports(self):
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


    def select_path(self):
        dialog = QFileDialog()
        if self.lineEdit.text():
            open_path = self.lineEdit.text()
        else:
            open_path = self.direc.homePath()
        path, t = dialog.getOpenFileName(self, "选择BD板固件.bin",
                                         open_path,
                                         'BD固件 (*.bin);;所有文件 (*.*)')
        if path:
            self.lineEdit.setText(path)

    def start_download(self):
        current_port = self.comboBox.currentText().split(' ')[0]    # 选中当前串口
        current_baud = int(self.comboBox_2.currentText())    # 选中当前波特率，注意转为整型
        current_path = self.lineEdit.text()    # 选择路径
        self.download = Downloading(current_port, current_path, current_baud)    # 下载实例
        self.thread = ThreadDoanloading()
        self.thread.get_para(self.download)
        self.thread.downlodSignal.connect(self.change_status)
        self.thread.start()

    def change_status(self, flag_list):
        # 处理下载线程返回标识
        self.label_3.setText(flag_list[1])
        # 按照不同情况设置标签颜色，注意先设置setAutoFillBackgound设置True
        self.label_3.setAutoFillBackground(True)
        pale = QPalette()
        pale.setColor(QPalette.Window, QColor(flag_list[2]))
        self.label_3.setPalette(pale)
        if flag_list[0] == 1:
            self.pushButton.setDisabled(False)
            with open('downloadpara.json', 'w', ) as f:
                # 读取配置文件并进行写入，indent缩进格式, ensure_ascii所有非Ascii字符被转义输出，这里要输出中文选择不转义
                txt = json.dumps(self.download.__dict__, indent='\t', ensure_ascii=False)
                f.write(txt)
        elif flag_list[0] == -1:
            self.pushButton.setDisabled(True)
        elif flag_list[0] == 0:
            self.pushButton.setDisabled(False)


class JSONObject:
    """
    作为把序列化字符串恢复为实例对象的object_hook, 用法：
    data=json.loads(f_str, object_hook=JSONObject)
    """
    def __init__(self, d):
        self.__dict__ = d


def main_logic():
    """
    执行下载
    :return:
    """
    import sys
    app = QApplication(sys.argv)
    download = DownloadUi()
    download.show()
    download.pushButton_2.clicked.connect(download.select_path)
    download.pushButton.clicked.connect(download.start_download)
    sys.exit(app.exec_())
if __name__ == '__main__':
    main_logic()
