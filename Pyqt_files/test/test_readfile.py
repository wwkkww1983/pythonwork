# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
这只是一个pyqt5的简单示例程序
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets


class WindowTest(QWidget):
    def __init__(self, parent=None):
        super(WindowTest, self).__init__(parent)
        self.readFile()

        windowSize = (850, 600)
        titlePlace = (10, 20)
        self.resize(*windowSize)
        self.setWindowTitle('A Test Window')

        font = QtGui.QFont()
        font.setFamily('宋体')
        font.setPointSize(28)
        font.setBold(True)

        self.label = QtWidgets.QLabel('', self)
        self.label.setText('Test')
        self.label.setFont(font)
        self.label.move(*titlePlace)

        self.table = QtWidgets.QTableWidget(self)
        tablePlace = (0, 0)
        self.table.move(*tablePlace)
        self.table.setRowCount(10)
        self.table.setColumnCount(8)
        tableSize = (600, 500)
        self.table.resize(*tableSize)
        self.table.setHorizontalHeaderLabels(['Num', 'header_label1', 'label2', 'header_label3', '4'])
        self.table.setVerticalHeaderLabels(['1', '2', '3', '4', '5', '6'])

        newItem = QtWidgets.QTableWidgetItem("apple")
        self.table.setItem(0, 0, newItem)

        layout = QtWidgets.QVBoxLayout()
        layout.addSpacing(50)
        layout.addWidget(self.table)
        layout.addSpacing(100)
        self.setLayout(layout)

    def readFile(self):
        filePath = r'test_readText.txt'
        file = open(filePath, 'r', -1, 'gbk')
        f = file.readlines()
        for lineId in range(len(f)):
            f[lineId] = f[lineId].strip('\n')

        label1 = QtWidgets.QLabel(self)
        label1.setText(f[0])
        label1.move(100,20)
        label2 = QtWidgets.QLabel(self)
        label2.setText(f[1])
        label2.move(200, 20)
        print(f)


app = QApplication(sys.argv)
win = WindowTest()
win.show()
sys.exit(app.exec_())
