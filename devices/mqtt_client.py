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

HOST = "mqtt.v-box.net"
PORT = 1883

topic = "pibox/cts/V020011805178896a933a47b0b8"
userdata = {"username": "wecon", "password": "wecon123$%^"}
global cts_message
nowtimefmt = lambda localtime : time.strftime('%Y-%m-%d %H:%M:%S', localtime)    # 格式化当前时间
nowtimestamp = lambda localtime: time.mktime(localtime)


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
    message_str = msg.topic + " " + str(msg.payload)
    # message_str = message_str.replace(r"\t", "")
    # message = json.loads(message_str)
    # localtime = time.localtime()
    # mess = "{}, {}, {}, {}".format(nowtimefmt(localtime), msg.topic, message["act"], message['machine_code'])
    # mess = message['act']
    # print(nowtimefmt(), client, userdata, message)
    print(message_str)

def mqtt_go():
    client = mqtt.Client()
    client.user_data_set(userdata["username"])
    client.username_pw_set(userdata["username"], userdata["password"])
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST, PORT, 125)
    client.loop_forever()


if __name__ == "__main__":
    mqtt_go()

    # while True:
    #     try:
    #         client.loop_forever()
    #     except:
    #         pass
    #         # exit()

