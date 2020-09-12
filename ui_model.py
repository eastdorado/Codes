# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_model.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Model(object):
    def setupUi(self, Model):
        Model.setObjectName("Model")
        Model.resize(350, 467)
        self.verticalLayout = QtWidgets.QVBoxLayout(Model)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hl_model = QtWidgets.QHBoxLayout()
        self.hl_model.setObjectName("hl_model")
        self.toolButton_model = QtWidgets.QToolButton(Model)
        self.toolButton_model.setObjectName("toolButton_model")
        self.hl_model.addWidget(self.toolButton_model)
        self.label_model = QtWidgets.QLabel(Model)
        self.label_model.setObjectName("label_model")
        self.hl_model.addWidget(self.label_model)
        self.verticalLayout.addLayout(self.hl_model)
        self.lineEdit_model = QtWidgets.QLineEdit(Model)
        self.lineEdit_model.setObjectName("lineEdit_model")
        self.verticalLayout.addWidget(self.lineEdit_model)
        self.listWidget_model = QtWidgets.QListWidget(Model)
        self.listWidget_model.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.listWidget_model.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget_model.setObjectName("listWidget_model")
        self.verticalLayout.addWidget(self.listWidget_model)

        self.retranslateUi(Model)
        self.toolButton_model.clicked.connect(Model.slot_tmp)
        self.lineEdit_model.textChanged['QString'].connect(Model.slot_tmp)
        self.listWidget_model.clicked['QModelIndex'].connect(Model.slot_tmp)
        QtCore.QMetaObject.connectSlotsByName(Model)

    def retranslateUi(self, Model):
        _translate = QtCore.QCoreApplication.translate
        Model.setWindowTitle(_translate("Model", "Dialog"))
        self.toolButton_model.setText(_translate("Model", "..."))
        self.label_model.setText(_translate("Model", "TextLabel"))
