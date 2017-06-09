# this is a test files
# -*- coding: utf-8 -*-
import math
x1 = 0
x2 = 0
def quadratic(a,b,c):
    d = b ** 2 - 4 * a * c
    if d >= 0:
        x1 = (- b + math.sqrt(d)) / 2 * a
        x2 = (- b - math.sqrt(d)) / 2 * a
        return x1,x2
    else:
        print(u'''此方程无解''')
        return

A = int(input())
B = int(input())
C = int(input())
Y=quadratic(A, B, C)
print(Y)
#print('%dx**2+%dx+%d=0的一元二次方程的解为：x1=%f,x2=%f'%(A,B,C,))