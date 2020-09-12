# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_go.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_goBoard(object):
    def setupUi(self, goBoard):
        goBoard.setObjectName("goBoard")
        goBoard.resize(745, 567)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(goBoard)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.wg_board = QtWidgets.QWidget(goBoard)
        self.wg_board.setObjectName("wg_board")
        self.horizontalLayout_2.addWidget(self.wg_board)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pb_withdraw = QtWidgets.QPushButton(goBoard)
        self.pb_withdraw.setObjectName("pb_withdraw")
        self.horizontalLayout.addWidget(self.pb_withdraw)
        self.pb_manual = QtWidgets.QPushButton(goBoard)
        self.pb_manual.setObjectName("pb_manual")
        self.horizontalLayout.addWidget(self.pb_manual)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textBrowser = QtWidgets.QTextBrowser(goBoard)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(goBoard)
        QtCore.QMetaObject.connectSlotsByName(goBoard)

    def retranslateUi(self, goBoard):
        _translate = QtCore.QCoreApplication.translate
        goBoard.setWindowTitle(_translate("goBoard", "追日"))
        self.pb_withdraw.setText(_translate("goBoard", "悔棋"))
        self.pb_manual.setText(_translate("goBoard", "记谱"))
