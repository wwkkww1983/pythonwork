#!/usr/bin/python3
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name：     SJF_file_to_xls_main.spec
# Description :
#   Author:      fan
#   date:        2018/1/8
#   IDE:         PyCharm Community Edition
# -----------------------------------------------------------
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import xlwt, os
from ui_dialog import Ui_Dialog
import SJF_file_to_xls as sjf


def add_to_xls(xls, tables):
    """
    将表格信息按照一定格式（表格名_str，字段_tuple，数据_tuple(tuple)）记录到指定xls文件当中
    """
    table_name = tables[0]
    table_firstline = tables[1]
    table_data = tables[2]
    # xls = xlwt.Workbook()
    sheet = xls.add_sheet(table_name)
    sheet.write(0, 0, table_name)
    for i in range(len(table_firstline)):
        sheet.write(1, i, tables[1][i])

    for i in range(len(table_data)):
        for j in range(len(table_data[0])):
            sheet.write(i+2, j, table_data[i][j])


class Main(QWidget, Ui_Dialog):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(self.label.text())
        self.db_file_name = ''
        self.xls_file_name = ''
        self.workpath = os.getcwd()
        self.lineEdit_3.setText(os.path.join(self.workpath, '*.sjf'))
        self.lineEdit_6.setText(os.path.join(self.workpath, '*.xls'))

    def set_read_dbfile(self):
        """
        选择要打开的文件：
        参数说明：self参数、设置默认打开的窗口（当前工作目录）、设置文件对话框标题、设置文件类型筛选
        :return:None
        """
        self.db_file_name = ''
        db_file_dialog = QFileDialog()
        read_db_name, name_ok = db_file_dialog.getOpenFileName(self, "打开文件",
                                                               self.workpath,
                                                               "示教文件 (*.db; *.sjf);;All Files (*.*)")
        if read_db_name:
            self.lineEdit_3.setText(read_db_name)
            self.db_file_name = self.lineEdit_3.text()
        else:
            print('fail to read sjf file.')

    def set_save_xlsfile(self):
        initial_save_name = os.path.splitext(self.db_file_name)[0] + '.xls'
        self.xls_file_name = ''
        xls_file_dialog = QFileDialog()
        save_xls_name, get_xls_ok = xls_file_dialog.getSaveFileName(self,
                                                                    '另存为',
                                                                    os.path.join(self.workpath, initial_save_name),
                                                                    'xls Files (*.xls)')
        if save_xls_name:
            self.lineEdit_6.setText(save_xls_name)
            self.xls_file_name = self.lineEdit_6.text()
            self.do_something()
        else:
            print('fail to save xls file.')

    def do_something(self):
        """
        从UI获取.db文件名和欲保存.xls名，经过处理后保存.xls文件
        :return: 无返回
        """
        glue_info = sjf.func_get_sqlite_data(self.db_file_name,
                                             'SJJT_GlueInfo',
                                             ['ID', 'GlueName', 'XCompensation', 'YCompensation', 'ZCompensation'])
        point_info = sjf.func_get_sqlite_data(self.db_file_name,
                                              'SJJT_PointInfo',
                                              ['ID', 'ElemIndex', 'ElemType', 'X', 'Y', 'Z', 'OpenGlueDelayTime'])
        arry_info = sjf.func_get_sqlite_data(self.db_file_name,
                                             'SJJT_ArrayInfo',
                                             ['ID', 'X', 'Y', 'Z'])
        arry_format = sjf.func_get_sqlite_data(self.db_file_name,
                                               'SJJT_FileInfo',
                                               ['XDirectionNum', 'YDirectionNum'])
        glue_io_position_data = sjf.func_get_glueio_positon(glue_info[2], point_info[2], arry_info[2], arry_format[2])
        xls = xlwt.Workbook()
        add_to_xls(xls, glue_info)
        add_to_xls(xls, point_info)
        add_to_xls(xls, arry_info)
        add_to_xls(xls, arry_format)
        add_to_xls(xls, glue_io_position_data)
        xls.save(self.xls_file_name)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    # 点击保存按钮则在目录下生成.xls文件
    win.pushButton_3.clicked.connect(win.set_read_dbfile)
    win.pushButton_4.clicked.connect(win.set_save_xlsfile)
    win.pushButton_save_xls.clicked.connect(win.)
    sys.exit(app.exec_())
