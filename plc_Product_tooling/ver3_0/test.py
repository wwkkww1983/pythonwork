# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
# test.py
"""
只是一个pyqt5的简单示例程序
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets


# class WindowTest(QWidget):
class WindowTest(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(WindowTest, self).__init__(parent)
        self.setGeometry(100, 100, 800, 600)
        # self.setSizePolicy(4, 4)
        self.setObjectName('MainWindow')
        self.setWindowTitle('A Test Window')

        font = QtGui.QFont()
        font.setFamily('宋体')
        font.setPointSize(28)
        font.setBold(True)

        self.label = QtWidgets.QLabel('', self)
        self.label.setText('Test')
        self.label.setFont(font)
        self.label.move(10, 10)

        # self.button = QtWidgets.QPushButton('', self)
        # self.button.isChecked()
        # self.button.setChecked()
        # self.button.setAutoFillBackground(True)
        # palette = QtGui.Q

        self.child_widget_top = QtWidgets.QWidget(self)
        self.child_widget_top.setGeometry(0, 0, 800, 100)
        self.child_widget_top.setObjectName('')
        self.child_widget_top.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        color = QtGui.QColor(192, 253, 123)
        palette.setColor(self.child_widget_top.backgroundRole(), color)
        self.child_widget_top.setPalette(palette)

        self.child_widget_left = QtWidgets.QWidget(self)
        self.child_widget_left.setGeometry(0,100,200,500)
        self.child_widget_left.setAutoFillBackground(True)
        color = QtGui.QPixmap('source/backgroud_800_600px.png')
        palette.setBrush(self.child_widget_left.backgroundRole(),QtGui.QBrush(color))
        self.child_widget_left.setPalette(palette)

        self.child_widget_right = QtWidgets.QWidget(self)
        self.child_widget_right.setGeometry(200, 100, 600, 500)
        self.child_widget_right.setAutoFillBackground(True)
        color = QtGui.QColor(125, 193, 150)
        palette.setColor(self.child_widget_right.backgroundRole(), color)
        self.child_widget_right.setPalette(palette)


        self.lable_1 = QtWidgets.QLabel(self.child_widget_top)
        self.lable_1.setText('Test at top')
        self.lable_1.move(0, 0)

        self.label_2 = QtWidgets.QLabel(self.child_widget_left)
        self.label_2.setText('Test at left')
        self.label_2.move(0, 0)

        self.label_3 = QtWidgets.QLabel(self.child_widget_right)
        self.label_3.setText('Test at right')
        self.label_3.move(0, 0)

app = QApplication(sys.argv)
win = WindowTest()
win.show()
sys.exit(app.exec_())
