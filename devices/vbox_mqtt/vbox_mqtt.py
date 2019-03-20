#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: vbox_mqtt
# Author:    fan
# date:      2019/3/5 005
# -----------------------------------------------------------
import paho.mqtt.client as mqtt
import time
import json
import threading
import random
import gzip
from modbus_rtu_master import ModbusRtu

nowtimefmt = lambda: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 格式化当前时间
nowtimestamp = lambda: time.mktime(time.localtime())
ACT_MEANING = {  # 盒子端发布消息含义，1004为服务器发出的遗言消息
    "1000": "getonline",
    "1001": "renewpoint",
    "1002": "datarecord",
    "1003": "alarm",
    "1004": "getoffline",
    1: "feedsuccess"

}


class MqttClient(object):
    def __init__(self, host, port, keepalive, userdata, **parameters):
        self.host = host
        self.port = port
        self.keepalive = keepalive
        self.userdata = userdata
        self.params = parameters
        self.client = mqtt.Client()
        self.sub_topic = None
        self.pub_topic = None
        self.message_str = None
        self.temp = None
        self.actcount = {
            "1000": 0,
            "1001": 0,
            "1002": 0,
            "1003": 0,
            "1004": 0,
            1: 0
        }

    def onconnect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.client.subscribe(self.sub_topic)  # 将订阅放到连接回调中意味着如果连接丢失可以进行重新连接

    def onmessage(self, client, userdata, msg):
        # self.tst_sub_message(msg)
        # print("msg.payload: ", msg.payload)
        message_str = ""
        if msg.payload[:1] == b"{":
            message_str = msg.payload.decode()
            # print("message_str无需解压: ", message_str)
        else:
            try:
                message_str = gzip.decompress(msg.payload)[:-1].decode()  # 新版本增加数据接收解压操作,解压后语调末尾1字节
                # print("message_str已解压: ", message_str)
            except Exception as e:
                print("gzip decompressed error: {}, {}".format(message_str, e))
        act = None
        try:
            message_str = json.loads(message_str.replace(r"\t", ""))
            act = message_str['act']
        except Exception as e:
            print("json loads error: {}, {}".format(message_str, e))
        if act not in ["1000", "1002", "1004"]:  # 处理上线、在线、下线的消息
            pass
            # self.parse_sub_message(act, message_str)
        else:
            self.log_online_state(act, message_str)

    def connect(self):
        self.client.user_data_set(self.userdata["username"])
        self.client.username_pw_set(self.userdata["username"], self.userdata["password"])  # 设置mqtt用户信息
        self.client.connect(self.host, self.port, self.keepalive)

    def disconnect(self):
        print("Disconnected.")
        self.client.disconnect()

    def publish(self, topic, msg):
        self.client.publish(topic, msg)

    def subscribe(self, topic):
        self.sub_topic = topic
        self.client.on_connect = self.onconnect
        self.client.on_message = self.onmessage

    def tst_sub_message(self, message):
        print(message.payload)
        # if message.payload[0] == b"{":
        #     print(str(message.payload))
        # else:
        #     print(gzip.decompress(message.payload))

    def mqtt_go(self):
        self.client.loop_forever()

    def modify_monitor_value(self, **params2):
        topic = "pibox/stc/" + params2["machine_code"]
        # print(params2)
        addr_list = [str(a) for a in params2["addr_list"]]
        value_list = [str(v) for v in params2["value_list"]]
        if len(value_list) == 0:
            value_list = [str(random.randint(0, 32767))] * len(addr_list)
        addr_value_map_list = [{"addr_id": str(addr), "value": value} for addr, value in zip(addr_list, value_list)]
        # print(addr_value_map_list)
        data_modify_monitor_value = {
            "operate_data_list": [{
                "addr_list": addr_value_map_list,
                "com": str(params2["com"])
            }]
        }
        modify_monitor_value = {
            "act": 2000,
            "data": data_modify_monitor_value,
            "feedback": 1,
            "machine_code": params2["machine_code"],
            "sign": ""
        }
        pub_message = json.dumps(modify_monitor_value)
        print(topic, pub_message)
        self.publish(topic, pub_message)

    def parse_sub_message(self, act, message):
        results = {}
        machine_code = "*" * 27
        nowtime = nowtimefmt()
        addrlist = []
        if act == 1:  # act=1 的1属于int类型
            results["type"] = str(message["feedback_act"]) + ": feedback==ok"
            self.actcount["1"] += 1
        if act == "1000":
            results["type"] = "上线"
        if act == "1001":
            results["type"] = "监控"
            self.actcount["1001"] += 1
            addr_list = message["data"]["act_time_data_list"][0]["addr_list"]
            for addr in addr_list:
                if addr["state"] == "1":
                    addrlist.append(addr["addr_id"])
            # results["addrlist_len"] = len(addrlist)  # 实时监控点地址长度
            results["addrlist"] = addrlist
        if act == "1002":
            results["type"] = "记录"
        if act == "1003":
            results["type"] = "报警"
        if act == "1004":
            results["type"] = "下线"''
        results["act"] = message['act']
        results["machine_code"] = message["machine_code"]
        results["count"] = self.actcount
        results_list = ["{}={}".format(key, results[key]) for key in sorted(results)]
        results_str = ", ".join(results_list)
        print(results_str)

    @staticmethod
    def log_online_state(act, message):
        # act in ["1000","1002","1004"]
        logtime = nowtimefmt()
        logtimestamp = nowtimestamp()
        machine_code = message["machine_code"]
        client_id = message["client_id"]
        line = dic[machine_code]  # 先将dic赋值给临时变量（处理完后反向赋值，精简代码）

        if act == "1000":
            if line["count1000"] + line["count1002"] != 0:  # 不是第一次在线,先计算离线时间，再记录上线时间
                if client_id != line["client_id"]:  # 重连时client id会变更,计算上次离线时间
                    line["client_id"] = client_id
                    line["keep_offline"] = logtimestamp - line["get_offline"]
                    line["count1000"] += 1
                    line["warning"] = "上线"
                else:
                    line["warning"] = "服务器未响应重试"
            else:  # 第一次记录到上线，记录client id, 初始化上线时间、下线时间
                line["client_id"] = client_id
                line["get_offline"] = logtimestamp
                line["count1000"] = 1
                line["warning"] = "第一条上线消息"
            line["get_online"] = logtimestamp  # 做完相关判断和记录后，更新上线时间

        elif act == "1002":
            if line["count1002"] + line["count1000"] != 0:  # 常规数据记录不需要更新client id
                line["count1002"] += 1
                line["warning"] = "--"
            else:
                line["client_id"] = client_id
                line["get_offline"] = logtimestamp
                line["get_online"] = logtimestamp
                line["count1002"] = 1
                line["warning"] = "第一条数据记录消息"

        elif act == "1004":
            if line["count1002"] + line["count1000"] != 0:
                if client_id == line["client_id"]:
                    line["keep_online"] = logtimestamp - line["get_online"]
                    line["count1004"] += 1
                    line["warning"] = "下线"
                else:
                    line["count1004"] += 1
                    line["warning"] = "下线记录client id匹配异常"
            else:  # 第一条即记录到下线消息
                line["client_id"] = client_id
                line["get_online"] = logtimestamp
                line["count1004"] = 1
                line["warning"] = "记录开始时已下线"
            line["get_offline"] = logtimestamp  # 做完相关判断和记录后，更新上线时间

        else:
            pass

        line["act"] = act
        line["meaning"] = ACT_MEANING[act]
        # line["client_id"] = client_id
        line["time"] = logtime
        line["timestamp"] = logtimestamp
        line["machinecode"] = machine_code[12:15]
        logfilename = "{}.csv".format(machine_code)
        logline = ",".join([str(line[key]) for key in line_k])

        if act == "1002":  # 数据记录太多，限制log次数
            # if line["count1002"] % 100 != 1:
            #     print(logline)
            # else:
            #     write_line_to_csv(logfilename, logline)
            print(logline)
        else:
            write_line_to_csv(logfilename, logline)
        dic[machine_code] = line  # 反向赋值，更新dic


