# -*- coding: utf-8 -*-
from PyQt5.QtCore import (pyqtSignal, pyqtSlot,  QMutex, QMutexLocker, QPoint, QSize, Qt,
                          QThread, QWaitCondition)
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton, QLabel, QLCDNumber, QApplication, QGridLayout
from usb_hid import MYUSBHID as myhid
from sys import argv,exit
from time import sleep


class MyThreads(QThread):
    heartBeartSignal = pyqtSignal()

    def __init__(self, parent=None):
        super(MyThreads, self).__init__(parent)

    def run(self):
        while True:
            sleep(0.001)
            self.heartBeartSignal.emit()


class MyThreads2(QThread):
    heartBeartSignal = pyqtSignal(int)

    def __init__(self, parent=None):
        super(MyThreads2, self).__init__(parent)
        self.number = 0

    def run(self):
        while True:
            num = self.number
            if num < 0 or num >= 9999:
                num = 0
            else:
                num += 1
            self.number = num
            sleep(0.005)
            self.heartBeartSignal.emit(self.number)


class MyWindow(QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.thread = MyThreads2()
        self.number = 0
        self.button = None
        self.lcdnum = None
        self.label = None
        self.running = False
        self.initUI()
        self.messagebox = QMessageBox()
        self.button.clicked.connect(self.control)

    def initUI(self):
        button = QPushButton()
        button.setText('Start')
        label = QLabel()
        label.setText('Stopped')

        lcdnum = QLCDNumber()
        lcdnum.display(0)
        grid = QGridLayout()
        grid.addWidget(button, 2, 0)
        grid.addWidget(label, 1, 0)
        grid.addWidget(lcdnum, 0, 0)

        self.setLayout(grid)
        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('Data Shower')
        self.button = button
        self.label = label
        self.lcdnum = lcdnum

    def showdata(self, num):
        # self.numadd()
        self.number = num
        self.display()

    def control(self):
        text = self.button.text()
        if text == 'Stop':
            self.stop()
        if text == 'Start':
            self.start()

    def numadd(self):
        num = self.number
        if num < 0 or num >= 9999:
            num = 0
        else:
            num += 1
        self.number = num

    def display(self):
        self.lcdnum.display(self.number)

    def start(self):
        if self.running is not False:
            self.messagebox.information(self, '提示', 'Process has been running')
        else:
            self.button.setText('Stop')
            self.label.setText('Running')
            self.thread.heartBeartSignal.connect(self.showdata)
            self.thread.start()
            self.running = True

    def stop(self):
        if self.running is False:
            self.messagebox.information(self, '提示', 'Process has been stopped')
        else:
            self.button.setText('Start')
            self.label.setText('Stopped')
            self.thread.disconnect()
            self.running = False


def main():
    app = QApplication(argv)
    wd = MyWindow()
    wd.show()
    exit(app.exec_())

if __name__ == '__main__':
    main()
