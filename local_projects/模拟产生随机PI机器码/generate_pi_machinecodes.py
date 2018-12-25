#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: generate_pi_machinecodes
# Author:    fan
# date:      2018/12/5
# -----------------------------------------------------------
# java DES加解密到Python算法的坑：http://www.cnblogs.com/sammy1989/p/9814983.html

import base64
from random import randrange
import json
from pyDes import *
from Crypto.Cipher import DES    # py3无法直接安装crypto,需安装pycryptohome模块
from binascii import b2a_base64, a2b_base64


def get_random_chars(chars_lengh, chars_type):
    chars = "0123456789abcdefghigklmnopqrstuvwxyz"
    if chars_type == "letter":
        rg = (10, 36)
    elif chars_type == "number":
        rg = (0, 10)
    elif chars_type == "char":
        rg = (0, 36)
    else:
        rg = (0, 0)
        print("chars_type error.")
    ran_chars = []
    while chars_lengh:
        ran_chars.append(chars[randrange(*rg)])
        chars_lengh -= 1
    return ''.join(ran_chars)


def generate_machinecodes():
    j = 0
    machine_codes = []
    code_start = "187001161214"
    while j < 5:
        code_mid = str(j).zfill(4)    # 数字高位补零（补足位数）-> 字符串
        code_end = ''
        tem = get_random_chars(11, 'char')
        code_end = ''.join([code_end, tem])
        code = ''.join([code_start, code_mid, code_end, "\n"])
        machine_codes.append(code)
        j += 1
    return machine_codes


# def des_encrypt(d_des, k_des):
#     encrypt = DES.new(k_des, DES.MODE_CBC, k_des)
#     count = len(d_des)
#     add = DES.block_size - (count % DES.block_size)
#     d_des += ('\0' * add)
#     encrypteddata = encrypt.encrypt(d_des)
#     return encrypteddata

def des_encrypt(d_des, k_des):
    k = des(k_des[:8].encode(), ECB, pad=None, padmode=PAD_PKCS5)
    encrypt_data = k.encrypt(d_des)
    decrypt_data = k.decrypt(encrypt_data)
    print(base64.b64encode(encrypt_data))
    print(decrypt_data)

    return base64.b64encode(encrypt_data)


if __name__ == '__main__':
    # codes = generate_machinecodes()
    # print(codes)
    # with open("machinecodes.csv", "w", encoding="utf-8") as f:
    #     f.writelines(codes)
    special_code = "187201509180001e1c767f4fb69"
    data_dict = {
        "function": 45057,
        "msgDetail": {
            "machineCode": special_code,
            "userPwd": "888888",
            "upnpport": -1,
            "devModel": "PI8070",
            "imageList": "SysSet_V1.5.26-P:A8 2018-03-14,"
                         "HMIUI_V1.0.0,Remote_V3.2.6-P:A8 2018-02-08,"
                         "HMITerm_V1.0.0,web_V4.0.28-P:A8 2018-07-03,"
                         "HMImonitor_V3.0.81-P:A8 2018-08-07,"
                         "update_V1.0.25-P:A8 2017-12-20,"
                         "fseMMC_V1.0.23-P:A8 2018-07-07,"
                         "Project_V4.2.81 ??汾-P:A8",
            "lcd": "800,480",
            "delay": "-1",
            "status": "0",
            "connType": "-1",
            "isRecodrLog": "0",
            "note": {"key": "value", "key2": "value2"},
            "upnpIp": "192.168.41.222"
        }
    }    # 待加密字典,机器码（special_code为变量）
    data = json.dumps(data_dict, sort_keys=True)   # 数值json化，需要按key排序
    key = "@^_^123aBcZ*"
    key = "@^_^123a"
    desed_data = des_encrypt(data, key)
    # print(desed_data.decode('unicode_escape'))
    print(special_code)
    # print(desed_data)
