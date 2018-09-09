#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: redmine_count_panel_ui
# Author:    fan
# date:      2018/9/7
# -----------------------------------------------------------

from ui_redmine_count_panel import Ui_RedminePanel
from PyQt5.QtWidgets import QWidget, QApplication
import logging as log
log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')

USERS = {
    '软件一部': ['刘衍青', '洪慰'],
    '软件二部': ['许章赫', '黄元盛'],
    '软件三部': ['刘建敏', '刘小彬'],
    '测试部': ['范春回', '叶倩', '兰秋琳', '王艳如', '贾小洁'],
    '技术支持部': ['林艳梅', '宋飏'],
    '硬件部': ['李祥', '魏龙强']
         }


class RedminePannel(QWidget, Ui_RedminePanel):
    def __init__(self, parent=None):
        super(RedminePannel, self).__init__(parent)
        self.setupUi(self)

    def get_task_type(self):
        ischecked = [
            self.checkBox_taskTest.isChecked(),
            self.checkBox_taskBug.isChecked(),
            self.checkBox_taskHard.isChecked(),
            self.checkBox_taskTask.isChecked()
        ]
        log.info('task type: {}'.format(ischecked))

    def get_status(self):
        ischecked = [
            self.checkBox_statusNew.isChecked(),
            self.checkBox_statusWorking.isChecked(),
            self.checkBox_statusCheck.isChecked(),
            self.checkBox_statusWaitcheck.isChecked(),
            self.checkBox_statusOver.isChecked()
        ]
        log.info('status: {}'.format(ischecked))

    def get_assigned_to(self):
        self.comboBox_assignedTo.activated.

    def click_count(self):
        self.pushButton_count.clicked.connect(self.get_task_type)
        self.pushButton_count.clicked.connect(self.get_status)



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    red = RedminePannel()
    red.show()
    red.click_count()
    sys.exit(app.exec_())
