#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name：     democlass.py
# Description :
#   Author:      fan
#   date:        2017/9/20
#   IDE:         PyCharm Community Edition
# -----------------------------------------------------------


class Triangle(object):
    def __init__(self):
        self.istriangle = False
        self.sides = ()

    def maketriangle(self, a, b, c):
        istriangle = False
        sides = (a, b, c)
        for i in sides:
            if i <= 0:
                istriangle = False
                break
            new = list(sides)
            new.remove(i)
            sub = new[0] + new[1]
            diff = max(new) - min(new)
            if diff < i < sub:
                istriangle = True
                self.sides = sides
            else:
                istriangle = False
                self.sides = ()
        self.sides = sides
        self.istriangle = istriangle

        return self.istriangle

if __name__ == '__main__':
    demo = Triangle()
    demo.maketriangle(3, 4, 5)
    print(demo.istriangle, demo.sides)
