#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: vbox_mqtt
# Author:    fan
# date:      2019/3/5 005
# -----------------------------------------------------------
import paho.mqtt.client as mqtt
import json
import threading
import random
import gzip
from make_time_formated import *
from zipfile import zlib

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
        self.g2_data_list = []
        self.g2_start_bag_exists = False
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
        self.client.on_message = self.tst_sub_message

    def tst_sub_message(self, client, userdata, msg):

        if msg.payload[:1] == b"{":  # 必须用切片才能取到长度为1的字节串，用单个索引方式只能得到该字节对应的10进制值
            print(str(msg.payload))
        elif msg.payload[:2] == b'\x7f~':
            bag = msg.payload
            # print("包开头{}, 包版本{}, 数据长度{}, 包标识{}, CRC32校验{}, 报结尾{}".format(
            #    bag[:2], bag[2:3], bag[3:7], bag[7:8], bag[-6:-2], bag[-2:]))
            data = bag[7:-6]
            bag_flag = data[:1]
            if bag_flag == b'\x00':
                print('{} 开始包_{}'.format(nowtimestr(), data))
                self.g2_data_list = []  # 创建列表，准备按顺序存放从数据包内取出的压缩数据
                self.g2_start_bag_exists = True
            elif bag_flag == b'\x01':
                print('{} 数据包_{}'.format(nowtimestr(), data))
                real_data_len = data[1:3]
                bag_num = data[3:4]
                real_data = data[5:]  # 前5个字节：包标识0、本包有效数据长度12、包序号34
                if self.g2_start_bag_exists:
                    self.g2_data_list.append(real_data)
            elif bag_flag == b'\x02':
                print('{} 结束包_{}'.format(nowtimestr(), data))
                if self.g2_data_list:
                    zipped_data = b''.join(self.g2_data_list)[4:]  # 头4个字节为解压后长度，要截掉
                    msgs = []
                    try:
                        unzipobj = zlib.decompressobj()
                        unzipped_data = unzipobj.decompress(zipped_data)
                        print("{} 解压后数据_{}".format(nowtimestr(), unzipped_data))
                        unzipped_data_str = unzipped_data.decode()
                        msgs = json.loads(unzipped_data_str)  # 结构[{}] 或者[{}, {}, ...]
                    except Exception as e:
                        print('faile to unzip zipped_data{}'.format(zipped_data), '\ndetail: {}'.format(e))
                    for item in msgs:
                        print("act=={}".format(item["act"]), json.dumps(item))
                    self.g2_data_list = []  # 清空包存放列表，标识清除，准备下一轮解析过程
                    self.g2_start_bag_exists = False
        else:
            pass

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
        machine_code = None
        client_id = None
        try:
            machine_code = message["machine_code"]
            client_id = message["client_id"]
        except Exception as e:
            print("message key error: {}. message info: {}".format(e, message))
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
        line["machinecode"] = machine_code[-4:]
        logfilename = "{}.csv".format(machine_code)
        logline = ",".join([str(line[key]) for key in line_k])

        if act == "1002":  # 数据记录太多，限制log次数
            # if line["count1002"] % 100 != 1:
            #     print(logline)
            # else:
            #     write_line_to_csv(logfilename, logline)
            if line["warning"] != "第一条数据记录消息":
                print(logline)
            else:
                write_line_to_csv(logfilename, logline)
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


