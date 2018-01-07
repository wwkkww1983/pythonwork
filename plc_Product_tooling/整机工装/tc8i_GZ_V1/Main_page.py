# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '首页.ui'
#
# Created: Sat Dec  9 10:15:01 2017
#      by: PyQt5 UI code generator 5.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1263, 503)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(290, 100, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.main_text_browser = QtWidgets.QTextBrowser(Dialog)
        self.main_text_browser.setGeometry(QtCore.QRect(200, 150, 291, 41))
        self.main_text_browser.setObjectName("main_text_browser")
        self.main_find_device_pushButton = QtWidgets.QPushButton(Dialog)
        self.main_find_device_pushButton.setGeometry(QtCore.QRect(510, 150, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.main_find_device_pushButton.setFont(font)
        self.main_find_device_pushButton.setObjectName("main_find_device_pushButton")
        self.main_test_byone_pushButton = QtWidgets.QPushButton(Dialog)
        self.main_test_byone_pushButton.setGeometry(QtCore.QRect(230, 340, 301, 61))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(28)
        self.main_test_byone_pushButton.setFont(font)
        self.main_test_byone_pushButton.setObjectName("main_test_byone_pushButton")
        self.main_debug_pyge_toolButton = QtWidgets.QToolButton(Dialog)
        self.main_debug_pyge_toolButton.setGeometry(QtCore.QRect(330, 10, 61, 21))
        self.main_debug_pyge_toolButton.setObjectName("main_debug_pyge_toolButton")
        self.label2 = QtWidgets.QLabel(Dialog)
        self.label2.setGeometry(QtCore.QRect(690, 160, 521, 121))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(72)
        self.label2.setFont(font)
        self.label2.setText("")
        self.label2.setObjectName("label2")

        self.retranslateUi(Dialog)
        # self.main_debug_pyge_toolButton.clicked.connect(Dialog.open_second_window)
        # self.main_find_device_pushButton.clicked.connect(Dialog.check_device)
        # self.main_test_byone_pushButton.clicked.connect(Dialog.begin_check_one)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        # Dialog.show()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "被检测模块型号"))
        self.label2.setText(_translate("Dialog",'    '))
        self.main_find_device_pushButton.setText(_translate("Dialog", "查找设备"))
        self.main_test_byone_pushButton.setText(_translate("Dialog", "一 键 检 测"))
        self.main_debug_pyge_toolButton.setText(_translate("Dialog", "调试页面"))

