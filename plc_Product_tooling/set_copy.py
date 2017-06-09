# !/usr/bin/env python3
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
        self.Selected_device = '请选择校准对象设备'

        self.parity_dict = {'EVEN': 'E',
                            'ODD': 'O',
                            'NONE': 'N'}
        self.datasize_dict = {'7位': 7,
                              '8位': 8}
        self.stopbits_dict = {'1位': 1,
                              '2位': 2,
                              '无': 0}

    def open_port(self):
        # 设置端口A
        porta_id = self.ui.comboBox_PortA_Id.currentText()
        porta_paudrate = self.ui.comboBox_PortA_Paudrate.currentText()
        porta_datasize = self.ui.comboBox_PortA_Datasize.currentText()
        porta_parity = self.ui.comboBox_PortA_Parity.currentText()
        porta_stopbits = self.ui.comboBox_PortA_Stopbits.currentText()

        self.porta_options = (porta_id, porta_paudrate, porta_datasize, porta_parity, porta_stopbits)
        # 获取串口设置
        if self.porta_options:
            self.porta_options = (porta_id, int(porta_paudrate), self.datasize_dict[porta_datasize],
                                  self.parity_dict[porta_parity], self.stopbits_dict[porta_stopbits])
            # 将UI上获取的文本转为串口模块能接收的参数
        else:
            print('串口A设置无效')
        print(self.porta_options)
        self.go_calibration_window()
        # 刷新进入校准按钮

    def go_calibration_window(self):
        if self.porta_options:
            self.ui.pushButton_Go_Calibration.setEnabled(True)
        else:
            self.ui.pushButton_Go_Calibration.setDisabled(True)


class Calibration(QWidget):
    def __init__(self, parent=None):
        super(Calibration, self).__init__(parent)
        self.ui = Ui_Dialog_calibration()
        self.ui.setupUi(self)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    setup = SetUp()
    calibration = Calibration()

    setup.go_calibration_window()
    # 刷新进入校准按钮

    setup.show()

    def switch_window_to_calbration():
        setup.show()
        calibration.show()
        print('进入校准窗口')

    def switch_window_to_setup():
        calibration.hide()
        setup.show()
        print('返回串口设置窗口')

    setup.ui.pushButton_Open_Port.clicked.connect(setup.open_port)
    # 打开串口按钮被按下：执行串口打开的函数  信号和槽参考：http://www.cnblogs.com/tkinter/p/5632266.html

    setup.ui.pushButton_Go_Calibration.clicked.connect(switch_window_to_calbration)
    # 进入校准按钮被按下：执行跳转函数到校准窗口

    calibration.ui.pushButton_back_set.clicked.connect(switch_window_to_setup)

    sys.exit(app.exec_())


