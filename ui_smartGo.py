# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_smartGo.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SmartGo(object):
    def setupUi(self, SmartGo):
        SmartGo.setObjectName("SmartGo")
        SmartGo.resize(744, 569)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/big/.designer/backup/res/go.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        SmartGo.setWindowIcon(icon)
        self.verticalLayoutWidget = QtWidgets.QWidget(SmartGo)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 111, 321))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.vl_main = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.vl_main.setContentsMargins(0, 0, 0, 0)
        self.vl_main.setObjectName("vl_main")
        self.horizontalLayoutWidget = QtWidgets.QWidget(SmartGo)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(550, 20, 111, 331))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.hl_main = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.hl_main.setContentsMargins(0, 0, 0, 0)
        self.hl_main.setObjectName("hl_main")
        self.gb_apps = QtWidgets.QGroupBox(SmartGo)
        self.gb_apps.setGeometry(QtCore.QRect(190, 240, 261, 91))
        self.gb_apps.setTitle("")
        self.gb_apps.setObjectName("gb_apps")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.gb_apps)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(50, 20, 160, 41))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.hl_apps = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.hl_apps.setContentsMargins(0, 0, 0, 0)
        self.hl_apps.setObjectName("hl_apps")
        self.pb_app_1 = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.pb_app_1.setObjectName("pb_app_1")
        self.hl_apps.addWidget(self.pb_app_1)
        self.gridLayoutWidget = QtWidgets.QWidget(SmartGo)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(250, 40, 160, 80))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gl_groups = QtWidgets.QGridLayout()
        self.gl_groups.setContentsMargins(0, 0, 0, 0)
        self.gl_groups.setObjectName("gl_groups")
        self.pb_order_1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pb_order_1.setObjectName("pb_order_1")
        self.gl_groups.addWidget(self.pb_order_1, 0, 0, 1, 1)

        self.retranslateUi(SmartGo)
        self.pb_order_1.clicked.connect(SmartGo.slot1)
        self.pb_app_1.clicked.connect(SmartGo.slot2)
        QtCore.QMetaObject.connectSlotsByName(SmartGo)

    def retranslateUi(self, SmartGo):
        _translate = QtCore.QCoreApplication.translate
        SmartGo.setWindowTitle(_translate("SmartGo", "快速启动"))
        self.pb_app_1.setText(_translate("SmartGo", "PushButton"))
        self.pb_order_1.setText(_translate("SmartGo", "PushButton"))
