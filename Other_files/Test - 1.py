# this is a test files
# -*- coding: utf-8 -*-
import math


def quadratic(a, b, c):
    x1 = None
    x2 = None
    if a == 0 and b == 0:
        print('二次项和一次项系数无效，方程不成立')
        return
    if a == 0 and b != 0:
        print('二次项系数无效，转为一元一次方程，只有一个解')
        x1 = c / b
    if a != 0 and b != 0:
        d = b ** 2 - 4 * a * c
        if d >= 0:
            x1 = (- b + math.sqrt(d)) / 2 * a
            x2 = (- b - math.sqrt(d)) / 2 * a
        else:
            print(u'''此方程无解''')
            return
    return x1, x2
print('构造二元一次方程')
A = int(input('请输入二次项x^2的系数：a = '))
B = int(input('请输入一次项x系数：b = '))
C = int(input('请输入常数项：c = '))
print('方程：{}*x^2 + {}*x + {} = 0 '.format(A, B, C))
Y = quadratic(A, B, C)
if Y:
    print('方程的解为：x1 = {}, x2 = {}'.format(Y[0], Y[1]))
