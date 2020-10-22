#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@项目名称    : PyCharm
@File       : BenchWin.py
@Time       : 2020/10/18 21:18
@Author     : big
@Contact    : shdorado@126.com  
@License    : Copyright (C) 2020-2020 BIG
@Version    : 1.0 
@Desciption :
"""

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from utilities import Utils, MyLog


# class Workbench(QtWidgets.QWidget):
#     def __init__(self, *args, **kwargs):
#         super(Workbench, self).__init__()
#
#         self.title_h = 50  # 标题栏高度
#         self.radius = 10  # 窗体的圆角半径
#         self.deep = 10  # 窗体的阴影宽度
#         self.mPos = None  # 鼠标位置
#         self.log = MyLog()
#
#         self._init_wb()
#         self._init_ui()
#
#     def _init_wb(self):
#         self.resize(700, 500)
#
#         self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)  # 设置窗体无边框
#         self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置背景透明
#         Utils.set_effect(self, 1, self.deep, 5, 5, QtGui.QColor(0, 0, 0, 180))
#
#     def _init_ui(self):
#         qss = '/*border-top-right-radius:10 px;*/' \
#               'min-width: 30px;max-width: 30px;' \
#               'min-height: 30px;max-height: 30px;' \
#               'background: rgba(25,225,25, 150);'
#
#         self.pb_exit = QtWidgets.QPushButton('exit')
#         self.pb_exit.setStyleSheet(qss)
#         self.pb_exit.clicked.connect(self.on_pb_exit_clicked)
#
#         self.pb_min = QtWidgets.QPushButton('min')
#         self.pb_min.setStyleSheet(qss)
#         self.pb_min.clicked.connect(self.on_pb_min_clicked)
#
#         lv = QtWidgets.QVBoxLayout(self)
#         lv.addWidget(self.pb_min)
#         lv.addWidget(self.pb_exit)
#
#     def mousePressEvent(self, e: QtGui.QMouseEvent):
#         if e.button() == QtCore.Qt.LeftButton:
#             if e.pos().y() <= self.title_h:  # 工具栏高度范围内可以移动窗体
#                 self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标
#                 self.mPos = e.pos()
#                 # self.mPos = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
#             else:
#                 self.mPos = None
#
#             e.accept()
#
#     def mouseMoveEvent(self, e: QtGui.QMouseEvent):
#         if QtCore.Qt.LeftButton and self.mPos:
#             self.move(self.mapToGlobal(e.pos() - self.mPos))  # 更改窗口位置
#             e.accept()
#
#     def mouseReleaseEvent(self, e: QtGui.QMouseEvent):
#         self.mPos = None
#         self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
#         e.accept()
#
#     def on_pb_exit_clicked(self):
#         """
#         关闭窗口
#         """
#         self.close()
#
#     def on_pb_min_clicked(self):
#         """
#         最小化窗口
#         """
#         self.showMinimized()
#
#     def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
#         self.pb_min.move(self.width() - self.deep - 75, 5)
#         self.pb_exit.move(self.width() - self.deep - 35, 5)
#
#     def paintEvent(self, event):
#         print('paint')
#         # opt = QStyleOption()
#         # opt.initFrom(self)
#         p = QtGui.QPainter(self)
#         p.setRenderHint(QtGui.QPainter.Antialiasing)  # 抗锯齿
#         # self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
#         # super(Canvas, self).paintEvent(event)
#
#         # # ��ʾȫͼ����
#         # img = QImage('./res//background/bk5.jpg')
#         # w, h = self.width(), self.height()
#         # ratio_w = img.width() / w
#         # ratio_h = img.height() / h
#         #
#         # is_w = True if ratio_w < ratio_h else False
#         # img_new = img.scaledToWidth(h) if is_w else img.scaledToHeight(w)
#         # p.setBrush(QtGui.QBrush(QtGui.QPixmap.fromImage(img_new)))  # 图片刷子
#         p.setBrush(QtGui.QBrush(QtGui.QPixmap(r'E:\Codes\res\background\bk3.jpg')))  # 图片刷子
#         # painter.setBrush(QBrush(Qt.blue))
#         p.setPen(QtCore.Qt.transparent)
#
#         rect = self.rect()
#         rect.setWidth(rect.width() - self.deep)
#         rect.setHeight(rect.height() - self.deep)
#         p.drawRoundedRect(rect, self.radius, self.radius)
#         # painterPath= QPainterPath()
#         # painterPath.addRoundedRect(rect, 15, 15)
#         # painter.drawPath(painterPath)
#
#         # 直接填充图片
#         # pix = QPixmap('./res/images/background11.jpg')
#         # painter.drawPixmap(self.rect(), pix)
#
#         super(Workbench, self).paintEvent(event)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # win = Workbench()
    win.show()
    sys.exit(app.exec_())
