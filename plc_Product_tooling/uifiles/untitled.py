# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
from ui_untitled import Ui_MainWindow
from ui_no_used_simple_qt_demo2 import Ui_Dialog as child
from PyQt5.QtWidgets import QApplication, QWidget

class UiMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(UiMainWindow, self).__init__()
        self.setupUi(self)
        self.setObjectName('MainWindow')
        self.setWindowTitle('A Test Window')
        self.setGeometry(100, 100, 800, 600)

        palette = QtGui.QPalette()
        # palette.setBrush(QtGui.QPalette.Background,
        #                  QtGui.QBrush(QtGui.QPixmap(r"source\backgroud_800_600px.png")))
        palette.setColor(self.backgroundRole(), QtGui.QColor(197, 215, 187))
        # palette.setBrush(self.backgroundRole(),
        #                  QtGui.QBrush(QtGui.QPixmap('source/backgroud_800_600px.png')))
        self.setPalette(palette)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = UiMainWindow()
    win.show()
    sys.exit(app.exec_())