def publish():
    client.subscribe(topic)
    pub_params = {"machine_code": "V02001180517880c2d35f9f14f6",
                  "com": 1722,  # 通过mqtt工具获取通讯口id（int）填入此处
                  "addr_list": [87362, 87361, 87360],  # 通过网页获取监控点编号填入此处
                  "value_list": []  # 可不填写
                  }

    # 可以模拟单个、离散、连续等方式地址写入
    v = 1
    a = 1
    while True:
        time.sleep(0.1)
        pub_params["value_list"] = [v] * len(pub_params["addr_list"])
        v += 1
        if v == 32767:
            a += 1
            print("测试次数达到：{}".format(a * v))
            v = 1
        client.modify_monitor_value(**pub_params)


def write_line_to_csv(filename: str, line: str, writetype="a"):
    print(line)
    with open(filename, writetype) as f:
        f.write(line + "\n")


def write_record_to_csv():
    while True:
        lines = json.dumps(dic)
        write_line_to_csv("record.csv", lines, "w")


def power_and_net_control():
    count_linked, count_broken = 0, 0
    randint = random.randint
    port_property = ("com9", 9600, 8, 1, "N")
    plc = ModbusRtu(port_property)
    plc.write_coil(1, 0xfc00, 1)
    count_linked += 1
    # write_line_to_csv("control.csv", "Ethernet linked", "a")
    con_line = "{}, {}, {}, {}, {}, {}".format(nowtimefmt(), "linked", 1, 0, "--", 0)
    write_line_to_csv("control.csv", con_line)
    while True:
        linked_time = randint(5, 50)
        time.sleep(linked_time)
        plc.write_coil(1, 0xfc00, 0)
        count_broken += 1
        con_line = "{}, {}, {}, {}, {}, {}".format(
            nowtimefmt(),
            "broken",
            count_linked,
            count_broken,
            linked_time,
            "--")
        write_line_to_csv("control.csv", con_line)
        broken_time = randint(5, 60 * 2)
        time.sleep(broken_time)
        plc.write_coil(1, 0xfc00, 1)
        count_linked += 1
        con_line = "{}, {}, {}, {}, {}, {}".format(
            nowtimefmt(),
            "linked",
            count_linked,
            count_broken,
            "--",
            broken_time)
        write_line_to_csv("Ethernet.csv", con_line)  # 网线通断
        # write_line_to_csv("Ethernet-power.csv", con_line)  # 网线模式电源通断
        # write_line_to_csv("Wifi.csv", con_line)  # Wifi（信号）通断
        # write_line_to_csv("Wifi-power.csv", con_line)  # Wifi模式电源通断
        # write_line_to_csv("G4.csv", con_line)  # 4G（信号）通断
        # write_line_to_csv("G4-power.csv", con_line)  # 4G模式电源通断


