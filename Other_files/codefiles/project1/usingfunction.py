#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#ÁÎÑ©·åPython½Ì³Ì (http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/00143167832686474803d3d2b7d4d6499cfd093dc47efcd000#0)


'''
#no using function
r1 = 12.34
r2 = 2.5
r3 = 6.54
s1 = 3.14 * 12.34 * 12.34
s2 = 3.14 *2.5 *2.5
s3 = 3.14 *6.54 *6.54
print(s1,s2,s3)
'''
#using function

def circlearea(radius):
	pi = 3.14
	if radius > 0:
		return pi *radius **2
	else:
		print('The radius must be greater than 0!')
		return None
		
r = float(input('Please input the radius of circle:\nr = '))
s = circlearea(r)
#inputradius = (input('please input the radius of circle:'))
print('\nThe area of the circle is:\ns = ',s)	


def sum_1ton(n):
	sum = 0
	for n in range(1,n+1):
		sum = sum + n
	return sum
	
x =int(input('Please input a integer:\nn = '))
sum = sum_1ton(x)
print('Sum of 1 to x is:\n sum = ',sum)