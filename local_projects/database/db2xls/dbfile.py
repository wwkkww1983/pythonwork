#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name：     sjfile
# Description :
#   Author:      fan
#   date:        2018/1/17
#   IDE:         PyCharm Community Edition
# -----------------------------------------------------------
import sqlite3 as sql
import os


class DB(object):
    def __init__(self):
        self.name = ''
        self.path = ''
        self.tablelist = []
        self.cursor = None

    def get_cursor(self, dbpath):
        c = None
        try:
            conn = sql.connect(dbpath)
            c = conn.cursor()
        except:
            print('fail to connect', dbpath)
        self.path = dbpath
        self.name = os.path.split(dbpath)[1]
        self.cursor = c
        return c

    def get_tablesnames(self):
        tablesnames = []
        if self.cursor:
            c = self.cursor
            for table in c.execute("SELECT name FROM sqlite_master WHERE type='table'"):
                tablesnames.append(table[0])
        else:
            print('cursor not existed while getting tablesnames.')
        self.tablelist = tuple(tablesnames)
        return self.tablelist

    def get_table_fields(self, tablename):
        table_fields = []
        if self.cursor:
            for info in self.cursor.execute("PRAGMA table_info('{}')".format(tablename)):
                table_fields.append(info[1])
        else:
            print('cursor not existed while getting table fields.')
        return tuple(table_fields)

    def get_table_data(self, tablename, fields=''):
        tabledata = ()
        if self.cursor:
            if tablename:
                if not fields:
                    tabledata = self.cursor.execute('SELECT * FROM {0}'.format(tablename))
                else:
                    tabledata = self.cursor.execute('SELECT {0} FROM {1}'.format(fields, tablename))
            else:
                print('table not found:', tablename)
        return tuple(tabledata)

    def execute(self, sqltext):
        data = []
        if self.cursor:
            try:
                data = self.cursor.execute(sqltext)
            except Exception as e:
                print('the sql order is not corrected: "{}"'.format(sqltext))
        return tuple(data)

    def add_records(self, record_counts=1, ):
        pass


if __name__ == '__main__':
    pass
    file = DB()
    file.get_cursor('示教文件demo.db')
    file.get_tablesnames()
    fields = file.get_table_fields('SJJT_PointInfo')
    data = file.get_table_data('SJJT_PointInfo', 'ID, X, Y, Z')
    data2 = file.execute('SELECT name FROM sqlite_master WHERE type=\'table\'')
    print("""get .sjf file:
             path: {}
             name: {}
             cursor: {}
             table list: {}""".format(file.path, file.name, file.cursor, file.tablelist))
    print(fields)
    print(data)
    print(data2)
