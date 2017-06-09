# !/user/bin/python3
# _*_ coding: utf-8 _*_
# created on2.23,2017
# author: fan
import math
sq = math.sqrt


def quadratic(a, b, c):
    # 接收一个数值a, b, c组成的列表，求方程a*x^2 + b*x + c = 0的截
    det = b**2 - 4*a*c
    if a !=0:
        if det >= 0:
            x1 = (0 - b + sq(det)) / (2*a)
            x2 = (0 - b - sq(det)) / (2*a)
            print(x1, x2)
            return x1, x2
        else:
            print('参数输入错误，请重新输入！')
    else:
        x1 = c/b
        x2 = x1
        print(x1, x2)

a = int(input('请输入a: '))
b = int(input('请输入b: '))
c = int(input('请输入c: '))
quadratic(a, b, c)
