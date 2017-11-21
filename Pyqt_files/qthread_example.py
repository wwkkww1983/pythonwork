#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name：     qthread_example
# Description :
#   Author:      fan
#   date:        2017/11/17
#   IDE:         PyCharm Community Edition
# -----------------------------------------------------------

import sys, time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import  QPushButton, QDialog, QApplication, QLabel


class TimerQthread(QThread):
    finished_signal = pyqtSignal(str)

    def __init__(self, rest, parent=None):
        super().__init__(parent)
        self._rest = rest
        self.value = 0.00

    def run(self):
        for i in range(1000):
            value = '{:.3}'.format(self.value)
            print(value)
            self.finished_signal.emit(value)
            time.sleep(self._rest)
            self.value += 0.01


class MyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(400, 200)
        self.button = QPushButton(self)
        self.button.setText('DO IT')
        self.button.setGeometry(10, 10, 80, 20)
        self.button.clicked.connect(self._click_to_do_something)

        self.label = QLabel(self)
        self.label.setText('0.00')
        self.label.setGeometry(10, 40, 80, 20)


    @staticmethod
    def _show_message(message):
        print(message)

    def _renew(self, message):
        self.label.setText(message)


    def _click_to_do_something(self):
        self.timer_thread = TimerQthread(0.01)
        # self.timer_thread.finished_signal.connect(self._show_message)
        self.timer_thread.finished_signal.connect(self._renew)
        self.timer = self.timer_thread.value
        self.timer_thread.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = MyDialog()

    dialog.show()
    sys.exit(app.exec())