def loopall():
    threads = []
    # t4 = threading.Thread(target=power_and_net_control, args=())
    # threads.append(t4)
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
    # 2G 数据包队列
    l = [
        b'{"act":"1004","client_id":"T20190509101337JQ","machine_code":"V060011102249945e30117c71b8","data":{"machine_code":"V060011102249945e30117c71b8"},"feedback":"0"}',
        b'\x7f~\x00\x00\x00\x00\x08\x00\x00\x00\x00\x01\x08\x00\x02G\x8a\t\xfaU\xaa',
        b"\x7f~\x00\x00\x00\x01\x05\x01\x01\x00\x00\x00\x00\x00\x01\x86x\x9c\x95OMK\x031\x10\xfd+\x92s\xbbL\xb2\x9f\xe9Q\x10\xedAz)E\x10\t\xd9\xec\xac\x06\x9b\xec\x92\xc4\x15)\xfb\xdf\x9dh\xfd\x01\xe60\xbc7\xf3\xde\x9b\xc9\xf3\x85i\x93\xd8\x8eq\x00`\x1bf\xce\x16}Rv\xa0\xd6Q\x00\x97P\x83\xe4\xc0+\xc1\x0f{\x9a;m\xde\xacGe\xa6\x01Ir\x82\x06\x80s\x0eBTRV5\x96\xc4Z\xd3\xf2\xbe#\xf1\xa0\x93f\xbb\x0b\x1bp\xb1\x06\x95\xf5\xe3\x94\xe9\xbf2f\x1d\xe3\xe7\x14\xf2=\xdd\xcf\xcb\xb9\xb8(G\xe6svoo\x0fO7w[qO\x83\x98t\xca\x91\x9c\xb0\xc7\xa4\xd2\xd7\xfcG\xc7\x0fo\x08\x96l\xfd\xf5\x8f6\xb8|\xcc\xa8\xbcvYD1G\x0cn\xf3\xf0\xb8w\x93\xb7i\n\xd9\xa5\x16\x0cy\x0b/DQ6\x9bSY\x10\x12l\xa5\x94\x11q\xe8\xb5y\xbf.\xb0\x91>\xe4\xe6\x801^;\xd1\xbez\x82}\xd37e\xa7\x9b\xb2\xd2 \xa9t\xdc@=B+u'@c\xf4\x12\xdd\xdbU\xaa",
        b'\x7f~\x00\x00\x00\x00\r\x01\x00\x08\x00\x01\xcd\xd6\x97o\x9b\xb6n\x86\xf1i})U\xaa',
        b'\x7f~\x00\x00\x00\x00\x01\x02[\x10\xa7NU\xaa',
        b'\x7f~\x00\x00\x00\x00\x08\x00\x00\x00\x00\x01\x08\x00\x02G\x8a\t\xfaU\xaa',
        b"\x7f~\x00\x00\x00\x01\x05\x01\x01\x00\x00\x00\x00\x00\x01\x86x\x9c\x95OMK\x031\x10\xfd+\x92s\xbbL\xb2\x9f\xe9Q\x10\xedAz)E\x10\t\xd9\xec\xac\x06\x9b\xec\x92\xc4\x15)\xfb\xdf\x9dh\xfd\x01\xe60\xbc7\xf3\xde\x9b\xc9\xf3\x85i\x93\xd8\x8eq\x00`\x1bf\xce\x16}Rv\xa0\xd6Q\x00\x97P\x83\xe4\xc0+\xc1\x0f{\x9a;m\xde\xacGe\xa6\x01Ir\x82\x06\x80s\x0eBTRV5\x96\xc4Z\xd3\xf2\xbe#\xf1\xa0\x93f\xbb\x0b\x1bp\xb1\x06\x95\xf5\xe3\x94\xe9\xbf2f\x1d\xe3\xe7\x14\xf2=\xdd\xcf\xcb\xb9\xb8(G\xe6svoo\x0fO7w[qO\x83\x98t\xca\x91\x9c\xb0\xc7\xa4\xd2\xd7\xfcG\xc7\x0fo\x08\x96l\xfd\xf5\x8f6\xb8|\xcc\xa8\xbcvYD1G\x0cn\xf3\xf0\xb8w\x93\xb7i\n\xd9\xa5\x16\x0cy\x0b/DQ6\x9bSY\x10\x12l\xa5\x94\x11q\xe8\xb5y\xbf.\xb0\x91>\xe4\xe6\x801^;\xd1\xbez\x82}\xd37e\xa7\x9b\xb2\xd2 \xa9t\xdc@=B+u'@c\xf4\x12\xdd\xdbU\xaa",
        b'\x7f~\x00\x00\x00\x00\r\x01\x00\x08\x00\x01\xcd\xd6\x97o\x9b\xb6n\x86\xf1i})U\xaa',
        b'\x7f~\x00\x00\x00\x00\x01\x02[\x10\xa7NU\xaa',
        b'\x7f~\x00\x00\x00\x00\x08\x00\x00\x00\x00\x01\x08\x00\x02G\x8a\t\xfaU\xaa',
        b"\x7f~\x00\x00\x00\x01\x05\x01\x01\x00\x00\x00\x00\x00\x01\x86x\x9c\x95O\xcbJ\x041\x10\xfc\x15\xc9yw\xe8d\x9e\xd9\xa3 >P\xbc,\x8b \x122\x99\x1e\rn2C\x12Gd\x99\x7f\xb7\xa3\xeb\x07\x98CS\xd5]U\xddy>1m\x12\xdb1\x0e\x00l\xc3\xcc\xd1\xa2O\xca\x0e\xd4\xda\x0b\xe0\x12j\x90\x1cx\r\xe2\xfe\x8e\xe6N\x9b7\xebQ\x99i@\x92\x1c\xa0\x01\xe0\x9c\x83\x10\x95\x94U\x8d%\xb1\xd6\xb4\xbc\xefH<\xe8\xa4\xd9\xee\xc4\x06\\\xacAe\xfd8e\xfa\xaf\x8cY\xc7\xf89\x85|O\xf7\xf3r..\xca\x91\xf9\x98\xdd\xdb\xcb\xc7\xa7\x8b\xab\xad\xb8\xa6AL:\xe5HN\xd8cR\xe9k\xfe\xa3\xe3\x877\x04K\xb6\xfe\xfaG\x1b\\>fT^\xbb,\xa2\x98=\x06\xb7\xb9y\xb8u\x93\xb7i\n\xd9\xa5\x16\x0cy\x0b/DQ6\x9bCY\x10\x12l\xa5\x94\x11q\xe8\xb5y?/\xb0\x91>\xe4\xe6\x801\x9e;\xd1\xbez\x82}\xd37e\xa7\x9b\xb2\xd2 \xa9t\xdc@=B+u'@c\x9b\xd3\xc0,U\xaa",
        b'\x7f~\x00\x00\x00\x00\r\x01\x00\x08\x00\x01\xcd\xd6\x97o\x98\xffn\x84r\x99\x05\xa4U\xaa',
        b'\x7f~\x00\x00\x00\x00\x01\x02[\x10\xa7NU\xaa',
        b'\x7f~\x00\x00\x00\x00\x08\x00\x00\x00\x00\x01\t\x00\x02FHc\xcdU\xaa',
        b'\x7f~\x00\x00\x00\x01\x05\x01\x01\x00\x00\x00\x00\x00\x01\x86x\x9c\x95O\xcbN\xc30\x10\xfc\x15\xe4s\x1b\xad\x9d8\x8f\x1e\x11\xa8p@\\\xaa\n\t!\xcbq6`Q;\x91m\x82P\x95\x7fg\r\xe5\x03\xf0a5\xb3;3\xbb~>3m\x12\xdb1\x0e\x00l\xc3\xcc\xc9\xa2O\xca\x0e\xd4:\x08\xe0\x1dH\xe88p)\xab\xfd\r\xcd\x9d6o\xd6\xa32\xd3\x80$9B\r\xc09\x07!\xaa\xae\xab$\x96\xc4\x1a\xd3\xf0\xbe%\xf1\xa0\x93f\xbb3\x1bp\xb1\x06\x95\xf5\xe3\x94\xe9\xbf2f\x1d\xe3\xe7\x14\xf2=\xed\xcf\xcb\xb9\xb8(G\xe6Svo\xaf\x1f\x9f\xaen\xb7bO\x83\x98t\xca\x91\x9c\xb0\xc7\xa4\xd2\xd7\xfcG\xc7\x0fo\x08\x96l\xfd\xf5\x8f6\xb8|\xcc\xa8\xbcvYD1\x07\x0cns\xf7p\xef&o\xd3\x14\xb2K-\x18\xf2\x16^\x88\xa2\xac7\xc7\xb2 $\xd8J)#\xe2\xd0k\xf3~Y`#}\xc8\xcd\x01c\xbct\xa2}\xf5\x04\xfb\xba\xaf\xcbV\xd7e\xa5\xa1\xa3\xd2r\x03r\x84\xa6\xd3\xad\x00\x1c\xb3fKU\xaa',
        b'\x7f~\x00\x00\x00\x00\x0e\x01\x00\t\x00\x01\x8d\x92\xad/\xdf\x93\xa5n\x80\xb6\xed%\nU\xaa',
        b'\x7f~\x00\x00\x00\x00\x01\x02[\x10\xa7NU\xaa']
    # 设置要测试的机器码，印度（晚2.5小时），波兰（晚6小时），泰国（晚1小时），越南（晚1小时）
    vbox_wecon = [
        # "V0200118051788206bc83233386",  # LAN 网络通断
        # "V020011811156605a9e4f5f659b",  # LAN 网络通断
        # "V02001181115662a2d12c524140",  # WIFI 网络通断
        # "V02001181115664a2d12c0e20a2",  # WIFI 网络通断
        # "V020011811156635a9e4f5f58d3",  # LAN 持续连接
        #  "V02001181115661a675e8634171",  # LAN 持续连接
        # "V02001180517880c2d35f9f14f6",  # 4G  持续连接
        # "V02001181119999a2d12c528096",  # 4G  持续连接
        # "V02001181119996a2d12c0dcfe5",  # WIFI 周期上下电
    ]
    vbox_forign = [
        # # india
        # "V010011809170059eefb5e1144b",  # Ethernet  ok
        # "V010011807160329eefb5e172e6",  # Wifi      ok
        # "V0200118031300206bc832305a7",  # 4G        ok
        #
        # # poland
        # "V020011801290046a933a475a48",  # 4G        ok
        #
        # # thailand
        # "V0200118030900206bc832020a3",  # WIfi?     ok
        #
        # # vietnam
        # "V02002181120005a2d12c52c89f",  # 4G
    ]
    vbox_vpn = [
        # "V01001190423704a685e08d5f31",  # wifi V-BOX1
        # "V01001190423703a685e0e37557",  # wifi V-BOX2
        # "V01001190423706a685e08df163",  # wifi V-BOX3
        # "V01001190423705a685e0e37515",  # wifi V-BOX4
        # "V020011806280085a828594122e",  # wifi V-BOX5
    ]
    # vbox_2g = [
    #     'V060011102249945e30117c71b8'  # 芯唐2G盒子
    # ]
    # vbox = vbox_wecon + vbox_forign + vbox_vpn + vbox_2g
    s = input('请输入2G盒子机器码，按回车确认。如有多个机器码，请用小写逗号隔开\n>>')
    vbox = s.split(',')
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
    host, port, keepalive, userdata = "mqtt.v-box.net", 1883, 125, {"username": "admin", "password": "password"}
    parse_params = dict()  # 参数设计：停止条件（消息计数、计时、特殊条件）
    client = MqttClient(host, port, keepalive, userdata, **parse_params)
    client.connect()
    client.subscribe(topic)
    print(topic)
    # 开始轮询
    loopall()
