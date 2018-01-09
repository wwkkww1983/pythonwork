#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name：     helloworld.py
# Description :
#   Author:      fan
#   date:        2018/1/9
#   IDE:         PyCharm Community Edition
# -----------------------------------------------------------

print('hello world')
input('Waiting')

"""
例子：pyinstaller -F demo.py
参数	含义
-F	指定打包后只生成一个exe格式的文件
-D	–onedir 创建一个目录，包含exe文件，但会依赖很多文件（默认选项）
-c	–console, –nowindowed 使用控制台，无界面(默认)
-w	–windowed, –noconsole 使用窗口，无控制台
-p	添加搜索路径，让其找到对应的库。
-i	改变生成程序的icon图标
"""
if __name__ == '__main__':
    pass