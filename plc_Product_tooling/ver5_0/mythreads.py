# -*- coding: utf-8 -*-
from PyQt5.QtCore import (pyqtSignal, QMutex, QMutexLocker, QPoint, QSize, Qt,
                          QThread, QWaitCondition)
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLCDNumber, QApplication, QGridLayout
from usb_hid import MYUSBHID as myhid
from sys import argv,exit


# class MYTHREADS(QThread):
#     finishSignal = pyqtSignal(list)
#
#     def __init__(self, parent=None):
#         super(MYTHREADS, self).__init__(parent)
#
#         self.digit_hid = None
#         self.anolog_hid = None
#
#     def run(self):
#         while True:
#             for i in range(99999999):
#                 if i % 10000 == 0:
#                     print(i)
#                 else:
#                     pass


class MYWINDOW(QMainWindow):
    def __init__(self, parent=None):
        super(MYWINDOW, self).__init__(parent)
        self.number = 0

        button = QPushButton()
        button.setText('BigButton')
        self.button = button

        label = QLabel()
        label.setText('')
        self.label = label

        lcdnum = QLCDNumber()
        lcdnum.setNumDigits(0)
        self.lcdnum = lcdnum

        grid = QGridLayout()
        self.grid = grid
        grid.addWidget(self.button, 0, 0)
        grid.addWidget(self.lcdnum, 1, 0)
        self.setLayout(self.grid)


    def numadd(self):
        self.number += 1
        self.lcdnum.setNumDigits(self.number)
if __name__ == '__main__':
    app = QApplication(argv)
    wd = MYWINDOW()
    wd.button.clicked.connect(wd.numadd)
    wd.show()
    exit(app.exec_())