def loopall():
    threads = []
    t4 = threading.Thread(target=power_and_net_control, args=())
    threads.append(t4)
    # t3 = threading.Thread(target=write_record_to_csv, args=())
    # threads.append(t3)
    # t2 = threading.Thread(target=publish, args=())
    # threads.append(t2)
    t1 = threading.Thread(target=client.mqtt_go, args=())
    threads.append(t1)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()


if __name__ == '__main__':

    # 设置要测试的机器码，印度，波兰，泰国
    vbox_india = [
        "V0200118051788206bc83233386",
        "V020011811156635a9e4f5f58d3",
        "V02001181115661a675e8634171",
        "V020011811156605a9e4f5f659b",
        "V02001181115662a2d12c524140",
        "V02001181115664a2d12c0e20a2",
        # "V02001180517880c2d35f9f14f6"
    ]
    vbox_poland = []
    vbox_thailand = []
    vbox = vbox_india + vbox_poland + vbox_thailand
    topic = []
    dic = dict()
    line = dict()
    line_k = ["time", "timestamp", "client_id", "act", "meaning",
              "count1000", "count1004", "count1002", "get_online", "get_offline",
              "keep_online", "keep_offline", "warning", "machinecode"]
    line_v = ["", 0.0, "", "", "",
              0, 0, 0, 0.0, 0.0,
              0, 0, "", ""]
    if len(line_k) == len(line_v):
        for k, v in zip(line_k, line_v):
            line[k] = v
    for machinecode in vbox:
        line0 = "{}\n开始测试时间:{}\n".format(machinecode, nowtimefmt())
        line1 = ",".join(line_k)
        filename = machinecode + ".csv"
        write_line_to_csv(filename, line0 + line1, "w")
        dic[machinecode] = line.copy()  # 要使用不同的字典否则数据是重叠的 |非常重要|

        # 生成订阅主题，QoS等级均为0
        topic.append(("pibox/cts/" + machinecode, 0))

    # 创建电源和网络控制日志
    con_lin0 = "全部慧盒都有,开始测试时间:{}\n".format(nowtimefmt())
    con_lin1 = "time, operation, linkedcount, brokencount linkedtime, brokentime"
    write_line_to_csv("control.csv", con_lin0 + con_lin1, "w")

    # 设置账户并连接主机
    host, port, keepalive, userdata = "192.168.45.190", 1883, 125, {"username": "admin", "password": "password"}
    parse_params = dict()  # 参数设计：停止条件（消息计数、计时、特殊条件）
    client = MqttClient(host, port, keepalive, userdata, **parse_params)
    client.connect()
    client.subscribe(topic)
    print(topic)
    # 开始轮询
    loopall()
