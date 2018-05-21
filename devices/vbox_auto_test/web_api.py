#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: web_api
# Author:    fan
# date:      2018/5/19
# -----------------------------------------------------------
import os
import requests as req
import json
import hashlib
import time

debug = True
url_test = "http://192.168.45.186:8686/box-data/api/"
url_normal = "http://api.v-box.net/box-data/api/"
api_login = 'we-data/login'
keyvalue="key=f1cd9351930d4e589922edbcf3b09a7c"    # headers参数，特定值，研发提供（猜测跟公司绑定）

common_para_dic = {"comid": "1",
                   "compvtkey": "27a010966282423fbd202bf3f45267c0",
                   "ts": None,    # ts在调用参数时动态生成
                   # "isremeber": 1
                   }

login_data_dic = {"alias": "test_fan",
                  "password": "123456",
                  # "isremember": 1
                  }
headers_without_common = {"Host": "v-box.net",
                          "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0",
                          # "Accept": "*/*",
                          # "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                          # "Accept-Encoding": "gzip, deflate",
                          "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                          # "Referer": "http://www.v-box.net/web/html/user/login.html",
                          # "Origin": "http://www.v-box.net",
                          "Connection": "keep-alive"
                          }
nowtime = lambda: int(round(time.time()*1000))    # 当前时间戳单位ms
# lambda表达式，冒号前表示匿名函数传入参数，冒号后表示匿名函数返回值


def cal_md5(string):
    md5 = hashlib.md5()
    md5.update(string.encode("utf8"))
    return md5.hexdigest()


def sign(para_dict: dict):
    """
    对全局参数和业务参数进行签名
    :param global_para_dict:全局参数字典
    :param data_dic:业务参数字典
    :return:所有参数的MD5校验值
    """
    para_dict['ts'] = nowtime()    # ts动态更新
    sorted_dic_list = sorted(para_dict, key=lambda x: x[0], reverse=False)    # 返回已排序字典，排序依据=每个key的首元素，升序
    # sorted_dic_list = sorted(para_dict)    # 按sorted默认方式排序即可
    # print(sorted_dic_list)
    para_str = ''
    for key in sorted_dic_list:
        para_str += '{k}={v}&'.format(k=key, v=para_dict[key])
    para_str += keyvalue  # 待算md5的字符串准备完毕
    # print(para_str)
    para_str_md5_value = cal_md5(para_str)
    # print(para_str_md5_value)
    return para_str_md5_value


def post(api, data_dic, common_dic):
    newurl = url_normal + api
    r = req.get(newurl, data=data_dic)
    print(r.headers)


def headers():
    pass


def do_login():
    url = url_normal + api_login
    login_data_dic2 = login_data_dic.copy()    # 使用字典备份，避免原字典被污染
    common_para_dic2 = common_para_dic.copy()

    newpasword = login_data_dic2.get("password")    # 密码值替换为对应MD5字符串
    login_data_dic2["password"] = cal_md5(newpasword)
    common_para_dic2["ts"] = nowtime()    # ts时间戳更新

    # login接口的sign是使用commondict与logindict合并后计算的
    new_login_dict = dict(list(login_data_dic2.items()) + list(common_para_dic2.items()))
    common_para_dic2["sign"] = sign(new_login_dict)

    # header
    headers_dict = headers_without_common.copy()
    headers_dict["common"] = json.dumps(common_para_dic2)
    if debug:
        print("newdict: {nd}\n\n"
              "common_para_dict2: {cpd}\n\n"
              "headers: {hds}\n".format(nd=new_login_dict, cpd=common_para_dic2, hds=headers_dict))
    r = req.post(url, data=new_login_dict, headers=headers_dict)\

    login_response_dict = r.json()
    if debug:
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
    do_login()

