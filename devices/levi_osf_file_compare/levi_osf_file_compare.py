#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: levi_osf_file_compare
# Author:    fan
# date:      2019/6/21 021
# -----------------------------------------------------------
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QPushButton, \
    QTextBrowser, QMessageBox, QFileDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, QThread
from ui_app import Ui_MainWindow
from myosf import *
import _thread


from devices.levi_osf_file_compare.myosf import do_compare

ui = Ui_MainWindow()
import sys
import os


class ThreadPrint(QThread):
    global logline
    printsignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ThreadPrint, self).__init__(parent)
        self.logline = 'Null'
        self.path1 = None
        self.path2 = None

    def set_params(self, path1, path2):
        self.path1 = path1
        self.path2 = path2

    def run(self):
        while True:
            self.printsignal.emit(logline)


class Ui(QMainWindow, Ui_MainWindow):
    """"定义构造主窗口"""
    def __init__(self):
        super(Ui, self).__init__()
        self.left_path = None
        self.right_path = None
        self.logline = 'Null'
        self.workpath = os.getcwd()
        # self.threadprint = ThreadPrint()
        # self.threadprint.printsignal.connect(self.printlog)

        self.setupUi(self)
        self.run()

    def set_file_path1(self):
        dlg = QFileDialog
        filepath, t = dlg.getOpenFileName(self, "选择文件",
                                          self.workpath,
                                          "所有文件 (*.*);;All Files (*.*)")
        self.left_path = filepath
        self.lineEdit.setText(filepath)

    def set_file_path2(self):
        dlg = QFileDialog
        filepath, t = dlg.getOpenFileName(self, "选择文件",
                                          self.workpath,
                                          "所有文件 (*.*);;All Files (*.*)")
        self.right_path = filepath
        self.lineEdit_2.setText(filepath)

    def compare(self):
        # self.threadprint.set_params(self.left_path, self.right_path)
        # if not self.threadprint.isRunning():
        #     self.threadprint.start()
        self.path1 = r"E:\Redmine2019\LEVIOEM测试\OEM_通用_7.1.5\NUC972_750ML_OEM_7.1.5_2019-05-15\productfile.osf"
        self.path2 = r"E:\Redmine2019\LEVIOEM测试\OEM_通用_7.1.5\NUC972_750ML_OEM_7.1.5_2019-05-15\productfile.osf"
        _thread.start_new_thread(do_compare, (self.path1, self.path2))
        # do_compare(self.path1, self.path2)


    def printlog(self, logline:str):
        print(logline)

    def run(self):

        self.pushButton.clicked.connect(self.set_file_path1)
        self.pushButton_2.clicked.connect(self.set_file_path2)
        self.pushButton_3.clicked.connect(self.compare)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui()
    ui.show()

    sys.exit(app.exec_())

