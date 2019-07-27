#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: mqtt_client
# Author:    fan
# date:      2018/7/30
# -----------------------------------------------------------
import paho.mqtt.client as mqtt
import time
import json
import threading
from watchcom import set_port, write_bit

HOST = "mqtt.v-box.net"
PORT = 1883
userdata = {"username": "wecon", "password": "wecon123$%^"}
nowtimefmt = lambda localtime : time.strftime('%Y-%m-%d %H:%M:%S', localtime)    # 格式化当前时间
nowtimestamp = lambda localtime: time.mktime(localtime)


def set_power(y: str, state: int) -> None:
    write_bit(port, y, state)


def on_connect(client, userdata, flags, rc):
    """
    客户端收到服务器响应消息（CONNACK）时的回调
    :param client: 客户端对象
    :param userdata:
    :param flags: 是一个包含代理回复的标志的字典
    :param rc: 决定了连接成功或者不成功，0：连接成功，1~5：错误类型
    :return: 作为客户端连接回调
    """
    print("Connected with result code " + str(rc))
    client.subscribe(topic)  # 将订阅放到连接回调中意味着如果连接丢失可以进行重新连接


def on_message(client, userdata, msg):
    """
    客户端从客户端收到订阅消息时的回调
    :param client: 客户端对象
    :param userdata:
    :param msg: 订阅的消息
    :return: 作为客户端收到订阅信息时的回调
    """
    global box_acts
    message_str = str(msg.payload)[2:-1]
    message = json.loads(message_str.replace(r"\t", ""))
    localtime = time.localtime()
    act = message['act']
    machine_code = message["machine_code"]
    if act == "1000":
        box_acts[machine_code] = act
    # print(box_acts)


def mqtt_go():
    client = mqtt.Client()
    client.user_data_set(userdata["username"])
    client.username_pw_set(userdata["username"], userdata["password"])
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST, PORT, 125)
    client.loop_forever()
    return client


def close_connect(mqtt_client: mqtt.Client):
    mqtt_client.disconnect()


def offline_report(machinecode):
    print("v-box with machine code[{}] is offline!".format(machinecode))

if __name__ == "__main__":
    global box_acts
    port = set_port("com12", 9600, 7, 1, "E")
    machinecodes = [
        'V020011811156605a9e4f5f659b',
        'V02001181115661a675e8634171',
        'V02001181115662a2d12c524140',
        'V020011811156635a9e4f5f58d3',
        'V02001181115664a2d12c0e20a2'
    ]
    box_powerset = dict([(m, "y" + m[14]) for m in machinecodes])
    box_acts = dict([(m, "None") for m in machinecodes])
    topic = [("pibox/cts/" + machinecode, 0) for machinecode in machinecodes]
    timeout = 60
    thread = threading._start_new_thread(mqtt_go, ())
    i, j, z = 0, 0, 0
    while i < 10000:
        i += 1
        for m in machinecodes:
            set_power(box_powerset[m], 0)
        time.sleep(timeout)
        for k, v in box_acts.items():
            # print(k, v)
            if v is None:
                print("{} V-BOX[{}] is not online in {}, act={}.".format(nowtimefmt(time.localtime()), k, timeout, v))
            if v == str(1000):
                print("{} V-BOX[{}] is online in {}, act={}.".format(nowtimefmt(time.localtime()), k, timeout, v))
                j += 1
                box_acts[k] = None
            # if v == str(1004):
            #     print("{} V-BOX[{}] is offline, act={}.".format(nowtimefmt(time.localtime()), k, timeout, v))
        print("上电联网测试，测试{}次，成功{}次".format(5*i, j))
        time.sleep(1)
        box_acts.clear()
        for m in machinecodes:
            set_power(box_powerset[m], 0)
        time.sleep(4)


