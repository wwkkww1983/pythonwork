#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
遍历指定目录下的所有子目录和文件，并返回所有文件的完整文件路径
"""

import os


def get_files(given_dir):
    """定义函数获取给定目录下的所有文件名（不包含目录名），并添加到列表中"""
    files = []

    def findfiles(current_dir):
        """定义函数遍历所有子目录"""
        for each_path in os.listdir(current_dir):
            each_abspath = os.path.join(current_dir, each_path)
            """遍历当前一层目录并组装为绝对路径"""

            if os.path.isfile(each_abspath):
                """如果是文件，添加文件完整路径到列表中"""
                files.append(each_path)
            else:
                """如果是目录，则什么都不做"""
                pass

    findfiles(given_dir)
    return files

if __name__ == '__main__':
    test_path = r'C:\Users\fan\Desktop\哈巴机实验-范春回\数据-9.1'
    l = get_files(test_path)
    print('\n在目录：', test_path, '\n存在的全部xls文件为：')
    for i in l:
        if i[-3:] == 'xls':
            print(i)




