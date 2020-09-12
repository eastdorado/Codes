#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @项目名称: python
# @File    : uiBridge.py
# @Time    : 2020/3/25 13:43
# @Author  : big
# @Email   : shdorado@126.com

import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from functools import partial
from utilities import Utils, AnimWin

from ui_docs import Ui_MainWindow


class UiDocManager(Ui_MainWindow):
    def __init__(self):
        self.parent = None

    def setupUI(self, Main):
        super().setupUi(Main)

        self.parent = Main
        self.parent.resize(1200, 1000)

        # TODO 修改原始控件

    def slot_tools_clicked(self, action):
        name = action.objectName()
        print(name)
        if name == 'action_exit':
            QtCore.QCoreApplication.instance().quit()
        elif name == 'action_split_pdf':
            self.parent.split_pdf()
        elif name == 'action_open':
            path, _ = QtWidgets.QFileDialog.getOpenFileName(self, '请选择文件', '',
                'pdf(*.pdf);;word(*.docx *.doc);;excel(*.xlsx *.xls);;ppt(*.pptx *.ppt)')
            if not path:
                return
            if _.find('*.doc') or _.find('*.docx'):
                return self.parent.openOffice(path, 'Word.Application')
            if _.find('*.xls'):
                return self.parent.openOffice(path, 'Excel.Application')
            if _.find('*.ppt') or _.find('*.pptx'):
                return self.parent.openOffice(path, 'PowerPoint.Application')
            if _.find('*.pdf'):
                return self.parent.openPdf(path)
        elif name == 'action_save_as':
            self.parent.flushMap()


class MainWindow(QtWidgets.QMainWindow, UiDocManager):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUI(self)

        # TODO 修改原始控件

    def resizeEvent(self, event):
        palette = QtGui.QPalette()
        pix = QtGui.QPixmap('res/images/background9.jpg')
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(palette)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
