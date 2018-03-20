# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sign_up.ui'
#
# Created: Tue Mar 20 13:07:06 2018
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
        self.layoutWidget.setGeometry(QtCore.QRect(32, 231, 332, 41))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.layoutWidget1 = QtWidgets.QWidget(dialog_sign)
        self.layoutWidget1.setGeometry(QtCore.QRect(88, 60, 206, 151))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        self.label.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_name = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.gridLayout.addWidget(self.lineEdit_name, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_pswd = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_pswd.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.lineEdit_pswd.setAutoFillBackground(True)
        self.lineEdit_pswd.setObjectName("lineEdit_pswd")
        self.gridLayout.addWidget(self.lineEdit_pswd, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_sign = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_sign.setObjectName("pushButton_sign")
        self.horizontalLayout.addWidget(self.pushButton_sign)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_cancel = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(dialog_sign)
        QtCore.QMetaObject.connectSlotsByName(dialog_sign)

    def retranslateUi(self, dialog_sign):
        _translate = QtCore.QCoreApplication.translate
        dialog_sign.setWindowTitle(_translate("dialog_sign", "注册"))
        self.label_3.setText(_translate("dialog_sign", "用户名由6~16位字符组成，只能包含a~z、A~Z、0~9、_"))
        self.label_4.setText(_translate("dialog_sign", "密码由6~16位字符组成，包含a~z、A~Z、0~9、及常用符号"))
        self.label.setText(_translate("dialog_sign", "用户名："))
        self.label_2.setText(_translate("dialog_sign", "密  码："))
        self.pushButton_sign.setText(_translate("dialog_sign", "登录"))
        self.pushButton_cancel.setText(_translate("dialog_sign", "取消"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog_sign = QtWidgets.QDialog()
    ui = Ui_dialog_sign()
    ui.setupUi(dialog_sign)
    dialog_sign.show()
    sys.exit(app.exec_())

