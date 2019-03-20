#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: 使用回调函数callback
# Author:    fan
# date:      2019/3/6 006
# -----------------------------------------------------------


def func1(m):
    n = input("请输入\n>>")
    print("输入了 {}".format(m+n))
    return m+n


def callfunc1(m, func):
    print(m, func(m))


def main(l):
    callfunc1(l, func1)

if __name__ == '__main__':
    l = "666"
    main(l)
