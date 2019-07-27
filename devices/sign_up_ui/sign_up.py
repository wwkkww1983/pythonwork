#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: sign_up.py
# Author:    fan
# date:      2018/3/19
# -----------------------------------------------------------

from ui_sign_up import Ui_dialog_sign
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QPixmap, QBrush
from PyQt5.QtWidgets import (QMessageBox, QApplication, QWidget, QMainWindow, QGridLayout, QLineEdit, QLabel)


class SignUp(QWidget, Ui_dialog_sign):
    def __init__(self):
        super(SignUp, self).__init__()
        self.setupUi(self)
        self.setMaximumSize(400, 300)
        self.setMinimumSize(400, 300)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('用户登录')
        palette = QPalette()
        picture = QPixmap('background.jpg')
        palette.setBrush(self.backgroundRole(), QBrush(picture))
        self.setPalette(palette)
        self.pushButton_cancel.clicked.connect(self.cancel)
        self.pushButton_sign.clicked.connect(self.start_sign)
        self.messagebox = QMessageBox()
        self.name = ''
        self.pswd = ''

    def get_sign_result(self, word):
        """
        获取登录结果，弹出消息提示框
        :param word: 
        :return: 
        """
        if word == '登录成功！':
            info = word
        else:
            info = word + '，登录失败！'
        self.messagebox.information(self,
                                    '提示',
                                    info,
                                    QMessageBox.Ok)


    def show_sign_info(self):
        pass

    def check_name(self):
        name = self.name
        try:
            for i in list(name):
                if not (48 <= ord(i) <= 57 or 65 <= ord(i) <= 90 or 97 <= ord(i) <= 122 or ord(i) == 95):
                    return False
            return True
        except:
            return False

    def check_pswd(self):
        pswd = self.pswd
        try:
            for i in list(pswd):
                if not (32 <= ord(i) <= 126):
                    return False
            return True
        except:
            return False

    def cancel(self):
        self.close()

    def start_sign(self):
        name = self.lineEdit_name.text()
        pswd = self.lineEdit_pswd.text()
        self.name = name
        self.pswd = pswd
        self.keyword = ''
        if not name:
            self.keyword = '用户名为空'
        elif not pswd:
            self.keyword = '密码为空'
        elif len(name) < 6:
            self.keyword = '用户名太短'
        elif len(name) > 16:
            self.keyword = '用户名太长'
        elif len(pswd) < 6:
            self.keyword = '密码太短'
        elif len(pswd) > 16:
            self.keyword = '密码太长'
        elif not self.check_name():
            self.keyword = '用户名包含不支持的字符'
        elif not self.check_pswd():
            self.keyword = '密码包含不支持的字符'
        else:
            self.keyword = '登录成功！'

        self.get_sign_result(self.keyword)

# lineedit = QLineEdit()
# lineedit.text()
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    signup = SignUp()
    signup.show()
    sys.exit(app.exec_())

