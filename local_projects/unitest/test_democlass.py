# 单元测试参考博客：
# https://www.ibm.com/developerworks/cn/linux/l-pyunit/

import unittest
from democlass import Triangle


class TestTriangle(unittest.TestCase):
    def setUp(self):
        # 初始化，测试对象实例化
        self.triangle = Triangle()

    def tearDown(self):
        # 单元测试结束，销毁该单元测试对象
        self.triangle = None

    def test_maketriangle(self):
        # 一个测试对象的方法，对应一个单元测试类的方法
        sidecases = [(3, 4, 5), (100, 101, 102), (-1, 3, 5), (5, 0, 3)]
        results = [True, True, False, False]
        for sidecase, result in zip(sidecases, results):
            self.triangle.maketriangle(*sidecase)
            self.assertEqual(self.triangle.istriangle, result)
            self.assertEqual(self.triangle.sides, sidecase)


if __name__ == '__main__':
    # 若使用unitest.main(), 需保证单元测试的方法都是以test为开头，
    # 另参考unitest.TestSuite方法
    unittest.main()
