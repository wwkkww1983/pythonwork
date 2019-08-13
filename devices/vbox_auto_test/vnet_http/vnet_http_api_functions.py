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
nowtime = lambda: int(round(time.time() * 1000))  # 当前时间戳单位ms
nowtimefmt = lambda: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())    # 格式化当前时间
# lambda表达式，冒号前表示匿名函数传入参数，冒号后表示匿名函数返回值
keyvalue = "key=5cee621329f24e5cbdc43daa959ce9a1"  # headers参数，特定值，研发提供（猜测跟公司绑定）

host_test = "192.168.45.190:8686"
# url_test = "http://" + host_test + "/box-data/api/"
url_test = "http://" + host_test + "/box-web/api/"
host_normal = "rc.v-box.net:8080"
url_normal = "http://" + host_normal + "/box-web/api/"

# 变更内外网时，修改这两个参数
host = host_test
url = url_test

api_signin = 'user/signin'  # 登录接口
api_check = 'user/check'  # 检查？该接口无提交数据
api_userinfo = 'user/userinfo'  # 获取用户信息，该接口无提交数据
api_getboxgroup = 'baseInfoAction/getBoxGroup'  # 获取盒子分组信息,该接口无提交数据
api_showbasefinfo = 'baseInfoAction/showBaseInfo'  # 获取盒子基本信息
api_boxes = 'data/boxs'  # 获取盒子列表,获取数据与getboxgroup接口类似，该接口无提交数据
# api_realdata = "/actDataAction/getFloatInfo"
api_saveplcinfo = 'plcInfoAction/savePlcInfo'  # 新建通讯口连接
api_showallplcconf = 'plcInfoAction/showAllPlcConf'  # 获取所有通讯口设置信息
api_unbundledplc = 'plcInfoAction/unbundledPlc'  # 删除指定通讯口
api_chgstrategystate = 'strategyAction/chgStrategyState' # 修改制定脚本状态：启用/停用

data_headers_common = {
    "cuid": "123456789",
    "pid": "1",
    "sv": "1.0",
    "ts": None,
    "mt": 255,
    "lan": "zh",
    # "sid": "",  # "b83c797ded6243b7a8c86c8e98a882cb"
    # "sign": None,  # "6d1e9d8e01d778c05adefe29511255a0"
}
data_headers_without_common = {
    "Host": host,
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/69.0.3497.92 '
                  'Safari/537.36',
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Connection": "keep-alive"
}
data_signin = {
    "alias": "test_fann",
    "password": "123456",
    "isremeber": 0  # 网页接口这个键是个错别字
}
data_showbaseinfo = {
    "device_id": None  # 获取指定盒子的基本信息，必须指定已存在id
}
data_saveplcinfo = {
  "check_bit": "EVEN",
  "data_length": 7,
  "comtype": 0,
  "port": "COM2",
  "retry_timeout": 0,
  "retry_times": 2,
  "wait_timeout": 300,
  "state": 1,
  "dev_model": "V-BOX+S-4G",
  "net_ipaddr": 0,
  "com_stepinterval": 0,
  "net_broadcastaddr": 0,
  "net_port": 0,
  "net_type": 0,
  "net_isbroadcast": 0,
  "box_stat_no": 0,
  "baudrate": 9600,
  "stop_bit": 1,
  "type": "Delta+Controler+PROTOCOL",
  "plc_id": 0,
  "rev_timeout": 50,
  "driver": "libDelta_Controler_PROTOCOL.so",
  "device_id": 148,
  "com_iodelaytime": 0,
  "plc_stat_no": 1
}
data_showallplcconf = {
    "device_id": 148,  # 应该从慧盒列表数据中取值，确定要操作哪个盒子
    "dev_model": "V-BOX+S-4G"
}
data_unbundledplc = {
    "plc_id": None  # 应该从showallplcconf响应数据中取值，对通讯口id
}
data_chgstrategystate = {
    "strategy_id": 864,
    "state": 1
}


def cal_md5(string):
    md5 = hashlib.md5()
    md5.update(string.encode("utf8"))
    return md5.hexdigest()
#
#
# def sort_dict(dic):
#     """
#     字典排序：Return a new sorted list from the items in iterable.
#     :param dic:
#     :return: 排序后的字典key构成的列表
#     """
#     return sorted(dic)
#
#
# def url_encode(lis, dic):
#     """
#     按照格式和lis规定的key顺序，将dic进行字符串拼接
#     :param lis:
#     :param dic:
#     :return: 拼接后字符串
#     """
#     encoded_url_without_key = "&".join(["{}={}".format(k, dic[k]) for k in lis])
#     encoded_url = encoded_url_without_key + "&" + keyvalue
#     if debug:
#         print("encoded_url:", encoded_url)
#     return encoded_url


