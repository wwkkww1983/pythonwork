# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_result.ui'
#
# Created: Mon May  8 01:30:57 2017
#      by: PyQt5 UI code generator 5.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_widget_Result_Show(object):
    def setupUi(self, widget_Result_Show):
        widget_Result_Show.setObjectName("widget_Result_Show")
        widget_Result_Show.resize(837, 104)
        self.groupBox = QtWidgets.QGroupBox(widget_Result_Show)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 833, 97))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setEnabled(True)
        self.pushButton_2.setGeometry(QtCore.QRect(448, 16, 180, 65))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(25)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setEnabled(True)
        self.label_2.setGeometry(QtCore.QRect(226, 32, 185, 33))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setEnabled(True)
        self.pushButton.setGeometry(QtCore.QRect(632, 16, 180, 65))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(25)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(16, 32, 185, 33))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(widget_Result_Show)
        QtCore.QMetaObject.connectSlotsByName(widget_Result_Show)

    def retranslateUi(self, widget_Result_Show):
        _translate = QtCore.QCoreApplication.translate
        widget_Result_Show.setWindowTitle(_translate("widget_Result_Show", "Form"))
        self.pushButton_2.setText(_translate("widget_Result_Show", "停止检测"))
        self.label_2.setText(_translate("widget_Result_Show", "检测结果"))
        self.pushButton.setText(_translate("widget_Result_Show", "开始检测"))
        self.label.setText(_translate("widget_Result_Show", "运行状态"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget_Result_Show = QtWidgets.QWidget()
    ui = Ui_widget_Result_Show()
    ui.setupUi(widget_Result_Show)
    widget_Result_Show.show()
    sys.exit(app.exec_())

