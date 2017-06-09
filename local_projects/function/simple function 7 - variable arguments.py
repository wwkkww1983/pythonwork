# !user/bin/python3
# _*_ coding: utf-8 _*_
# created on 2.23,2017
# author: fun


def sum_numbers_1(*nums):
    s = 0
    for i in nums:
        s += i**2
    return s
L = list(range(1, 101))
c = sum_numbers_1
b = c(*L)
a = c(*range(1, 101))
print('b = ', b, '\ta = ', a)

def join_str(*strs):
    l = ''
    for s in strs:
        l += s + ' '
    print(l)
    return
join_str('I', 'am', 'a', 'student.')
join_str('Hello', 'world')
join_str('Nice', 'to', 'meet', 'you.')
strings = ['My', 'name', 'is', 'Han', 'mei.']
join_str(*strings)
