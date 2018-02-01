#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: xlsfile
# Author:    fan
# date:      2018/1/31
# -----------------------------------------------------------
import xlrd, xlwt, os


class XLS(object):
    def __init__(self):
        self.book = None
        self.filepath = None
        self.name = None
        self.workdir = None
        self.sheetnames = None
        self.currentsheet = None
        self.currentsheet_fieldcount = None
        self.currentsheet_name = None
        self.currentsheet_fields = None
        self.currentsheet_data = None

    def get_xls(self, xlspath):
        [workdir, name] = os.path.split(xlspath)
        book = xlrd.open_workbook(xlspath)
        if book:
            self.book = book
            self.filepath = xlspath
            self.workdir = workdir
            self.name = name
        return book

    def get_sheet_names(self):
        shtnms = None
        if self.filepath and self.book:
            shtnms = self.book.sheet_names()
        else:
            print("can't find any sheets in this xls book")
        self.sheetnames = shtnms
        return shtnms

    def get_read_sheet(self, sheetname):
        sheet = None
        name = ''
        fields = []
        data = []
        row_count = 0
        col_count = 0
        if self.book and self.sheetnames and sheetname:
            sheet = self.book.sheet_by_name(sheetname)
            name = sheet.row_values(0)[0]
            [row_count, col_count] = sheet.nrows, sheet.ncols
            fields = tuple(sheet.row_values(1))
            for i in range(2, row_count):
                rowdata = list(sheet.row_values(i))
                for j in range(len(rowdata)):
                    try:
                        s = int(rowdata[j])
                    except:
                        s = rowdata[j]
                    rowdata[j] = s
                data.append(rowdata)
            data = tuple(data)
        else:
            print("can't find any sheets in this xls book")
        self.currentsheet = sheet
        self.currentsheet_name = name
        self.currentsheet_fields = fields
        self.currentsheet_fieldcount = col_count
        self.currentsheet_records = row_count-2
        self.currentsheet_data = data

    def get_read_cell_data(self):
        pass


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
            sheet.write(i + 2, j, table_data[i][j])


if __name__ == '__main__':
    xls = XLS()
    xls.get_xls('demo.xls')
    xls.get_sheet_names()
    print("""\
    xls.filepath: {0},
    xls.name: {1},
    xls.workdir: {2},
    xls.book: {3}
    xls.sheetnames: {4}""".format(xls.filepath,
                                  xls.name,
                                  xls.workdir,
                                  xls.book,
                                  xls.sheetnames))

    print("    ********************我是分割线********************")
    xls.get_read_sheet('COMPANY')
    print("""\
    sheet.name: {0}
    sheet.fields: {1}
    sheet.records: {2}
    sheet.fieldcount: {3}
    sheet.data: {4}
    sheet: {5}     """.format(xls.currentsheet_name,
                              xls.currentsheet_fields,
                              xls.currentsheet_records,
                              xls.currentsheet_fieldcount,
                              xls.currentsheet_data,
                              xls.currentsheet))

