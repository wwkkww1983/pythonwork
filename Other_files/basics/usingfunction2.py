#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#using function
'''
def power(x):
	return x*x

k=int(input())
print(power(k))		
'''

#Ĭ�Ϻ������Խ��ͺ��������Ѷȣ�����ÿ����������λ�ô��ݣ�������Ҫ���ӵ���ʱ���ֿ��Դ��ݸ��ഫ�ݡ��򵥵��ú͸��ӵ��ã�����ֻ�趨��һ��
def enroll(name,gender,city='Beijing',age=15):
	print('name:',name)
	print('gender:',gender)
	print('city:',city)
	print('age:',age)
	print('\n')
enroll('Xiaoming','F')
enroll('Lihua','A','Fuzhou')
enroll('Hanmei','B',age=16)

#�����÷���Ĭ�ϲ�������ָ�򲻱����Ĭ�ϲ�������Ҳ�Ǳ��������Ա��ı䣺��ָ��ɱ����ʱ����Lָ��[]��Ĭ�ϲ�������Ҳ�����ź������ñ��ı�
def add_end(L=[]):
	L.append('end')
	return L
	
print(add_end())
print(add_end())


#��ȷ�÷�
def add_end2(L=None):
	if L==None:		#�������Σ�����NoneʱL������ָ���List
		L = []
	L.append('end')
	return L

print(add_end2())
print(add_end2())


#�ɱ����:�����������̶���������1��2��...
def squre_sum(numbers):
	sum=0
	for n in numbers:
		sum = sum + n*n
	return sum
numbers1 = [1,2,3,4,5]
print(squre_sum([1,2,3,4,5]))
print(squre_sum((1,2,3,4,5)))
print(squre_sum(numbers1))

#�ɱ�����÷�2��*nums
def squre_sum2(*nums):
	sum = 0
	for n in nums:
		sum = sum + n*n
	return sum
num1=[1,2,3,4,5,6]
num2=(num1[0],num1[3],num1[-1])
print(squre_sum2(*num1))
print(squre_sum2(*num2))

#�ؼ��ֲ���
#�����ؼ��ֲ���
#�������
#�������� - С��