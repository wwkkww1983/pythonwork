#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: hmieditor_package_manager
# Author:    fan
# date:      2018/11/22
# -----------------------------------------------------------
import zipfile, rarfile
import os
from os import path
import time
from pywinauto import application, mouse, keyboard
import psutil
from mylog import mylog
import shutil

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


class LeviSetupManager(object):
    """
    levi 安装包的管理：获取安装包信息并安装，返回安装目录
    """
    def __init__(self, packagepath):
        if not os.path.isfile(packagepath):
            mylog("文件不存在，{}".format(packagepath))
        else:
            self.package_path = packagepath
            package_dir, package_full_name = os.path.split(packagepath)
            package_name, package_extension = os.path.splitext(package_full_name)
            self.install_dir = os.path.join(r"D:\Program Files\WECONSOFT\中性及OEM", package_name)
            self.quik_dir = os.path.join(r"WECONSOFT\中性及OEM", package_name)
            self.setup_type = package_extension
            mylog("准备安装，安装包路径：{}".format(packagepath))
        self.temp_unzip_dir = r"E:\Redmine2019\LEVIOEM测试\temp"
        self.setup_file_path = None
        self.installed_path = None
        self.isinstalled = False
        self.isunstalled = False

    def get_package_info(self):
        inst_target_dir = None
        for key in WECONSOFT.keys():
            if key.upper() in self.package_path.upper():
                inst_target_dir = path.join(INSTROOT, WECONSOFT[key])
        return inst_target_dir

    # def get_setup_path(self):
    #     """
    #     解析安装包路径，如果是压缩包则解压到C盘下，返回安装包.exe的完整路径
    #     :return:
    #     """
    #     setup_path = None
    #     dir, fullname = path.split(self.package_path)
    #     name, extension = path.splitext(fullname)
    #     if extension.lower() == ".exe":
    #         setup_path = self.package_path
    #     elif extension.lower() in [".zip", ".rar", ".7z"]:
    #         if not path.exists("C:\we_inst"):
    #             os.mkdir("C:\we_inst")
    #         command = "7z x -tzip " + self.package_path + "-y -o" + "C:\we_inst\\temp"  # 7z解压缩，选择是，安装到指定路径
    #         os.popen(command)
    #         for f in os.listdir("C:\we_inst\\temp"):
    #             try:
    #                 f_name, f_extension = path.splitext(f)
    #                 if f_extension == ".exe":
    #                     setup_path = path.join("C:\we_inst\\temp", f)
    #                     print("解压成功，", self.package_path)
    #                     break
    #             except Exception as e:
    #                 print(e)
    #     else:
    #         print("file type not supported:", self.package_path)
    #     self.setup_file_path = setup_path
    #     return setup_path

    def get_setup_file_path(self):
        exe_path = None
        if not path.exists(self.package_path):
            mylog("安装包错误，文件不存在：{}".format(self.package_path))
        else:
            newroot = self.temp_unzip_dir
            if path.exists(newroot):
                shutil.rmtree(newroot)
                time.sleep(0.5)
                os.mkdir(newroot)
            if self.setup_type.lower() == ".exe":
                exe_path = self.package_path
            elif self.setup_type.lower() == ".zip":
                zip = zipfile.ZipFile(self.package_path)
                zip.extractall(newroot)
                for f in os.listdir(newroot):
                    try:
                        f_name, f_extension = path.splitext(f)
                        if f_extension.lower() == ".exe":
                            exe_path = path.join(newroot, f)
                            mylog("解压成功，{}".format(self.temp_unzip_dir))
                            break
                    except Exception as e:
                        print(e)
                        continue
            else:
                mylog("解压失败，安装压缩包格式错误：{}".format(self.package_path))
        self.setup_file_path = exe_path
        return exe_path

    def install(self):
        # 执行安装操作。模拟进行安装向导的操作，直到安装完成，重复安装会覆盖此前安装的文件。
        result = False
        self.setup_file_path = self.get_setup_file_path()
        exedir, holename = os.path.split(self.setup_file_path)
        filename, lastname = os.path.splitext(holename)
        if not path.exists(self.setup_file_path):
            mylog("安装失败，文件不存在：{}".format(self.setup_file_path))
        else:
            app.start(self.setup_file_path)
            time.sleep(3)
            install_pid = get_process_pid("{}.tmp".format(filename))
            mylog("正在安装，安装向导PID = {}".format(install_pid))
            # 开始安装
            app.connect(process=install_pid)
            win = app[u"安装向导 - HMIEditor"]
            # win.print_control_identifiers()
            win['下一步(&N) >'].Click()
            time.sleep(0.5)
            win["TEdit"].SetText(self.install_dir)
            time.sleep(0.2)
            win['下一步(&N) >'].Click()
            win['下一步(&N) >'].Click()
            time.sleep(1)
            win["TEdit"].SetText(self.quik_dir)
            time.sleep(0.5)
            win['下一步(&N) >'].Click()
            time.sleep(0.5)
            re = win["ListBox"].rectangle()
            mouse.click("left", (re.left, re.top + 30))
            win['下一步(&N) >'].Click()
            time.sleep(0.5)
            win['安装(&I)'].Click()
            win["完成(&F)"].wait("ready", timeout=100)
            time.sleep(0.5)
            re = win["ListBox"].rectangle()
            mouse.click("left", (re.left, re.top + 10))
            mouse.click("left", (re.left, re.top + 30))
            win["完成(&F)"].Click()
            result = True
            mylog("安装成功，{}".format(self.install_dir))
        self.isinstalled = result
        return result


def get_process_pid(process_name):
    # 获取程序pid（供Pywinauto的application模块进行绑定）
    process_pid = None
    pids = psutil.pids()
    for pid in pids:
        if process_name == psutil.Process(pid).name():
            process_pid = pid
            break
    return process_pid


def uninstall(installpath):
    result = False
    unins000_path = os.path.join(installpath, "unins000.exe")
    if not path.exists(unins000_path):
        mylog("卸载失败，文件不存在: {}".format(unins000_path))
    else:
        app.start(unins000_path)
        time.sleep(1)
        unins_pid = get_process_pid("_iu14D2N.tmp")
        app.connect(process=unins_pid)
        time.sleep(0.5)
        win = app['HMIEditor 卸载向导']
        # win.print_control_identifiers()
        win['是(&Y)'].Click()
        win["确定Button"].wait("ready", timeout=40)
        win["确定Button"].Click()
        mylog("卸载成功，{}".format(unins000_path))
        result = True
    return result


if __name__ == '__main__':
    zip_p = r"E:\Redmine2019\LEVIOEM测试\测试 #9445 测试欧华485通讯优化的OEM软件\欧华OVAHMI20190612.zip"
    man = LeviSetupManager(zip_p)
    man.install()
    # uninstall(r"D:\Program Files\WECONSOFT\中性及OEM\欧华OVAHMI20190610")

