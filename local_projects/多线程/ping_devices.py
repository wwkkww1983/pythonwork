# -*- coding: utf-8 -*-
# python3.4 pingIP.py

import platform
import sys
import os
import time
import _thread as thread
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QGridLayout, QTextBrowser, QLabel, QApplication
ip_addresses = []


def get_os():
    """
    get os 类型
    """
    os = platform.system()
    if os == "Windows":
        return "n"
    else:
        return "c"
     

def ping_ip(ip_str):
    cmd = ["ping", "-{op}".format(op=get_os()),
           "1", ip_str]
    output = os.popen(" ".join(cmd)).readlines()
     
    flag = False
    global ip_addresses
    for line in list(output):
        if not line:
            continue
        if str(line).upper().find("TTL") >= 0:
            flag = True
            break
    if flag:
        print("ip: %s is ok ***" % ip_str)
        print(ip_str)
    ip_addresses.append(ip_str)


def test_ip(ip_addr, tms=10, lenth=1024):
    """
    对单个IP地址进行检测
    :param ip_addr: ip地址字符串
    :param tms: 发送次数
    :param lenth: 包长度
    :return:
    """
    cmd = ['ping', '-{op}'.format(op=get_os()), tms, '-l', lenth, ip_addr]
    output = os.popen(''.join(cmd)).readlines()

    flag = False
    for line in list(output):
        if not line:
            continue
        elif str(line).upper().find("TTL") >= 0:
            continue
        else:
            pass


def find_ips(ip_prefix):
    """
    给出当前的127.0.0，然后扫描整个段所有地址
    """
    for i in range(1, 50):
        ip = '%s.%s' % (ip_prefix, i)
        thread.start_new_thread(ping_ip, (ip,))
        time.sleep(0.1)




class Ui(QWidget):
    def __init__(self, parent=None):
        super(Ui, self).__init__(parent)
        self.initUi()

    def initUi(self):

        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        titleLabel = QLabel('以太网BD板出厂硬件检测工具')
        authorLabel = QLabel('版本1.0，测试部fanch')
        reviwLabel = QTextBrowser()
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(title, 1, 0)
        grid.addWidget(titleLabel, 1, 1)
        grid.addWidget(author, 2, 0)
        grid.addWidget(authorLabel, 2, 1)
        grid.addWidget(review, 3, 0)
        grid.addWidget(reviwLabel, 3, 1, 5, 1)

        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')
        self.show()


class MyThreads(QThread):
    ipSignal = pyqtSignal(list)

    def __init__(self, ip, parent=None):
        super(MyThreads, self).__init__(parent)
        self.ip = ip

    def run(self):
        ip = self.ip
        find_ips(ip)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Ui()


    print("start time %s" % time.ctime())
    ip_prefix = '192.168.22'
    find_ips(ip_prefix)
    ip_pool = ip_addresses
    print(ip_pool)
    print("end time %s" % time.ctime())
    sys.exit(app.exec_())

