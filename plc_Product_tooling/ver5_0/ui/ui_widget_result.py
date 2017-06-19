# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_result.ui'
#
# Created: Tue May  9 00:53:20 2017
#      by: PyQt5 UI code generator 5.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_widget_Result_Show(object):
    def setupUi(self, widget_Result_Show):
        widget_Result_Show.setObjectName("widget_Result_Show")
        widget_Result_Show.resize(1031, 0)
        self.label_Operating_Flag = QtWidgets.QLabel(widget_Result_Show)
        self.label_Operating_Flag.setEnabled(True)
        self.label_Operating_Flag.setGeometry(QtCore.QRect(48, 32, 180, 43))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(75)
        self.label_Operating_Flag.setFont(font)
        self.label_Operating_Flag.setObjectName("label_Operating_Flag")
        self.pushButton_Start_Calibration = QtWidgets.QPushButton(widget_Result_Show)
        self.pushButton_Start_Calibration.setEnabled(True)
        self.pushButton_Start_Calibration.setGeometry(QtCore.QRect(744, 24, 233, 57))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Start_Calibration.sizePolicy().hasHeightForWidth())
        self.pushButton_Start_Calibration.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(32)
        self.pushButton_Start_Calibration.setFont(font)
        self.pushButton_Start_Calibration.setObjectName("pushButton_Start_Calibration")
        self.label_Calibration_Result = QtWidgets.QLabel(widget_Result_Show)
        self.label_Calibration_Result.setEnabled(True)
        self.label_Calibration_Result.setGeometry(QtCore.QRect(272, 32, 180, 43))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(75)
        self.label_Calibration_Result.setFont(font)
        self.label_Calibration_Result.setObjectName("label_Calibration_Result")
        self.pushButton_Stop_Calibration = QtWidgets.QPushButton(widget_Result_Show)
        self.pushButton_Stop_Calibration.setEnabled(True)
        self.pushButton_Stop_Calibration.setGeometry(QtCore.QRect(496, 24, 233, 57))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Stop_Calibration.sizePolicy().hasHeightForWidth())
        self.pushButton_Stop_Calibration.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(32)
        self.pushButton_Stop_Calibration.setFont(font)
        self.pushButton_Stop_Calibration.setObjectName("pushButton_Stop_Calibration")

        self.retranslateUi(widget_Result_Show)
        QtCore.QMetaObject.connectSlotsByName(widget_Result_Show)

    def retranslateUi(self, widget_Result_Show):
        _translate = QtCore.QCoreApplication.translate
        widget_Result_Show.setWindowTitle(_translate("widget_Result_Show", "Form"))
        self.label_Operating_Flag.setText(_translate("widget_Result_Show", "运行状态"))
        self.pushButton_Start_Calibration.setText(_translate("widget_Result_Show", "开始检测"))
        self.label_Calibration_Result.setText(_translate("widget_Result_Show", "检测结果"))
        self.pushButton_Stop_Calibration.setText(_translate("widget_Result_Show", "停止检测"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget_Result_Show = QtWidgets.QWidget()
    ui = Ui_widget_Result_Show()
    ui.setupUi(widget_Result_Show)
    widget_Result_Show.show()
    sys.exit(app.exec_())

