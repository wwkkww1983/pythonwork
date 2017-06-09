# !user/bin/python 3
# _*_ coding: utf-8 _*_
# created on 2.21,2017
# author: fan
"""
def fib(n):
# 输出一个基于n的斐波纳数列
    a, b = 0, 1
    while b < n:
        print(a, b)
        a, b = b, a+b
fib(100)

def fib1(num):
    n, m = 0, 1
    l = ''
    while m < num:
        print(n, m)
        l += str(m) + ' '
        print('----', l)
        n, m = m, m+n
    else:
        print('小于%d的斐波纳数列为：' % num, l)
fib1(100)

def printnum(k):
    l = 0
    m = 0
    n = 0
    for i in range(1, k+1):
        print(i)
        l = i**2
        m = i**3
        n += i
        print(l, m, n)
    print('%d的平方为%d, 立方为%d, 1到%d之间累计求和为%d' % (k, l, m, k, n))
printnum(10)
"""


def area_square():
    l1 = input('请输入长方形一边长:')
    l2 = input('请输入长方形另一边长:')
    a = float(l1)
    b = float(l2)
    if a > 0 and b > 0:
        print('此长方形的面积为', a*b)
    else:
        print('长和宽只能为正整数！请重新输入:')
        area_square()


area_square()




