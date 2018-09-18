#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: redmine_count_app
# Author:    fan
# date:      2018/9/7
# -----------------------------------------------------------
from redmine_count_panel_ui import RedminePannel
from redminego import RedmineGo
from redmine_methods import get_some_issues
from PyQt5.QtWidgets import QApplication

urll = "http://192.168.11.118:7777/redmine/"  # 公司Redmine服务器
usern = "fanchunhui"
passw = "a6361255"

STATUS_ID = {"新建": 1, "进行中": 2, "已完成": 3, '审核&评审': 7, '已挂起': 8, '待验证': 9}  # 待定
TRACKER_ID = {"BUG": 1, "任务": 2, "测试": 24}  # 待定



def update_data():
    redminego = RedmineGo()
    redminego.login(urll, usern, passw)
    redminego.get_all_projects()
    redminego.get_all_issues()
    redminego.get_all_users()

def main():
    import sys
    app = QApplication(sys.argv)
    red = RedminePannel()
    red.show()
    red.click_add()
    red.click_del()
    red.click_clear()
    red.click_count()
    red.pushButton_renew.clicked.connect(update_data)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
