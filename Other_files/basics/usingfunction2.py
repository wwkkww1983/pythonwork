#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#using function
'''
def power(x):
	return x*x

k=int(input())
print(power(k))		
'''

#默认函数可以降低函数调用难度（不必每个参数都按位置传递）；当需要复杂调用时，又可以传递更多传递。简单调用和复杂调用，函数只需定义一个
def enroll(name,gender,city='Beijing',age=15):
	print('name:',name)
	print('gender:',gender)
	print('city:',city)
	print('age:',age)
	print('\n')
enroll('Xiaoming','F')
enroll('Lihua','A','Fuzhou')
enroll('Hanmei','B',age=16)

#错误用法，默认参数必须指向不变对象。默认参数本身也是变量，可以被改变：当指向可变对象时（如L指向[]）默认参数本身也会随着函数调用被改变
def add_end(L=[]):
	L.append('end')
	return L
	
print(add_end())
print(add_end())


#正确用法
def add_end2(L=None):
	if L==None:		#特殊情形：传入None时L必须先指向空List
		L = []
	L.append('end')
	return L

print(add_end2())
print(add_end2())


#可变参数:参数个数不固定，可以是1，2，...
def squre_sum(numbers):
	sum=0
	for n in numbers:
		sum = sum + n*n
	return sum
numbers1 = [1,2,3,4,5]
print(squre_sum([1,2,3,4,5]))
print(squre_sum((1,2,3,4,5)))
print(squre_sum(numbers1))

#可变参数用法2：*nums
def squre_sum2(*nums):
	sum = 0
	for n in nums:
		sum = sum + n*n
	return sum
num1=[1,2,3,4,5,6]
num2=(num1[0],num1[3],num1[-1])
print(squre_sum2(*num1))
print(squre_sum2(*num2))

#关键字参数
#命名关键字参数
#参数组合
#函数参数 - 小结