def sign_easy(dic: dict):
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
    sign = cal_md5(encoded_url)  # 签名加密
    if debug:
        print('sign: ', sign)
    return sign


def post(api: str, business_dic: dict, sid):
    print("--------api:", api)
    print("----post data:", business_dic)
    print("----sid:", sid)
    newurl = url + api
    businessdic = business_dic.copy()  # 使用字典备份，避免原字典被污染
    commondic = data_headers_common.copy()
    commondic["ts"] = nowtime()
    if api == api_signin:
        businessdic["password"] = cal_md5(businessdic["password"])
    else:
        commondic["sid"] = sid
    mergedic = dict(list(businessdic.items()) + list(commondic.items()))
    commondic["sign"] = sign_easy(mergedic)

    headers_dict = data_headers_without_common.copy()
    headers_dict["common"] = json.dumps(commondic)

    if debug:
        print("tosigndict: {nd}\n"
              "commondict: {cpd}\n"
              "headersdict: {hds}".format(nd=mergedic, cpd=commondic, hds=headers_dict))
    print("----url: {}".format(newurl))
    r = req.post(newurl, data=businessdic, headers=headers_dict)
    js = r.json()
    print("----feedback data: {}\n".format(js))
    return js


def do_signin():
    r_signin = post(api_signin, data_signin, '')
    return r_signin


def do_get_vboxs():
    r2 = post(api_getboxgroup, {}, sid)
    with open("boxeslistresult.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(r2, ensure_ascii=False, indent=4))


def do_saveplcinfo(_sid):
    return post(api_saveplcinfo, data_saveplcinfo, _sid)


def do_showallplcconf(_sid):
    return post(api_showallplcconf, data_showallplcconf, _sid)


def do_unbundledplc(_sid):
    return post(api_unbundledplc, data_unbundledplc, _sid)


def do_chgstrategystate(_sid):
    return post(api_chgstrategystate, data_chgstrategystate, _sid)

"""
辅助性函数
"""


def text_to_dict(text: str):
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

if __name__ == '__main__':
    r1 = do_signin()
    sid = r1["result"]["sid"]
    print("sid:", sid)
    do_get_vboxs()
    i = 1
    slptime = 1
    data_chgstrategystate["strategy_id"] = 770
    while i <= 20000:
        time.sleep(slptime)
        data_chgstrategystate["state"] = 0
        off = do_chgstrategystate(sid)["code"]
        time.sleep(slptime)
        data_chgstrategystate["state"] = 1
        on = do_chgstrategystate(sid)["code"]
        print("{}, count: {}/1000, off={}, on={}".format(nowtimefmt(), i, off, on))
        i += 1

    # # 以下执行plc驱动增删改
    # do_saveplcinfo(sid)
    # allplcconf = do_showallplcconf(sid)
    # if allplcconf["code"] == 200:
    #     conf = allplcconf["result"]["infoDatas"]
    #     if len(conf) > 0:
    #         data_unbundledplc["plc_id"] = conf[-1]["plcId"]
    # time.sleep(5)
    # do_unbundledplc(sid)
    # do_showallplcconf(sid)


    # 以下：将周期性获取盒子在线状态，形成记录
    # with open("vbox_state_log.csv", 'w', encoding='gb2312') as f:
    #     f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8}\n'.format(
    #         '记录时间', '测试部882', '测试部883', '测试部884', '测试部885', '测试部886', '测试部887', '测试部888', '测试部889'))
    # i = 0
    # while i < 200:
    #     i += 1
    #     r2 = post(api_boxes_list, {}, sid)
    #     boxeslist_result = r2.json()
    #     tobe_write_down = nowtimefmt()
    #     name_state = {}
    #     if boxeslist_result["code"] != 200:
    #         tobe_write_down += '获取v-box列表失败：状态码{}\n'.format(boxeslist_result["code"])
    #     else:
    #         for box in boxeslist_result["result"]["list"][0]['boxList']:
    #             for s in ['测试部882', '测试部883', '测试部884', '测试部885',
    #                       '测试部886', '测试部887', '测试部888', '测试部889']:
    #                 if box['boxName'] == s:
    #                     name_state[s] = box['state']
    #         for c in sorted(name_state):
    #             tobe_write_down += ',{}'.format(str(name_state[c]))
    #         tobe_write_down += '\n'
    #         print(tobe_write_down)
    #     with open("vbox_state_log.csv", 'a', encoding='utf-8') as f:
    #         f.write(tobe_write_down)
    #     time.sleep(30)
