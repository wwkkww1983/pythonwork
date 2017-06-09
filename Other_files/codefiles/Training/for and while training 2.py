# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
# created on 2.17,2017
# author: fan

"""练习
对已有的计算0-99累计之和的代码进行修改，通过增加continue 语句，使得只计算奇数之和
sum = 0
x = 1
while True:
    sum = sum + x
    x = x + 1
    if x > 100:
        break
print(sum)
"""
sum100 = 0
x = 0
while True:
    x += 1
    print('-----', x)
    if x > 100:
        break
    if x % 2 == 0:
        print(u'x = 偶数:', x)
        continue
    else:
        sum100 = sum100 + x
        print('x= %d, sum100= %d' % (x, sum100))
print(sum100)
