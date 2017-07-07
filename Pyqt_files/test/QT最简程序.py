# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import  QtWidgets


def change():
    time_str = time.strftime("%Y.%m.%d %H:%M:%S", time.gmtime())
    return time_str
def main():
    window	= QMainWindow()
    window.setGeometry(100, 100, 800, 600)

    button = QtWidgets.QPushButton(window)
    button.setText('button')
    button.setGeometry(200,100,100,50)

    label = QtWidgets.QLabel(window)
    label.setText('')
    label.setGeometry(200,200,200,50)

    combobox = QtWidgets.QComboBox(window)
    combobox.setGeometry(200,300,100,50)
    combobox.addItem('A')
    combobox.addItem('B')

    def show_time():
        label.setText(change())

    button.clicked.connect(show_time)
    combobox.currentIndexChanged.connect(change)

    window.show()
    return app.exec_()


if __name__ == '__main__':
  app = QApplication(sys.argv)
  main()