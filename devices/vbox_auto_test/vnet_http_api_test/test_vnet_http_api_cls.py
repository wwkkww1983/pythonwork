#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: test_vnet_http_api_cls
# Author:    fan
# date:      2019/7/3 003
# -----------------------------------------------------------
# 单元测试参考博客：
# https://www.ibm.com/developerworks/cn/linux/l-pyunit/
from unittest import TestSuite

import requests as req
import json
import hashlib
import time
import unittest
import HTMLTestRunner
from ddt import ddt, data, unpack  # ddt 将测试变量参数化

debug = False
nowtime = lambda: int(round(time.time() * 1000))  # 当前时间戳单位ms
nowtimefmt = lambda: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 格式化当前时间
# lambda表达式，冒号前表示匿名函数传入参数，冒号后表示匿名函数返回值
keyvalue = "key=f1cd9351930d4e589922edbcf3b09a7c"  # headers参数，特定值，研发提供（猜测跟公司绑定）第三方接口，某些api可能不支持

host_test = "192.168.45.190:8686"
url_test = "http://" + host_test + "/box-data/api/"
host_normal = "api.v-box.net"
url_normal = "http://" + host_normal + "/box-data/api/"

data_headers_common = {
    "comid": "1",
    "compvtkey": "27a010966282423fbd202bf3f45267c0",
    "ts": None,  # ts在调用参数时动态生成
}
data_headers_without_common = {
    "Host": host_normal,
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/69.0.3497.92 '
                  'Safari/537.36',
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Connection": "keep-alive"
}

api_signin = 'we-data/login'
data_signin = {
    "alias": "test_fan",
    "password": "123456",
    "isremeber": 0  # 网页接口文档上这个键是个错别字正确拼写isremember
}

api_boxes = 'we-data/boxs'  # 获取盒子列表,获取数据与getboxgroup接口类似，该接口无提交数据

api_realgroups = 'we-data/realgroups'  # 获取实时监控点分组列表
data_realgroups = {
    'boxId': None  # 盒子ID（不传为自定义的监控点分组）
}

api_realcfgs = 'we-data/realcfgs'  # 获取实时监控点配置
data_realcfgs = {
    'boxId': None,
    'groupId': None,  # 组ID，必传
    'pageSize': 10,  # 每页数量,不传默认10条
    'pageIndex': 1,  # 第几页，从1开始
}

api_realdata = 'we-data/realdata'  # 获取实时数据
data_realdata = {
    'boxId': None,
    'groupId': None,  # 组ID，必传
    'pageSize': 10,  # 每页数量,不传默认10条
    'pageIndex': 1,  # 第几页，从1开始
}

api_updrealdata = 'we-data/updrealdata'  # 修改实时监控点数据
data_updrealdata = {
    'monitorId': None,  # 监控点序号
    'value': None,  # 值
}

api_monitors = 'we-data/monitors'  # 获取历史监控点名称列表
data_monitors = {
    'boxId': None,  # 盒子ID，可为空
}

api_historydata = 'we-data/historydata'  # 获取历史数据
data_historydata = {
    'monitorId': None,  # 监控点序号, 必填
    'monitorBeginTime': None,  # 监控开始时间，可为空，格式：2018-12-05 12:20:20
    'monitorEndTime': None,  # 监控结束时间，可为空
    'pageSize': 10,  # 每页数量,不传默认10条
    'pageIndex': 1,  # 第几页，从1开始
}

api_alarmdata = 'we-data/alarmdata'  # 获取报警数据
data_alarmdata = {
    'boxId': None,  # 监控点序号, 必填
    'monitorBeginTime': None,  # 监控开始时间，可为空
    'monitorEndTime': None,  # 监控结束时间，可为空
    'pageSize': 10,  # 每页数量,不传默认10条
    'pageIndex': 1,  # 第几页，从1开始
    'state': None,  # 状态1-未确认，2-已确认
    'alarmType': None,  # 报警事件：1-触发报警， 0-解除报警（可为空）
    'alarmLevel': None  # 报警等级：1-一般，2-严重，3-特别严重
}


