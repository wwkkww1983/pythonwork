# !user/bin/python3
# _*_ coding: utf-8 _*_
# created on 2.23,2017
# author: fun
def greet(x='world'):
    print('Hello, %s.' % x)
# a = input('Please input your name:\n')
# greet(a)
# greet()

def market(how_many, how_much=5, what='苹果'):
    print('这里是%5d个%5d元的%10s ,收您%5d 元，欢迎再次光临！' % (how_many, how_much, what, how_many*how_much))
m = market
m(1, 10, '香蕉')
m(3, 2)
m(5, what='草莓')
m(3)


def teammate(name, age, grade, phone, city='Fuzhou', ok=True):
    print('----- teammate information ----- \nname = ', name)
    print('age = ', age)
    print('grade = ', grade)
    print('phone number = ', phone)
    print('city = ', city)
    print('OK = ', ok)
t = teammate
t('Li', '25', 'male', '13123456789', 'Fuzhou', True)
t('Li', '25', 'male', '13123456789')
t('Li', '25', 'male', '13123456789', ok=False)
