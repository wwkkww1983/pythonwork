# !/user/bin/python3
# _*_ coding: utf-8 _*_
# created on2.23,2017
# author: fan


def sum_numbers(l):
    if not isinstance(l, (tuple, list)):
        raise TypeError('bad operand type')
    if l:
        s = 0
        for i in l:
            s += i ** 2
        return s


sum_num = sum_numbers([5, 6, 2])
L = list(range(1, 101))
print(sum_num)
print(sum_numbers(L))
print(sum_numbers((1, 5, 6, 8)))
