# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

from PyQt5.QtWidgets import QApplication, QWidget,QMainWindow
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets


class WindowTest(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(WindowTest, self).__init__(parent)

        self.setObjectName('MainWindow')
        self.setWindowTitle('A Test Window')
        self.setGeometry(100, 100, 800, 600)

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(r"source\backgroud_800_600px.png")))
        self.setPalette(palette)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = WindowTest()
    win.show()
    sys.exit(app.exec_())
