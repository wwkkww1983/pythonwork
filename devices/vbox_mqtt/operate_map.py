#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: operate_map
# Author:    fan
# date:      2019/3/7 007
# -----------------------------------------------------------
import json

# 模拟网页端进行数据修改操作，data字段
data_modify_monitor_value = {
    "operate_data_list": [{
        "addr_list": [{
            "addr_id": "87362",
            "value": "01010"}],
        "com": "1722"
    }]
}

data_add_monitor_point = {
    "upd_real_his_cfg_list": [{
        "cfg_list": [{
            "com": "1665",
            "digit_limit": "0,65535",
            "addr_type": 2,
            "data_limit": "0 999999",
            "his_cycle": 0,
            "float_point": -1,
            "rid": "4",
            "dir_id": 3479,
            "digit_binary": "十进制",
            "digit_count": "5,0",
            "addr_stat_no": -1,
            "data_id": 105,
            "data_type": 0,
            "name": "批量",
            "dead_set": "",
            "upd_time": "2019-03-06 20:30:35",
            "addr": "100",
            "addr_id": 104979}],
        "com": "1665"}]
}

data_del_monitor_point = {
    "del_cfg_list": [{
        "com": "1665",
        "del_type": 0,
        "cfg_id_list": [{
            "upd_time": "2019-03-06 20:29:08",
            "addr_id": 104958}]}]
}

data_add_alarm_point = {}

data_del_alarm_point = {}

data_add_history_point = {}

data_del_history_pint = {}

modify_monitor_value = {
    "act": 2000,
    "data": data_modify_monitor_value,
    "feedback": 1,
    "machine_code": "V02001180517880c2d35f9f14f6",
    "sign": ""
}

print(json.dumps(modify_monitor_value))
if __name__ == '__main__':
    pass
