#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#list and tunple

fruits = ['apple','banana','orange','pich']
fruits.append('patato')
print(fruits)
fruits.insert(1,'egg')
print(fruits)
l = len(fruits)		#return the number of iterms of sequence or mapping
for i in range(0,l):	#return i from 0(default) to l-1
	fr1=fruits
	l1=len(fr1)
	print(fr1[i],fr1[-i])

fr2=fruits
for j in range(len(fr2),0,-1):	#range(start,stop[stop,step])
	fr2.pop(-j)
	print(fr2,'\n lengh =',len(fr2))

fr3=[1,-5,0.9,100,20e10,-9.9]
print(fr3)
fr3.sort()
print(fr3)

years = (2010,2011,2012,2013,2014,2015,2016,2017)
print(years)
for k in range(1,len(years)):
	print(years[-k])

Autumn = ['Jaun','July','August']
oneyear = ('Spring','Summer',Autumn,'Winter')
print(oneyear)
Autumn.pop(1)
oneyear = ('Spring','Summer',Autumn,'Winter')
print(oneyear)
#for m in range(0,len(oneyear)):
	print(oneyear[m])

student = ['namber','name','score',('sexual','age')]
for n in range(len(student)):
	print(student[n])
print(student[3][0])
	