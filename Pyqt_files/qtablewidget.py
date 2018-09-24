#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: qtablewidget.py
# Author:    fanch
# date:      2018/09/24
# -----------------------------------------------------------

from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout, QApplication


class MyDialog(QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        self.MyTable = QTableWidget(4,3)
        self.MyTable.setHorizontalHeaderLabels(['姓名','身高','体重'])

        newItem = QTableWidgetItem("松鼠")
        self.MyTable.setItem(0, 0, newItem)

        newItem = QTableWidgetItem("10cm")
        self.MyTable.setItem(0, 1, newItem)

        newItem = QTableWidgetItem("60g")
        self.MyTable.setItem(0, 2, newItem)

        layout = QHBoxLayout()
        layout.addWidget(self.MyTable)
        self.setLayout(layout)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    myWindow = MyDialog()
    myWindow.show()
    sys.exit(app.exec_())
