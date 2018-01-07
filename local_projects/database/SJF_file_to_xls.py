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


def get_point_table(db_path, table_name, fields_str):
    conn = sqlite3.connect(db_path)
    print('db文件对象已连接：', conn)
    c = conn.cursor()
    tables = []
    for table in c.execute("SELECT name FROM sqlite_master WHERE type='table'"):
        # 获取所有数据表名
        tables.append(table[0])
    print(tables)

    table_fields = []
    print('指定数据表：\n{}'.format(table_name))

    for table_info in c.execute("PRAGMA table_info('{}')".format(table_name)):
        # 获取指定数据表的结构：字段名
        table_fields.append(table_info[1])

    fields_list = []
    for f in fields_str.split(','):
        if f in table_fields:
            fields_list.append(f)

    fields_tuple = tuple(fields_list)
    print('字段名：\n', fields_tuple)

    print('数据：')
    point_data = c.execute('SELECT ElemIndex, ElemType, X, Y, Z, OpenGlueDelayTime FROM {} ORDER BY ID'.format(table_name))
    point_data = tuple(point_data)
    for row in point_data:
        # 获取指定数据表按指定字段顺序排列
        print(row)
    return table_name, table_fields, point_data


def get_compensation_table(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    fields = 'SortID, GlueName, MainGlue, XCompensation, YCompensation, ZCompensation, OpenGlueDelayedTime'
    tablename = 'SJJT_GlueInfo'
    data = c.execute(
        'SELECT {0} FROM {1} ORDER BY ID'.format(fields, tablename))
    for row in data:
        print(row)
    tabledata = tuple(fields.split(','))
    print(tabledata)
    print(tuple(data))

if __name__ == '__main__':
    get_point_table('示教文件demo.db', 'SJJT_PointInfo', 'ElemIndex, ElemType, X, Y, Z, OpenGlueDelayTime')
    # get_compensation_table('示教文件demo.db')
