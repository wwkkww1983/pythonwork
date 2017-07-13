# -*- coding: utf-8 -*-
from PyQt5.QtCore import (pyqtSignal, QMutex, QMutexLocker, QPoint, QSize, Qt,
                          QThread, QWaitCondition)
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLCDNumber, QApplication, QGridLayout
from usb_hid import MYUSBHID as myhid
from sys import argv,exit
from time import sleep


class MyThreads(QThread):
    finishSignal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(MyThreads, self).__init__(parent)

        self.num = 0

    def run(self):
        for i in range(50):
            sleep(.1)
            self.num = i


class MYWINDOW(QWidget):
    def __init__(self, parent=None):
        super(MYWINDOW, self).__init__(parent)
        self.thread = MyThreads()
        self.number = 0
        self.button = None
        self.lcdnum = None

        self.thread.finishSignal.connect(self.numadd)
        self.initUI()

    def initUI(self):
        button = QPushButton()
        button.setText('BigButton')

        label = QLabel()
        label.setText('')

        lcdnum = QLCDNumber()
        lcdnum.display(0)

        grid = QGridLayout()
        grid.addWidget(button, 0, 0)
        grid.addWidget(lcdnum, 1, 0)

        self.setLayout(grid)
        self.setGeometry(300, 300, 400, 100)
        self.setWindowTitle('Data Shower')

        self.button = button
        self.lcdnum = lcdnum

    def numadd(self):
        if self.number >= 99999:
            self.number = 0
            print(self.number)
        else:
            self.number += 1
        self.lcdnum.display(self.number)

    def end(self):
        print('end')



def main():
    app = QApplication(argv)
    wd = MYWINDOW()
    wd.button.clicked.connect(wd.numadd)
    wd.show()
    exit(app.exec_())

if __name__ == '__main__':
    main()
