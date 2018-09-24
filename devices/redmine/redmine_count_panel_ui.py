#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: redmine_count_panel_ui
# Author:    fan
# date:      2018/9/7
# -----------------------------------------------------------

from ui_redmine_count_panel import Ui_RedminePanel
from redmine_methods import get_some_issues
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QAbstractItemView, QMessageBox
import logging as log
from redminego import RedmineGo
log.basicConfig(level=log.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')
STATUS_ID = {"新建": 1, "进行中": 2, "已完成": 3, '审核&评审': 7, '已挂起': 8, '待验证': 9}  # 待定
TRACKER_ID = {"BUG": 1, "任务": 2, "测试": 24, "硬件任务": 28}  # 待定
ASSIGNED_NAME = ['范 春回', '黄 海燕', '王 艳如', '陶 艳杰', '兰 秋琳',
                 '李 云', '赖 永珍', '叶 倩', '张 艳虹', '贾 小洁']

field_list = ['id', 'project name', 'subject', 'tracker name',
              'assigned_to name', 'author name', 'status name', 'due_date']


class RedminePannel(QWidget, Ui_RedminePanel):
    def __init__(self, parent=None):
        super(RedminePannel, self).__init__(parent)
        self.setupUi(self)
        self.statuses = None
        self.tasks = None
        self.assignedTo = None
        self.messagebox = QMessageBox()
        self.comboBox_assignedTo.setCurrentText('测试部')
        self.users = {
            '软件一部': ['刘 衍青', '洪 慰'],
            '软件二部': ['许 章赫', '黄 元盛'],
            '软件三部': ['刘 建敏', '刘 小彬'],
            '测试部': ['范 春回', '叶 倩', '兰 秋琳', '王 艳如', '贾 小洁', '黄 海燕', '陶 艳杰', '赖 永珍',
                    '张 艳虹'],
            '技术支持部': ['林 艳梅', '宋 飏'],
            '硬件部': ['李 祥', '魏 龙强'],
            '外贸支持': ['徐 玉洁', '许 清杭']
        }
        self.switch_assigned_to()
        self.switch_assigned_to()

        self.setWindowTitle('Redmine任务查询工具V1.0')

        # 设置可以进行多选
        self.listWidget_partMembers.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget_assignedTo.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableWidget_taskList.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # 设置可以进行自动排序
        self.tableWidget_taskList.setSortingEnabled(True)

    def get_task_type(self):
        """
         获取任务类型
        :return:
        """
        checked_tasks = []
        for chb in [
            self.checkBox_taskTest,
            self.checkBox_taskBug,
            self.checkBox_taskHard,
            self.checkBox_taskTask
        ]:
            if chb.isChecked():
                checked_tasks.append(chb.text())
        log.info('task type: {}'.format(checked_tasks))
        self.tasks = checked_tasks

    def get_status(self):
        """
        获取任务状态
        :return:
        """
        checked_statuses = []
        for chb in [
            self.checkBox_statusNew,
            self.checkBox_statusWorking,
            self.checkBox_statusCheck,
            self.checkBox_statusWaitcheck,
            self.checkBox_statusOver
        ]:
            if chb.isChecked():
                checked_statuses.append(chb.text())
        log.info('status: {}'.format(checked_statuses))
        self.statuses = checked_statuses

    def switch_assigned_to(self):
        """
        对切换部门，并显示当前部门成员，也可以切换到全部，显示所有成员
        :return:
        """
        self.listWidget_partMembers.clear()
        usrs = []
        text = self.comboBox_assignedTo.currentText()
        if text == '全部':
            for v in self.users.values():
                usrs[len(usrs):] = v
        else:
            usrs = self.users[text]
        # print(usrs)
        for usr in usrs:
            item = QtWidgets.QListWidgetItem(usr)
            self.listWidget_partMembers.addItem(item)

    def add_assigned_to(self):
        items2 = []
        for idx in range(self.listWidget_assignedTo.count()):
            items2.append(self.listWidget_assignedTo.item(idx).text())
        items = self.listWidget_partMembers.selectedItems()
        for item in items:
            if item.text() not in items2:
                self.listWidget_assignedTo.addItem(item.text())

    def del_assigned_to(self):
        """
        删除被指派成员，注意代码顺序不可调换
        :return:
        """
        items = self.listWidget_assignedTo.selectedItems()
        for item in items:
            n = self.listWidget_assignedTo.currentRow()
            self.listWidget_assignedTo.takeItem(n)
            self.listWidget_assignedTo.removeItemWidget(item)

    def get_assigned_to(self):
        items2 = []
        for id in range(self.listWidget_assignedTo.count()):
            items2.append(self.listWidget_assignedTo.item(id).text())
        log.info('assigned to: {}'.format(items2))
        self.assignedTo = items2

    def count(self):
        """
        获取查询信息，排布在表格控件中
        :return:
        """
        tasks = self.tasks
        statuses = self.statuses
        assignedto = self.assignedTo
        if tasks == [] or statuses == [] or assignedto == []:
            self.messagebox.information(self,
                                        '提示',
                                        '任务类型或者任务状态或者被指派人不能为空，请确认无误后再查询',
                                        QMessageBox.Ok)
        else:
            task_ids = [TRACKER_ID[i] for i in tasks]
            status_ids = [STATUS_ID[i] for i in statuses]
            log.info('要查询的条件是taskes={}, statuses={}, assigned to={}'.format(tasks, statuses, assignedto))
            issues = get_some_issues(status_ids, task_ids, assignedto, field_list)
            horiheaderitems = issues[0].split('|||')  # 获取表头字段
            tasklist = [i.split('|||') for i in issues[1:-1]]  # 获取任务列表，并将每个任务分离成列表
            x = len(horiheaderitems)
            y = len(tasklist)
            self.tableWidget_taskList.setColumnCount(x)
            self.tableWidget_taskList.setRowCount(y)  # 设置表宽度和长度
            self.tableWidget_taskList.setHorizontalHeaderLabels(horiheaderitems)  # 设置表头

            # 必须保证所有项跟字段具有相同的宽度
            for i in range(y):
                for j in range(x):
                    # 按照表格坐标设置每个任务的每个元素
                    item = QtWidgets.QTableWidgetItem(tasklist[i][j])
                    self.tableWidget_taskList.setItem(i, j, item)

    def clickbutton(self):
        self.pushButton_assignedAdd.clicked.connect(self.add_assigned_to)

        # 单独的对列表控件进行全部清除的方法
        self.pushButton_assignedClear.clicked.connect(self.listWidget_assignedTo.clear)

        self.comboBox_assignedTo.currentTextChanged.connect(self.switch_assigned_to)
        self.pushButton_assignedDel.clicked.connect(self.del_assigned_to)
        self.pushButton_count.clicked.connect(self.get_task_type)
        self.pushButton_count.clicked.connect(self.get_status)
        self.pushButton_count.clicked.connect(self.get_assigned_to)
        self.pushButton_count.clicked.connect(self.count)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    redminego = RedmineGo()
    # redminego.login(urll, usern, passw)
    red = RedminePannel()
    red.show()
    red.clickbutton()
    sys.exit(app.exec_())
