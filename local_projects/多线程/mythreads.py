# -*- coding: utf-8 -*-
from PyQt5.QtCore import (pyqtSignal, pyqtSlot,  QMutex, QMutexLocker, QPoint, QSize, Qt,
                          QThread, QWaitCondition)
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton, QLabel, QLCDNumber, QApplication, QGridLayout
from usb_hid import MYUSBHID as myhid
from sys import argv,exit
from time import sleep


# class MyThreads(QThread):
#     heartBeartSignal = pyqtSignal()
#
#     def __init__(self, parent=None):
#         super(MyThreads, self).__init__(parent)
#
#     def run(self):
#         while True:
#             sleep(0.001)
#             self.heartBeartSignal.emit()


class MyThreads(QThread):
    heartBeartSignal = pyqtSignal(int)

    def __init__(self, parent=None):
        super(MyThreads, self).__init__(parent)
        self.number = 0

    def run(self):
        num = self.number
        while True:
            if num < 0 or num >= 999:
                num = 0
            else:
                num += 1
                sleep(.01)
                print(num)
                self.number = num
                self.heartBeartSignal.emit(self.number)


class MyWindow(QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.thread = MyThreads()
        self.number = 0
        self.button = None
        self.lcdnum = None
        self.label = None
        self.running = False
        self.initUI()
        self.messagebox = QMessageBox()
        self.button.clicked.connect(self.control)

    def initUI(self):
        button = QPushButton('START')
        button1 = QPushButton('关闭线程')
        label = QLabel('Stopped')
        label1 = QLabel('状态：线程已开启')

        lcdnum = QLCDNumber()
        lcdnum.display(0)

        grid = QGridLayout()
        grid.addWidget(lcdnum, 0, 0)
        grid1 = QGridLayout()
        grid1.addWidget(label, 0, 0)
        grid1.addWidget(label1, 0, 1)
        grid1.addWidget(button, 1, 0)
        grid1.addWidget(button1, 1, 1)
        grid.addLayout(grid1, 1, 0)

        self.setLayout(grid)
        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('Data Shower')
        self.button = button
        self.label = label
        self.lcdnum = lcdnum

    def control(self):
        text = self.button.text()
        if text == 'STOP':
            self.stop()
        if text == 'START':
            self.start()

    def start(self):
        if self.running is not False:
            self.messagebox.information(self, '提示', 'Process has been running')
        else:
            self.button.setText('STOP')
            self.label.setText('Running')
            self.thread.heartBeartSignal.connect(self.showdata)
            self.thread.start()
            self.running = True

    def showdata(self, num):
        self.number = num
        self.display()

    def display(self):
        self.lcdnum.display(self.number)

    def stop(self):
        if self.running is False:
            self.messagebox.information(self, '提示', 'Process has been stopped')
        else:
            self.thread.terminate()
            self.thread.wait()
            self.running = False
            self.button.setText('START')
            self.label.setText('Stopped')


def main():
    app = QApplication(argv)
    wd = MyWindow()
    wd.show()
    exit(app.exec_())

if __name__ == '__main__':
    main()
