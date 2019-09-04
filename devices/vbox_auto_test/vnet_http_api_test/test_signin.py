#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: test_signin
# Author:    fan
# date:      2019/8/12 012
# -----------------------------------------------------------
# from devices.vbox_auto_test.vnet_http_api_test.vnet_http_api_cls import *
import HTMLTestRunner

from vnet_http_api_cls import VnetHttpApi
import unittest


class TestVnetSignin(unittest.TestCase):
    def setUp(self):
        """
        测试环境初始化，适用于每个用例开始执行前
        :return:
        """
        self.vnet = VnetHttpApi("api.v-box.net")
        self.api_signin = 'we-data/login'
        self.data_signin = {
            "alias": "",
            "password": "",
            "isremeber": 0  # 文档中即如此拼写
        }

    def tearDown(self):
        """
        测试环境清理，适用于每个用例执行完毕后
        :return:
        """
        self.vnet = None

    def test_signin_correct(self):
        """
        测试登录接口, 帐号密码正确
        :return:
        """
        self.data_signin["alias"] = "test_fan"
        self.data_signin["password"] = "123456"
        r = self.vnet.vnet_post(self.api_signin, self.data_signin, '')
        self.assertEqual(r["code"], 200)

    def test_signin_password_error(self):
        """
        测试登录接口, 密码错误
        :return:
        """
        self.data_signin["alias"] = "test_fan"
        self.data_signin["password"] = "12345*"
        r = self.vnet.vnet_post(self.api_signin, self.data_signin, '')
        self.assertEqual(r["code"], 11003)

    def test_signin_password_empty(self):
        """
        测试登录接口, 密码为空
        :return:
        """
        self.data_signin["alias"] = "test_fan"
        self.data_signin["password"] = ""
        r = self.vnet.vnet_post(self.api_signin, self.data_signin, '')
        self.assertEqual(r["code"], 11003)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestVnetSignin("test_signin_correct"))
    suite.addTest(TestVnetSignin("test_signin_password_error"))
    suite.addTest(TestVnetSignin("test_signin_password_empty"))

    report_file = open(u"慧网登录接口测试报告.txt", "w")
    runner = unittest.TextTestRunner(stream=report_file, verbosity=2)

    # report_file = open(u"慧网登录接口测试报告.html", "wb")
    # runner = HTMLTestRunner.HTMLTestRunner(stream=report_file, title=u"慧网登录接口测试报告")

    runner.run(suite)
    report_file.close()
