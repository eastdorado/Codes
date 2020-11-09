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
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from utilities import Utils, MyLog, ImageConvert, AnimWin
from PIL import Image, ImageFilter
from functools import partial

log = MyLog()


class FoWorld(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(FoWorld, self).__init__()
        self.deep = 10
        self.radius = 10

        desktop = QtWidgets.QApplication.desktop()
        print(desktop.width(), desktop.height())
        self.setGeometry(600, 20, 500, 900)  # 黄金分割

        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)  # 设置窗体无边框
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置背景透明
        # Utils.set_effect(self, 1, self.deep, 5, 5, QtGui.QColor(0, 0, 0, 180))
        # self.setMouseTracking(True)

        self.vl_main = QtWidgets.QVBoxLayout(self)
        self.vl_main.setContentsMargins(0, 0, 0, 0)
        self.vl_main.setSpacing(0)

        self._init_ui()

    def _init_ui(self):
        qss1 = '''/*滑动条槽（整体）的美化*/
        QSlider::groove:horizontal{height: 12px;left: 0px;right: 0px;
        border:0px;    /*指定无边框*/
        border-radius:6px;    /*指定圆角*/
        background:rgba(0,0,0,50);} 
        /*滑块的美化*/
        QSlider::handle:horizontal{width:  50px;height: 50px;
        margin-top: -20px; margin-left: 0px;
        margin-bottom: -20px;margin-right: 0px;
        border-image:url(:/res/images/setting_slider_handle.png);} 
        /*已滑过的进度美化*/
        QSlider::sub-page:horizontal{background:rgba(80,166,234,1);}
        '''
        qss = '''
        QSlider::groove:horizontal,QSlider::add-page:horizontal{
        height:3px;
        border-radius:3px;
        background:#18181a;
        }
        
        QSlider::sub-page:horizontal{
        height:8px;
        border-radius:3px;
        background:#008aff;
        }
        
        QSlider::handle:horizontal{
        width:12px;
        margin-top:-5px;
        margin-bottom:-4px;
        border-radius:6px;
        background:qradialgradient(spread:pad,cx:0.5,cy:0.5,radius:0.5,fx:0.5,fy:0.5,stop:0.6 #565656,stop:0.8 #565656);
        bacder-image:url(./res/images/live/GOUGOU.png)
        }

        QSlider::groove:vertical,QSlider::sub-page:vertical{
        width:8px;
        border-radius:3px;
        background:#D8D8D8;
        }
        
        QSlider::add-page:vertical{
        width:8px;
        border-radius:3px;
        background:#008aff;
        }
        
        QSlider::handle:vertical{
        height:12px;
        margin-left:-5px;
        margin-right:-4px;
        border-radius:6px;
        background:qradialgradient(spread:pad,cx:0.5,cy:0.5,radius:0.5,fx:0.5,fy:0.5,stop:0.6 #565656,stop:0.8 #565656);
        bacder-image:url(./res/images/live/GOUGOU.png)
        }
        '''

        # region 标题搜索栏
        hl_title = QtWidgets.QHBoxLayout()
        tb_setting = QtWidgets.QToolButton()
        le_search = QtWidgets.QLineEdit()
        tb_search = QtWidgets.QToolButton()
        hl_title.addWidget(tb_setting)
        hl_title.addStretch()
        hl_title.addWidget(le_search)
        hl_title.addWidget(tb_search)
        self.vl_main.addLayout(hl_title)
        # endregion

        # region 歌曲封面/歌词/歌名/演唱者
        wg_cover = QtWidgets.QWidget()
        lb_background = QtWidgets.QLabel(wg_cover)
        lb_lyrics = QtWidgets.QLabel(wg_cover)
        lb_name = QtWidgets.QLabel(wg_cover)
        lb_author = QtWidgets.QLabel(wg_cover)
        self.vl_main.addWidget(wg_cover)
        # endregion

        # region 播放进度条
        hl_progress = QtWidgets.QHBoxLayout()
        lb_now = QtWidgets.QLabel('0.00')
        sl_progress = QtWidgets.QSlider()
        sl_progress.setOrientation(QtCore.Qt.Horizontal)  # 水平方向
        sl_progress.setStyleSheet(qss)
        lb_length = QtWidgets.QLabel('4.98')
        hl_progress.addWidget(lb_now)
        hl_progress.addWidget(sl_progress)
        hl_progress.addWidget(lb_length)
        self.vl_main.addLayout(hl_progress)
        # endregion

        # region 歌曲控制条
        hl_controls = QtWidgets.QHBoxLayout()
        tb_prev = QtWidgets.QToolButton()
        tb_acting = QtWidgets.QToolButton()
        tb_next = QtWidgets.QToolButton()
        hl_controls.addWidget(tb_prev)
        hl_controls.addWidget(tb_acting)
        hl_controls.addWidget(tb_next)
        self.vl_main.addLayout(hl_controls)
        # endregion

        # region 声音控制条
        hl_voice = QtWidgets.QHBoxLayout()
        lb_low = QtWidgets.QLabel('0')
        sl_voice = QtWidgets.QSlider()
        sl_voice.setOrientation(QtCore.Qt.Horizontal)  # 水平方向
        lb_high = QtWidgets.QLabel('100')
        hl_voice.addWidget(lb_low)
        hl_voice.addWidget(sl_voice)
        hl_voice.addWidget(lb_high)
        self.vl_main.addLayout(hl_voice)
        # endregion

        # region 播放控制面板
        hl_plane = QtWidgets.QHBoxLayout()
        tb_order = QtWidgets.QToolButton()  # 播放顺次：单曲循环/随机/顺序播放
        tb_favourite = QtWidgets.QToolButton()
        tb_share = QtWidgets.QToolButton()
        tb_download = QtWidgets.QToolButton()
        tb_return = QtWidgets.QToolButton()  # 退回歌曲列表页面
        hl_plane.addWidget(tb_order)
        hl_plane.addWidget(tb_favourite)
        hl_plane.addWidget(tb_share)
        hl_plane.addWidget(tb_download)
        hl_plane.addWidget(tb_return)
        self.vl_main.addLayout(hl_plane)
        # endregion

    def paintEvent(self, event):
        # opt = QStyleOption()
        # opt.initFrom(self)
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)  # 抗锯齿
        # self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
        # super(Canvas, self).paintEvent(event)

        # image = Image.open(r'E:\Codes\res\background\bk2.jpg')
        # image = image.filter(MyGaussianBlur(radius=6))
        # image.save('./tmp.jpg')
        img_new = Utils.img_center(self.rect().width(), self.rect().height(),
                                   r'E:\Codes\res\background\bk2.jpg')
        p.setBrush(QtGui.QBrush(img_new))  # 图片刷子
        # p.setBrush(QtGui.QBrush(QtGui.QPixmap(r'E:\Codes\res\background\bk3.jpg')))  # 图片刷子
        # painter.setBrush(QBrush(Qt.blue))
        p.setPen(QtCore.Qt.transparent)

        rect = self.rect()
        # rect.setWidth(rect.width() - self.deep)
        # rect.setHeight(rect.height() - self.deep)
        p.drawRoundedRect(rect, self.radius, self.radius)
        # painterPath= QPainterPath()
        # painterPath.addRoundedRect(rect, 15, 15)
        # painter.drawPath(painterPath)

        # 直接填充图片
        # pix = QPixmap('./res/images/background11.jpg')
        # painter.drawPixmap(self.rect(), pix)

        super(FoWorld, self).paintEvent(event)


if __name__ == '__main__':
    import cgitb  # 相当管用

    # cgitb.enable(format='text')  # 解决 pyqt5 异常只要进入事件循环,程序就崩溃,而没有任何提示
    sys.excepthook = cgitb.enable(1, None, 5, '')
    app = QtWidgets.QApplication(sys.argv)
    w = FoWorld()
    w.show()
    sys.exit(app.exec_())
