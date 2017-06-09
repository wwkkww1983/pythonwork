# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'can_open_analyse_tool.ui'
#
# Created: Tue Mar 21 18:14:56 2017
#      by: PyQt5 UI code generator 5.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_usb2CanDataAnalTool(object):
    def setupUi(self, usb2CanDataAnalTool):
        usb2CanDataAnalTool.setObjectName("usb2CanDataAnalTool")
        usb2CanDataAnalTool.resize(939, 625)
        font = QtGui.QFont()
        font.setFamily("宋体")
        usb2CanDataAnalTool.setFont(font)
        usb2CanDataAnalTool.setLayoutDirection(QtCore.Qt.RightToLeft)
        usb2CanDataAnalTool.setAutoFillBackground(False)
        self.pushButton_closeWin = QtWidgets.QPushButton(usb2CanDataAnalTool)
        self.pushButton_closeWin.setGeometry(QtCore.QRect(808, 576, 75, 23))
        self.pushButton_closeWin.setObjectName("pushButton_closeWin")
        self.label_Title = QtWidgets.QLabel(usb2CanDataAnalTool)
        self.label_Title.setGeometry(QtCore.QRect(416, 8, 121, 16))
        self.label_Title.setObjectName("label_Title")
        self.label_FileInfo = QtWidgets.QLabel(usb2CanDataAnalTool)
        self.label_FileInfo.setGeometry(QtCore.QRect(16, 48, 54, 12))
        self.label_FileInfo.setObjectName("label_FileInfo")
        self.label_DataTable = QtWidgets.QLabel(usb2CanDataAnalTool)
        self.label_DataTable.setGeometry(QtCore.QRect(16, 160, 54, 12))
        self.label_DataTable.setObjectName("label_DataTable")
        self.table_Widget = QtWidgets.QTableWidget(usb2CanDataAnalTool)
        self.table_Widget.setGeometry(QtCore.QRect(32, 184, 881, 377))
        self.table_Widget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.table_Widget.setAutoFillBackground(True)
        self.table_Widget.setObjectName("table_Widget")
        self.layoutWidget = QtWidgets.QWidget(usb2CanDataAnalTool)
        self.layoutWidget.setGeometry(QtCore.QRect(32, 64, 633, 89))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_Can1 = QtWidgets.QLabel(self.layoutWidget)
        self.label_Can1.setObjectName("label_Can1")
        self.gridLayout.addWidget(self.label_Can1, 2, 1, 1, 1)
        self.label_Time = QtWidgets.QLabel(self.layoutWidget)
        self.label_Time.setObjectName("label_Time")
        self.gridLayout.addWidget(self.label_Time, 3, 0, 1, 1)
        self.label_Date = QtWidgets.QLabel(self.layoutWidget)
        self.label_Date.setObjectName("label_Date")
        self.gridLayout.addWidget(self.label_Date, 3, 1, 1, 1)
        self.label_Can2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_Can2.setObjectName("label_Can2")
        self.gridLayout.addWidget(self.label_Can2, 2, 0, 1, 1)
        self.label_Name = QtWidgets.QLabel(self.layoutWidget)
        self.label_Name.setObjectName("label_Name")
        self.gridLayout.addWidget(self.label_Name, 1, 1, 1, 1)
        self.label_dataNum = QtWidgets.QLabel(self.layoutWidget)
        self.label_dataNum.setObjectName("label_dataNum")
        self.gridLayout.addWidget(self.label_dataNum, 1, 0, 1, 1)

        self.retranslateUi(usb2CanDataAnalTool)
        self.pushButton_closeWin.released.connect(usb2CanDataAnalTool.close)
        QtCore.QMetaObject.connectSlotsByName(usb2CanDataAnalTool)

    def retranslateUi(self, usb2CanDataAnalTool):
        _translate = QtCore.QCoreApplication.translate
        usb2CanDataAnalTool.setWindowTitle(_translate("usb2CanDataAnalTool", "mainlog"))
        self.pushButton_closeWin.setText(_translate("usb2CanDataAnalTool", "退出"))
        self.label_Title.setText(_translate("usb2CanDataAnalTool", "USB2CAN 数据分析工具"))
        self.label_FileInfo.setText(_translate("usb2CanDataAnalTool", "TextLabel"))
        self.label_DataTable.setText(_translate("usb2CanDataAnalTool", "TextLabel"))
        self.label_Can1.setText(_translate("usb2CanDataAnalTool", "TextLabel"))
        self.label_Time.setText(_translate("usb2CanDataAnalTool", "TextLabel"))
        self.label_Date.setText(_translate("usb2CanDataAnalTool", "TextLabel"))
        self.label_Can2.setText(_translate("usb2CanDataAnalTool", "TextLabel"))
        self.label_Name.setText(_translate("usb2CanDataAnalTool", "TextLabel"))
        self.label_dataNum.setText(_translate("usb2CanDataAnalTool", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    usb2CanDataAnalTool = QtWidgets.QDialog()
    ui = Ui_usb2CanDataAnalTool()
    ui.setupUi(usb2CanDataAnalTool)
    usb2CanDataAnalTool.show()
    sys.exit(app.exec_())

