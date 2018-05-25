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

debug = False
url_test = "http://192.168.45.186:8686/box-data/api/"
url_normal = "http://api.v-box.net/box-data/api/"
api_login = 'we-data/login'
api_boxes_list = 'we-data/boxs'
nowtime = lambda: int(round(time.time() * 1000))  # 当前时间戳单位ms
nowtimefmt = lambda: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())    # 格式化当前时间
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
    if debug:
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
    if debug:
        print('sign: ', sign)
    return sign


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


if __name__ == '__main__':

    r1 = post(api_login, login_data_dic, '')
    # r2 = post('we-data/boxs', {})
    sid = r1.json()["result"]["sid"]
    print("log in result:", r1.json(), '\n')
    print('sid: ', sid, '\n')

    # f = open("boxeslistresult.json", "w", encoding="utf-8")
    # f.write(json.dumps(boxeslist_result, ensure_ascii=False, indent=4))
    with open("vbox_state_log.csv", 'w', encoding='gb2312') as f:
        f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8}\n'.format(
            '记录时间', '测试部882', '测试部883', '测试部884', '测试部885', '测试部886', '测试部887', '测试部888', '测试部889'))
    i = 0
    while i < 200:
        i += 1
        r2 = post(api_boxes_list, {}, sid)
        boxeslist_result = r2.json()
        tobe_write_down = nowtimefmt()
        name_state = {}
        if boxeslist_result["code"] != 200:
            tobe_write_down += '获取v-box列表失败：状态码{}\n'.format(boxeslist_result["code"])
        else:
            for box in boxeslist_result["result"]["list"][0]['boxList']:
                for s in ['测试部882', '测试部883', '测试部884', '测试部885',
                          '测试部886', '测试部887', '测试部888', '测试部889']:
                    if box['boxName'] == s:
                        name_state[s] = box['state']
            for c in sorted(name_state):
                tobe_write_down += ',{}'.format(str(name_state[c]))
            tobe_write_down += '\n'
            print(tobe_write_down)
        with open("vbox_state_log.csv", 'a', encoding='utf-8') as f:
            f.write(tobe_write_down)
        time.sleep(30)
