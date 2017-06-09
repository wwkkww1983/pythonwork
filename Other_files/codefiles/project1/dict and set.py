#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#dict and set

dict1 = {'USA':10,'India':12,'China':13,'Japan':3}
print(dict1)
print(dict1['USA'])
dict1['USA'] = 11
print(dict1['USA'])

dict1.pop('USA')		#从dict中弹出一个key,圆括号
print(dict1)
print('key-"USA"是否在字典中:\n','USA' in dict1)
print('key-"Japan"是否在字典中:\n','Japan' in dict1)

d = {6:100,1:200,3:400,4:600,7:900}	
print(d)
print('取出key-5对应的value:\n',d.get(5))
print('取出key-6对应的value:\n',d.get(6))

#set
l1 = [1,3,5,7,9]
l2 = ['a','c','b','f','z','e']
l3 = [0,1,2,3,4,5,6,7,8,9,10]
print(l1,'\n',l2,'\n',l3,'\n')
set1 = set(l1)
set2 = set(l2)
print('这三个集合分别为：\n',set1,set2,set(l3))
print('交集',set1 & set(l3))
print('并集',set1 | set(l3))	#集合操作

set1.add(11)		#在集合中添加一个元素“11”
print(set1)
set1.remove(1)		#在集合中移除一个元素“1”
print(set1)
