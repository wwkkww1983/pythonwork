# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_calibration.ui'
#
# Created: Fri Jul  7 18:50:32 2017
#      by: PyQt5 UI code generator 5.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_widget_Calibration(object):
    def setupUi(self, widget_Calibration):
        widget_Calibration.setObjectName("widget_Calibration")
        widget_Calibration.setWindowModality(QtCore.Qt.NonModal)
        widget_Calibration.resize(842, 397)
        self.progressBar_Calibration = QtWidgets.QProgressBar(widget_Calibration)
        self.progressBar_Calibration.setGeometry(QtCore.QRect(32, 328, 761, 41))
        self.progressBar_Calibration.setStyleSheet("background-color: #1a1a1a;\n"
"")
        self.progressBar_Calibration.setProperty("value", 50)
        self.progressBar_Calibration.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.progressBar_Calibration.setTextVisible(False)
        self.progressBar_Calibration.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar_Calibration.setInvertedAppearance(False)
        self.progressBar_Calibration.setObjectName("progressBar_Calibration")
        self.layoutWidget = QtWidgets.QWidget(widget_Calibration)
        self.layoutWidget.setGeometry(QtCore.QRect(360, 32, 321, 273))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_Module_Type = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_Module_Type.setFont(font)
        self.label_Module_Type.setObjectName("label_Module_Type")
        self.verticalLayout_2.addWidget(self.label_Module_Type)
        self.label_Object_Type = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_Object_Type.setFont(font)
        self.label_Object_Type.setObjectName("label_Object_Type")
        self.verticalLayout_2.addWidget(self.label_Object_Type)
        self.label_Hardware_Code = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_Hardware_Code.setFont(font)
        self.label_Hardware_Code.setObjectName("label_Hardware_Code")
        self.verticalLayout_2.addWidget(self.label_Hardware_Code)
        self.label_Error = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_Error.setFont(font)
        self.label_Error.setObjectName("label_Error")
        self.verticalLayout_2.addWidget(self.label_Error)
        self.layoutWidget1 = QtWidgets.QWidget(widget_Calibration)
        self.layoutWidget1.setGeometry(QtCore.QRect(184, 32, 153, 273))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_1 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        self.label_1.setFont(font)
        self.label_1.setObjectName("label_1")
        self.verticalLayout.addWidget(self.label_1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)

        self.retranslateUi(widget_Calibration)
        QtCore.QMetaObject.connectSlotsByName(widget_Calibration)

    def retranslateUi(self, widget_Calibration):
        _translate = QtCore.QCoreApplication.translate
        widget_Calibration.setWindowTitle(_translate("widget_Calibration", "Form"))
        self.label_Module_Type.setText(_translate("widget_Calibration", "LX - XXXX"))
        self.label_Object_Type.setText(_translate("widget_Calibration", "PT"))
        self.label_Hardware_Code.setText(_translate("widget_Calibration", "FFFF"))
        self.label_Error.setText(_translate("widget_Calibration", "无错误"))
        self.label_1.setText(_translate("widget_Calibration", "模块型号："))
        self.label_2.setText(_translate("widget_Calibration", "检测类型："))
        self.label_3.setText(_translate("widget_Calibration", "硬件检测："))
        self.label_4.setText(_translate("widget_Calibration", "错误警告："))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget_Calibration = QtWidgets.QWidget()
    ui = Ui_widget_Calibration()
    ui.setupUi(widget_Calibration)
    widget_Calibration.show()
    sys.exit(app.exec_())

