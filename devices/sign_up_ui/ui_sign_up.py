# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sign_up.ui'
#
# Created: Tue Mar 20 00:19:34 2018
#      by: PyQt5 UI code generator 5.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialog_sign(object):
    def setupUi(self, dialog_sign):
        dialog_sign.setObjectName("dialog_sign")
        dialog_sign.setWindowModality(QtCore.Qt.NonModal)
        dialog_sign.resize(386, 300)
        self.layoutWidget = QtWidgets.QWidget(dialog_sign)
        self.layoutWidget.setGeometry(QtCore.QRect(90, 60, 201, 101))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_name = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.gridLayout.addWidget(self.lineEdit_name, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_pswd = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_pswd.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.lineEdit_pswd.setAutoFillBackground(True)
        self.lineEdit_pswd.setObjectName("lineEdit_pswd")
        self.gridLayout.addWidget(self.lineEdit_pswd, 1, 1, 1, 1)
        self.widget = QtWidgets.QWidget(dialog_sign)
        self.widget.setGeometry(QtCore.QRect(32, 256, 314, 32))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.widget1 = QtWidgets.QWidget(dialog_sign)
        self.widget1.setGeometry(QtCore.QRect(88, 200, 201, 25))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_sign = QtWidgets.QPushButton(self.widget1)
        self.pushButton_sign.setObjectName("pushButton_sign")
        self.horizontalLayout.addWidget(self.pushButton_sign)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_cancel = QtWidgets.QPushButton(self.widget1)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)

        self.retranslateUi(dialog_sign)
        QtCore.QMetaObject.connectSlotsByName(dialog_sign)

    def retranslateUi(self, dialog_sign):
        _translate = QtCore.QCoreApplication.translate
        dialog_sign.setWindowTitle(_translate("dialog_sign", "注册"))
        self.label.setText(_translate("dialog_sign", "用户："))
        self.label_2.setText(_translate("dialog_sign", "密码："))
        self.label_3.setText(_translate("dialog_sign", "用户名由6~16位字符组成，只能包含a~z、A~Z、0~9、_构成"))
        self.label_4.setText(_translate("dialog_sign", "密码由6~16位字符组成，a~z、A~Z、0~9、及常用符号构成"))
        self.pushButton_sign.setText(_translate("dialog_sign", "注册"))
        self.pushButton_cancel.setText(_translate("dialog_sign", "取消"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog_sign = QtWidgets.QDialog()
    ui = Ui_dialog_sign()
    ui.setupUi(dialog_sign)
    dialog_sign.show()
    sys.exit(app.exec_())

