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
import xlrd, xlwt


def func_get_sqlite_data(db_path, table_name, table_fields):
    """
    :param db_path: .db(.sjf)文件位置
    :param table_name: 指定表名
    :param table_fields: 需查询的字段
    :return: 表名_str，字段_tuple，数据_tuple(tuple)
    """

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


def func_get_glueio_positon(common_pos, point_arr):
    """
    点类型：
        0：孤立点
        1,2,3: 折线起点、中间点、终点
        4,5,6: 圆弧起点、中间点、终点
        7,8,9: 整圆起点、中间点、终点
    """
    table_name = '示教文件开关胶动作位置列表'
    # 获取基准点位置
    common_pos_x = common_pos[0][2]
    common_pos_y = common_pos[0][3]
    common_pos_z = common_pos[0][4]
    # 获取点列表
    point_data = point_arr
    table_fields = ('开关胶点ID', '点类型', 'X位置', 'Y位置',  'Z位置', '开关胶')
    POINTTYPE = {0:'孤立点', 1: '折线起点', 2: '折线中间点', 3:'折线终点', 4:'圆弧起点',
                 5:'圆弧中间点', 6:'圆弧终点', 7:'整圆起点', 8:'整圆中间点', 9:'整圆终点'}
    common_pos = (0, '基准点', common_pos_x, common_pos_y, common_pos_z, '--')
    glue_io_positions = [common_pos]
    x_pos = common_pos_x
    y_pos = common_pos_y
    z_pos = common_pos_z
    for point in point_data:
        # 开关胶动作时机：孤立点、折线起点、圆弧起点、整圆起点 -- 触发开胶；孤立点、折线终点、圆弧终点、整圆终点 -- 触发关胶
        point_id = point[0]
        point_type = POINTTYPE[point[1]]
        x_pos += point[2]
        y_pos += point[3]
        z_pos += point[4]

        if point_type in ['孤立点', '折线起点', '圆弧起点', '整圆起点']:
            glue_act = '开胶'
            glue_io_currentpos = (point_id, point_type, x_pos, y_pos, z_pos, glue_act)
            glue_io_positions.append(glue_io_currentpos)
        if point_type in ['孤立点', '折线终点', '圆弧终点', '整圆终点']:
            glue_act = '关胶'
            glue_io_currentpos = (point_id, point_type, x_pos, y_pos, z_pos, glue_act)
            glue_io_positions.append(glue_io_currentpos)
    return table_name, table_fields, glue_io_positions


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
            sheet.write(i+2, j, table_data[i][j])

if __name__ == '__main__':
    point_array = func_get_sqlite_data('示教文件demo.db', 'SJJT_GlueInfo',
                         ['SortID', 'GlueName', 'XCompensation', 'YCompensation', 'ZCompensation'])
    common_position = func_get_sqlite_data('示教文件demo.db', 'SJJT_PointInfo',
                         ['ElemIndex', 'ElemType', 'X', 'Y', 'Z', 'OpenGlueDelayTime'])
    glue_io_position_data = func_get_glueio_positon(point_array[2], common_position[2])
    print(glue_io_position_data[0])
    for point in glue_io_position_data[1]:
        print(point)

    xls = xlwt.Workbook()
    add_to_xls(xls, point_array)
    add_to_xls(xls, common_position)
    add_to_xls(xls, glue_io_position_data)
    xls.save('示教胶头动作点列表1.xls')

