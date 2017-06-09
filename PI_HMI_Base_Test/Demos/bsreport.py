# coding:utf8
__author__ = 'admin'

import os
import unittest
import HTMLTestRunner
# HTMLTestRunner是Python标准库的unittest模块的扩展。 它生成易于使用的HTML测试报告。

# from baseproject import BaseChangeScrTest
# from baseprojscr1 import ButtonTest
from baseprojscr2 import NumberTest
# from baseprojscr3 import WordSwitchTest
# from baseprojscr5 import CombinationTest
# from baseprojscr6 import MeterTest


path_dir = os.path.dirname(__file__)

# changescr = unittest.TestLoader().loadTestsFromTestCase(BaseChangeScrTest)
# button = unittest.TestLoader().loadTestsFromTestCase(ButtonTest)
number = unittest.TestLoader().loadTestsFromTestCase(NumberTest)
# wswitch = unittest.TestLoader().loadTestsFromTestCase(WordSwitchTest)
# comb = unittest.TestLoader().loadTestsFromTestCase(CombinationTest)
# meter = unittest.TestLoader().loadTestsFromTestCase(MeterTest)
# ll = [changescr, button, number, wswitch, comb, meter]
tester = unittest.TestSuite([number])        # 多个测试用例使用1个测试套件驱动
outfile = open(path_dir + '//' + 'changescr' + 'Report.html', 'w')                # 创建结果输出文件

runner = HTMLTestRunner.HTMLTestRunner(stream=outfile, title=u'跳转测试',
                                           description=u'功能开关画面跳转')
runner.run(tester)                                            # 执行测试