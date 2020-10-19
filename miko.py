#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Project    : Codes
@File       : miko.py
@Time       : 2020/10/19 13:13
@Author     : big QQ: 260125177
@Contact    : shdorado@126.com  
@License    : Copyright (C) 2018-2020 BIG
@Version    : 1.0 
@Desciption :
"""

import sys
from PyQt5 import QtWidgets, QtCore, QtGui


class MainWin(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWin, self).__init__()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWin()
    w.show()
    sys.exit(app.exec_())
