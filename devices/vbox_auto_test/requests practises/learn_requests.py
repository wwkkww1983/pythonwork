#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: learn_requests
# Author:    fan
# date:      2018/5/19
# -----------------------------------------------------------
import requests
import json

if __name__ == '__main__':
    # r1 = requests.get('https://github.com/timeline.json')
    # r2 = requests.post("http://httpbin.org/post")
    # r3 = requests.put("http://httpbin.org/put")
    # r4 = requests.delete("http://httpbin.org/delete")
    # r5 = requests.head("http://httpbin.org/get")
    # r6 = requests.options("http://httpbin.org/get")
    # paradic = {"key1": "value1", "key2": "value2", "key3": "value3"}
    # r7 = requests.get("http://httpbin.org/get", params=paradic)
    #
    # for r in [r1, r2, r3, r4, r5, r6, r7]:
    #     print("\n", r.url)
    #
    # print(r1.encoding)

    # url = "https://api.github.com/some/endpoint"
    # payload = {"some": "data"}
    # headers = {"content-type": "application/json"}
    # r8 = requests.post(url, data=json.dumps(payload), headers=headers, timeout=10)
    # for key, value in r8.headers.items():
    #     print(key, ' = ', value)
    # print("\n", r8.headers["server"])

    url = "http://p.3.cn/prices/mgets?"
    para = {"skuIds": "J_19766392901", "type": "1"}
    r9 = requests.get(url, params=para)
    print(r9.url)

