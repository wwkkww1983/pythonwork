# !user/bin/python3
# -*- coding: utf-8 -*-
# created on 2.19,2017
# author: fan
i = 1
n = 0
sum_1 = 0
for i in range(20):
    n = 2**i
    sum_1 += n
    print('i = ', i, 'n = ', n, 'sum_1 =', sum_1)
print(sum_1)
