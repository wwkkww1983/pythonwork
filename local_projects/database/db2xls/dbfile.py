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
import os, time


class DB(object):
    def __init__(self):
        self.path = ''
        self.name = ''
        self.filedir = ''
        self.tablenames = []
        self.conn = None
        self.cursor = None

    def get(self, dbpath):
        [dbdir, dbname] = os.path.split(dbpath)
        if dbdir == '':
            dbdir = os.curdir
        if dbname in os.listdir(dbdir):
            print('There has been a file named {} in target dir BEFORE creating'.format(dbname))
        else:
            print('There has been a file named {} in target dir AFTER creating'.format(dbname))
        conn = None
        c = None
        try:
            conn = sql.connect(dbpath)
            c = conn.cursor()
        except:
            print('fail to connect', dbpath)
        self.path = dbpath
        [self.filedir, self.name] = os.path.split(dbpath)
        self.conn = conn
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
        self.tablenames = tuple(tablesnames)
        return self.tablenames

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

    def create_table(self, tablename, tablefields):
        create_success = False
        if self.cursor:
            c = self.cursor
            if tablename in self.get_tablesnames():
                # 当且仅当db文件中不存在同名数据表时，才进行创建
                print('There has been a table named {} in this db file'.format(tablename))
                create_success = False
            else:
                c.execute("CREATE TABLE {0} ({1})".format(tablename, tablefields))
                create_success = True
                self.conn.commit()
        return create_success

    def add_data(self, tablename, tabledata):
        add_success = False
        if self.cursor:
            c = self.cursor
            if tablename not in self.get_tablesnames():
                print('No table named {} in this db file, adding data fail.'.format(tablename))
                add_success = False
            else:
                # 增加数据行，注意字段和数据的格式：括号，‘字符串形式’而不是‘列表或元组形式’
                fieldsstr = ','.join(self.get_table_fields(tablename))
                for rowdata in tabledata:
                    rowdatastr = ','.join(rowdata)
                    c.execute("INSERT INTO {tbn} ({fdstr}) VALUES ({rdtstr})".format(tbn=tablename,
                                                                                     fdstr=fieldsstr,
                                                                                     rdtstr=rowdatastr))
                add_success = True
                self.conn.commit()
        return add_success

    def add_records(self, tablename, rowdata):
        add_success = False
        if self.cursor:
            c = self.cursor
            if tablename not in self.get_tablesnames():
                print('No table named {} in this db file, adding data fail.'.format(tablename))
                add_success = False
            else:
                # 增加数据行，注意字段和数据的格式：括号，‘字符串形式’而不是‘列表或元组形式’
                fieldsstr = ','.join(self.get_table_fields(tablename))
                rowdatastr = ','.join(rowdata)
                c.execute("INSERT INTO {tbn} ({fdstr}) VALUES ({rdtstr})".format(tbn=tablename,
                                                                                 fdstr=fieldsstr,
                                                                                 rdtstr=rowdatastr))
                add_success = True
                self.conn.commit()
        return add_success

    def execute(self, sqltext):
        data = []
        if self.cursor:
            try:
                data = self.cursor.execute(sqltext)
                self.conn.commit()
            except Exception as e:
                print('the sql order is not corrected: "{}"'.format(sqltext))
        return tuple(data)

if __name__ == '__main__':
    # 链接已存在的db文件
    file = DB()
    file.get('示教文件demo.db')
    file.get_tablesnames()
    print("""get .sjf file:
             path: {}
             name: {}
             cursor: {}
             table list: {}""".format(file.path,
                                      file.name,
                                      file.cursor,
                                      file.tablenames))
    fields = file.get_table_fields('SJJT_PointInfo')
    data = file.get_table_data('SJJT_PointInfo', 'ID, X, Y, Z')
    data2 = file.execute('SELECT name FROM sqlite_master WHERE type=\'table\'')
    print(fields)
    print(data)
    print(data2)
    file.conn.close()

    print('*'*50 + '我是分割线' + '*'*50)
    time.sleep(.2)
    # 创建并链接db文件
    os.remove('demo.db')
    db = DB()
    dbpath = 'demo.db'
    tbn = 'COMPANY'
    tbfd =  """ID INT PRIMARY KEY     NOT NULL,
               NAME           TEXT    NOT NULL,
               AGE            INT     NOT NULL,
               ADDRESS        CHAR(50),
               SALARY         REAL"""
    db.get(dbpath)
    if db.create_table(tbn, tbfd):
        time.sleep(1)
        db.get_tablesnames()
        fields = db.get_table_fields(tbn)
        print("""get .db file:
                 path: {}
                 name: {}
                 cursor: {}""".format(db.path,
                                      db.name,
                                      db.cursor,
                                      db.tablenames,))
        print("""about table:
                 table names: {}
                 table fields: {}:{}""".format(db.tablenames,
                                               tbn,
                                               fields))

    # data = file.get_table_data(tbn, '')
        db.conn.close()

