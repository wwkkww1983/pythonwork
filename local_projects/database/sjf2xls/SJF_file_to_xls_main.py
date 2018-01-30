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
        point_array = sjf.func_get_sqlite_data('示教文件demo.db',
                                               'SJJT_GlueInfo',
                                               ['SortID', 'GlueName', 'XCompensation', 'YCompensation',
                                                'ZCompensation'])
        common_position = sjf.func_get_sqlite_data('示教文件demo.db',
                                                   'SJJT_PointInfo',
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
    win.pushButton_3.clicked.connect(win.set_read_dbfile)
    win.pushButton_4.clicked.connect(win.set_save_xlsfile)
    sys.exit(app.exec_())
