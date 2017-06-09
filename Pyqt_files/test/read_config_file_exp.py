# -*- coding: utf-8 -*-

# python:2.x

__author__ = 'Administrator'

import sys, datetime

from PyQt5.QtCore import Qt

from PyQt5 import QtGui, QtCore, Qt

#from aa import Ui_Form


class Example(QtGui.QDialog, Ui_Form):
    def __init__(self, parnet=None):
        super(Example, self).__init__(parnet)
        self.setupUi(self)
        self.read1()

    def read1(self):  # 读取
        settings1 = QtCore.QSettings(r'a.ini', QtCore.QSettings.IniFormat)  # 当前目录的INI文件
        settings1.beginGroup('a')
        settings1.setIniCodec('UTF-8')
        s1 = settings1.value(r'cpu:', self.lineEdit.text()).toString()
        s2 = settings1.value(r'cpu1:', self.lineEdit_2.text()).toString()
        self.lineEdit.setText(unicode(s1))
        self.lineEdit_2.setText(unicode(s2))
        settings1.endGroup()
        return True

    def write(self):  # 写入
        settings1 = QtCore.QSettings(r'a.ini', QtCore.QSettings.IniFormat)  # 当前目录的INI文件
        settings1.beginGroup('a')
        settings1.setIniCodec('UTF-8')
        s1 = settings1.setValue(r'cpu:', self.lineEdit.text())
        s2 = settings1.setValue(r'cpu1:', self.lineEdit_2.text())
        self.lineEdit.setText(unicode(s1))
        self.lineEdit_2.setText(unicode(s2))
        settings1.endGroup()
        return True

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.write()
            event.accept()
        else:
            event.ignore()

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
main()