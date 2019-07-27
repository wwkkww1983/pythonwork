#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: web_api
# Author:    fan
# date:      2018/5/19
# -----------------------------------------------------------
import os
import requests as req
from urllib.parse import urlencode, urlparse
import json
import hashlib
import time

debug = False
nowtime = lambda: int(round(time.time() * 1000))  # 当前时间戳单位ms
nowtimefmt = lambda: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 格式化当前时间
# lambda表达式，冒号前表示匿名函数传入参数，冒号后表示匿名函数返回值
keyvalue = "key=f1cd9351930d4e589922edbcf3b09a7c"  # headers参数，特定值，研发提供（猜测跟公司绑定）第三方接口，某些api可能不支持

host_test = "192.168.45.190:8686"
url_test = "http://" + host_test + "/box-data/api/"
host_normal = "api.v-box.net"
url_normal = "http://" + host_normal + "/box-data/api/"

api_signin = 'we-data/login'
api_boxes = 'we-data/boxs'  # 获取盒子列表,获取数据与getboxgroup接口类似，该接口无提交数据

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
data_signin = {
    "alias": "test_fan",
    "password": "123456",
    "isremeber": 0  # 网页接口文档上这个键是个错别字正确拼写isremember
}

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

    def do_signin(self):
        r = self.post(api_signin, data_signin, '')
        self.sid = r["result"]["sid"]
        return r

    def do_boxes(self):
        """获取盒子列表"""
        r = self.post(api_boxes, {}, self.sid)
        return r

    def do_realgroups(self):
        r = self.post(api_realgroups, data_realgroups, self.sid)
        return r

    def do_realcfgs(self):
        r = self.post(api_realcfgs, data_realcfgs, self.sid)
        return r

    def do_realdata(self):
        """实时监控点数据列表"""
        r = self.post(api_realdata, data_realdata, self.sid)
        return r

    def do_updrealdata(self):
        """修改实时监控点数据"""
        r = self.post(api_updrealdata, data_updrealdata, self.sid)
        return r

    def do_monitors(self):
        """获取历史监控点名称列表"""
        r = self.post(api_monitors, {}, self.sid)
        return r

    def do_historydata(self):
        """获取指定监控点历史数据"""
        r = self.post(api_historydata, data_historydata, self.sid)
        return r

    def do_alarmdata(self):
        """获取报警数据"""
        r = self.post(api_alarmdata, data_alarmdata, self.sid)
        return r


if __name__ == '__main__':
    vnet = VnetHttpApi()
    vnet.do_signin()
    # vnet.do_boxes()
    # vnet.do_realgroups()
    # vnet.do_realcfgs()
    # vnet.do_realdata()
    # vnet.do_updrealdata()
    # vnet.do_monitors()
    # vnet.do_historydata()
    # vnet.do_alarmdata()
