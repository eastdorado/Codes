#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @Product: PyCharm
#  @Project: Neworld
#  @File    : SportsMan.py
#  @Author  : big
#  @Email   : shdorado@126.com
#  @Time    : 2020/7/14 0:09
#  功能：

import sys

from ctypes import cdll
from ctypes.wintypes import HWND, DWORD

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget


class Demo(QWidget):
    """ 亚克力效果的实现 """

    def __init__(self):
        super().__init__()

        self.resize(500, 500)
        # 去除边框,没有这一步的话窗口阴影也会加上亚克力效果
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 调用api
        hWnd = HWND(int(self.winId()))  # 直接HWND(self.winId())会报错
        gradientColor = DWORD(0x01f100f3)  # 前两位是透明度，后面六位是bgr 设置和亚克力效果相叠加的背景颜色
        cdll.LoadLibrary('./res/dll/acrylic.dll').setBlur(hWnd, gradientColor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
