#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: redmine_count_panel_ui
# Author:    fan
# date:      2018/9/7
# -----------------------------------------------------------

from ui_redmine_count_panel import Ui_RedminePanel
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication


class RedminePannel(QWidget, Ui_RedminePanel):
    def __init__(self, parent=None):
        super(RedminePannel, self).__init__(parent)
        # self.ui = Ui_RedminePanel()
        self.setupUi(self)

    def get_task_type(self):
        ischecked = [
            self.checkBox_taskTest.isChecked(),
            self.checkBox_taskBug.isChecked(),
            self.checkBox_taskHard.isChecked(),
            self.checkBox_taskTask.isChecked()
        ]
        print(ischecked)

    def click_count(self):
        self.pushButton_count.clicked.connect(self.get_task_type)



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    red = RedminePannel()
    red.show()
    red.click_count()
    sys.exit(app.exec_())
