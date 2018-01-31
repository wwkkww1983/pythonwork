#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name：     read_sqlite3_file
# Description :
#   Author:      fan
#   date:        2018/1/6
#   IDE:         PyCharm Community Edition
# -----------------------------------------------------------

import sqlite3, os


def read_db():
    conn = sqlite3.connect('示教文件demo.db')
    print('db文件对象已连接：', conn)
    c = conn.cursor()
    tables = []
    for table in c.execute("SELECT name FROM sqlite_master WHERE type='table'"):
        # 获取所有数据表名
        tables.append(table[0])
    print(tables)

    targetable = tables[1]
    table_fields = []
    print('指定数据表：{}'.format(targetable))

    for table_info in c.execute("PRAGMA table_info('{}')".format(targetable)):
        # 获取指定数据表的结构：字段名
        table_fields.append(table_info[1])
    print('字段名：\n', tuple(table_fields))

    print('数据：')
    for row in c.execute('SELECT * FROM {} ORDER BY ID'.format(targetable)):
        # 获取指定数据表按指定字段顺序排列
        print(row)


def create_db(dbpath, tablename, fieldstypes, rowdata):
    """
    创建db文件并创建数据表和增加记录
    connect(): 	sqlite3.connect(database [,timeout ,other optional arguments])
    如果给定db文件存在，则返回一个数据库连接对象conn。
    如果给定db文件不存在，则该调用将创建一个数据库并返回新数据库的连接对象conn。
    如果您不想在当前目录中创建数据库，那么您可以指定带有路径的文件名，这样您就能在任意地方创建数据库。
    """
    conn = sqlite3.connect(dbpath)

    # cursor: 理解为用于Python调用sqlite3执行数据库命令的接口、指针
    c = conn.cursor()
    c.execute("""CREATE TABLE {} ({})""".format(tablename, fieldstypes))
    fields = []
    for info in c.execute("PRAGMA table_info('{}')".format(tablename)):
        fields.append(info[1])
    print(fields)
    c.execute("INSERT INTO COMPANY ({}) VALUES ({})".format(','.join(fields), rowdata))
    data = c.execute("SELECT * FROM COMPANY")
    print(list(data))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    os.remove('demo.db')
    dbpath = 'demo.db'
    tbn = 'COMPANY'
    tbfd = """ID INT PRIMARY KEY     NOT NULL,
               NAME           TEXT    NOT NULL,
               AGE            INT     NOT NULL,
               ADDRESS        CHAR(50),
               SALARY         REAL"""
    rowdata = "1, 'Paul', 32, 'California', 20000.00"
    create_db(dbpath, tbn, tbfd, rowdata)

