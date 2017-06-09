# !user/bin/python3
# -*- coding: utf-8 -*-
# created on 2.19,2017
# author: fan
for i in range(50):
    if i % 10 == 0:
        print(i, '-----------------------------------------')
        for k in range(5):
            print('>>>>>>>>>')
            if k > 1:
                pass
        continue
    if i >= 40:
        break
    print(i)
print(i)
print('-----next title-----')
l = 0
sum50 = 0
while l < 50:
    l += 1
    sum50 += l
    print(l, sum50)
else:
    print('end')
print(l, sum50)