#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Python教程 类和实例 （http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431864715651c99511036d884cf1b399e65ae0d27f7e000）

'''
多行注释
'''
#No.2
class Student(object):
	def __init__(self,name,score):	#定义一个特殊的方法-创建实例
		self.name  = name			#用“方法”绑定“属性名”
		self.score = score
									
	def print_score(self):			#方法，打印分数（直接引用属性）
		print('%s: %s' %(self.name,self.score))
									
	def get_grade(self):			#增加方法，分数等级（从属性计算）
		if self.score >=80:
			return'A'
		elif self.score>=60:
			return'B'
		else:
			return'C'
									
Li = Student('Lilei',60)			#给实例绑定属性
Han= Student('Hanmeimei',99)

print('Class \"Student\" Info:\n',Student)
print('Instance \"Li\" Info:\n',Li)

print('Li.name  = ',Li.name)
print('Li.score = ',Li.score)
Li.print_score()

print('Grade of Li is: ',Li.get_grade()) 
print('Grade of Han is: ',Han.get_grade())


hg = Han.get_grade()
print(hg)
