# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
# test.py
"""
只是一个pyqt5的简单示例程序
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets

class WindowTest(QWidget):
    def __init__(self,parent=None):
        super(WindowTest, self).__init__(parent)

        windowSize = (800, 600)
        self.resize(*windowSize)
        self.setObjectName('Dialog')
        self.setWindowTitle('A Test Window')


        font = QtGui.QFont()
        font.setFamily('宋体')
        font.setPointSize(19)
        font.setBold(True)

        self.label = QtWidgets.QLabel('', self)
        self.label.setText('Test')
        self.label.setFont(font)
        self.label.move(100,100)

        self.button = QtWidgets.QPushButton('', self)
        self.button.setText('pushbutton')
        self.button.move(200,100)

        self.combobox = QtWidgets.QComboBox(self)
        self.combobox.addItem("")
        self.combobox.addItem("")
        self.combobox.setItemText(0,'A')
        self.combobox.setItemText(1,'B')
        self.combobox.move(300,100)
        self.combobox.setDisabled()


        self.label2 = QtWidgets.QLabel('', self)
        self.label2.setText(self.combobox.currentText())
        self.label2.move(400, 100)





        # self.table = QtWidgets.QTableWidget(self)
        # tablePlace = (0, 0)
        # self.table.move(*tablePlace)
        # self.table.setRowCount(10)
        # self.table.setColumnCount(8)
        # tableSize = (600, 500)
        # self.table.resize(*tableSize)
        # self.table.setHorizontalHeaderLabels(['Num', 'header_label1', 'label2', 'header_label3', '4'])
        # self.table.setVerticalHeaderLabels(['1', '2', '3', '4', '5', '6'])
        #
        # newItem = QtWidgets.QTableWidgetItem("apple")
        # self.table.setItem(0, 0,newItem)
        #
        # layout = QtWidgets.QVBoxLayout()
        # layout.addSpacing(50)
        # layout.addWidget(self.table)
        # layout.addSpacing(100)
        # self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WindowTest()

    win.show()
    sys.exit(app.exec_())