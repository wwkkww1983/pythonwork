#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: vbox_port_penetration
# Author:    fan
# date:      2019/6/5 005
# V-BOX软件穿透功能自动实现穿透和结束穿透并通过PLC串口测试确认穿透是否成功
# -----------------------------------------------------------

import pyautogui
from time import sleep
from pywinauto import application
from make_time_formated import nowtimestr

CLICK_LOCATION = {
    "开始穿透": (620, 700),
    "开始穿透_OK": (1018, 581),
    "穿透成功_OK": (1022, 560),
    "结束穿透": (444, 743),
    "穿透结束_OK": (1026, 560),
    "远程下载_刷新": (1082, 94)
}
click = pyautogui.click


def start_penetration():
    """
    通过屏幕鼠标操作开始穿透，开始穿透前要将软件界面切换至盒子 - 远程下载，并保存唯一一组穿透串口设置，记录虚拟串口编号：
    如 COM43
    :return:
    """
    click(100, 20)  # 切换回V-BOX界面
    sleep(1)
    click(*CLICK_LOCATION["远程下载_刷新"])
    sleep(4)
    click(*CLICK_LOCATION["开始穿透"])
    sleep(3)
    click(*CLICK_LOCATION["开始穿透_OK"])
    sleep(5)
    click(*CLICK_LOCATION["穿透成功_OK"])
    sleep(2)
    click(*CLICK_LOCATION["远程下载_刷新"])


def end_penetration():
    """
    结束穿透
    :return:
    """
    click(100, 20)  # 切换回V-BOX界面
    sleep(1)
    click(*CLICK_LOCATION["远程下载_刷新"])
    sleep(4)
    click(*CLICK_LOCATION["结束穿透"])
    sleep(5)
    click(*CLICK_LOCATION["穿透结束_OK"])
    sleep(2)
    click(*CLICK_LOCATION["远程下载_刷新"])


def check_penetration(app_plc):
    """
    利用PLCEditor通讯测试确认穿透是否成功, 测试准备：打开软件，移动窗口到屏幕右半边。
    新建文件（勿保存），打开通讯测试对话框, 确认串口号
    :param app_plc: 已绑定的PLCEditor App对象
    :return:
    """
    global count_fail
    global count_success
    global total_count
    global current_num
    win_comm = app_plc["通讯设置"]
    # win_comm["USB 连接（最好使用屏蔽良好的线缆）"].click()
    # sleep(1)
    win_comm["串口连接"].click()
    win_comm["COM端口ComboBox"].select("{}-Virtual Serial Port 8 (Eltima Software)".format(portname))
    win_comm["通讯测试"].click()
    if app_plc["Wecon PLC Editor"].exists(10):
        if app_plc["Wecon PLC Editor"]['与LX3V连接成功！'].exists(1):
            count_success += 1
        elif app_plc["Wecon PLC Editor"]['无法与PLC通讯！'].exists(1):
            count_fail += 1
        else:
            print("通讯测试信息异常")
            app_plc["Wecon PLC Editor"].print_control_identifiers()
            count_fail += 1
        app_plc["Wecon PLC Editor"]["确定"].click()
    line = "{} 完成进度 {}/{}，通讯成功次数 {}, 通讯失败次数 {}".format(
        nowtimestr(), current_num, total_count, count_success, count_fail)
    with open("盒子穿透次数记录.log", 'a') as f:
        f.write(line + "\n")
    print(line)


def main():
    print("准备开始穿透")
    start_penetration()
    app_plc = application.Application()
    app_plc.connect(title="Wecon PLC Editor - 梯形图（写入）")
    print("正在检查通讯")
    check_penetration(app_plc)
    end_penetration()
    print("结束穿透，盒子将重启（60）")
    sleep(60)


if __name__ == '__main__':
    count_success = 0
    count_fail = 0
    input("测试准备: 打开V-BOX配置工具，启用并配置好虚拟串口。\n"
          "将画面定位到盒子 - 远程下载，设置唯一一组串口设置记录。\n"
          "PLCEditor新建工程（勿保存文件），然后打开通讯口测试对话框\n"
          "按任意键继续...")
    portname = input("请输入虚拟串口编号（如COM22、COM43）：\n")
    total_count = input("请输入测试次数：\n")
    with open("盒子穿透次数记录.log", 'w') as f:
        f.write("测试开始时间: {}\n".format(nowtimestr()))
    current_num = 1
    while current_num <= int(total_count):
        try:
            main()
        except Exception as e:
            print(e)
            input()
        current_num += 1
    input("测试结束，请确认数据，按任意键退出...")