class VnetHttpApi(object):
    def __init__(self):
        self.sid = None

    def text_to_dict(self, text: str):
        d = dict()
        if "&" in text:
            l = text.split("&")
            for i in l:
                k, v = i.split("=")
                if v.isdigit():
                    v = int(v)
                d[k] = v
        if debug:
            print(d)
        return d

    def cal_md5(self, string: str):
        md5 = hashlib.md5()
        md5.update(string.encode("utf-8"))
        return md5.hexdigest()

    def sign_easy(self, dic: dict):
        """
        简化版的sign函数，把中间过程拆分便于其他用途。对全局参数和业务参数进行签名
        :param dic: 全局参数和业务参数合并之字典
        :return:合并字典的MD5校验值，即本次post的sign签名值
            """
        lis = sorted(dic)  # 键值升序排列
        encoded_url_without_key = "&".join(["{}={}".format(k, dic[k]) for k in lis])  # 拼接字符串
        encoded_url = encoded_url_without_key + "&" + keyvalue  # 末尾加上key
        if debug:
            print("encoded_url:", encoded_url)
        sign = self.cal_md5(encoded_url)  # 签名加密
        if debug:
            print('sign: ', sign)
        return sign

    def post(self, api: str, business_dic: dict, sid: str):
        print("----api:", api)
        print("----post data:", business_dic)
        print("----sid:", sid)
        newurl = url_normal + api
        businessdic = business_dic.copy()  # 使用字典备份，避免原字典被污染
        commondic = data_headers_common.copy()
        commondic["ts"] = nowtime()
        if api == api_signin:
            businessdic["password"] = self.cal_md5(businessdic["password"])
        else:
            commondic["sid"] = sid
        mergedic = dict(list(businessdic.items()) + list(commondic.items()))
        commondic["sign"] = self.sign_easy(mergedic)

        headers_dict = data_headers_without_common.copy()
        headers_dict["common"] = json.dumps(commondic)
        if debug:
            print("tosigndict: {nd}\n"
                  "commondict: {cpd}\n"
                  "headersdict: {hds}".format(nd=mergedic, cpd=commondic, hds=headers_dict))
        r = req.post(newurl, data=businessdic, headers=headers_dict)
        print("----url: {}".format(newurl))
        print("----feedback data: {}\n".format(r.text))
        js = r.json()
        # print("----feedback data: {}\n".format(r.text))
        return js
    #
    # def do_signin(self):
    #     r = self.post(api_signin, data_signin, '')
    #     self.sid = r["result"]["sid"]
    #     return r
    #
    # def do_boxes(self):
    #     """获取盒子列表"""
    #     r = self.post(api_boxes, {}, self.sid)
    #     return r
    #
    # def do_realgroups(self):
    #     r = self.post(api_realgroups, data_realgroups, self.sid)
    #     return r
    #
    # def do_realcfgs(self):
    #     r = self.post(api_realcfgs, data_realcfgs, self.sid)
    #     return r
    #
    # def do_realdata(self):
    #     """实时监控点数据列表"""
    #     r = self.post(api_realdata, data_realdata, self.sid)
    #     return r
    #
    # def do_updrealdata(self):
    #     """修改实时监控点数据"""
    #     r = self.post(api_updrealdata, data_updrealdata, self.sid)
    #     return r
    #
    # def do_monitors(self):
    #     """获取历史监控点名称列表"""
    #     r = self.post(api_monitors, {}, self.sid)
    #     return r
    #
    # def do_historydata(self):
    #     """获取指定监控点历史数据"""
    #     r = self.post(api_historydata, data_historydata, self.sid)
    #     return r
    #
    # def do_alarmdata(self):
    #     """获取报警数据"""
    #     r = self.post(api_alarmdata, data_alarmdata, self.sid)
    #     return r


