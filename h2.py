#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

import cgitb  # 相当管用

cgitb.enable(format='text')  # 解决 pyqt5 异常只要进入事件循环,程序就崩溃,而没有任何提示


class MainWin(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWin, self).__init__(*args, **kwargs)

    def __str__(self):
        return '1'

    __repr__ = __str__


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())
