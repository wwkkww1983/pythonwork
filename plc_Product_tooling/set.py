# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
create on 2017.2.16
author:fan
"""

from serial import Serial
import binascii
import time
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets, QtCore
from ui_set import Ui_Dialog_Set
from ui_calibration import Ui_Dialog_calibration
# 导入UI模块文件


class SetUp(QWidget):
    """定义UI运行的类，实现串口的设置打开以及校准对象类型的选择"""

    def __init__(self, parent=None):
        super(SetUp, self).__init__(parent)
        self.ui = Ui_Dialog_Set()
        self.ui.setupUi(self)
        self.porta_options = ()
        self.portb_options = ()
        self.Port_A = None
        self.Port_B = None

        self.ui.pushButton_Open_Port.clicked.connect(self.open_port)
        self.ui.pushButton_Go_Calibration.clicked.connect(self.go_calibration)
        # 打开串口按钮被按下：执行串口打开的函数  信号和槽参考：http://www.cnblogs.com/tkinter/p/5632266.html

    def open_port(self):
        # 定义点击按钮的操作
        parity_dict = {'EVEN': 'E',
                       'ODD': 'O',
                       'NONE': 'N'}
        datasize_dict = {'7位': 7,
                         '8位': 8}
        stopbits_dict = {'1位': 1,
                         '2位': 2,
                         '无': 0}
        # 设置端口A
        porta_id = self.ui.comboBox_PortA_Id.currentText()
        porta_paudrate = self.ui.comboBox_PortA_Paudrate.currentText()
        porta_datasize = self.ui.comboBox_PortA_Datasize.currentText()
        porta_parity = self.ui.comboBox_PortA_Parity.currentText()
        porta_stopbits = self.ui.comboBox_PortA_Stopbits.currentText()
        self.porta_options = (porta_id, porta_paudrate, porta_datasize, porta_parity, porta_stopbits)
        # 获取串口设置
        if self.porta_options:
            l1 = self.porta_options
            m1 = (l1[0], int(l1[1]), datasize_dict[l1[2]], parity_dict[l1[3]], stopbits_dict[l1[-1]])
            self.Port_A = Serial(*m1)
            # 将UI上获取的文本转为串口模块能接收的参数，并打开串口
            print(self.Port_A.applySettingsDict)
            # 打开串口A
        else:
            print('无法打开串口A')

        # 设置端口 B
        portb_id = self.ui.comboBox_PortB_Id.currentText()
        portb_paudrate = self.ui.comboBox_PortB_Paudrate.currentText()
        portb_datasize = self.ui.comboBox_PortB_Datasize.currentText()
        portb_parity = self.ui.comboBox_PortB_Parity.currentText()
        portb_stopbits = self.ui.comboBox_PortB_Stopbits.currentText()
        self.portb_options = (portb_id, portb_paudrate, portb_datasize, portb_parity, portb_stopbits)
        # 获取串口设置
        if self.portb_options:
            l2 = self.portb_options
            m2 = (l2[0], int(l2[1]), datasize_dict[l2[2]], parity_dict[l2[3]], stopbits_dict[l2[-1]])
            # 将UI上获取的文本转为串口模块能接收的参数，并打开串口
            self.Port_B = Serial(*m2)
            print(self.Port_B.applySettingsDict)
            # 打开串口B
        else:
            print('无法打开串口B')

#     def go_calibration(self):
#
#         pass
#
#
# class Calibration(QWidget):
#     def __init__(self, parent=None):
#         super(Calibration, self).__init__(parent)
#         self.ui = Ui_Dialog_calibration()
#         self.ui.setupUi(self)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    setup = SetUp()
    # setup.open_port()
    setup.show()
    sys.exit(app.exec_())


