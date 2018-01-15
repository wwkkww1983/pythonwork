#!/usr/bin/python3
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name：     SJF_file_to_xls_main.py
# Description :
#   Author:      fan
#   date:        2018/1/8
#   IDE:         PyCharm Community Edition
# -----------------------------------------------------------
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import xlwt, os
from ui_dialog import Ui_Dialog
import SJF_file_to_xls as sjf


class Main(QWidget, Ui_Dialog):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(self.label.text())
        self.db_file_name = ''
        self.xls_file_name = ''
        self.workpath = os.getcwd()

    def get_read_dbfile_path(self):
        db_path, db_path_ok = QFileDialog.getOpenFileName(self,
                                                          self.workpath,
                                                          "打开文件",
                                                          "All Files (*);;DB Files (*.db);;SFJ Files (*.sjf)")
        self.lineEdit_3.SetText(db_path)
        self.db_file_name = self.lineEdit_3.SetText(db_path)

    def get_save_xlsfile_path(self):
        self.xls_file_name, xls_save_ok = QFileDialog.getSaveFileName(self,
                                                                      "另存为",
                                                                      self.workpath,
                                                                      "All Files (*);;DB Files (*.db);;SFJ Files (*.sjf)")

    def do_something(self):
        """
        从UI获取.db文件名和欲保存.xls名，经过处理后保存.xls文件
        :return: 无返回
        """
        point_array = sjf.func_get_sqlite_data('示教文件demo.db', 'SJJT_GlueInfo',
                                           ['SortID', 'GlueName', 'XCompensation', 'YCompensation', 'ZCompensation'])
        common_position = sjf.func_get_sqlite_data('示教文件demo.db', 'SJJT_PointInfo',
                                               ['ID', 'ElemIndex', 'ElemType', 'X', 'Y', 'Z', 'OpenGlueDelayTime'])
        glue_io_position_data = sjf.func_get_glueio_positon(point_array[2], common_position[2])
        xls = xlwt.Workbook()
        sjf.add_to_xls(xls, point_array)
        sjf.add_to_xls(xls, common_position)
        sjf.add_to_xls(xls, glue_io_position_data)
        xls.save(self.xls_file_name)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    # 点击保存按钮则在目录下生成.xls文件
    win.pushButton_3.clicked.connect(win.get_read_dbfile_path)
    win.pushButton.clicked.connect(win.do_something)

    sys.exit(app.exec_())
