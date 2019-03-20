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
from modbus_rtu_master import ModbusRtu

# HOST = "mqtt.v-box.net"
HOST = "192.168.45.190"
PORT = 1883
# userdata = {"username": "wecon", "password": "wecon123$%^"}
userdata = {"username": "admin", "password": "password"}
nowtimefmt = lambda: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())    # 格式化当前时间
nowtimestamp = lambda: time.mktime(time.localtime())
box_acts = {}    # mqtt消息盒子机器码: act值
box_powerstate ={}    # 盒子机器码: 当前上下电状态
thetime = {"starttime": 0, "endtime": 0}


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
    global box_powerstate
    global box_record
    message_str = str(msg.payload)[2:-1]
    print(message_str)


def mqtt_go():
    client = mqtt.Client()  # 创建mqtt client对象
    client.user_data_set(userdata["username"])
    client.username_pw_set(userdata["username"], userdata["password"])  # 设置mqtt用户信息
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST, PORT, 125)  # 设置连接超时，连接
    client.loop_forever()  # client执行循环程序
    return client


def close_connect(mqtt_client: mqtt.Client):
    mqtt_client.disconnect()


if __name__ == "__main__":
    topic = "pibox/cts/V02001180517880c2d35f9f14f6"
    mqtt_go()