@ddt
class TestVnetHttpApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.vnet = VnetHttpApi()
        r = cls.vnet.post(api_signin, data_signin, '')
        cls.vnet.sid = r["result"]["sid"]
        cls.sid = cls.vnet.sid

    @classmethod
    def tearDownClass(cls):
        pass

    # @data(("test_fanch", "123456"))
    # @unpack
    # def test_do_signin(self, user, password):
    #     """测试登录接口"""
    #     data_signin["alias"] = user
    #     data_signin["password"] = password
    #     r = self.vnet.do_signin()
    #     self.assertEqual(r["code"], 200)
    def test_do_boxes(self):
        r = self.vnet.post(api_boxes, {}, self.sid)
        self.assertEqual(r["code"], 200)

    @data(("150", ), ("157", ))
    @unpack
    def test_do_realgroups(self, boxid):
        """测试获取实时监控点分组"""
        data_realgroups["boxId"] = boxid
        r = self.vnet.post(api_realgroups, data_realgroups, self.sid)
        self.assertEqual(r["code"], 200)

    @data(("150", "906"), ("157", "7561"))
    @unpack
    def test_do_realcfgs(self, boxid, groupid):
        """测试获取实时监控点配置信息"""
        data_realcfgs['boxId'] = boxid
        data_realcfgs["groupId"] = groupid
        r = self.vnet.post(api_realcfgs, data_realcfgs, self.sid)
        self.assertEqual(r["code"], 200)

    @data(("150", "906"), ("157", "7561"))
    @unpack
    def test_do_realdata(self, boxid, groupid):
        """测试获取实时监控点数据列表"""
        data_realdata["boxId"] = boxid
        data_realdata["groupId"] = groupid
        r = self.vnet.post(api_realdata, data_realdata, self.sid)
        self.assertEqual(r["code"], 200)

    @data((136340, "1"), (136337, "32767"))
    @unpack
    def test_do_updrealdata(self, monitorid, value):
        data_updrealdata["monitorId"] = monitorid
        data_updrealdata["value"] = str(value)
        r = self.vnet.post(api_updrealdata, data_updrealdata, self.sid)
        self.assertEqual(r["code"], 200)

    def test_do_monitors(self):
        """测试获取历史监控点名称列表"""
        r = self.vnet.post(api_monitors, {}, self.sid)
        self.assertEqual(r["code"], 200)

    @data(136339, 136338)
    def test_do_historydata(self, monitorid):
        """测试获取指定历史监控点历史数据"""
        _data_historydata = data_historydata.copy()  # 因为用到了pop方法，提前备份接口参数dict
        _data_historydata["monitorId"] = monitorid
        _data_historydata.pop("monitorBeginTime")
        _data_historydata.pop("monitorEndTime")
        r = self.vnet.post(api_historydata, _data_historydata, self.sid)
        self.assertEqual(r["code"], 200)

    @data(150, 157)
    def test_do_alarmdata(self, boxid):
        """测试获取报警数据接口"""
        _data_alarmdata = data_alarmdata.copy()
        _data_alarmdata["boxId"] = boxid
        _data_alarmdata.pop("monitorBeginTime")
        _data_alarmdata.pop("monitorEndTime")
        # _data_alarmdata.pop("state")
        _data_alarmdata["state"] = 1
        _data_alarmdata.pop("alarmType")
        _data_alarmdata.pop("alarmLevel")
        r = self.vnet.post(api_alarmdata, _data_alarmdata, self.sid)
        self.assertEqual(r["code"], 200)


if __name__ == '__main__':
    # # 直接调用unittest.main方法进行测试
    # unittest.main()
    # 构造测试套件进行测试
    suite = unittest.TestSuite()
    # test_methods = {
    #      "test_do_boxes": 1,
    #      "test_do_realgroups": 2,
    #      "test_do_realcfgs": 2,
    #      "test_do_realdata": 2,
    #      "test_do_updrealdata": 2,
    #      "test_do_monitors":1,
    #      "test_do_historydata": 2,
    #      "test_do_alarmdata": 2
    # }
    #
    # def add_test(test_suite):
    #     for test in test_methods.keys():
    #         if test_methods[test] == 1:
    #             test_suite.addTest(TestVnetHttpApi(test))
    #         else:
    #             for i in range(1, test_methods[test]+2):
    #                 test_suite.addTest(TestVnetHttpApi(test+"_{}".format(i)))
    #     return test_suite
    # add_test(suite)

    runner = unittest.TextTestRunner(verbosity=2)
    report_file = open("慧网接口测试报告.html", "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=report_file, title=u"慧网接口测试报告")
    runner.run(suite)
    report_file.close()
