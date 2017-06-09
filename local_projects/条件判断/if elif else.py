# !user/bin/python3
# -*- coding: utf-8 -*-
# created on 2.19,2017
# author: fan
"""条件判断语句的使用方法，注意条件的排列顺序"""
a = input('please type a integer:')
b = int(a)
l = ''
if b >= 100:
    l = u'b大于100, 超水平发挥！'
elif b >= 80:
    l = u'b大于80，发挥良好。'
elif b >= 60:
    l = u'b大于60，发挥的还行。'
else:
    l = u'b小于60，读的什么玩意，考的什么玩意！'
print(l)
