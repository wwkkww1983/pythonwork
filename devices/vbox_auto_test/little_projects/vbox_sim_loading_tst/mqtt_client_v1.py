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

HOST = "mqtt.v-box.net"
PORT = 1883
userdata = {"username": "wecon", "password": "wecon123$%^"}
nowtimefmt = lambda: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())    # 格式化当前时间
nowtimestamp = lambda: time.mktime(time.localtime())
box_acts = {}    # mqtt消息盒子机器码: act值
box_powerstate ={}    # 盒子机器码: 当前上下电状态
thetime = {"starttime": 0, "endtime": 0}

START_ADDRESS = {
    'Y0': 0x0C00,  # 物理地址
    'X0': 0x1200,  # 物理地址
    'M0': 0x0000,  # 物理地址
    'M8000': 0x0E00,  # 物理地址
    'C0_B': 0x01E0,
    'T0_B': 0x0200,
    'S0': 0x0280,
    'D0': 0x4000,
    'D8000': 0x0E00,
    'C0_W': 0x0A00,
    'C200_W': 0x0C00,
    'T0_W': 0x1000
}


def add_map(plc_add: str):
    add_tag = plc_add[0].upper()
    mdb_add = None
    if add_tag in ['Y', 'X']:
        start = START_ADDRESS[add_tag + '0']
        mdb_add = int(plc_add[1:], 8) + start
    if add_tag in ['M']:
        start = START_ADDRESS[add_tag + '0']
        mdb_add = int(plc_add[1:], 10) + start
    if add_tag == 'D':
        if int(plc_add[1:]) <= 8000:
            start = START_ADDRESS['D0']
        else:
            start = START_ADDRESS['D8000']
        mdb_add = int(plc_add[1:], 10) + start
    return mdb_add


def set_power(add_m: str, state: int) -> None:    # 设置Y为0或1
    master.write_coil(1, add_map(add_m), state)


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
    act = "0" * 4
    machine_code = "*" * 27
    try:
        message = json.loads(message_str.replace(r"\t", ""))
        act = message['act']
        machine_code = message["machine_code"]
    except Exception as e:
        print("ERROR: ", e)
    # print([(m[12:15], box_acts[m]) for m in box_acts])
    box_acts[machine_code] = act
    if act == "1000":
        box_record[machine_code]["success"] += 1
        box_record[machine_code]["constamp"] = nowtimestamp()  # 联网成功时间
        connectsecs = box_record[machine_code]["constamp"] - box_record[machine_code]["powstamp"]
        # 将当前次的连接耗时与最大连接耗时、最小连接耗时比较后正确记录
        if box_record[machine_code]["min"] == 0 or connectsecs < box_record[machine_code]["min"]:
            box_record[machine_code]["min"] = connectsecs
        if box_record[machine_code]["max"] == 0 or connectsecs > box_record[machine_code]["max"]:
            box_record[machine_code]["max"] = connectsecs
        # 计算平均值，第一次记录时原记录为0需特殊处理
        if box_record[machine_code]["aver"] == 0:
            box_record[machine_code]["aver"] = connectsecs
        else:
            aversecs = box_record[machine_code]["aver"]
            n = box_record[machine_code]["success"]
            aversecs = aversecs + (connectsecs - aversecs) / n
            box_record[machine_code]["aver"] = aversecs
        set_power(box_y[machine_code], 0)    # 机器码对应盒子下电
        box_powerstate[machine_code] = 0    # 记录下电状态
        write_json(box_record)    # 文件保存记录
        print(box_record)
        # print([(i[12:15], box_record[i]) for i in box_record])


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


def vbox_control():
    global box_powerstate
    global box_acts
    global machinecodes
    global box_record
    while True:
        # 循环运行以下程序，遍历box_powerstate，若发现盒子已下电，则进行相关处理
        time.sleep(0.2)
        # print([(m[12:15], box_powerstate[m]) for m in box_powerstate])
        for m in machinecodes:
            if box_powerstate[m] == 0:
                box_record[m]["total"] += 1  # 测试次数+1
                box_acts[m] = "None"  # act值置None
                time.sleep(2)
                set_power(box_y[m], 1)  # 上电
                box_powerstate[m] = 1  # 记录上电状态
                box_record[m]["powstamp"] = nowtimestamp()  # 上电时间
                time.sleep(0.1)


def write_json(dic: dict):
    if dic:
        with open("record.json", 'w', encoding='utf-8') as f:
            f.write(json.dumps(dic, ensure_ascii=False, indent=4))
        return True


if __name__ == "__main__":
    port = set_port("com7", 9600, 8, 1, "N")
    master = ModbusRtu(port)
    for y in ['m' + str(i) for i in range(5)]:
        set_power(y, 0)
    time.sleep(10)
    machinecodes = [
        'V020011811156605a9e4f5f659b',
        'V02001181115661a675e8634171',
        'V02001181115662a2d12c524140',
        'V020011811156635a9e4f5f58d3',
        'V02001181115664a2d12c0e20a2'
    ]
    box_y, box_acts, box_powerstate, box_record = {}, {}, {}, {}
    for m in machinecodes:
        box_y[m] = "m" + m[14]
        box_acts[m] = "None"
        box_powerstate[m] = 0
        box_record[m] = {
            "total": 0,  # 上电次数
            "success": 0,  # 连接成功测试
            "powstamp": 0,  # 上电时间戳
            "constamp": 0,  # 连接成功时间戳
            "aver": 0,  # 平均连接时长（s）
            "min": 0,  # 最短连接时长（s）
            "max": 0  # 最长连接时长（s）
        }
    # box_y = dict([(m, "y" + m[14]) for m in machinecodes])
    # box_acts = dict([(m, "None") for m in machinecodes])
    # box_powerstate = dict([(m, 0) for m in machinecodes])
    # box_record = dict([(m, {"total": 0, "success": 0, "seconds": [0, 0, 0, 0]}) for m in machinecodes])
    topic = [("pibox/cts/" + machinecode, 0) for machinecode in machinecodes]
    threads = []
    t2 = threading.Thread(target=vbox_control, args=())
    threads.append(t2)
    t1 = threading.Thread(target=mqtt_go, args=())
    threads.append(t1)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
