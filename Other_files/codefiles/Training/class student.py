#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Student(object):
    def __init__(self,name,height,weight):	#定义一个特殊的方法-创建实例
        self.name  = name			#用“方法”绑定“属性名”
        self.height = height
        self.weight = weight
    def print_bmi(self):
        bmi = self.weight / self.height**2
        s =''
        print('The BMI of %s is %.2f' % (self.name,bmi))
        if   bmi <=18.5:
            s = 'Too light'
        elif bmi <=25:
            s = 'Normal'
        elif bmi <=28:
            s = 'Too heavy'
        elif bmi <=32:
            s = 'Obesity'
        else:
            s = 'Severe obesity'
        print('The suggest is:%s\n' % s)
A = Student('Lilei',1.70,70)			#给实例绑定属性
B= Student('Hanmeimei',1.80,100)
C= Student('Xiaoming',1.75,80.5)
D= Student('Mike',1.80,60)
E= Student('Lily',1.70,45)
A.print_bmi()
B.print_bmi()
C.print_bmi()
D.print_bmi()
E.print_bmi()