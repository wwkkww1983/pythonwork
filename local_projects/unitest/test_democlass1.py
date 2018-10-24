#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: test_democlass1
# Author:    fan
# date:      2018/10/17
# -----------------------------------------------------------
import unittest
from democlass1 import Demo

class TestDemo(unittest.TestCase):
    def setUp(self):
        self.demo = Demo()
        self.data = []
        self.results = []
        with open("test_data.txt", "r", encoding="utf-8") as f:
            for line in f.readlines():
                self.data.append(line.strip())

    def tearDown(self):
        with open("test_result.txt", 'w', encoding="utf-8") as f:
            f.writelines(self.results)
        self.demo = None

    def test_addstr(self):
        for line in self.data:
            if line not in ["title"] + [str(i) for i in range(100)]:
                line2list = [j.strip() for j in line.split(',')]    # 分解字符串，去空格
                if line2list.__len__() != 1:
                    # 非用例行（标题，模块名）禁用半角逗号
                    inputs = line2list[1:4]
                    result = line2list[4]
                    # self.demo.addstr(*inputs)
                    try:
                        self.result = (self.demo.addstr(*inputs) == result)
                    except:
                        self.result = False
                    self.results.append(line2list[0] + ', ' + str(self.result) + '\n')
                    self.assertEqual(1, 1)
                else:
                    self.results.append(line+'\n')
            else:
                self.results.append(line+'\n')

if __name__ == '__main__':
    unittest.main()
