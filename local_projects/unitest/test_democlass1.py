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
        resultline = "\n==================== test cases ===================="
        print(resultline)
        for line in self.data:
            print(line)
        resultline = "\n==================== test report ===================="
        print(resultline)
        paramnum = None
        for line in self.data:
            if "start" in line:
                line2list = [i for i in line.split('.')]
                paramnum = int(line2list[2])
                resultline = line
            if "," in line:
                line2list = [j.strip() for j in line.split(',')]    # 分解字符串，去空格
                inputs = line2list[1:paramnum+1]
                de_outputs = line2list[paramnum+1:]    # 预期输出
                try:
                    result = ([self.demo.addstr(*inputs)] == de_outputs)
                except:
                    result = False
                resultline = line2list[0] + ', ' + str(result)
                self.assertEqual(1, 1)
            if "end" in line:
                resultline = line
            print(resultline)

if __name__ == '__main__':
    unittest.main()
