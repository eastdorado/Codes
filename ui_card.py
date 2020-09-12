# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_card.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Card(object):
    def setupUi(self, Card):
        Card.setObjectName("Card")
        Card.resize(602, 423)
        Card.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Card)
        self.verticalLayout.setObjectName("verticalLayout")
        self.wg_title = QtWidgets.QWidget()
        self.hl_title = QtWidgets.QHBoxLayout(self.wg_title)
        self.hl_title.setObjectName("hl_title")
        self.toolButton_title_exit = QtWidgets.QToolButton(Card)
        self.toolButton_title_exit.setObjectName("toolButton_title_exit")
        self.hl_title.addWidget(self.toolButton_title_exit)
        self.label_title = QtWidgets.QLabel(Card)
        self.label_title.setObjectName("label_title")
        self.hl_title.addWidget(self.label_title)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hl_title.addItem(spacerItem)
        self.toolButton_title_save = QtWidgets.QToolButton(Card)
        self.toolButton_title_save.setObjectName("toolButton_title_save")
        self.hl_title.addWidget(self.toolButton_title_save)
        # self.verticalLayout.addLayout(self.hl_title)
        self.verticalLayout.addWidget(self.wg_title)
        self.listWidget = QtWidgets.QListWidget(Card)
        self.listWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget.setDragEnabled(True)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)

        self.retranslateUi(Card)
        self.toolButton_title_exit.clicked.connect(Card.slot_tmp)
        self.toolButton_title_save.clicked.connect(Card.slot_save)
        QtCore.QMetaObject.connectSlotsByName(Card)

    def retranslateUi(self, Card):
        _translate = QtCore.QCoreApplication.translate
        Card.setWindowTitle(_translate("Card", "Dialog"))
        self.toolButton_title_exit.setText(_translate("Card", "..."))
        self.label_title.setText(_translate("Card", "TextLabel"))
        self.toolButton_title_save.setText(_translate("Card", "..."))
