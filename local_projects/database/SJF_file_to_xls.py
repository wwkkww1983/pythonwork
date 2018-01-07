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


def func_get_sqlite_data(db_path, table_name, table_fields):
    fields_str = ', '.join(table_fields)
    conn = sqlite3.connect(db_path)
    print('db文件对象已连接：', conn, db_path)
    c = conn.cursor()
    tables = []
    for table in c.execute("SELECT name FROM sqlite_master WHERE type='table'"):
        # 获取所有数据表名
        tables.append(table[0])
    print('数据表列表', tables)
    if table_name not in tables:
        print('指定数据表不存在：', table_name)
        return '指定数据表不存在'
    else:
        print('查询数据表：{}'.format(table_name))
        fields = []
        for table_info in c.execute("PRAGMA table_info('{}')".format(table_name)):
            # 获取指定数据表的结构：字段名
            fields.append(table_info[1])
        print('指定数据表存在字段：{}'.format(fields))
        temp_list = []
        for f in table_fields:
            # 判断需查找的字段是否都存在
            if f not in fields:
                print('指定数据表不存在字段：', f)
                break
            else:
                temp_list.append(f)

        if temp_list == table_fields:
            print('查询字段：{}'.format(table_fields))
            print('数据：')
            table_data = c.execute('SELECT {0} FROM {1} ORDER BY ID'.format(fields_str, table_name))
            table_data = tuple(table_data)
            for row in table_data:
                # 获取指定数据表按指定字段顺序排列
                print(row)
            print('**********我是分割线**********')
            return table_name, table_fields, table_data

if __name__ == '__main__':
    func_get_sqlite_data('示教文件demo.db', 'SJJT_GlueInfo',
                         ['SortID', 'GlueName', 'XCompensation', 'YCompensation', 'ZCompensation'])
    func_get_sqlite_data('示教文件demo.db', 'SJJT_PointInfo',
                         ['ElemIndex', 'ElemType', 'X', 'Y', 'Z', 'OpenGlueDelayTime'])

