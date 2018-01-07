#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name：     read_sqlite3_file
# Description :
#   Author:      fan
#   date:        2018/1/6
#   IDE:         PyCharm Community Edition
# -----------------------------------------------------------

import sqlite3


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


def create_db():
    conn = sqlite3.connect('demo.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE stocks(id text, x integer, y integer, z integer)""")


if __name__ == '__main__':
    read_db()
