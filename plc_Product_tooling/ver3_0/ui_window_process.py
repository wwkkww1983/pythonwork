# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window_process.ui'
#
# Created: Tue May  9 00:53:20 2017
#      by: PyQt5 UI code generator 5.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1030, 657)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("source/window_24_24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(168, 16, 841, 65))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.comboBox_Select_page = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_Select_page.setGeometry(QtCore.QRect(288, 16, 121, 25))
        self.comboBox_Select_page.setObjectName("comboBox_Select_page")
        self.comboBox_Select_page.addItem("")
        self.comboBox_Select_page.addItem("")
        self.comboBox_Select_page.addItem("")
        self.pushButton_Open_Ports = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_Open_Ports.setGeometry(QtCore.QRect(16, 16, 113, 25))
        self.pushButton_Open_Ports.setObjectName("pushButton_Open_Ports")
        self.pushButton_Reset_Module = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_Reset_Module.setGeometry(QtCore.QRect(152, 16, 113, 25))
        self.pushButton_Reset_Module.setObjectName("pushButton_Reset_Module")
        self.groupBox_1 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_1.setGeometry(QtCore.QRect(16, 8, 137, 73))
        self.groupBox_1.setObjectName("groupBox_1")
        self.comboBox_Select_Module = QtWidgets.QComboBox(self.groupBox_1)
        self.comboBox_Select_Module.setGeometry(QtCore.QRect(8, 24, 119, 25))
        self.comboBox_Select_Module.setObjectName("comboBox_Select_Module")
        self.comboBox_Select_Module.addItem("")
        self.comboBox_Select_Module.addItem("")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(16, 96, 137, 425))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.stackedWidget = QtWidgets.QStackedWidget(self.groupBox_2)
        self.stackedWidget.setGeometry(QtCore.QRect(8, 8, 121, 409))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(168, 96, 841, 425))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.stackedWidget_2 = QtWidgets.QStackedWidget(self.groupBox_3)
        self.stackedWidget_2.setGeometry(QtCore.QRect(8, 8, 825, 409))
        self.stackedWidget_2.setObjectName("stackedWidget_2")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.stackedWidget_2.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.stackedWidget_2.addWidget(self.page_4)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(16, 536, 993, 113))
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.stackedWidget_3 = QtWidgets.QStackedWidget(self.groupBox_4)
        self.stackedWidget_3.setGeometry(QtCore.QRect(8, 8, 977, 97))
        self.stackedWidget_3.setObjectName("stackedWidget_3")
        self.page_7 = QtWidgets.QWidget()
        self.page_7.setObjectName("page_7")
        self.stackedWidget_3.addWidget(self.page_7)
        self.page_8 = QtWidgets.QWidget()
        self.page_8.setObjectName("page_8")
        self.stackedWidget_3.addWidget(self.page_8)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.comboBox_Select_page.setItemText(0, _translate("MainWindow", "下载固件"))
        self.comboBox_Select_page.setItemText(1, _translate("MainWindow", "校准画面"))
        self.comboBox_Select_page.setItemText(2, _translate("MainWindow", "工装后台"))
        self.pushButton_Open_Ports.setText(_translate("MainWindow", "打开串口"))
        self.pushButton_Reset_Module.setText(_translate("MainWindow", "复位被测板"))
        self.groupBox_1.setTitle(_translate("MainWindow", "选择模块"))
        self.comboBox_Select_Module.setItemText(0, _translate("MainWindow", "LX 8PT"))
        self.comboBox_Select_Module.setItemText(1, _translate("MainWindow", "LX 8TC"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

