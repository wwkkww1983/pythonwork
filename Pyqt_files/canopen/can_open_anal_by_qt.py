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

        windowSize = (900, 600)
        self.resize(*windowSize)
        self.setWindowTitle(r'Usb2Can Analyse Tool')

        font = QtGui.QFont()
        font.setFamily('宋体')
        font.setPointSize(20)
        font.setBold(True)

        self.label = QtWidgets.QLabel('', self)
        self.label.setText(r'Usb2Can Analyse Tool')
        self.label.setFont(font)
        self.label.setGeometry(200,10,400,30)

        self.table = QtWidgets.QTableWidget(self)
        tablePlace = (0, 0)
        self.table.move(*tablePlace)
        self.table.setRowCount(10)
        self.table.setColumnCount(8)
        tableSize = (600, 500)
        self.table.resize(*tableSize)
        self.table.setHorizontalHeaderLabels(['通道号', '时间标识', '传输方向', '帧ID', '帧类型','帧格式','数据长度','数据[Hex]'])
        self.table.setVerticalHeaderLabels(['1', '2', '3', '4', '5', '6'])

        newItem = QtWidgets.QTableWidgetItem("apple")
        self.table.setItem(0, 0, newItem)

        layout = QtWidgets.QVBoxLayout()
        layout.addSpacing(170)
        layout.addWidget(self.table)
        layout.addSpacing(100)
        self.setLayout(layout)

    def readFile(self):
        filePath = r'canOpenAnal.txt'
        file = open(filePath, 'r', -1, 'gbk')
        f = file.readlines()
        for lineId in range(len(f)):
            f[lineId] = f[lineId].strip('\n')

        labelvspace = 50
        labelhspace = 25

        label0 = QtWidgets.QLabel(self)
        label0.setText('文件信息：')
        label0.move(10, 30)


        label1 = QtWidgets.QLabel(self)
        label1.setText(f[1])
        label1.move(labelhspace,labelvspace)
        label2 = QtWidgets.QLabel(self)
        label2.setText(f[2])
        label2.move(labelhspace,labelvspace+20)
        label3 = QtWidgets.QLabel(self)
        label3.setText(f[3])
        label3.move(labelhspace,labelvspace+2*20)
        label4 = QtWidgets.QLabel(self)
        label4.setText(f[4])
        label4.move(labelhspace,labelvspace+3*20)
        label5 = QtWidgets.QLabel(self)
        label5.setText(f[5])
        label5.move(labelhspace,labelvspace+4*20)

        label6 = QtWidgets.QLabel(self)
        label6.setText('解析数据：')
        label6.move(10, labelvspace+5*20)
        print(f)


app = QApplication(sys.argv)
win = WindowTest()
win.show()
sys.exit(app.exec_())
