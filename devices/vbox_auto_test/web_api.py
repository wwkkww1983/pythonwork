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

server_addr_test = "http://192.168.45.186:8686/box-data/api/{acturl}"
server_addr_normal = "http://api.v-box.net/box-data/api/{acturl}"
global_parameter = {"sid": "",     # sessionid 会话ID，登录时必传
                    "comid": "1",     # 公司ID
                    "compytkey": "27a010966282423fbd202bf3f45267c0",     # 公司私有key
                    "ts": "",     # 时间戳
                    "sign": ""    # 签名，包含MD5校验值
                    }
nowtime = lambda: int(round(time.time()*1000))    # 当前时间戳单位ms


def cal_sign_md5(sign_string):
    m = hashlib.md5()
    m.update(sign_string)
    return m.hexdigest()


if __name__ == '__main__':
    pass
