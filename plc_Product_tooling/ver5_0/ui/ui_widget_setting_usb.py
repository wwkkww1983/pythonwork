# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_setting_usb.ui'
#
# Created: Wed Jun 28 17:26:01 2017
#      by: PyQt5 UI code generator 5.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_widget_Setting(object):
    def setupUi(self, widget_Setting):
        widget_Setting.setObjectName("widget_Setting")
        widget_Setting.resize(112, 386)
        self.widget = QtWidgets.QWidget(widget_Setting)
        self.widget.setGeometry(QtCore.QRect(0, 40, 111, 181))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pushButton_Link_Digit_Board = QtWidgets.QPushButton(self.widget)
        self.pushButton_Link_Digit_Board.setObjectName("pushButton_Link_Digit_Board")
        self.gridLayout.addWidget(self.pushButton_Link_Digit_Board, 1, 0, 1, 1)
        self.pushButton_Link_Analog_Board = QtWidgets.QPushButton(self.widget)
        self.pushButton_Link_Analog_Board.setObjectName("pushButton_Link_Analog_Board")
        self.gridLayout.addWidget(self.pushButton_Link_Analog_Board, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.comboBox_PortA_Id = QtWidgets.QComboBox(self.widget)
        self.comboBox_PortA_Id.setObjectName("comboBox_PortA_Id")
        self.comboBox_PortA_Id.addItem("")
        self.comboBox_PortA_Id.addItem("")
        self.comboBox_PortA_Id.addItem("")
        self.comboBox_PortA_Id.addItem("")
        self.comboBox_PortA_Id.addItem("")
        self.comboBox_PortA_Id.addItem("")
        self.comboBox_PortA_Id.addItem("")
        self.comboBox_PortA_Id.addItem("")
        self.comboBox_PortA_Id.addItem("")
        self.comboBox_PortA_Id.addItem("")
        self.comboBox_PortA_Id.addItem("")
        self.gridLayout.addWidget(self.comboBox_PortA_Id, 4, 0, 1, 1)
        self.pushButton_Link_Tested_Board = QtWidgets.QPushButton(self.widget)
        self.pushButton_Link_Tested_Board.setObjectName("pushButton_Link_Tested_Board")
        self.gridLayout.addWidget(self.pushButton_Link_Tested_Board, 5, 0, 1, 1)

        self.retranslateUi(widget_Setting)
        QtCore.QMetaObject.connectSlotsByName(widget_Setting)

    def retranslateUi(self, widget_Setting):
        _translate = QtCore.QCoreApplication.translate
        widget_Setting.setWindowTitle(_translate("widget_Setting", "Form"))
        self.label.setText(_translate("widget_Setting", "工装："))
        self.pushButton_Link_Digit_Board.setText(_translate("widget_Setting", "连接数字板"))
        self.pushButton_Link_Analog_Board.setText(_translate("widget_Setting", "连接模拟板"))
        self.label_2.setText(_translate("widget_Setting", "被测板："))
        self.comboBox_PortA_Id.setItemText(0, _translate("widget_Setting", "选择串口"))
        self.comboBox_PortA_Id.setItemText(1, _translate("widget_Setting", "COM1"))
        self.comboBox_PortA_Id.setItemText(2, _translate("widget_Setting", "COM2"))
        self.comboBox_PortA_Id.setItemText(3, _translate("widget_Setting", "COM3"))
        self.comboBox_PortA_Id.setItemText(4, _translate("widget_Setting", "COM4"))
        self.comboBox_PortA_Id.setItemText(5, _translate("widget_Setting", "COM5"))
        self.comboBox_PortA_Id.setItemText(6, _translate("widget_Setting", "COM6"))
        self.comboBox_PortA_Id.setItemText(7, _translate("widget_Setting", "COM7"))
        self.comboBox_PortA_Id.setItemText(8, _translate("widget_Setting", "COM8"))
        self.comboBox_PortA_Id.setItemText(9, _translate("widget_Setting", "COM9"))
        self.comboBox_PortA_Id.setItemText(10, _translate("widget_Setting", "COM10"))
        self.pushButton_Link_Tested_Board.setText(_translate("widget_Setting", "连接"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget_Setting = QtWidgets.QWidget()
    ui = Ui_widget_Setting()
    ui.setupUi(widget_Setting)
    widget_Setting.show()
    sys.exit(app.exec_())

