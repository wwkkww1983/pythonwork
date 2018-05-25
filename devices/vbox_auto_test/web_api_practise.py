#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: web_api
# Author:    fan
# date:      2018/5/19
# -----------------------------------------------------------
import os
import requests as req
from urllib.parse import urlencode
import json
import hashlib
import time

debug = True
url_test = "http://192.168.45.186:8686/box-data/api/"
url_normal = "http://api.v-box.net/box-data/api/"
api_login = 'we-data/login'
api_boxes_list = 'we-data/boxs'
nowtime = lambda: int(round(time.time() * 1000))  # 当前时间戳单位ms
# lambda表达式，冒号前表示匿名函数传入参数，冒号后表示匿名函数返回值
keyvalue = "key=f1cd9351930d4e589922edbcf3b09a7c"  # headers参数，特定值，研发提供（猜测跟公司绑定）

common_para_dic = {"comid": "1",
                   "compvtkey": "27a010966282423fbd202bf3f45267c0",
                   "ts": None,  # ts在调用参数时动态生成
                   }

login_data_dic = {"alias": "test_fan",
                  "password": "123456",
                  "isremember": 1
                  }

headers_without_common = {"Host": '192.168.45.186:8686',
                          "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                                        'Chrome/31.0.1650.63 '
                                        'Safari/537.36',
                          "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                          "Connection": "keep-alive"
                          }


def cal_md5(string):
    md5 = hashlib.md5()
    md5.update(string.encode("utf8"))
    return md5.hexdigest()


def sort_dict(dic):
    """
    字典排序：Return a new sorted list from the items in iterable.
    :param dic:
    :return: 排序后的字典key构成的列表
    """
    return sorted(dic)


def url_encode(lis, dic):
    """
    按照格式和lis规定的key顺序，将dic进行字符串拼接
    :param lis:
    :param dic:
    :return: 拼接后字符串
    """
    encoded_url = ''
    for key in lis:
        encoded_url += '{k}={v}&'.format(k=key, v=dic[key])
    encoded_url += keyvalue
    print("encoded_url:", encoded_url)
    return encoded_url


def sign_easy(merged_dic: dict):
    """
    简化版的sign函数，把中间过程拆分便于其他用途。对全局参数和业务参数进行签名
    :param merged_dic: 全局参数和业务参数合并之字典
    :return:合并字典的MD5校验值，即本次post的sign签名值
    """
    merged_dic['ts'] = nowtime()
    sign = cal_md5(url_encode(sort_dict(merged_dic), merged_dic))
    print(sign)
    return sign


def sign(merged_dic: dict):
    """
    对全局参数和业务参数进行签名
    :param merged_dic: 全局参数和业务参数合并之字典
    :return:合并字典的MD5校验值，即本次post的sign签名值
    """
    merged_dic['ts'] = nowtime()  # ts动态更新
    # sorted_dic_list = sorted(para_dict, key=lambda x: x[0], reverse=False)    # 返回已排序字典，排序依据=每个key的首元素，升序
    # 注意！！！上下两种方式排列结果不同，应按照下面的方式
    sorted_dic_list = sorted(merged_dic)  # 按sorted默认方式排序即可
    para_str = ''
    for key in sorted_dic_list:
        para_str += '{k}={v}&'.format(k=key, v=merged_dic[key])
    para_str += keyvalue  # 待算md5的字符串准备完毕
    if debug:
        print('str to be signed: ', para_str)
    para_str_md5_value = cal_md5(para_str)
    # print(para_str_md5_value)
    return para_str_md5_value


def post(api: str, business_dic: dict, sid):
    newurl = url_normal + api
    businessdic = business_dic.copy()  # 使用字典备份，避免原字典被污染
    commondic = common_para_dic.copy()
    commondic["ts"] = nowtime()

    if api == api_login:
        businessdic["password"] = cal_md5(businessdic["password"])

    else:
        commondic["sid"] = sid

    mergedic = dict(list(businessdic.items()) + list(commondic.items()))
    commondic["sign"] = sign_easy(mergedic)

    headers_dict = headers_without_common.copy()
    headers_dict["common"] = json.dumps(commondic)

    if debug:
        print("newdict: {nd}\n\n"
              "common_para_dict2: {cpd}\n\n"
              "headers: {hds}\n".format(nd=mergedic, cpd=commondic, hds=headers_dict))

    r = req.post(newurl, data=mergedic, headers=headers_dict)
    return r


def headers():
    pass


def do_login():
    url = url_normal + api_login
    login_data_dic2 = login_data_dic.copy()  # 使用字典备份，避免原字典被污染
    common_para_dic2 = common_para_dic.copy()

    newpasword = login_data_dic2.get("password")  # 密码值替换为对应MD5字符串
    login_data_dic2["password"] = cal_md5(newpasword)
    common_para_dic2["ts"] = nowtime()  # ts时间戳更新

    # login接口的sign是使用commondict与logindict合并后计算的
    new_login_dict = dict(list(login_data_dic2.items()) + list(common_para_dic2.items()))
    common_para_dic2["sign"] = sign_easy(new_login_dict)

    # header
    headers_dict = headers_without_common.copy()
    headers_dict["common"] = json.dumps(common_para_dic2)
    if debug:
        print("newdict: {nd}\n\n"
              "common_para_dict2: {cpd}\n\n"
              "headers: {hds}\n".format(nd=new_login_dict, cpd=common_para_dic2, hds=headers_dict))

    r = req.post(url, data=new_login_dict, headers=headers_dict)
    login_response_dict = r.json()
    if debug:
        print('data:\n', urlencode(new_login_dict))
        print('login_response_dict')
        for k, v in login_response_dict.items():
            print("   ", k, "=", v)
        print("login_reponse_headers")
        for k, v in r.headers.items():
            print("   ", k, "=", v)
    return login_data_dic


if __name__ == '__main__':
    # sign(global_para_dic)
    # url = url_normal + api_login
    # password_md5 = cal_md5(login_data_dic.get("password"))
    # data_dic = login_data_dic.copy()
    # data_dic["password"] = password_md5
    # print(data_dic)
    # r = req.get(url, data=data_dic)
    # print(r.text)
    # do_login()
    r1 = post(api_login, login_data_dic, '')
    # r2 = post('we-data/boxs', {})
    sid = r1.json()["result"]["sid"]
    print(r1.json())
    print(sid)
    r2 = post(api_boxes_list, {}, sid)
    f = open("boxeslistresult.json", "w", encoding="utf-8")
    boxeslist_result = r2.json()
    f.write(json.dumps(boxeslist_result, ensure_ascii=False, indent=4))
    print(boxeslist_result)
    for box in r2.json()["result"]["list"][0]['boxList']:
        print(box)

