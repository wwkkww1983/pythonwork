#!/usr/bin/python3
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name：     SJF_file_to_xls_main.spec
# Description :
#   Author:      fan
#   date:        2018/1/8
#   IDE:         PyCharm Community Edition
# -----------------------------------------------------------
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
import xlwt, os
from ui_dialog import Ui_Dialog
from dbfile import DB
from tableintoxls import add_to_xls


class Main(QWidget, Ui_Dialog):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(self.label.text())
        self.db_file_name = ''
        self.xls_file_name = ''
        self.workpath = os.getcwd()
        self.messagebox = QMessageBox()

    def set_read_dbfile(self):
        """
        选择要打开的文件：
        参数说明：self参数、设置默认打开的窗口（当前工作目录）、设置文件对话框标题、设置文件类型筛选
        :return:None
        """
        self.db_file_name = ''
        db_file_dialog = QFileDialog()
        read_db_name, name_ok = \
            db_file_dialog.getOpenFileName(self, "打开文件",
                                           self.workpath,
                                           "示教文件 (*.db; *.sjf);;All Files (*.*)")
        if read_db_name:
            self.lineEdit_dbpath.setText(read_db_name)
            self.db_file_name = self.lineEdit_dbpath.text()
        else:
            print('fail to read sjf file.')

    def set_save_xlsfile(self):
        initial_save_name = os.path.splitext(self.db_file_name)[0] + '.xls'
        self.xls_file_name = ''
        xls_file_dialog = QFileDialog()
        save_xls_name, get_xls_ok = \
            xls_file_dialog.getSaveFileName(self,
                                            '导出',
                                            os.path.join(self.workpath, initial_save_name),
                                            'xls Files (*.xls)')
        self.xls_file_name = save_xls_name
        if save_xls_name:
            self.save_xls()
        else:
            self.messagebox.information(self,
                                        '提示',
                                        'xls未保存',
                                        QMessageBox.Ok)

    def save_xls(self):
        """
        从UI获取.db文件名和欲保存.xls名，经过处理后保存.xls文件
        :return: 无返回
        """
        db = DB()
        xls = xlwt.Workbook()

        db.get_cursor(self.db_file_name)
        tablenames = db.get_tablesnames()
        try:
            for tablename in tablenames:
                tablefields = db.get_table_fields(tablename)
                tabledata = db.get_table_data(tablename, '')
                add_to_xls(xls, (tablename, tablefields, tabledata))

            xls.save(self.xls_file_name)
            self.messagebox.information(self,
                                        '提示',
                                        '保存成功',
                                        QMessageBox.Ok)
        except Exception as e:
            self.messagebox.information(self,
                                        '提示',
                                        e,
                                        QMessageBox.Ok)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    # 点击保存按钮则在目录下生成.xls文件
    win.pushButton_selecdb.clicked.connect(win.set_read_dbfile)
    win.pushButton_db2xls.clicked.connect(win.set_save_xlsfile)
    sys.exit(app.exec_())
