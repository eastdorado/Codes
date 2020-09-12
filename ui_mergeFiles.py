# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mergeFiles.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

from customTableWg import CustTableWidget
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(818, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/big/.designer/backup/res/images/watermark.jpg"), QtGui.QIcon.Active, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pb_add_files = QtWidgets.QPushButton(self.centralwidget)
        self.pb_add_files.setObjectName("pb_add_files")
        self.horizontalLayout.addWidget(self.pb_add_files)
        self.pb_open_dir = QtWidgets.QPushButton(self.centralwidget)
        self.pb_open_dir.setObjectName("pb_open_dir")
        self.horizontalLayout.addWidget(self.pb_open_dir)
        self.lineEdit_src_dir = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_src_dir.setToolTip("")
        self.lineEdit_src_dir.setStatusTip("")
        self.lineEdit_src_dir.setText("")
        self.lineEdit_src_dir.setObjectName("lineEdit_src_dir")
        self.horizontalLayout.addWidget(self.lineEdit_src_dir)
        self.pb_clear = QtWidgets.QPushButton(self.centralwidget)
        self.pb_clear.setObjectName("pb_clear")
        self.horizontalLayout.addWidget(self.pb_clear)
        self.cb_select_all = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_select_all.setObjectName("cb_select_all")
        self.horizontalLayout.addWidget(self.cb_select_all)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.tableWidget = CustTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBox)
        self.lineEdit_save_path = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_save_path.setObjectName("lineEdit_save_path")
        self.horizontalLayout_3.addWidget(self.lineEdit_save_path)
        self.pb_save_path = QtWidgets.QPushButton(self.centralwidget)
        self.pb_save_path.setToolTip("")
        self.pb_save_path.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("res/images/cross_1.png"), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap("res/images/cross.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.pb_save_path.setIcon(icon1)
        self.pb_save_path.setIconSize(QtCore.QSize(20, 20))
        self.pb_save_path.setObjectName("pb_save_path")
        self.horizontalLayout_3.addWidget(self.pb_save_path)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.cb_eyebrow = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_eyebrow.setObjectName("cb_eyebrow")
        self.horizontalLayout_4.addWidget(self.cb_eyebrow)
        self.cb_watermark = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_watermark.setObjectName("cb_watermark")
        self.horizontalLayout_4.addWidget(self.cb_watermark)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.rb_digit_little = QtWidgets.QRadioButton(self.centralwidget)
        self.rb_digit_little.setObjectName("rb_digit_little")
        self.horizontalLayout_4.addWidget(self.rb_digit_little)
        self.rb_digit_big = QtWidgets.QRadioButton(self.centralwidget)
        self.rb_digit_big.setObjectName("rb_digit_big")
        self.horizontalLayout_4.addWidget(self.rb_digit_big)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.pb_merge = QtWidgets.QPushButton(self.centralwidget)
        self.pb_merge.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pb_merge.setFont(font)
        self.pb_merge.setAutoFillBackground(False)
        self.pb_merge.setObjectName("pb_merge")
        self.horizontalLayout_4.addWidget(self.pb_merge)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.cb_open_dst_file = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_open_dst_file.setObjectName("cb_open_dst_file")
        self.horizontalLayout_5.addWidget(self.cb_open_dst_file)
        self.cb_open_dst_dir = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_open_dst_dir.setObjectName("cb_open_dst_dir")
        self.horizontalLayout_5.addWidget(self.cb_open_dst_dir)
        self.cb_delete_src_files = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_delete_src_files.setObjectName("cb_delete_src_files")
        self.horizontalLayout_5.addWidget(self.cb_delete_src_files)
        self.cb_exit = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_exit.setObjectName("cb_exit")
        self.horizontalLayout_5.addWidget(self.cb_exit)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_5.addWidget(self.progressBar)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 818, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_4 = QtWidgets.QAction(MainWindow)
        self.action_4.setObjectName("action_4")
        self.action_5 = QtWidgets.QAction(MainWindow)
        self.action_5.setObjectName("action_5")
        self.menu.addAction(self.action_4)
        self.menu.addAction(self.action_5)
        self.menu.addAction(self.action_3)
        self.menu_2.addAction(self.action)
        self.menu_2.addAction(self.action_2)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Word文档处理"))
        self.pb_add_files.setText(_translate("MainWindow", "添加文件"))
        self.pb_open_dir.setText(_translate("MainWindow", "添加文件夹"))
        self.pb_clear.setText(_translate("MainWindow", "清空"))
        self.cb_select_all.setText(_translate("MainWindow", "全选"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "名称"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "总页数"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "输出范围"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "大小"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "最终修改日期"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "状态"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "操作"))
        self.label.setText(_translate("MainWindow", "输出路径："))
        self.comboBox.setCurrentText(_translate("MainWindow", "自定义目录"))
        self.comboBox.setItemText(0, _translate("MainWindow", "自定义目录"))
        self.comboBox.setItemText(1, _translate("MainWindow", "源文件目录"))
        self.comboBox.setItemText(2, _translate("MainWindow", "云目录"))
        self.label_3.setText(_translate("MainWindow", "源文件处理："))
        self.cb_eyebrow.setText(_translate("MainWindow", "去眉页和眉脚"))
        self.cb_watermark.setText(_translate("MainWindow", "去水印"))
        self.label_6.setText(_translate("MainWindow", "排序方式："))
        self.rb_digit_little.setText(_translate("MainWindow", "123 …"))
        self.rb_digit_big.setText(_translate("MainWindow", "一二三 …"))
        self.pb_merge.setText(_translate("MainWindow", "合并"))
        self.label_2.setText(_translate("MainWindow", "合并完成后："))
        self.cb_open_dst_file.setText(_translate("MainWindow", "打开输出文件"))
        self.cb_open_dst_dir.setText(_translate("MainWindow", "打开输出文件夹"))
        self.cb_delete_src_files.setText(_translate("MainWindow", "删除源文件"))
        self.cb_exit.setText(_translate("MainWindow", "退出程序"))
        self.label_5.setText(_translate("MainWindow", "      总进度："))
        self.menu.setTitle(_translate("MainWindow", "功能"))
        self.menu_2.setTitle(_translate("MainWindow", "帮助"))
        self.action.setText(_translate("MainWindow", "语言"))
        self.action_2.setText(_translate("MainWindow", "关于"))
        self.action_3.setText(_translate("MainWindow", "设置"))
        self.action_4.setText(_translate("MainWindow", "文件改名"))
        self.action_5.setText(_translate("MainWindow", "转为PDF"))
