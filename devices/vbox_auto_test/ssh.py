#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: ssh.py
# Author:    fan
# date:      2018/5/18
# -----------------------------------------------------------
import paramiko

ssh = paramiko.SSHClient()    # 创建ssh客户端


class Ssh(object):
    def __init__(self):
        self.ssh = paramiko.SSHClient()

    def login(self, ip_, usrname_, password_):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 跳过是否接收保存密码信息
        self.ssh.connect(ip_, 22, usrname_, password_)  # 用户登录

    def do_cmd(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        out = stdout.readlines()
        for line in out:
            print(line[:-1])
        # out = stdout.read()
        # print(out)
        # ssh.close()
if __name__ == '__main__':
    client = Ssh()
    ip = '192.168.39.115'
    usrname = 'root'
    password = 'weconily'

    cmd1 = 'top -b -n 1'  # 执行命令：监控当前系统 资源
    cmd2 = 'tail -n 1 /mnt/data/log/HMImo'    # 显示文件最后一行
    client.login(ip, usrname, password)
    client.do_cmd(cmd1)
    client.do_cmd(cmd2)
