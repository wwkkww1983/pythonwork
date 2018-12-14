#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: generate_pi_machinecodes
# Author:    fan
# date:      2018/12/5
# -----------------------------------------------------------
from random import randrange
import json
import pyDes

code1 = "1870011605040035dd4dc83e9bf"
codel = []
nums = "0123456789"
chars = "0123456789abcdefghigklmnopqrstuvwxyz"
# nums_list = [i for i in nums]
# chars_list = [i for i in chars]
get_num = lambda: nums[randrange(0, 10)]
get_char = lambda: chars[randrange(0, len(chars))]
j = 0
code_end = ''
machine_codes = []
code_start = "187001161214"
while j < 10000:
    code_mid = str(j).zfill(4)    # 数字高位补零（补足位数）-> 字符串
    code_end = ''
    k = 0
    while k < 11:
        tem = get_char()
        code_end = ''.join([code_end, tem])
        k += 1
    code = ''.join([code_start, code_mid, code_end, "\n"])
    machine_codes.append(code)
    j += 1
with open("machinecodes.csv", "w", encoding="utf-8") as f:
    f.writelines(machine_codes)

# data_dict = {
#     "function": 45057,
#     "msgDetail": {
#         "machineCode": "1870011605040035dd4dc83e9bf",
#         "userPwd": "888888",
#         "upnpport": -1,
#         "devModel": "PI8070",
#         "imageList": "SysSet_V1.5.26-P:A8 2018-03-14,"
#                      "HMIUI_V1.0.0,Remote_V3.2.6-P:A8 2018-02-08,"
#                      "HMITerm_V1.0.0,web_V4.0.28-P:A8 2018-07-03,"
#                      "HMImonitor_V3.0.81-P:A8 2018-08-07,"
#                      "update_V1.0.25-P:A8 2017-12-20,"
#                      "fseMMC_V1.0.23-P:A8 2018-07-07,"
#                      "Project_V4.2.81 ??汾-P:A8",
#         "lcd": "800,480",
#         "delay": "-1",
#         "status": "0",
#         "connType": "-1",
#         "isRecodrLog": "0",
#         "note": {"key": "value", "key2": "value2"},
#         "upnpIp": "192.168.41.222"
#     }
# }
# data_des = json.dumps(data_dict, sort_keys=True)    # 数值json化，需要按key排序
# key_des = "@^_^123aBcZ*"
# key_des = "@^_^123a"
#
# def desencryptdata(data):
#     k = pyDes.des(key_des)
#     encrypteddata = k.encrypt(data.encode())
#     return encrypteddata

if __name__ == '__main__':
    print(machine_codes)

