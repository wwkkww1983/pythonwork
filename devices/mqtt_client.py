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
client = mqtt.Client()
topic = "pibox/cts/V0200118051788806bc8325b1fa"
userdata = {"username": "wecon", "password": "wecon123$%^"}
global cts_message
nowtimefmt = lambda: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())    # 格式化当前时间


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)


def on_message(client, userdata, msg):

    message_str = ' ' + str(msg.payload)[2:-1]
    message = json.loads(message_str)
    mess = "{}, {}, {}".format(msg.topic, nowtimefmt(), message["act"])
    print(mess)

client.user_data_set(userdata["username"])
client.username_pw_set(userdata["username"], userdata["password"])
client.on_connect = on_connect
client.on_message = on_message
client.connect(HOST, PORT, 60)
try:
    client.loop_forever()
except:
    exit()


if __name__ == "__main__":
    pass

