# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window_process.ui'
#
# Created: Mon May  8 01:30:57 2017
#      by: PyQt5 UI code generator 5.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1030, 656)
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
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(8, 88, 169, 537))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_left = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_left.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_left.setObjectName("gridLayout_left")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(176, 95, 849, 417))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_middle = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_middle.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_middle.setObjectName("gridLayout_middle")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(176, 512, 849, 113))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_buttom = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_buttom.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_buttom.setObjectName("gridLayout_buttom")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(16, 632, 553, 16))
        self.label.setText("")
        self.label.setObjectName("label")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(176, 16, 833, 65))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.pushButton_Go_Backstage = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_Go_Backstage.setGeometry(QtCore.QRect(696, 24, 121, 23))
        self.pushButton_Go_Backstage.setObjectName("pushButton_Go_Backstage")
        self.groupBox_1 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_1.setGeometry(QtCore.QRect(16, 8, 124, 73))
        self.groupBox_1.setObjectName("groupBox_1")
        self.layoutWidget_5 = QtWidgets.QWidget(self.groupBox_1)
        self.layoutWidget_5.setGeometry(QtCore.QRect(16, 16, 94, 40))
        self.layoutWidget_5.setObjectName("layoutWidget_5")
        self.verticalLayout_1 = QtWidgets.QVBoxLayout(self.layoutWidget_5)
        self.verticalLayout_1.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.comboBox_Select_Module = QtWidgets.QComboBox(self.layoutWidget_5)
        self.comboBox_Select_Module.setObjectName("comboBox_Select_Module")
        self.comboBox_Select_Module.addItem("")
        self.comboBox_Select_Module.addItem("")
        self.verticalLayout_1.addWidget(self.comboBox_Select_Module)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_Go_Backstage.setText(_translate("MainWindow", "查看详细信息"))
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

