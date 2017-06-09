#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
运行can_open_anal.py 以打开USB2CAN帧数据解析工具
"""
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets
from ui_can_open_analyse_tool import Ui_usb2CanDataAnalTool

def readUsbCanDataFile(fPath):
    file_read = open(fPath, 'r', -1, 'gbk')
    f = file_read.readlines()
    head_info = []
    head_label = []
    data_table = []
    data_num = 0
    for line_id in range(len(f)):
        f[line_id] = f[line_id].rstrip()
        if 1 <= line_id <= 5:
            head_info.append(f[line_id])
        if  line_id == 8:
            head_label = f[line_id].split(maxsplit=8)
        if line_id >= 9:
            data_num += 1
            data_id = f[line_id].split(maxsplit=8)
            data_table.append(data_id)
    head_info.append('帧记录数：'+str(data_num)+' 条')
    """
    for i in head_info:
        print(i)
    print(head_label)
    for k in data_table:
        print(k)
        """
    file_read.close()
    return(head_info, head_label, data_table, data_num)


#filePath = r'C:\Users\fan\OneDrive\pythonwork\local_projects\IO\canOpenAnal.txt'
filePath = r'C:\Users\fan\OneDrive\pythonwork\local_projects\IO\CANMessage.txt'
ff = readUsbCanDataFile(filePath)


class Usb2CanDataAnalTool(QWidget):
    def __init__(self, parent=None):
        super(Usb2CanDataAnalTool, self).__init__(parent)

        self.ui = Ui_usb2CanDataAnalTool()
        self.ui.setupUi(self)

    def set_file_info(self, file_info):
        self.ui.label_FileInfo.setText('文件信息')
        self.ui.label_Name.setText(file_info[0])
        self.ui.label_Can1.setText(file_info[1])
        self.ui.label_Can2.setText(file_info[2])
        self.ui.label_Date.setText(file_info[3])
        self.ui.label_Time.setText(file_info[4])
        self.ui.label_dataNum.setText(file_info[5])
        self.ui.label_DataTable.setText('帧记录')
        
    def set_data_table(self, datahead, datatable, howmanydatarow):
        self.ui.table_Widget.setRowCount(howmanydatarow)
        self.ui.table_Widget.setColumnCount(9)
        self.ui.table_Widget.setColumnWidth(0, 80)
        self.ui.table_Widget.setColumnWidth(1, 80)
        self.ui.table_Widget.setColumnWidth(2, 120)
        self.ui.table_Widget.setColumnWidth(3, 80)
        self.ui.table_Widget.setColumnWidth(4, 80)
        self.ui.table_Widget.setColumnWidth(5, 80)
        self.ui.table_Widget.setColumnWidth(6, 80)
        self.ui.table_Widget.setColumnWidth(7, 80)
        self.ui.table_Widget.setColumnWidth(8, 160)
        """
        table_head = QtWidgets.QTableView.horizontalHeader(self)
        table_head.resizeSection(0, 20)
        table_head.resizeSection(1, 20)
        table_head.resizeSection(2, 20)
        table_head.resizeSection(3, 20)
        table_head.resizeSection(4, 20)
        table_head.resizeSection(5, 20)
        table_head.resizeSection(6, 20)
        table_head.resizeSection(7, 20)
        table_head.resizeSection(8, 20)
        self.ui.table_Widget.setHorizontalHeaderLabels(table_head)
        """


        self.ui.table_Widget.setHorizontalHeaderLabels(datahead)
        table_layout = QtWidgets.QVBoxLayout()
        table_layout.addSpacing(180)
        table_layout.addWidget(self.ui.table_Widget)
        table_layout.addSpacing(60)
        self.setLayout(table_layout)
        print(howmanydatarow)
        for rowid in range(howmanydatarow):
            for dataid in range(9):
                datatableitem = QtWidgets.QTableWidgetItem(datatable[rowid][dataid])
                self.ui.table_Widget.setItem(rowid, dataid, datatableitem)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    usb2CanDataAnal = Usb2CanDataAnalTool()
    usb2CanDataAnal.set_file_info(ff[0])
    usb2CanDataAnal.set_data_table(ff[1], ff[2], ff[3]-70000)
    usb2CanDataAnal.show()
    sys.exit(app.exec_())
