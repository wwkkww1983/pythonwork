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
from xlsfile import XLS, add_to_xls    # 导入XLS类、add_to_xls函数

# from tableintoxls import add_to_xls


class Main(QWidget, Ui_Dialog):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(self.label.text())
        self.select_db_name = ''
        self.save_xls_name = ''
        self.select_xls_name = ''
        self.save_db_name = ''
        self.workpath = os.getcwd()
        self.messagebox = QMessageBox()

    def set_select_dbfile(self):
        """
        选择要打开的文件：
        参数说明：self参数、设置默认打开的窗口（当前工作目录）、设置文件对话框标题、设置文件类型筛选
        :return:None
        """
        self.select_db_name = ''
        db_file_dialog = QFileDialog()
        select_path, select_type = \
            db_file_dialog.getOpenFileName(self, "打开数据库文件",
                                           self.workpath,
                                           "示教文件 (*.db; *.sjf);;All Files (*.*)")
        if select_path:
            self.lineEdit_dbpath.setText(select_path)
            self.select_db_name = self.lineEdit_dbpath.text()
        else:
            print('fail to read sjf file.')

    def set_save_xlsfile(self):
        initial_save_name = os.path.splitext(self.select_db_name)[0] + '.xls'
        self.save_xls_name = ''
        xls_file_dialog = QFileDialog()
        save_path, save_type = \
            xls_file_dialog.getSaveFileName(self,
                                            '导出',
                                            os.path.join(self.workpath, initial_save_name),
                                            'xls Files (*.xls)')
        self.save_xls_name = save_path
        if save_path:
            self.save_xls()
        else:
            self.messagebox.information(self,
                                        '提示',
                                        'xls未保存',
                                        QMessageBox.Ok)

    def set_select_xlsfile(self):
        self.select_xls_name = ''
        file_dialog = QFileDialog()
        select_path, select_type = \
            file_dialog.getOpenFileName(self, "打开Excel文件",
                                        self.workpath,
                                        "Excel文件 (*.xls);;All Files (*.*)")
        if select_path:
            # print(select_path)
            self.lineEdit_xlspath.setText(select_path)
            self.select_xls_name = self.lineEdit_xlspath.text()
        else:
            print('fail to select xls file.')

    def set_save_dbfile(self):
        initial_save_name = os.path.splitext(self.select_xls_name)[0] + '.db'
        self.save_db_name = ''
        file_dialog = QFileDialog()
        save_path, save_type = \
            file_dialog.getSaveFileName(self,
                                        '导出',
                                        os.path.join(self.workpath, initial_save_name),
                                        'Sqlite3数据文件(*.db);;示教文件(*.sjf) ')
        self.save_db_name = save_path
        if save_path:
            # print(save_path)
            self.save_db()
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

        db.get(self.select_db_name)
        tablenames = db.get_tablesnames()
        try:
            for tablename in tablenames:
                tablefields = db.get_table_fields(tablename)
                tablefield_types = db.get_table_field_types(tablename)
                tabledata = db.get_table_data(tablename, '')
                add_to_xls(xls, (tablename, tablefields, tablefield_types, tabledata))

            xls.save(self.save_xls_name)
            db.conn.commit()
            db.conn.close()
            self.messagebox.information(self,
                                        '提示',
                                        '保存成功',
                                        QMessageBox.Ok)
        except Exception as e:
            self.messagebox.information(self,
                                        '提示',
                                        e,
                                        QMessageBox.Ok)

    def save_db(self):
        """
        从UI获取.xls文件名和欲保存.db名，经过转换处理保存.db文件
        :return:
        """
        xls = XLS()
        xls.get_xls(self.select_xls_name)
        dbname = self.save_db_name
        # 创建空数据库文件
        db = DB()
        db.get(dbname)

        sheetnames = xls.get_sheet_names()
        print('get sheet names:',sheetnames)
        for sheetname in sheetnames:
            xls.get_read_sheet(sheetname)
            print("""\
            get the sheet: {}
            sheetfields: {}
            sheetdata: {}""".format(
                xls.currentsheet_name, xls.currentsheet_fields, xls.currentsheet_data
            ))
            fmt_fields = []
            for i, j in zip(xls.currentsheet_fields, xls.currentsheet_field_types):
                fmt_fields.append(' '.join([i, j]))
            # fmt_fields = [' '.join([i, j] for i,j in zip(xls.currentsheet_fields[i], xls.currentsheet_field_types[j]))]
            if db.create_table(sheetname, fmt_fields):
                print(fmt_fields)
            if db.add_data(sheetname, xls.currentsheet_data):
                print(db.get_table_data(sheetname, '*'))
        db.conn.commit()
        db.conn.close()




if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    # 按钮执行相关操作
    win.pushButton_selecdb.clicked.connect(win.set_select_dbfile)
    win.pushButton_db2xls.clicked.connect(win.set_save_xlsfile)
    win.pushButton_selecxls.clicked.connect(win.set_select_xlsfile)
    win.pushButton_xls2db.clicked.connect(win.set_save_dbfile)
    sys.exit(app.exec_())
