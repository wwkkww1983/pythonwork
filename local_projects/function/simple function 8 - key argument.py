# !usr/bin/python3
# _*_ coding: utf-8 _*_
# created on 2.24,2017
# author: fan


def teammate(name, age, grade, phone, city='Fuzhou', ok=True, *date, **other):
    """默认参数、可变参数和关键字参数"""
    print('\----- teammate information -----')
    print(name, age, grade, phone, city, ok, date, other)

t = teammate
o = {'rule': 'manager', 'score': 87}
days = [1, 2, 3]
t('Li', 25, 'female', '13823456789', 'Fuzhou', True)
t('Liu', 30, 'male', '15923456789')
t('Song', 29, 'male', '13123456789', ok=False)
t('Fan', 19, 'male', '16523456789', rule='manager', mail='13123456789@qq.com', like='football')
t('Tao', 28, 'female', '18898739234', **o)
t('Tao', 28, 'female', '18898739234', 'Beijing', True, *days, **o)

def teammate1(name, age, grade, *date, city='Beijing', job):
    """命名关键字参数：限制传入参数的范围"""
    print(name, age, grade, date, city, job)
te = teammate1
"""比较下列两种调用方式的输出结果"""
te('Lan', 22, 'female', 1, 3, 5, job='Engineer')
te('Lan', 22, 'female', 1, 3, 5, like='football')

def teammate2(*args, **kw):
    print(args, kw)
t2 = teammate2
t2('Tao', '28', 'female', '18898739234', 'Beijing', True, rule='manager', like='football')

