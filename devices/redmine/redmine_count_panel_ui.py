#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: redmine_count_panel_ui
# Author:    fan
# date:      2018/9/7
# -----------------------------------------------------------

from ui_redmine_count_panel import Ui_RedminePanel
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QAbstractItemView
import logging as log
log.basicConfig(level=log.ERROR,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')


class RedminePannel(QWidget, Ui_RedminePanel):
    def __init__(self, parent=None):
        super(RedminePannel, self).__init__(parent)
        self.setupUi(self)
        self.statuses = None
        self.tasks = None
        self.assignedTo = None
        self.comboBox_assignedTo.setCurrentText('测试部')
        self.users = {
            '软件一部': ['刘 衍青', '洪 慰'],
            '软件二部': ['许 章赫', '黄 元盛'],
            '软件三部': ['刘 建敏', '刘 小彬'],
            '测试部': ['范 春回', '叶 倩', '兰 秋琳', '王 艳如', '贾 小洁'],
            '技术支持部': ['林 艳梅', '宋 飏'],
            '硬件部': ['李 祥', '魏 龙强'],
            '外贸支持': ['徐 玉洁', '许 清杭']
        }
        self.switch_assigned_to()
        self.switch_assigned_to()
        self.listWidget_partMembers.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget_assignedTo.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableWidget_taskList.setSelectionMode(QAbstractItemView.ExtendedSelection)


    def get_task_type(self):
        checked_tasks = []
        for chb in [
            self.checkBox_taskTest,
            self.checkBox_taskBug,
            self.checkBox_taskHard,
            self.checkBox_taskTask
        ]:
            if chb.isChecked():
                checked_tasks.append(chb.text())
        # ischecked = [
        #     self.checkBox_taskTest.isChecked(),
        #     self.checkBox_taskBug.isChecked(),
        #     self.checkBox_taskHard.isChecked(),
        #     self.checkBox_taskTask.isChecked()
        # ]
        log.info('task type: {}'.format(checked_tasks))
        self.tasks = checked_tasks

    def get_status(self):
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
        # ischecked = [
        #     self.checkBox_statusNew.isChecked(),
        #     self.checkBox_statusWorking.isChecked(),
        #     self.checkBox_statusCheck.isChecked(),
        #     self.checkBox_statusWaitcheck.isChecked(),
        #     self.checkBox_statusOver.isChecked()
        # ]
        log.info('status: {}'.format(checked_statuses))
        self.statuses = checked_statuses

    def switch_assigned_to(self):
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
        items = self.listWidget_assignedTo.selectedItems()
        for item in items:
            n = self.listWidget_assignedTo.currentRow()
            self.listWidget_assignedTo.takeItem(n)
            self.listWidget_assignedTo.removeItemWidget(item)

    def click_add(self):
        self.pushButton_assignedAdd.clicked.connect(self.add_assigned_to)

    def click_clear(self):
        self.pushButton_assignedClear.clicked.connect(self.listWidget_assignedTo.clear)

    def click_del(self):
        self.pushButton_assignedDel.clicked.connect(self.del_assigned_to)

    def get_assigned_to(self):
        items2 = []
        for id in range(self.listWidget_assignedTo.count()):
            items2.append(self.listWidget_assignedTo.item(id).text())
        log.info('assigned to: {}'.format(items2))
        self.assignedTo = items2

    def click_count(self):
        self.pushButton_count.clicked.connect(self.get_task_type)
        self.pushButton_count.clicked.connect(self.get_status)
        self.pushButton_count.clicked.connect(self.get_assigned_to)
        self.pushButton_count.clicked.connect(self.count)

    def count(self):
        tasks = self.tasks
        statuses = self.statuses
        assignedto = self.assignedTo
        print(tasks, statuses, assignedto)
        return tasks, statuses, assignedto


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    red = RedminePannel()
    red.show()

    red.click_add()
    red.click_del()
    red.click_clear()
    red.click_count()

    sys.exit(app.exec_())
