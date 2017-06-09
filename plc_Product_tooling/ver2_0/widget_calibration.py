# -*- coding: utf-8 -*-

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QProgressBar, QStyle
from PyQt5.QtCore import Qt, QRect
from ui_widget_calibration import Ui_widget_Calibration

class Calibration(QWidget, Ui_widget_Calibration):

    def __init__(self):
        super(Calibration, self).__init__()
        self.setupUi(self)

        self.progressBar1 = QProgressBar(self)
        self.progressBar1.setGeometry(QRect(100, 100, 400, 30))
        self.progressBar1.setProperty("value", 66)
        self.progressBar1.setObjectName("progressBar")





if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = Calibration()
    win.show()
    sys.exit(app.exec_())
