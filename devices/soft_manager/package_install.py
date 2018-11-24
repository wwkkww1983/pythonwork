#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: package_install
# Author:    fan
# date:      2018/11/22
# -----------------------------------------------------------
import zipfile, rarfile
import os
from os import path
import time
from pywinauto import application, mouse, keyboard
import psutil

app = application.Application()
INSTROOT = r"D:\Program Files\WECONSOFT"
WECONSOFT = {
    "PIStudio": {"name": "PIStudio", "packagetype": "zip"},
    "HMIEditorP": {"name": "HMIEditorP"},
    "LeviStudio": {"name": "LeviStudio"},
    "LeviStudioU": {"name": "LeviStudioU"},
    "HMIEditor": {"name": "HMIEditor"},
    "PLCEditor": {"name": "PLCEditor"},
    "V-Box": {"name": "V-Box"}
}


def get_package_info(source_path: str):
    inst_target_dir = None
    for key in WECONSOFT.keys():
        if key.upper() in source_path.upper():
            inst_target_dir = path.join(INSTROOT, WECONSOFT[key])
    return inst_target_dir


def get_setup_path(source_path: str):
    """
    解析安装包路径，如果是压缩包则解压到C盘下，返回安装包.exe的完整路径
    :param source_path:
    :return:
    """
    setup_path = None
    dir, fullname = path.split(source_path)
    name, extension = path.splitext(fullname)
    if extension.lower() == ".exe":
        setup_path = source_path
    elif extension.lower() in [".zip", ".rar", ".7z"]:
        if not path.exists("C:\we_inst"):
            os.mkdir("C:\we_inst")
        command = "7z x -tzip " + source_path + "-y -o" + "C:\we_inst\\temp"  # 7z解压缩，选择是，安装到指定路径
        os.popen(command)
        for f in os.listdir("C:\we_inst\\temp"):
            try:
                f_name, f_extension = path.splitext(f)
                if f_extension == ".exe":
                    setup_path = path.join("C:\we_inst\\temp", f)
                    print("解压成功，", source_path)
                    break
            except Exception as e:
                print(e)
    else:
        print("file type not supported:", source_path)
    return setup_path


def get_ppid(process_name):
    process_pid = None
    pids = psutil.pids()
    for pid in pids:
        if process_name == psutil.Process(pid).name():
            process_pid = pid
            break
    return process_pid


def get_exe_path(package_path):
    # 文件覆盖解压
    exe_path = None
    if path.exists(package_path):
        root, name = path.split(package_path)
        newroot = path.join(root, r"temp")
        if not path.exists(newroot):
            os.mkdir(newroot)
        zip = zipfile.ZipFile(package_path)
        zip.extractall(newroot)
        os.listdir(newroot)
        for f in os.listdir(newroot):
            try:
                f_name, f_extension = path.splitext(f)
                if f_extension == ".exe":
                    exe_path = path.join(newroot, f)
                    print("解压成功，", package_path)
                    break
            except Exception as e:
                print(e)
                continue
        return exe_path


def install(exe_path):
    install_pid = None
    result = False
    if path.exists(exe_path):
        app.start(exe_path)
        time.sleep(3)
        install_pid = get_ppid("中性HMIEditor.tmp")
    if install_pid:
        app.connect(process=install_pid)
        win = app[u"安装向导 - HMIEditor"]
        # win.print_control_identifiers()
        win['下一步(&N) >'].Click()
        time.sleep(0.5)
        win["TEdit"].SetText(r"D:\Program Files\WECONSOFT\中性及OEM\20181121")
        time.sleep(0.8)
        win['下一步(&N) >'].Click()
        time.sleep(0.5)
        win["TEdit"].SetText(r"WECONSOFT\中性及OEM\20181121")
        time.sleep(0.2)
        win['下一步(&N) >'].Click()
        time.sleep(0.2)
        re = win["ListBox"].rectangle()
        mouse.click("left", (re.left, re.top+30))
        win['下一步(&N) >'].Click()
        time.sleep(0.2)
        win['安装(&I)'].Click()
        win["完成(&F)"].wait("ready", timeout=100)
        time.sleep(0.5)
        re = win["ListBox"].rectangle()
        mouse.click("left", (re.left, re.top+10))
        mouse.click("left", (re.left, re.top+30))
        win["完成(&F)"].Click()
        result = True
        print("安装成功，", exe_path)
    return result


def uninstall(uninstall_path):
    result = False
    if path.exists(uninstall_path):
        app.start(uninstall_path)
        time.sleep(1)
        unins_pid = get_ppid("_iu14D2N.tmp")
        app.connect(process=unins_pid)
        time.sleep(0.5)
        win = app['HMIEditor 卸载向导']
        # win.print_control_identifiers()
        win['是(&Y)'].Click()
        win["确定Button"].wait("ready", timeout=40)
        win["确定Button"].Click()
        print("卸载成功，", uninstall_path)
        result = True
    return result


if __name__ == '__main__':
    zip_p = r"C:\Users\fan\Desktop\软件安装\中性HMIEditor2070D-1.zip"
    # exe_p = r"C:\Users\fan\Desktop\软件安装\temp\中性HMIEditor.exe"
    unins_p = r"D:\Program Files\WECONSOFT\中性及OEM\20181121\unins000.exe"
    exe_p = get_exe_path(zip_p)
    install(exe_p)
    time.sleep(10)
    uninstall(unins_p)
