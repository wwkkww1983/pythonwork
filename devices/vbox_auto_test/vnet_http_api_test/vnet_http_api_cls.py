#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: web_api
# Author:    fan
# date:      2018/5/19
# -----------------------------------------------------------
import requests
import json
import hashlib
import time

debug = False


class VnetHttpApi(object):
    def __init__(self, vnet_host):
        self.sid = None
        # headers参数，特定值，研发提供（猜测跟公司绑定）第三方接口，某些api可能不支持
        self.keyvalue = "key=f1cd9351930d4e589922edbcf3b09a7c"
        self.url = "http://" + vnet_host + "/box-data/api/"
        self.headers_common_dic = {
            "comid": "1",
            "compvtkey": "27a010966282423fbd202bf3f45267c0",
            "ts": 0,  # ts在调用参数时动态生成
        }
        self.headers_without_common_dic = {
            "Host": vnet_host,
            "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/69.0.3497.92 '
                          'Safari/537.36',
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Connection": "keep-alive"
        }

    def get_dic_sign(self, dic: dict):
        """
        简化版的sign函数，把中间过程拆分便于其他用途。对全局参数和业务参数进行签名
        :param dic: 全局参数和业务参数合并之字典
        :return:合并字典的MD5校验值，即本次post的sign签名值
        """
        lis = sorted(dic)  # 键值升序排列
        encoded_url_without_key = "&".join(["{}={}".format(k, dic[k]) for k in lis])  # 拼接字符串
        encoded_url = encoded_url_without_key + "&" + self.keyvalue  # 末尾加上key
        if debug:
            print("encoded_url:", encoded_url)
        sign = self.cal_md5(encoded_url)  # 签名加密
        if debug:
            print('sign: ', sign)
        return sign

    def vnet_post(self, api: str, data_dic: dict, sid: str):
        print("----api:", api)
        print("----post data:", data_dic)
        print("----sid:", sid)
        newurl = self.url + api
        print("----url: {}".format(newurl))
        datadic = data_dic.copy()  # 使用字典备份，避免原字典被污染
        headerscommondic = self.headers_common_dic.copy()
        headerscommondic["ts"] = self.get_now_timestamp()
        if api == 'we-data/login' or 'user/signin':
            datadic["password"] = self.cal_md5(datadic["password"])
        else:
            headerscommondic["sid"] = sid

        merge_dic = dict()
        merge_dic.update(datadic)
        merge_dic.update(headerscommondic)
        headerscommondic["sign"] = self.get_dic_sign(merge_dic)
        headersdic = self.headers_without_common_dic.copy()
        headersdic["common"] = json.dumps(headerscommondic)
        if debug:
            print("tosigndict: {nd}\n"
                  "commondict: {cpd}\n"
                  "headersdict: {hds}".format(nd=merge_dic, cpd=headerscommondic, hds=headersdic))

        r = requests.post(newurl, data=datadic, headers=headersdic)
        print("----feedback data: {}\n".format(r.text))
        return r.json()

    @staticmethod
    def cal_md5(string: str):
        md5 = hashlib.md5()
        md5.update(string.encode("utf-8"))
        return md5.hexdigest()

    @staticmethod
    def get_now_timestamp():
        return int(round(time.time() * 1000))  # 将当前时间戳改为以ms表示, 四舍五入取整

    @staticmethod
    def get_now_strftime():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 将当前时间以特定格式字符串化


if __name__ == '__main__':
    # host = "192.168.45.190:8686"  # 内网测试网址
    host = "api.v-box.net"  # 第三方接口调用网址

    api_signin = 'we-data/login'
    data_signin = {
        "alias": "test_fan",
        "password": "123456",
        "isremeber": 0  # 文档中即如此拼写
    }

    vnet = VnetHttpApi(host)
    vnet.vnet_post(api_signin, data_signin, "")
