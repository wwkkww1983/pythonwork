#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: reboot_box
# Author:    fan
# date:      2018/5/30
# -----------------------------------------------------------
import pywinauto.application as app
from pywinauto import mouse, keyboard
import pyautogui
import time
import json
import win32api
from ssh import Ssh

nowtimefmt = lambda: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 格式化当前时间

with open("control_xys.json", 'r', encoding="utf-8") as f:
    control_xys = json.loads(f.read())
    # print("页面按钮坐标:\n", control_xys)
controls = {}
for k, v in control_xys.items():
    if '_comment' not in k:
        controls[k] = [int(i) for i in v.split(',')]
print("页面按钮坐标:\n", controls)
with open("box_info.json", 'r', encoding="utf-8") as f:
    box_ips = json.loads(f.read())
print("盒子列表:\n", box_ips)


def set_scrn_resol(width, height):
    # 利用win32api库修改屏幕分辨率
    dm = win32api.EnumDisplaySettings(None, 0)
    dm.PelsHeight = width
    dm.PelsWidth = height
    dm.BitsPerPel = 32
    dm.DisplayFixedOutput = 0
    win32api.ChangeDisplaySettings(dm, 0)


def start_box(exe_path):
    app_path = exe_path
    box = app.Application()
    box.start(app_path)
    time.sleep(5)
    return box


def click(control_name: str, mousekey='left'):
    try:
        mouse.click(button=mousekey, coords=controls[control_name])
        time.sleep(1)
    except Exception as e:
        print(e)


def download_reboot():
    """
    下载配置后重启
    """
    click("download")
    time.sleep(1)
    click('download_config')
    time.sleep(1)


def remote_reboot(box_es, n=1):
    """
    远程重启
    """
    click('monitor')
    time.sleep(5)
    click('default_group')
    for i in range(n):
        print("{}: round {} begins".format(nowtimefmt(), i))
        for box_id in box_es:
            click(box_id)
            time.sleep(1)
            click('basic_set')
            time.sleep(1)
            click('basic_set1')
            pyautogui.hotkey('end')
            time.sleep(1)
            pyautogui.hotkey('end')
            time.sleep(1)
            click("reboot_box")
            time.sleep(1)
            click("reboot_box_ok")
            time.sleep(1)
            click("box_reboot_ok")
            print("{}: box {} is rebooting".format(nowtimefmt(), box_id))
            time.sleep(1)
        print("{}: round {} finished".format(nowtimefmt(), i))


def check_boxes(box_ids, boxes_tobe=[1]*8):
    boxes_are_online = []
    for box_id in box_ids:
        ip = '192.168.' + box_ips[box_id][0]
        ssh = Ssh()
        try:
            ssh.login(ip)
            time.sleep(1)
            print("{}: current box: {} is online.".format(nowtimefmt(), box_ips[box_id][1]))
            boxes_are_online.append(1)
        except Exception as e:
            if "Unable to connect" or "连接尝试失败" in e:
                print("{}: current box: {} is offline.".format(nowtimefmt(), box_ips[box_id][1]))
            else:
                print("{}: 未知错误 {}".format(nowtimefmt(), e))
            boxes_are_online.append(0)
        finally:
            try:
                ssh.ssh.close()
            except Exception:
                pass
    if len(boxes_are_online):
        return boxes_are_online == boxes_tobe


def remote_reboot_single(box_id):
    click('monitor')
    time.sleep(3)
    click('default_group')
    click(box_id)
    time.sleep(1)
    click('basic_set')
    time.sleep(1)
    click('basic_set1')
    pyautogui.hotkey('end')
    time.sleep(1)
    pyautogui.hotkey('end')
    time.sleep(1)
    click("reboot_box")
    time.sleep(1)
    click("reboot_box_ok")
    time.sleep(1)
    click("box_reboot_ok")
    print("{}: box {} is rebooting".format(nowtimefmt(), box_id))
    time.sleep(1)


def penetrate_reboot_single(box_id):
    """
    穿透下载后重启
    """
    click('monitor')
    time.sleep(5)
    click('default_group')
    click(box_id)
    time.sleep(1)
    click('remote_download')
    time.sleep(1)
    click('start_to_penetrate')
    time.sleep(1)
    click('penetrate_confirm')
    time.sleep(2)
    click('penetrate_started_ok')
    time.sleep(5)  # 穿透进行中，等待时间较长
    click('finish_penetrate')
    time.sleep(1)
    click('penetrate_finished_ok')

    
def check_box_single(box_id, box_tobe):
    box_is_online = None
    ip = '192.168.' + box_ips[box_id][0]
    ssh = Ssh()
    try:
        ssh.login(ip)
        time.sleep(1)
        print("{}: current box: {} is online.".format(nowtimefmt(), box_ips[box_id][1]))
        box_is_online = 1
    except Exception as e:
        if "Unable to connect" or "连接尝试失败" in e:
            print("{}: current box: {} is offline.".format(nowtimefmt(), box_ips[box_id][1]))
        else:
            print("{}: 未知错误 {}".format(nowtimefmt(), e))
        box_is_online = 0
    finally:
        try:
            ssh.ssh.close()
        except Exception:
            pass
    return box_is_online == box_tobe


if __name__ == '__main__':
    set_scrn_resol(1366, 768)
    time.sleep(5)
    # box_path = r"D:\Program Files\WECONSOFT\V-Box\20180517测试\V-BOX.exe"
    # box_pc = start_box(box_path)
    # box_win = box_pc["V-BOX"]
    # # box_win.print_control_identifiers()
    # boxes = ['box2', 'box3', 'box4', 'box5']
    # # remote_reboot(boxes, 1)
    #
    # def tst_download_reboot():
    #     download_reboot()
    #     time.sleep(5)
    #     # a = check_boxes(boxes, [1]*4)
    #     a = check_box_single('box1', 0)
    #     time.sleep(20)
    #     b = check_box_single('box1', 1)
    #     print('{}: download reboot test passed? ={} {}'.format(nowtimefmt(), a, b))
    #
    # def tst_remote_reboot():
    #     remote_reboot_single('box2')
    #     time.sleep(5)
    #     c = check_box_single('box2', 0)
    #     time.sleep(20)
    #     d = check_box_single('box2', 1)
    #     print('{}: remote reboot test passed? ={} {}'.format(nowtimefmt(), c, d))
    #
    #
    # def tst_remote_reboot_multi(box_es):
    #     check_result = []
    #     for box in box_es:
    #         remote_reboot_single(box)
    #         time.sleep(5)
    #         c = check_box_single(box, 0)
    #         time.sleep(30)
    #         d = check_box_single(box, 1)
    #         check_result.append((c, d))
    #     print('{}: remote reboot test passed? ={}'.format(nowtimefmt(), check_result))
    #
    # # for i in range(1):
    # #     print("{}: round {} begins".format(nowtimefmt(), i))
    # #     # tst_download_reboot()
    # #     # tst_remote_reboot_multi(boxes)
    # #     penetrate_reboot_single(boxes[0])
    # #     print("{}: round {} finished".format(nowtimefmt(), i))
    # box_pc.kill()
    set_scrn_resol(1440, 900)
