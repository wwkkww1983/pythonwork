#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name：     qt_qclipboard
# Description :
#   Author:      fan
#   date:        2018/1/18
#   IDE:         PyCharm Community Edition
# -----------------------------------------------------------
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication
app = QApplication([])
clipboard = app.clipboard()


def on_clipboard_change():
    data = clipboard.mimeData()
    if data.hasFormat('text/uri-list'):
        for path in data.urls():
            print(path)
    if data.hasText():
        print(data.text())
clipboard.dataChanged.connect(on_clipboard_change)
app.exec_()
