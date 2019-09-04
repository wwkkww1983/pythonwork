#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: http_get_box_configs
# Author:    fan
# date:      2019/7/25 025
# -----------------------------------------------------------
import requests as req
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


class VnetHttpApi(object):
    def __init__(self):
        self.sid = None
        self.boxlist = None
        self.realgroups = None
        self.realdatas = None
        self.realcfgs = None

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
        return js

    def do_signin(self):
        r = self.post(api_signin, data_signin, '')
        self.sid = r["result"]["sid"]
        return r

    def get_all_boxes(self):
        """
        利用api_boxes，获取当前登录用户下包含盒子基本信息的列表，包含机器码和盒子分组情况
        :return:
        """
        r = self.post(api_boxes, {}, self.sid)
        boxlist = []
        for g in r["result"]["list"]:
            for b in g["boxList"]:
                b["groupName"] = g["groupName"]
                boxlist.append(b)
        self.boxlist = boxlist  # 通过机器码可以获取每台盒子的型号、是否报警、名称、在线状态、boxId等信息
        """
        元素结构={
                        "machineCode": "V02001180517884c2d35f9f3386",
                        "devModel": "V-BOX S-4G",
                        "isAlarm": 1,
                        "boxName": "884 3386",
                        "remark": "",
                        "state": "1",
                        "map": ",",
                        "boxId": "150"
                        "groupName": "默认组"
                    }
        """
        return boxlist

    def get_all_realdatas(self):
        realdatas = []
        for box in self.boxlist:
            params = data_realgroups.copy()
            params["boxId"] = box["boxId"]
            r = self.post(api_realgroups, params, self.sid)
            item = dict()
            item["boxId"] = box["boxId"]
            item["realgroups"] = []
            for grp in r["result"]["list"]:
                grp["dataList"] = []
                params = data_realcfgs.copy()
                params["groupId"] = grp['groupId']
                params["boxId"] = box["boxId"]
                r = self.post(api_realcfgs, params, self.sid)
                if "cfgList" in r["result"].keys():
                    grp["dataList"] = r["result"]["cfgList"]
                item["realgroups"].append(grp)
                # print(item)
            realdatas.append(item)
        self.realdatas = realdatas
        """
        realdatas元素=
    {
        "boxId": "150",
        "realgroups": [
            {
                "dataList": [],
                "groupId": 13354,
                "groupName": "默认组"
            },
            {
                "dataList": [],
                "groupId": 13918,
                "groupName": "其他分组"
            }
        ]
    }
    dataList元素={
                        "monitorId": 144129,
                        "dataLimit": "0 99999",
                        "digitCount": "5,0",
                        "addr": "9",
                        "roleType": 3,
                        "monitorName": "40_9",
                        "updTime": 1563776232000,
                        "rid": "4",
                        "addrType": 2,
                        "digitBinary": "十进制",
                        "dataId": 105
                    },

        """
        return realdatas


if __name__ == '__main__':
    vnet = VnetHttpApi()
    vnet.do_signin()
    vnet.get_all_boxes()
    vnet.get_all_realdatas()
    print(vnet.realdatas)
