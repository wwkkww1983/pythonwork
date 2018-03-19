#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: sign_up.py
# Author:    fan
# date:      2018/3/19
# -----------------------------------------------------------
import logging as log
from time import sleep
from ui_sign_up import Ui_dialog_sign
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (QMessageBox, QApplication, QWidget, QMainWindow, QGridLayout, QLineEdit, QLabel)


class SignUp(QWidget, Ui_dialog_sign):
    def __init__(self):
        super(SignUp, self).__init__()
        self.setupUi(self)
        self.setMaximumSize(400, 300)
        self.setMinimumSize(400, 300)
        self.pushButton_cancel.clicked.connect(self.cancel)
        self.pushButton_sign.clicked.connect(self.start_sign)
        self.messagebox = QMessageBox()

    def name_null_err(self):
        self.messagebox.information(self,
                                    '提示',
                                    '用户名为空，注册失败。',
                                    QMessageBox.Ok)

    def pswd_null_err(self):
        self.messagebox.information(self,
                                    '提示',
                                    '密码为空，注册失败。',
                                    QMessageBox.Ok)

    def name_len_err(self):
        self.messagebox.information(self,
                                    '提示',
                                    '用户名长度错误，注册失败。',
                                    QMessageBox.Ok)

    def pswd_len_err(self):
        self.messagebox.information(self,
                                    '提示',
                                    '密码长度错误，注册失败。',
                                    QMessageBox.Ok)

    def name_char_err(self, ch):
        self.messagebox.information(self,
                                    '提示',
                                    '用户名含不支持的字符<{}>，注册失败。'.format(ch),
                                    QMessageBox.Ok)

    def pswd_char_err(self, ch):
        self.messagebox.information(self,
                                    '提示',
                                    '密码含不支持的字符<{}>，注册失败。'.format(ch),
                                    QMessageBox.Ok)

    def sign_success(self):
        self.messagebox.information(self,
                                    '提示',
                                    '注册成功！',
                                    QMessageBox.Ok)

    def show_sign_info(self):
        pass

    def check_name(self):
        pass

    def check_pswd(self):
        pass

    def cancel(self):
        self.close()

    def start_sign(self):
        name = self.lineEdit_name.text()
        pswd = self.lineEdit_pswd.text()
        if not name:
            self.name_null_err()
        elif not pswd:
            self.pswd_null_err()
        elif not 6 <= len(name) <= 16:
            self.name_len_err()
        elif not 6 <= len(pswd) <= 16:
            self.pswd_len_err()
        else:
            self.sign_success()

# lineedit = QLineEdit()
# lineedit.text()
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    signup = SignUp()
    signup.show()
    sys.exit(app.exec_())

