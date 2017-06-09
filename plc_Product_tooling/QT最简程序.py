# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

import sys
from PyQt5.QtWidgets import QApplication, QWidget,QMainWindow
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets

def change():
    print('abc')
def main():  
    
    window	= QMainWindow()
    window.setGeometry(100, 100, 800, 600)

    button = QtWidgets.QPushButton(window)
    button.setText('button')
    button.setGeometry(200,200,100,50)

    combobox = QtWidgets.QComboBox(window)
    combobox.setGeometry(50,50,100,50)
    combobox.addItem('A')
    combobox.addItem('B')

    button.clicked.connect(change)
    combobox.currentIndexChanged.connect(change)

    window.show()
    return app.exec_()


if __name__ == '__main__':
  app = QApplication(sys.argv)
  main()