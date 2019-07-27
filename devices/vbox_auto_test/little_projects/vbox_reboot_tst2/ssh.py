#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: ssh.py
# Author:    fan
# date:      2018/5/18
# -----------------------------------------------------------
import paramiko


class Ssh(object):
    """
    ssh类，基于局域网IP建立shell链接，通过Linux终端执行远程命令或采集远程主机信息
    """
    def __init__(self):
        self.ssh = paramiko.SSHClient()

    def login(self, ip_, usrname_='root', password_='weconily'):
        """
        远程主机登录
        :param ip_:
        :param usrname_:
        :param password_:
        :return: ssh已登录对象
        """
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 跳过是否接收保存密码信息
        self.ssh.connect(ip_, 22, usrname_, password_, timeout=5)  # 用户登录

    def close(self):
        self.ssh.close()

    def do_cmd(self, cmd):
        """
        远程主机执行命令
        :param cmd: 命令内容
        :return: 返回屏显结果
        """
        stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=1)
        # din = stdin.readlines()
        # err = stderr.redlines()
        out = stdout.readlines()
        out_strlist = []
        # print(out)
        for line in out:
            out_strlist.append(line)
            # print(line[:-1])
        return out_strlist

    def cat_file(self, filepath):
        cmd = 'cat {file}'.format(file=filepath)
        stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=1)
        out = stdout.readlines()
        return out

    def get_lines(self, filepath, nline):
        cmd = 'tail -n {n} {f}'.format(n=nline, f=filepath)
        stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=1)
        out = stdout.readlines()
        return out

    @staticmethod
    def save_file(savepath, file1):
        newfile1 = []
        print(file1)
        for line in file1:
            newline = line.replace('\r', '')
            print(newline)
            newfile1.append(newline)
        print(newfile1)
        with open(savepath, 'w', encoding='gb2312') as f:
            f.writelines(newfile1)

if __name__ == '__main__':
    pass
