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
import xlwt


def func_get_sqlite_data(db_path, table_name, table_fields):
    """
    :param db_path: .db(.sjf)文件位置
    :param table_name: 指定表名
    :param table_fields: 需查询的字段
    :return: 表名_str，字段_tuple，数据_tuple(tuple)
    """
    # if db_path.endswith('.sjf'):
    #     db_path = db_path.split('.')[0] + '.db'
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
            table_data = c.execute('SELECT {0} FROM {1}'.format(fields_str, table_name))
            table_data = tuple(table_data)
            for row in table_data:
                # 获取指定数据表按指定字段顺序排列
                print(row)
            print('**********我是分割线**********')
            return table_name, table_fields, table_data


def func_get_glueio_positon(glues, pointseq, arraybase=None, arraycount=None):
    """
    胶头列表中有多少胶头、点列表中就有几组点列表对应
    点类型：
        0：孤立点
        1,2,3: 折线起点、中间点、终点
        4,5,6: 圆弧起点、中间点、终点
        7,8,9: 整圆起点、中间点、终点
    阵列加工方式：
            1.阵列第二个位置基准点为：SJJT_ArrayInfo数据表第二行与第一行相对位置
            2.加工顺序：蛇形；与SJJT_ArrayInfo点顺序不一致
    """
    table_name = '示教文件开关胶动作位置列表'
    # 获取点列表
    point_data = pointseq
    arry_basepoints = arraybase
    array_row_count = arraycount[0][1]
    array_col_count = arraycount[0][0]
    table_fields = ('胶头',
                    '开关胶点ID',
                    '点类型',
                    'X位置',
                    'Y位置',
                    'Z位置',
                    '开关胶')
    pointype = {0: '孤立点',
                1: '折线起点', 2: '折线中间点', 3: '折线终点',
                4: '圆弧起点',
                5: '圆弧中间点', 6: '圆弧终点', 7: '整圆起点', 8: '整圆中间点', 9: '整圆终点'}
    glue_io_positions = []
    for glue in glues:
        # 根据胶头列表将点列表分割处理
        # 获取胶头和胶头起始点
        glue_id = glue[0]
        x_base_pos = glue[2]
        y_base_pos = glue[3]
        z_base_pos = glue[4]
        # 基准点（起始点坐标）
        basepoint = (glue_id,
                     0,
                     '基准点',
                     x_base_pos,
                     y_base_pos,
                     z_base_pos,
                     '--')
        # print(basepoint)
        glue_io_positions.append(basepoint)
        for point in point_data:
            # 开关胶动作时机：
            # 孤立点、折线起点、圆弧起点、整圆起点 -- 触发开胶；
            # 孤立点、折线终点、圆弧终点、整圆终点 -- 触发关胶.
            if point[0] == glue_id:
                point_glueid = point[0]
                point_id = point[1]
                point_type = pointype[point[2]]
                # 点坐标：与基准点同一坐标系的绝对位置
                x_pos = x_base_pos + point[3]
                y_pos = y_base_pos + point[4]
                z_pos = z_base_pos + point[5]

                if point_type in ['孤立点', '折线起点', '圆弧起点', '整圆起点']:
                    glue_act = '开胶'
                    glue_io_currentpos = (point_glueid,
                                          point_id,
                                          str(point[2])+' '+point_type,
                                          x_pos,
                                          y_pos,
                                          z_pos,
                                          glue_act)
                    glue_io_positions.append(glue_io_currentpos)
                if point_type in ['孤立点', '折线终点', '圆弧终点', '整圆终点']:
                    glue_act = '关胶'
                    glue_io_currentpos = (point_glueid,
                                          point_id,
                                          str(point[2])+' '+point_type,
                                          x_pos,
                                          y_pos,
                                          z_pos,
                                          glue_act)
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
    filepath = '阵列示教-15商标_001.sjf'
    point_seq = func_get_sqlite_data(filepath,
                                     'SJJT_GlueInfo',
                                     ['SortID', 'GlueName', 'XCompensation', 'YCompensation', 'ZCompensation'])
    common_position = func_get_sqlite_data(filepath,
                                           'SJJT_PointInfo',
                                           ['ID', 'ElemIndex', 'ElemType', 'X', 'Y', 'Z', 'OpenGlueDelayTime'])
    arry_info = func_get_sqlite_data(filepath,
                                     'SJJT_ArrayInfo',
                                     ['ID', 'X', 'Y', 'Z'])
    arry_format = func_get_sqlite_data(filepath,
                                       'SJJT_FileInfo',
                                       ['XDirectionNum', 'YDirectionNum'])
    for i in [point_seq, common_position, arry_info, arry_format]:
        # 打印需要使用的数据表、数据列
        for row in i:
            print(row)
    glue_io_position_data = func_get_glueio_positon(point_seq[2], common_position[2], arry_info[2], arry_format[2])

    # print(glue_io_position_data[0])
    # for point in glue_io_position_data[2]:
    #     # 打印获得的点列表
    #     print(point)

    xls = xlwt.Workbook()
    add_to_xls(xls, point_seq)
    add_to_xls(xls, common_position)
    add_to_xls(xls, glue_io_position_data)
    xls.save('示教胶头动作点列表.xls')