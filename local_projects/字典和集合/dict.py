# !/usr/bin/python3
# _*_ coding: utf-8_*_
# created on 2.28,2017
# author: fan

"""学习字典和集合的概念和使用方法，使用常用方法进行dict和set的操作"""

"""            练习1
for 循环遍历如下的dict，打印出 name: score 来。
d = {
    'Adam': 95,
    'Lisa': 85,
    'Bart': 59
}

d = {
    'Adam': 95,
    'Lisa': 85,
    'Bart': 59
}
for item in d:
    print(item,'\b:', d[item])
print(d)
"""

"""            练习2
针对下面的set，给定一个list，对list中的每一个元素，如果在set中，就将其删除，如果不在set中，就添加进去。
s = set(['Adam', 'Paul'])
L = ['Adam', 'Lisa', 'Bart', 'Paul']
"""
s = set(['Adam', 'Paul'])
L = ['Adam', 'Lisa', 'Bart', 'Paul']

for strs in L:
    if strs in s:
        s.remove(strs)
        print(s)
    else:
        s.add(strs)
print(s, L)

"""
s1 = s & set(L)
s2 = s | set(L)
print(s1, s2)
s = s2
L = list(s1)
print('s = ', s, '\nL = ', L)
"""
