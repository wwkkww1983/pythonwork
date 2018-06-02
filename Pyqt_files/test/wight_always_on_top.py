#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: wight_always_on_top
# Author:    fan
# date:      2018/6/2
# -----------------------------------------------------------
import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QPainter, QPalette, QPixmap, QBrush
from PyQt5.QtCore import Qt


def change():
    time_str = time.strftime("%Y.%m.%d %H:%M:%S", time.gmtime())
    return time_str


def main():
    window= QMainWindow()
    window.setGeometry(100, 100, 800, 600)

    window.setAttribute()

    # 设置window背景
    palette = QPalette()
    picture = QPixmap('背景.jpg')
    palette.setBrush(window.backgroundRole(), QBrush(picture))
    window.setPalette(palette)

    button = QtWidgets.QPushButton(window)
    button.setText('button')
    button.setGeometry(200,100,100,50)

    label = QtWidgets.QLabel(window)
    label.setText('23456789')
    label.setGeometry(200,200,200,50)
    # 设置标签颜色
    label.setAutoFillBackground(True)
    pale = QPalette()
    pale.setColor(QPalette.Window, Qt.yellow)
    pale.setColor(QPalette.WindowText, Qt.red)
    label.setPalette(pale)
    # 设置标签颜色完毕
    # 设置字体
    label.setFont(QFont('Microsoft YaHei UI', 20, QFont.Bold))

    combobox = QtWidgets.QComboBox(window)
    combobox.setGeometry(200,300,100,50)
    combobox.addItem('A')
    combobox.addItem('B')
    combobox.currentText()

    lineEdit = QtWidgets.QLineEdit(window)
    lineEdit.setGeometry(200, 400, 100, 50)
    lineEdit.setText('abcd')
    lineEdit.text()

    def show_time():
        label.setText(change())

    button.clicked.connect(show_time)
    combobox.currentIndexChanged.connect(change)
    button.setDisabled(False)

    window.show()
    return app.exec_()


if __name__ == '__main__':
  app = QApplication(sys.argv)
  main()