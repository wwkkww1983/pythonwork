#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name：     use_pylib_1
# Description :
#   Author:      fan
#   date:        2017/10/28
#   IDE:         PyCharm Community Edition
# -----------------------------------------------------------
import matplotlib.pyplot as plt
# 面向过程时，使用该模块提供的函数快速制图
from pylab import *
from numpy.random import randn

# x = randn(100)
# y = randn(100)
x = [i for i in range(0, 100, 5)]
y = [n for n in range(20)]

fig = figure(figsize=(12, 6), dpi=80)  # 设置画布大小、分辨率
ax = fig.add_subplot(2, 3, 1)
ax2 = fig.add_subplot(2, 3, 2)
ax3 = fig.add_subplot(2, 3, 3)

ax.plot(x, y, 'o--')
ax2.bar(x, y)
ax3.pie(x, y)
# ax.set_xticks([0, 100])
ax.set_xticks([0, 25, 50, 75, 100])  # 横轴刻度记号
ax.set_xticklabels(['0', '25', '50', '75', '100'])
ax.set_title('Time')

if __name__ == '__main__':
    show()

