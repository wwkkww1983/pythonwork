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
    # print(message_str)
    act = "0" * 4
    machine_code = "*" * 27
    message = ""
    try:
        message = json.loads(message_str.replace(r"\t", ""))
        act = message['act']
        machine_code = message["machine_code"]
    except Exception as e:
        print("ERROR: ", e)
    # print([(m[12:15], box_acts[m]) for m in box_acts])
    box_acts[machine_code] = act
    nowtime = nowtimefmt()
    if act == "1002":
        box_record[machine_code]["datarecord"] += 1
        box_record[machine_code]["lastrecordtamp"] = nowtimestamp()
        box_record[machine_code]["lastrecordtime"] = nowtime  # 联网成功时间
        print("{} 记录次数{} = {}".format(
            box_record[machine_code]["lastrecordtime"],
            machine_code[12:15],
            box_record[machine_code]["datarecord"]
        ))
    if act == "1004":
        box_record[machine_code]["lastofflinetime"] = nowtime
        box_record[machine_code]["offlinecount"] += 1
        with open(machine_code + '.csv', 'a', encoding='utf-8') as f:
            f.write("{}, offline\n".format(nowtime))
    # if act == "1000":
    #     box_record[machine_code]["lastonlinetime"] = nowtime
    #     box_record[machine_code]["onlinecount"] += 1
    #     with open(machine_code + '.csv', 'a', encoding='utf-8') as f:
    #         f.write("{}, online\n".format(nowtime))
    if act == 1:
        # print(message)
        if message["msg"] == "success":
            box_record[machine_code]["lastonlinetime"] = nowtime
            box_record[machine_code]["onlinecount"] += 1
            with open(machine_code + '.csv', 'a', encoding='utf-8') as f:
                f.write("{}, online\n".format(nowtime))


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


def clock():
    global box_powerstate
    global box_acts
    global machinecodes
    global box_record
    i = 0
    while True:
        # 循环运行以下程序，检查盒子消息间隔，若发现盒子持续未收到消息则发出报警，否则继续运行
        time.sleep(5)
        for code in machinecodes:
            nowtime = nowtimefmt()
            record_timeout = nowtimestamp() - box_record[code]["lastrecordtamp"]
            if record_timeout >= 60 * 5:  # 判断如果距离上次记录时间超过了5分钟,则进行记录并发出警报
                print(nowtime, code, "v-box had been offline beyond 5 minutes！")
                box_record[code]["异常离线标识"] = 1
                with open(code + '.csv', 'a', encoding='utf-8') as f:
                    f.write("{}, un_normal offline.\n".format(nowtime, code))
            else:
                continue
        i += 1
        if i >= 100:
            # print(nowtimefmt(), box_record)
            write_json(box_record)
            i = 0


def write_json(dic: dict):
    if dic:
        with open("record.json", 'w', encoding='utf-8') as f:
            f.write(json.dumps(dic, ensure_ascii=False, indent=4))
        return True


if __name__ == "__main__":
    machinecodes = [
        # 'V020011811156605a9e4f5f659b',
        # 'V02001181115661a675e8634171',
        'V02001181115662a2d12c524140',
        # 'V020011811156635a9e4f5f58d3',
        'V02001181115664a2d12c0e20a2'
    ]
    box_y, box_acts, box_powerstate, box_record = {}, {}, {}, {}
    now = nowtimefmt()
    for m in machinecodes:
        box_y[m] = "m" + m[14]
        box_acts[m] = "None"
        box_powerstate[m] = 0
        box_record[m] = {
            "starttime": now,  # 开始测试时间
            "datarecord": 0,  # 数据记录次数
            "lastrecordtime": nowtimefmt(),  # 最后一次记录时间（收到1002）
            "lastrecordtamp": nowtimestamp(),  # 最后一次记录时间戳（计算用）
            "lastonlinetime": "",  # 盒子最后一次上线时间（收到1000）
            "lastofflinetime": "",  # 盒子最后一次下线时间（收到1004）
            "onlinecount": 0,  # 盒子上线次数（收到1000）
            "offlinecount": 0,  # 盒子下线次数（收到1004）
            "异常离线标识": 0
        }

    for i in machinecodes:    # 增加单台盒子的上下电及联网记录
        with open(i + '.csv', 'w', encoding='utf-8') as f:
            f.write('machinecode={}, starttime: {}\n'.format(i, now))

    topic1 = [("pibox/cts/" + machinecode, 0) for machinecode in machinecodes]
    topic2 = [("pibox/stc/" + machinecode, 0) for machinecode in machinecodes]
    topic = topic1 + topic2
    threads = []
    t2 = threading.Thread(target=clock, args=())
    threads.append(t2)
    t1 = threading.Thread(target=mqtt_go, args=())
    threads.append(t1)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
