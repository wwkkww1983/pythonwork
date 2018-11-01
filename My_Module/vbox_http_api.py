#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: vbox_http_api
# Author:    fan
# date:      2018/10/29
# -----------------------------------------------------------

import requests
import json
import hashlib
import time

nowtime = lambda: int(round(time.time() * 1000))  # 当前时间戳单位ms
nowtimefmt = lambda: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())    # 格式化当前时间
# lambda表达式，冒号前表示匿名函数传入参数，冒号后表示匿名函数返回值
debug = False


class VboxHttpApi(object):
    def __init__(self,
                 url="http://api.v-box.net/box-data/api/",
                 keyvalue="key=f1cd9351930d4e589922edbcf3b09a7c",
                 commonparadic=None,
                 headerswithoutcommon=None,
                 apilogin='we-data/login'
                 ):
        if commonparadic is None:
            commonparadic = {
                             "comid": "1",
                             "compvtkey": "27a010966282423fbd202bf3f45267c0",
                             "ts": None,  # ts在调用参数时动态生成
                            }
        if headerswithoutcommon is None:
            headerswithoutcommon = {
                                    "Host": '192.168.45.186:8686',
                                    "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                                                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                  'Chrome/31.0.1650.63 '
                                                  'Safari/537.36',
                                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                    "Connection": "keep-alive"
                                   }
        self.url = url
        self.keyvalue = keyvalue
        self.common_para_dic = commonparadic
        self.headers_without_common = headerswithoutcommon
        self.api_login = apilogin
        self.sid = None

    @staticmethod
    def cal_md5(string):
        md5 = hashlib.md5()
        md5.update(string.encode("utf8"))
        return md5.hexdigest()

    @staticmethod
    def sort_dict(dic):
        """
        字典排序：Return a new sorted list from the items in iterable.
        :param dic:
        :return: 排序后的字典key构成的列表
        """
        return sorted(dic)

    @staticmethod
    def merge_dic(*dics):
        """
        合并字典
        :param dics:
        :return:
        """
        dic_l = []
        for dic in dics:
            if dic:
                dic_l.extend(list(dic.items()))  # 将字典中所有键值对放到一个list中
        return dict(dic_l)  # 字典化并返回

    def url_encode(self, lst, dic):
        encoded_url = ''
        for key in lst:
            encoded_url += '{k}={v}&'.format(k=key, v=dic[key])
        encoded_url += self.keyvalue
        if debug:
            print("encoded_url:", encoded_url)
        return encoded_url

    def sign_easy(self, merged_dic: dict):
        """
        简化版的sign函数，把中间过程拆分便于其他用途。对全局参数和业务参数进行签名
        :param merged_dic: 全局参数和业务参数合并之字典
        :return:合并字典的MD5校验值，即本次post的sign签名值
        """
        merged_dic['ts'] = nowtime()
        sign = self.cal_md5(self.url_encode(self.sort_dict(merged_dic), merged_dic))
        if debug:
            print('sign: ', sign)
        return sign

    def post(self, api: str, business_dic: dict, sid):
        newurl = self.url + api
        businessdic = business_dic.copy()  # 使用字典备份，避免原字典被污染
        commondic = self.common_para_dic.copy()
        commondic["ts"] = nowtime()

        if api == self.api_login:
            businessdic["password"] = self.cal_md5(businessdic["password"])  # 登录操作需要密码
        else:
            commondic["sid"] = sid  # 登录之外的操作需要sid
        mergedic = self.merge_dic(businessdic, commondic)    # 合并全局参数字典和业务参数字典
        commondic["sign"] = self.sign_easy(mergedic)
        headers_dict = self.headers_without_common.copy()
        headers_dict["common"] = json.dumps(commondic)

        if debug:
            print("newdict: {nd}\n\n"
                  "common_para_dict2: {cpd}\n\n"
                  "headers: {hds}\n".format(nd=mergedic, cpd=commondic, hds=headers_dict))

        r = requests.post(newurl, data=mergedic, headers=headers_dict)  # 提交
        return r

    def login(self, logindic):
        login_result = self.post(self.api_login, logindic, '')
        self.sid = login_result.json()["result"]["sid"]
        return login_result

if __name__ == '__main__':
    # url_test = "http://192.168.45.186:8686/box-data/api/"
    # url = "http://api.v-box.net/box-data/api/"

    api_login = 'we-data/login'
    api_get_boxes_list = 'we-data/boxs'

    login_data_dic = {"alias": "test_fanch",
                      "password": "123456",
                      "isremember": 1
                      }
    a = VboxHttpApi()
    r1 = a.login(login_data_dic)
    sid = a.sid
    r2 = a.post(api_get_boxes_list, {}, sid)
    print("log in result:", r1.json(), '\n')
    print('box list info', r2.json(), '\n')
