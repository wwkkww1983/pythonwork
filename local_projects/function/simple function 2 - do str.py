# !user/bin/python 3
# _*_ coding: utf-8 _*_
# created on 2.21,2017
# author: fan


def find_max_asc(l):
    """求一个由单字符串组成的列表内各字符ASCII码值最大者和最小者并输出"""
    max_asc = 0
    min_asc = 0
    s = []
    for i in range(len(l)):
        s.append(ord(l[i]))
        print(l[i], s[i])
    print('l= ', l, '\ns= ', s)
    max_asc = s[0]
    min_asc = s[0]
    for m in s:
        if m > max_asc:
            max_asc = m
        elif m <= min_asc:
            min_asc = m
    print('ASCII码值最大和最小的字符是: "%s"(%d), "%s(%d)"' % (chr(max_asc), max_asc, chr(min_asc), min_asc))


l_asc = []
for n in range(40, 150):
    l_asc.append(chr(n))
    print(n, l_asc[n-40])
L = ['k', '9', '-', ')', 'A', 'z']
find_max_asc(L)
find_max_asc(l_asc)


