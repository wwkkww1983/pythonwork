#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: test_signin
# Author:    fan
# date:      2019/8/12 012
# -----------------------------------------------------------
from vnet_http_api_cls import *
import unittest
import HTMLTestRunner


class TestVnetSignin(unittest.TestCase):
    def setUp(self):
        # 测试对象初始化
        self.vnet = VnetHttpApi()

    def tearDown(self):
        # 测试用例结束
        self.vnet = None

    def test_signin_correct(self):
        # 测试登录接口, 帐号密码正确
        data_signin["alias"] = "test_fan"
        data_signin["password"] = "123456"
        r = self.vnet.post(api_signin, data_signin, '')
        self.assertEqual(r["code"], 200)

    def test_signin_password_error(self):
        # 测试登录接口, 密码错误
        data_signin["alias"] = "test_fan"
        data_signin["password"] = "12345*"
        r = self.vnet.post(api_signin, data_signin, '')
        self.assertEqual(r["code"], 11003)

    def test_signin_password_empty(self):
        # 测试登录接口, 密码为空
        data_signin["alias"] = "test_fan"
        data_signin["password"] = ""
        r = self.vnet.post(api_signin, data_signin, '')
        self.assertEqual(r["code"], 11003)

if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestSuite()
    # runner = unittest.TextTestRunner(verbosity=2)
    report_file = open("v-net api test report.txt", "wb")
    runner = unittest.TextTestRunner(stream=report_file, verbosity=2)
    # runner = HTMLTestRunner.HTMLTestRunner(stream=report_file, title=u"慧网接口测试报告")
    runner.run(suite)
    report_file.close()
