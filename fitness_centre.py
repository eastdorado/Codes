#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Project : Puck
#  File    : test3
#  Date    : 2020/7/14 1:06
#  Site    : https://github.com/eastdorado
#  Author  : By cyh
#            QQ: 260125177
#            Email: 260125177@qq.com 
#  Copyright = Copyright (c) 2020 CYH
#  Version   = 1.0

import os
import sys
import math
import pyttsx3
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from functools import partial
import numpy as np
from enum import IntEnum, unique
import piexif
from utilities import Utils, EllipseButton, StyleSheet, MyJson, CustomBG


# import cgitb  # 相当管用

# cgitb.enable(format='text')  # 解决 pyqt5 异常只要进入事件循环,程序就崩溃,而没有任何提示


# sys.setrecursionlimit(10000)

class VideoDisplay(QWidget):
    def __init__(self, *args, **kwargs):
        super(VideoDisplay, self).__init__(*args, **kwargs)
        self.parent = args[0]

        # 默认视频源为相机
        self.ui.radioButtonCam.setChecked(True)
        self.isCamera = True

        # 信号槽设置
        ui.Open.clicked.connect(self.Open)
        ui.Close.clicked.connect(self.Close)
        ui.radioButtonCam.clicked.connect(self.radioButtonCam)
        ui.radioButtonFile.clicked.connect(self.radioButtonFile)

        # 创建一个关闭事件并设为未触发
        self.stopEvent = threading.Event()
        self.stopEvent.clear()

    def radioButtonCam(self):
        self.isCamera = True

    def radioButtonFile(self):
        self.isCamera = False

    def Open(self):
        if not self.isCamera:
            self.fileName, self.fileType = QFileDialog.getOpenFileName(self.mainWnd, 'Choose file', '', '*.mp4')
            self.cap = cv2.VideoCapture(self.fileName)
            self.frameRate = self.cap.get(cv2.CAP_PROP_FPS)
        else:
            # 下面两种rtsp格式都是支持的
            # cap = cv2.VideoCapture("rtsp://admin:Supcon1304@172.20.1.126/main/Channels/1")
            self.cap = cv2.VideoCapture("rtsp://admin:Supcon1304@172.20.1.126:554/h264/ch1/main/av_stream")

        # 创建视频显示线程
        th = threading.Thread(target=self.Display)
        th.start()

    def Close(self):
        # 关闭事件设为触发，关闭视频播放
        self.stopEvent.set()

    def Display(self):
        self.ui.Open.setEnabled(False)
        self.ui.Close.setEnabled(True)

        while self.cap.isOpened():
            success, frame = self.cap.read()
            # RGB转BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.ui.DispalyLabel.setPixmap(QPixmap.fromImage(img))

            if self.isCamera:
                cv2.waitKey(1)
            else:
                cv2.waitKey(int(1000 / self.frameRate))

            # 判断关闭事件是否已触发
            if True == self.stopEvent.is_set():
                # 关闭事件置为未触发，清空显示label
                self.stopEvent.clear()
                self.ui.DispalyLabel.clear()
                self.ui.Close.setEnabled(False)
                self.ui.Open.setEnabled(True)
                break


class ItemDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.decorationPosition = QtWidgets.QStyleOptionViewItem.Right
        super(ItemDelegate, self).paint(painter, option, index)


# 圆形图片按钮
class RoundButton(QPushButton):
    def __init__(self, img_src, img_hovered, img_pressed, parent=None):
        super(RoundButton, self).__init__(parent)
        # self.setEnabled(True)
        self.a = img_src
        self.b = img_hovered
        self.c = img_pressed
        self.hovered = False
        self.pressed = False
        self.color = QColor(Qt.gray)
        self.hightlight = QColor(Qt.lightGray)
        self.shadow = QColor(Qt.black)
        self.opacity = 1.0
        self.roundness = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if self.isEnabled():
            if self.hovered:
                self.color = self.hightlight.darker(250)
        else:
            self.color = QColor(50, 50, 50)

        button_rect = QRect(self.geometry())
        painter.setPen(QPen(QBrush(Qt.red), 2.0))
        painter_path = QPainterPath()
        # painter_path.addRoundedRect(1, 1, button_rect.width() - 2, button_rect.height() - 2, self.roundness,
        # self.roundness)
        painter_path.addEllipse(1, 1, button_rect.width() - 2, button_rect.height() - 2)
        painter.setClipPath(painter_path)
        if self.isEnabled():
            if not self.pressed and not self.hovered:
                icon_size = self.iconSize()
                icon_position = self.calculateIconPosition(button_rect, icon_size)
                painter.setOpacity(1.0)
                painter.drawPixmap(icon_position, QPixmap(QIcon(self.a).pixmap(icon_size)))
            elif self.hovered and not self.pressed:
                icon_size = self.iconSize()
                icon_position = self.calculateIconPosition(button_rect, icon_size)
                painter.setOpacity(1.0)
                painter.drawPixmap(icon_position, QPixmap(QIcon(self.b).pixmap(icon_size)))
            elif self.pressed:
                icon_size = self.iconSize()
                icon_position = self.calculateIconPosition(button_rect, icon_size)
                painter.setOpacity(1.0)
                painter.drawPixmap(icon_position, QPixmap(QIcon(self.c).pixmap(icon_size)))
        else:
            icon_size = self.iconSize()
            icon_position = self.calculateIconPosition(button_rect, icon_size)
            painter.setOpacity(1.0)
            painter.drawPixmap(icon_position, QPixmap(QIcon(self.a).pixmap(icon_size)))

    def enterEvent(self, event):
        self.hovered = True
        self.repaint()
        QPushButton.enterEvent(self, event)

    def leaveEvent(self, event):
        self.hovered = False;
        self.repaint()
        QPushButton.leaveEvent(self, event)

    def mousePressEvent(self, event):
        self.pressed = True
        self.repaint()
        QPushButton.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):

        self.pressed = False
        self.repaint()
        QPushButton.mouseReleaseEvent(self, event)

    def calculateIconPosition(self, button_rect, icon_size):

        x = (button_rect.width() / 2) - (icon_size.width() / 2)
        y = (button_rect.height() / 2) - (icon_size.height() / 2)

        width = icon_size.width()
        height = icon_size.height()

        icon_position = QRect()
        icon_position.setX(x)
        icon_position.setY(y)
        icon_position.setWidth(width)
        icon_position.setHeight(height)

        return icon_position


class TitleBar(QtWidgets.QWidget):
    StyleSheet = """
    /*标题栏*/
    TitleBar {
        /*background: transparent;     全透明*/
        /*background-color: skyblue;   */
        /*background-color: rgba(0,0,0,50);   半透明*/
        background: rgba(0, 0, 0, 50);  /*半透明*/
        border-top-right-radius:15;
        /*background-image:url(./res/background/bk5.jpg);*/
        background-repeat: no-repeat;       /*背景不要重复*/
        background-position: center center;      /*图片的位置，居中，靠左对齐*/
    }
    /*最小化最大化关闭按钮通用默认背景*/
    #buttonMinimum,#buttonMaximum,#buttonClose {
        /*background-color: skyblue;*/
        /*background:rgba(0,0,0,0.3)      半透明*/
        border:none;    /*全透明*/
        color:rgb(0, 200, 200)
    }
    /*悬停*/
    #buttonMinimum:hover,#buttonMaximum:hover {
        /*background-color: green;*/
        /*color: red;放在下面的前面才有效果*/
        background:rgba(0,0,0,0.2)     /*半透明*/
    }
    /*鼠标按下不放*/
    #buttonMinimum:pressed,#buttonMaximum:pressed {
        /*background-color: Firebrick;*/
        /*color: blue;放在下面的前面才有效果*/
        background:rgba(0,0,0,0.4)      /*半透明*/
    }
    #buttonClose:hover {
        color: red;
        /*background-color: gray;*/
        /*background:rgba(0,0,0,0.4)      半透明*/
    }
    #buttonClose:pressed {
        color: red;
        /*background-color: Firebrick;*/
        /*background:rgba(0,0,0,0.4)      半透明*/
    }
    """

    # region 信号声明区
    # sign_pb_prev = pyqtSignal()  # 前一个
    # sign_pb_next = pyqtSignal()  # 后一个
    sign_win_minimize = QtCore.pyqtSignal()  # 窗口最小化信号
    sign_win_maximize = QtCore.pyqtSignal()  # 窗口最大化信号
    sign_win_resume = QtCore.pyqtSignal()  # 窗口恢复信号
    sign_win_close = QtCore.pyqtSignal()  # 窗口关闭信号
    sign_win_move = QtCore.pyqtSignal(QtCore.QPoint)  # 窗口移动

    # endregion

    def __init__(self, *args, **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)

        self.setStyleSheet(TitleBar.StyleSheet)

        self.setMouseTracking(True)
        # 窗体透明，控件不透明
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)  # 支持qss设置背景
        self.mPos = None
        self.iconSize = 20  # 图标的默认大小
        # 设置默认背景颜色,否则由于受到父窗口的影响导致透明
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(palette.Window, QtGui.QColor(240, 240, 240))
        self.setPalette(palette)

        # 布局
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 0, 0)

        # 窗口左图标
        self.lb_icon = QtWidgets.QLabel(self)
        self.lb_icon.setPixmap(QtGui.QPixmap('./res/images/star.png'))
        # self.lb_icon.setScaledContents(True)
        # self.lb_icon.setFixedWidth(100)
        # self.lb_icon.setStyleSheet('background: transparent; ')
        layout.addWidget(self.lb_icon)

        # pb_prev = QPushButton('前一个', self, clicked=self.sign_pb_prev.emit)
        # pb_prev.setStyleSheet('color:red')
        # 窗口标题
        layout.addStretch()
        self.lb_title = QtWidgets.QLabel(self.tr('运动达人'), self)
        self.lb_title.setMargin(2)
        self.lb_title.setStyleSheet(
            'color: rgb(255, 255, 0);font-size:24px;font-weight:bold;font-family:Roman times;')
        # pb_next = QPushButton('后一个')
        # layout.addWidget(pb_prev)
        layout.addWidget(self.lb_title)
        # layout.addWidget(pb_next)
        layout.addStretch()
        # 中间伸缩条
        # layout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        # 利用Webdings字体来显示图标
        font = self.font() or QtGui.QFont()
        font.setFamily('Webdings')

        # 最小化按钮
        self.min_button = QtWidgets.QPushButton(
            '0', self, clicked=self.sign_win_minimize.emit, font=font, objectName='buttonMinimum')
        # self.min_button.setAutoFillBackground(False)
        # self.min_button.setStyleSheet("background-color: rgb(28, 255, 3);")
        # self.min_button.setAutoDefault(False)
        # self.min_button.setDefault(False)
        # self.min_button.setFlat(False)
        layout.addWidget(self.min_button)
        # 最大化/还原按钮
        self.buttonMaximum = QtWidgets.QPushButton(
            '1', self, clicked=self.showMaximized, font=font, objectName='buttonMaximum')
        layout.addWidget(self.buttonMaximum)
        # 关闭按钮
        self.buttonClose = QtWidgets.QPushButton(
            'r', self, clicked=self.sign_win_close.emit, font=font, objectName='buttonClose')
        layout.addWidget(self.buttonClose)
        # 初始高度
        self.setHeight()

    def showMaximized(self):
        if self.buttonMaximum.text() == '1':
            # 最大化
            self.buttonMaximum.setText('2')
            self.sign_win_maximize.emit()
        else:  # 还原
            self.buttonMaximum.setText('1')
            self.sign_win_resume.emit()

    def setHeight(self, height=38):
        """设置标题栏高度"""
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        # 设置右边按钮的大小
        self.min_button.setMinimumSize(height, height)
        self.min_button.setMaximumSize(height, height)
        self.buttonMaximum.setMinimumSize(height, height)
        self.buttonMaximum.setMaximumSize(height, height)
        self.buttonClose.setMinimumSize(height, height)
        self.buttonClose.setMaximumSize(height, height)

    def setTitle(self, title):
        """设置标题"""
        self.lb_title.setText(title)

    def setIcon(self, icon):
        """设置图标"""
        self.iconLabel.setPixmap(icon.pixmap(self.iconSize, self.iconSize))

    def setIconSize(self, size):
        """设置图标大小"""
        self.iconSize = size

    def mouseDoubleClickEvent(self, event):
        super(TitleBar, self).mouseDoubleClickEvent(event)
        self.showMaximized()

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()  # widget窗口左上角相对于电脑屏幕的左上角的（x=0,y=0）偏移位置
            # pos = QtGui.QMouseEvent()
            # self.mPos = event.globalPos()  # 鼠标偏离电脑屏幕左上角（x=0,y=0）的位置
        event.accept()

    def mouseReleaseEvent(self, event):
        """鼠标弹起事件"""
        self.mPos = None
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.mPos:
            # 需要在主窗体隐藏后减去背景窗体的margins
            self.sign_win_move.emit(self.mapToGlobal(event.pos() - self.mPos - QtCore.QPoint(15, 15)))
            # self.sign_win_move.emit(event.globalPos() - self.mPos)
        event.accept()

    def enterEvent(self, event):
        self.setCursor(QtGui.QCursor(Qt.PointingHandCursor))  # 更改鼠标图标
        super(TitleBar, self).enterEvent(event)
        event.accept()

    def leaveEvent(self, event):
        self.setCursor(QtGui.QCursor(Qt.ArrowCursor))
        event.accept()

    def wheelEvent(self, event):
        event.accept()


@unique  # @unique 装饰器可以帮助我们检查保证value没有重复值
class Const(IntEnum):
    # 继承于Enum的枚举类中的Key不能相同，Value可以相，
    # 要Value也不能相同，那么在导入Enum的同时，需要导入unique函数
    # 枚举项可以用来比较，使用==，或者is。枚举类不能用来实例化对象,在类外部不能修改Value值
    CENTER = '0'
    TOP = 1
    BOTTOM = '2'
    LEFT = 3
    RIGHT = 4
    TL_CORNER = 5  # 左上角
    TR_CORNER = 6  # 右上角
    BL_CORNER = 7
    BR_CORNER = 8

    PADDING = 20  # 鼠标跟踪边框的边距，>=margin
    MARGIN = 15  # 四周边距


class MyQLabel(QLabel):
    clicked = pyqtSignal()  # 自定义单击信号
    DoubleClicked = pyqtSignal()  # 自定义双击信号

    def __init__(self, *args, **kwargs):
        super(MyQLabel, self).__init__(*args, **kwargs)
        # self.setFixedSize(200, 200)
        self.setMouseTracking(True)  # 鼠标移动跟踪
        # self.setScaledContents(True)  # 图片自适应QLabel大小

        self.img = None

    def set(self, img, border=0, padding=0, color=None, background_color=None, border_color=None):

        width, height = self.width(), self.height()
        wide = min(width, height)

        radius = wide // 2 + padding + border

        color = 'blue' if color is None else color
        background_color = 'green' if background_color is None else background_color
        border_color = 'gray' if border_color is None else border_color

        qss = None
        if img:
            pix = QtGui.QImage(img)

            ratio_w = pix.width() / width
            ratio_h = pix.height() / height

            is_w = True if ratio_w > ratio_h else False
            # print(sw, sh, is_w)

            img_new = pix.scaledToWidth(height) if is_w else pix.scaledToHeight(width)
            new_img = './tmp.jpg'
            img_new.save(new_img)
            # self.setAutoFillBackground(True)  # /Widget增加背景图片时，这句一定要。
            # wide = min(width, height)
            # pix = QtGui.QPixmap(img).scaled(wide, wide, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
            # self.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(img_new)))
            # self.setIconSize(QtCore.QSize(wide, wide))
            # self.setFlat(True)  # 就是这句能够实现按钮透明，用png图片时很有用
            # border = 0  # 消除边框，取消点击效果

            qss = '''
                color: %s;
                background-color: %s;
                background: transparent;     /*全透明*/
                background-image:url(%s);
                background-position: center center;      /*图片的位置，居中，靠左对齐*/
                background-repeat: no-repeat;       /*背景不要重复*/

                border-style:none;
                border:%dpx solid %s; 
                padding:%dpx;
                min-width:%dpx;max-width:%dpx;
                min-height:%dpx;max-height:%dpx;            
                border-radius:%dpx;
                ''' % (color, background_color, new_img, border, border_color, padding,
                       width, width, height, height, radius)
        else:
            qss = '''
                color: %s;
                background-color: %s;

                border-style:none;
                border:%dpx solid %s; 
                padding:%dpx;
                min-width:%dpx;max-width:%dpx;
                min-height:%dpx;max-height:%dpx;            
                border-radius:%dpx;
                ''' % (color, background_color, border, border_color, padding,
                       width, width, height, height, radius)
        # print(qss)
        self.setStyleSheet(qss)

        # radius = width // 2 + padding + border if width < height else height // 2 + padding + border
        # color = 'blue' if color is None else color
        # background_color = 'green' if background_color is None else background_color
        # border_color = 'gray' if border_color is None else border_color
        #
        # qss = None
        # if img:
        #     qss = '''
        #         color: %s;
        #         background-color: %s;
        #         background-image:url(%s);
        #
        #         border-style:none;
        #         border:%dpx solid %s;
        #         padding:%dpx;
        #         min-width:%dpx;max-width:%dpx;
        #         min-height:%dpx;max-height:%dpx;
        #         border-radius:%dpx;
        #         ''' % (color, background_color, img, border, border_color, padding, width, width,
        #                height, height, self.radius)
        # else:
        #     qss = '''
        #         color: %s;
        #         background-color: %s;
        #
        #         border-style:none;
        #         border:%dpx solid %s;
        #         padding:%dpx;
        #         min-width:%dpx;max-width:%dpx;
        #         min-height:%dpx;max-height:%dpx;
        #         border-radius:%dpx;
        #         ''' % (color, background_color, border, border_color, padding,
        #                width, width, height, height, radius)
        # # print(qss)
        # self.setStyleSheet(qss)

    @staticmethod
    def get_round_pixmap(pix_src, radius):
        if not pix_src:
            return QPixmap()

        size = QSize(2 * radius, 2 * radius)
        mask = QtGui.QBitmap(size)
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.fillRect(0, 0, size.width(), size.height(), Qt.white)
        painter.setBrush(QColor(0, 0, 0))
        painter.drawRoundedRect(0, 0, size.width(), size.height(), 99, 99);
        image = QPixmap(pix_src.scaled(size))
        image.setMask(mask)

        return image

    def set_img(self, img_file):
        self.img = img_file

    # def show_circle_img(self, img_file, scale=1.0):
    #     assert img_file, "参数错误"
    #
    #     #     # 显示圆形图标
    #     #     label.setStyleSheet('min-width:  100px;max-width:  100px;'
    #     #                     'min-height: 100px;max-height: 100px;'
    #     #                     'border-radius: 50px;border-width: 0 0 0 0;'
    #     #                     'border-image: url(./res/images/water.png) 0 0 0 0 stretch')
    #
    #     # 设置椭圆的长轴、短轴
    #     sw = self.width()
    #     sh = self.height()
    #
    #     pix = QtGui.QPixmap(img_file)
    #
    #     pix_new = QtGui.QPixmap(sw, sh)
    #     pix_new.fill(QtCore.Qt.transparent)
    #     painter = QtGui.QPainter(pix_new)
    #     painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
    #
    #     path = QtGui.QPainterPath()
    #     path.addEllipse(0, 0, sw, sh)  # 绘制椭圆
    #     painter.setClipPath(path)
    #
    #     painter.drawPixmap(0, 0, sw, sh, pix)
    #     # self.setPixmap(img_file)

    # 重写鼠标单击事件
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super(MyQLabel, self).resizeEvent(a0)
        self.show_center_img()

    def mousePressEvent(self, QMouseEvent):  # 单击
        self.clicked.emit()

    # 重写鼠标双击事件
    def mouseDoubleClickEvent(self, QMouseEvent):  # 双击
        self.DoubleClicked.emit()

    # 在widget四周画阴影
    # def paintEvent(self, event):
    #     m = 9
    #     path = QtGui.QPainterPath()
    #     path.setFillRule(Qt.WindingFill)
    #     path.addRect(m, m, self.width() - m * 2, self.height() - m * 2)
    #     painter = QtGui.QPainter(self)
    #     # painter.setRenderHint(QPainter.Antialiasing, True)
    #     painter.fillPath(path, QtGui.QBrush(Qt.white))
    #
    #     color = QColor(250, 100, 100, 30)
    #     # for(int i=0; i<10; i++)
    #
    #     for i in range(m):
    #         path = QtGui.QPainterPath()
    #         path.setFillRule(Qt.WindingFill)
    #         path.addRoundedRect(m - i, m - i, self.width() - (m - i) * 2, self.height() - (m - i) * 2, 1, 1)
    #
    #         al = 90 - math.sqrt(i) * 30
    #         # print(al)
    #         color.setAlpha(int(al))
    #         painter.setPen(QtGui.QPen(color, 1, Qt.SolidLine))
    #         painter.drawRoundedRect(QtCore.QRect(m - i, m - i, self.width() - (m - i) * 2, self.height() - (m - i) * 2),
    #                                 0, 0)


class ChildMenu(QWidget):
    def __init__(self):
        super(ChildMenu, self).__init__()
        self.parent = None
        self.menu_data = [
            [(QIcon(), '运动资源'), (QIcon(), '文案'), (QIcon(), '视频'), (QIcon(), '网页')],
            [(QIcon(), '锻炼部位'), (QIcon(), '手臂'), (QIcon(), '肩背'), (QIcon(), '腰腹'), (QIcon(), '腿部')],
            [(QIcon(), '个性规划'), (QIcon(), '占位')],
            [(QIcon(), '数据指数'), (QIcon(), '占位')],
            [(QIcon(), '设置'), (QIcon(), '占位')]
        ]
        self.button_width = 40
        self.button_spacing = 10
        self.button_margin = 10
        self.stack_index = 0
        # self.setFixedHeight(self.parent.parent.menu_height)
        # self.resize(800, 60)
        self.stacked_menu = QStackedWidget()
        # self.raise_()  # 非主窗口中窗口置顶

        # self.setMouseTracking(True)
        # self.stacked_menu.setMouseTracking(True)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)  # 设置无边框窗口
        # self.setWindowModality(Qt.ApplicationModal)# 窗口置顶
        # self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool |  # 窗体总在最前端
        #                     Qt.MSWindowsFixedSizeDialogHint |
        #                     Qt.WindowCloseButtonHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        self.setObjectName('child')
        self.setStyleSheet('QWidget#child {'
                           'background-color: #0f0 ;'
                           'border-top-right-radius:10;'
                           'border-bottom-right-radius:10;}')
        self.stacked_menu.setObjectName('stack')
        self.stacked_menu.setStyleSheet('#stack {background: transparent;     /*全透明*/'
                                        '/*background: rgb(52, 252, 152);*/'
                                        'border-top-right-radius:10;'
                                        'border-bottom-right-radius:10;}')

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        # b = QPushButton('dadgslajl')
        # layout.addWidget(b)
        layout.addWidget(self.stacked_menu)
        # self.stacked_menu.setContentsMargins(0, 0, 0, 0)

        # self.init_stack_menu(data_menu, None)
        # self.set_stack_index(1)
        self.hide()
        # self.show()

    def init_stack_menu(self, menu_data, father):
        self.menu_data = menu_data
        self.parent = father
        # print(type(father))

        for each in menu_data:
            wg_sub_menu = QWidget()
            # wg_sub_menu.setMouseTracking(True)
            wg_sub_menu.setObjectName(each[0][1])
            qss_wg = '#%s {background-color: rgb(164, 185, 55);' \
                     'border-color: rgb(170, 150, 163);' \
                     'color: rgb(26, 55, 246);}' \
                     'QPushButton{font-size:22px;font-weight:bold;font-family:Roman times;' \
                     'width:%dpx; color:blue;}' % (each[0][1], self.button_width)
            wg_sub_menu.setStyleSheet(qss_wg)
            lh = QHBoxLayout(wg_sub_menu)
            lh.setContentsMargins(self.button_margin, 0, self.button_margin, 0)
            lh.setSpacing(self.button_spacing)
            # print(type(each[1:]), each[1:])
            for btn in each[1:]:
                pb = QPushButton(QIcon(btn[0]), btn[1], self)
                # pb.setMouseTracking(True)
                pb.clicked.connect(self.slot_pb_clicked)
                # pb.setStyleSheet('font-size:20px;font-weight:bold;font-family:Roman times;'
                #                  'width:%dpx; color:rgb(200,120,10,255);' % self.button_width)
                lh.addWidget(pb)
            self.stacked_menu.addWidget(wg_sub_menu)

    def slot_pb_clicked(self):
        self.setWindowModality(Qt.WindowModal)
        self.hide()
        sender = self.sender()  # 获取发送控件
        self.parent.parent.submenu_clicked(sender.text())

    def select_stack(self, stack_index):
        self.stack_index = stack_index
        self.stacked_menu.setCurrentIndex(stack_index)

        # 把别的控件都隐藏，看看能改变大小不
        # print(self.stacked_menu.size())
        # for each in
        # for children in self.findChildren(QWidget):
        #     shadow = QGraphicsDropShadowEffect(blurRadius=15, xOffset=5, yOffset=5, color=QColor(0, 0, 0, 255))
        #     children.setGraphicsEffect(shadow)
        btn_count = len(self.menu_data[self.stack_index]) - 1
        width = btn_count * self.button_width + 2 * self.button_margin
        width += self.button_spacing * (btn_count - 1)
        height = self.parent.parent.menu_height
        # print(width, height)
        self.resize(width, height)
        self.stacked_menu.resize(width, height)

    # def show(self) -> None:
    #     print('child show')
    #     super(ChildMenu, self).show()

    def enterEvent(self, a0: QtCore.QEvent):
        # print('child enter', a0.pos())
        self.setWindowModality(Qt.ApplicationModal)
        # self.setCursor(Qt.OpenHandCursor)
        return super().enterEvent(a0)

    def leaveEvent(self, e: QEvent):
        # here the code for mouse leave
        self.setWindowModality(Qt.WindowModal)
        pos = self.mapFromGlobal(QCursor.pos())  # 获得鼠标相对位置
        # pos = e.pos()
        # print(type(pos), pos)
        if pos.x() <= self.parent.width():  # parent.left_width:
            # self.setCursor(Qt.ArrowCursor)
            pass
        else:
            self.hide()
        # print('child leave')
        # self.parent.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        e.accept()

    # def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
    #
    #     print('child move',a0.pos())


class MyQListWidget(QListWidget):
    def __init__(self, *args, **kwargs):
        super(MyQListWidget, self).__init__(*args, **kwargs)
        self.parent = args[0]
        assert isinstance(self.parent, Canvas), '列表的父窗体不正确'
        self.child = self.parent.sub_menu
        assert isinstance(self.child, ChildMenu), '列表的子菜单窗体不正确'

        self.cur_row = -1  # 换行标志
        self.is_done = False  # 动画完成
        self._animation = None

        self.initAnimation(self.child)
        self.setMouseTracking(True)
        # self.setAcceptsHoverEvents(True)
        # self.setFlags(QListWidget.ItemIsSelectable |
        #               QListWidgetItem.ItemIsMovable)

    def mouseMoveEvent(self, e: QMouseEvent):
        # sender = self.sender()
        # print('dfa', type(sender))
        # index = self.indexAt(e.pos())  #
        # row1 = index.row()
        item = self.itemAt(e.pos())
        # size = self.sizeHint()  # 尺寸
        # size = item.sizeHint()
        row = self.row(item)
        # row1 = e.pos().y() // size.height()
        if row != self.cur_row:  # 换行了，换新菜单
            # print(item.text(), row, self.child)

            self.cur_row = row
            self.child.select_stack(row)

            # if self.is_done:
            #     self.child.hide()
            # self.is_done = True

            x = self.parent.left_width
            y = (row * self.parent.menu_height)
            cw, ch = self.child.width(), self.child.height()

            # print('fe', self.pos(), e.pos())
            # print(self.mapToGlobal(self.pos()),e.globalPos())
            # 这里需要减法，由上面实验得出
            y += (self.mapToGlobal(self.pos()) - self.pos()).y()
            x += self.mapToGlobal(self.pos()).x()

            self.child.move(x, y)
            # self.child.setWindowModality(Qt.ApplicationModal)

            # self._animation.stop()
            # self._animation.setStartValue(QRect(x, y, 0, ch))
            # self._animation.setEndValue(QRect(x, y, cw, ch))
            # self._animation.start()
            # 参数 QAbstractAnimation.KeepWhenStopped  停止时不会删除动画
            #     QAbstractAnimation.DeleteWhenStopped   停止时动画将自动删除

            self.child.show()  # frameGeometry必须显示后用

        # e.ignore()

    def leaveEvent(self, e: QtCore.QEvent):
        # here the code for mouse leave
        # print('list leave')
        self.setCursor(Qt.ArrowCursor)
        self.cur_row = -1
        self.is_done = False
        pos = self.mapFromGlobal(QCursor.pos())  # 获得鼠标相对位置
        # pos = e.pos()
        # print(type(pos), pos)
        if pos.x() >= self.parent.left_width:
            # self.child.grabMouse()  # 得到正在捕获鼠标事件的窗口
            # 设置鼠标穿透
            # self.parent.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            # self.child.setWindowModality(Qt.ApplicationModal)
            pass
        else:
            self.child.hide()

        e.accept()

    #     # # 获取item里button
    #     # button = self.sender()
    #     # # 获取按钮相对于listwwdget的坐标
    #     # # listwidget 相对于窗体的坐标 减去 button 相对于窗体的坐标
    #     # buttonpos = button.mapToGlobal(QPoint(0, 0)) - self.listwidget.mapToGlobal(QPoint(0, 0))
    #     # # 获取到对象
    #     # item = self.listwidget.indexAt(buttonpos)
    #     # print(item)
    #     # # 获取位置
    #     # print(item.row())
    #
    def enterEvent(self, e: QEvent):
        # here the code for mouse hover
        self.child.setWindowModality(Qt.WindowModal)
        self.setCursor(Qt.PointingHandCursor)
        # print('enter')

    # def mousePressEvent(self, e: QMouseEvent):
    #     self.mouseMoveEvent(e)
    #
    #     print('press')
    #     # if event.buttons() == Qt.LeftButton:
    #     #     self.setCursor(Qt.OpenHandCursor)
    #     #     self.parent.m_drag = True
    #     #     self.parent.m_DragPosition = event.globalPos() - self.parent.pos()
    #     # event.accept()
    #     e.ignore()

    # # def hoverEnterEvent(self, event):
    # #     print('Enter')
    # #     # accept()        # 表示事件已处理，不需要向父窗口传播
    # #     # buttons()  # 返回哪个鼠标按键被按住了。
    # #     # ignore()        # 表示事件未处理，继续向父窗口传播
    #
    # # def hoverLeaveEvent(self, event):
    # #     print('Leave')
    # #
    # # def hoverMoveEvent(self, event):
    # #     print('Moving')
    #
    # """重写鼠标事件，实现窗口拖动。"""

    # item.setText(name)  # 设置
    # item_name = item.text()  # 获取
    # item.setData(Qt.UserRole, name)  # 设置
    # item_name = item.data(Qt.UserRole)  # 获取
    #
    # try:
    #     if event.buttons() and Qt.LeftButton:
    #         self.parent.move(event.globalPos() - self.parent.m_DragPosition)  # move将窗口移动到指定位置
    #         event.accept()
    # except AttributeError:
    #     pass
    # event.ignore()

    # def mouseReleaseEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.m_drag = False
    #         self.unsetCursor()

    # 菜单动画显示

    # def contextMenuEvent(self, event):
    #     pos = event.globalPos()
    #     print('右键菜单')
    #     size = self._contextMenu.sizeHint()
    #     x, y, w, h = pos.x(), pos.y(), size.width(), size.height()
    #     self._animation.stop()
    #     self._animation.setStartValue(QRect(x, y - h // 2, 0, 0))
    #     self._animation.setEndValue(QRect(x, y - h // 2, w, h))
    #     self._animation.start()
    #     self._contextMenu.exec_(event.globalPos())
    #     # self._contextMenu.exec_(QPoint(x, y+h//2))
    #

    # def initMenu(self):
    #     self._contextMenu = QMenu(self)
    #     self._contextMenu.addAction('菜单1', self.hello)
    #     self._contextMenu.addAction('菜单2', self.hello)
    #     self._contextMenu.addAction('菜单3', self.hello)
    #     self._contextMenu.addAction('菜单4', self.hello)
    #     self._contextMenu.addAction('菜单5', self.hello)
    #     self._contextMenu.addAction('菜单6', self.hello)

    def initAnimation(self, control):
        # 按钮动画
        self._animation = QPropertyAnimation(control, b'geometry', self)
        self._animation.setEasingCurve(QEasingCurve.Linear)
        self._animation.setDuration(300)
        # easingCurve 修改该变量可以实现不同的效果
        # s = self._animation.loopCount()  # 返回动画总循环次数
        # print(s)


# 动作幕布/画布
class Curtain(QWidget):
    def __init__(self, parent):
        super(Curtain, self).__init__(parent)
        self.parent = parent
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.use_palette()

        self.data_dir = None
        self.is_carousel = False  # 轮播展示还是单幅图展示
        self.is_acting = False  # 动作图还是封面图
        self.title = ''  # 标题
        self.resume = ''  # 简介
        self.notice = []  # 每天所有锻炼动作的总体要求，以及组数，次数，休息时间
        self.action = []  # 每天的所有锻炼动作，名称、要领、动图示范
        self.cur_act = 0  # 当前动作
        self.cover = []  # 封面图
        self.cur_cov = 0

        self.stay = 60  # 动作之间停留的秒数
        # self.engine = pyttsx3.init()  # 初始化语音库
        self.timer = QTimer(self)  # 初始化一个定时器

        self.pb_style = QPushButton('显示封面')
        self.pb_prev = QPushButton("前图")
        self.pb_next = QPushButton("后图")
        self.pb_model = QPushButton('翻看')

        self.lb_title = QLabel()  # 每个锻炼计划的标题
        self.lb_resume = QLabel()  # 每个锻炼计划的标题及意义
        self.lb_notice = QLabel()  # 当日提示
        self.lb_gist = QLabel()  # 锻炼步骤
        self.lb_img = QLabel()  # 锻炼动图
        self.movie = QMovie()  # 锻炼动图

        self.init_ui()
        # self.clear()
        # self.data_serialize(r'E:\dumbbell\plan\16图')
        # self.start()

        Utils.center_win(self)

    def init_ui(self):
        # font = QtGui.QFont('微软雅黑', 15)
        # self.setFont(font)
        self.timer.timeout.connect(self._motion)  # 每次计时到时间时发出信号

        # region 自定义工具栏
        toolbar = QFrame()
        toolbar.setObjectName('w')
        toolbar.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        toolbar.setFrameStyle(QFrame.NoFrame | QFrame.Raised)  # Box
        # ./res/background/bk5.jpg
        Utils.bg_trans('./tmp.png', 200, 100, (255, 255, 255, 100))
        toolbar.setStyleSheet(
            "background-image:url(./tmp.png); /*  */"
            "/*background-color: cyan;   */"
            "/*color:red;  */"
            "font-size:24px;font-weight:bold;font-family:微软雅黑;")

        lh = QHBoxLayout(toolbar)

        lb = QLabel('占位')
        # wg.setFixedWidth(20)
        lb.setPixmap(Utils.bg_trans('', 200, 100, (255, 55, 255, 120)))
        # wg.setVisible(False)

        self.pb_style.setEnabled(False)
        self.pb_prev.setEnabled(False)
        self.pb_next.setEnabled(False)
        self.pb_model.setEnabled(False)
        self.pb_style.clicked.connect(partial(self.slot_tools_clicked, self.pb_style))
        self.pb_prev.clicked.connect(partial(self.slot_tools_clicked, self.pb_prev))
        self.pb_next.clicked.connect(partial(self.slot_tools_clicked, self.pb_next))
        self.pb_model.clicked.connect(partial(self.slot_tools_clicked, self.pb_model))

        lh.addWidget(self.pb_style)
        lh.addWidget(self.pb_prev)
        lh.addWidget(self.pb_next)
        # lh.addWidget(lb)
        lh.addWidget(self.pb_model)
        # endregion

        # region 工作区
        self.lb_title.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.lb_title.setAlignment(Qt.AlignCenter)
        self.lb_title.setStyleSheet(
            "background:white;color:rgba(255,0,0,255);"
            "font-size:26px;font-weight:bold;font-family:微软雅黑;")

        self.lb_resume.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.lb_resume.setWordWrap(True)
        self.lb_resume.setStyleSheet(
            "background:white;color:rgba(0,255,0,255);"
            "font-size:24px;font-weight:bold;font-family:微软雅黑;")

        self.lb_notice.setAlignment(Qt.AlignCenter)
        self.lb_notice.setWordWrap(True)
        self.lb_notice.setStyleSheet(
            "background:white;color:blue;"
            "font-size:24px;font-weight:bold;font-family:微软雅黑;")

        self.lb_gist.setVisible(False)
        self.lb_gist.setWordWrap(True)
        # self.lb_gist.setMinimumWidth(100)
        self.lb_gist.setStyleSheet(
            "background:white;color:green;border: 2px solid gray;"
            "font-size:24px;font-weight:bold;font-family:微软雅黑;")

        self.lb_img.setMinimumSize(400, 400)
        self.lb_img.setMaximumSize(800, 800)
        self.lb_img.setAlignment(Qt.AlignCenter)
        self.lb_img.setStyleSheet("background: transparent;     /*全透明*/;"
                                  "border: 0px solid green")
        # self.lb_img.setScaledContents(True)

        self.movie.setScaledSize(self.lb_img.size())  # 设置GIF位置以及大小和 label一致
        # speed = self.movie.speed()
        # print(speed)
        # self.movie.setSpeed(100)
        # self.movie.setSpeed(self.movie.speed() -100)
        # self.engine.setProperty('rate', self.engine.getProperty('rate') - 50)  # 设置语速
        # self.engine.setProperty('volume', self.engine.getProperty('volume') + 5)  # 设置音量

        # voices = self.engine.getProperty('voices')  # 选择语音
        # # for voice in voices:
        # #     print(voice.id, voice.languages)
        # self.engine.setProperty("voice", voices[0].id)
        # endregion

        # region 总布局
        lv_main = QVBoxLayout(self)
        lv_main.setContentsMargins(10, 0, 10, 0)
        lv_main.addWidget(toolbar)
        lv_main.addWidget(self.lb_title)
        lv_main.addWidget(self.lb_resume)
        lv_main.addWidget(self.lb_notice)
        lv_main.addStretch()
        lv_main.addWidget(self.lb_gist)
        lv_main.addWidget(self.lb_img)
        lv_main.addStretch()
        # lv_main.setAlignment(Qt.AlignHCenter)
        # endregion

    def set_title(self, title):
        self.title = title
        self.lb_title.setText(title)

    # 初始化数据
    def data_serialize(self, data_dir):
        # data = [
        #     "       大部分的初学者都会选这哑铃这个器械来锻炼身体但却不知道哑铃的各个部位的锻炼方法，"
        #     "今天小编也给大家整理了15个哑铃动作，这大大福利可要拿稳啦。",
        #     "每个动作为一组，每组1-2分钟，组间休息30s，记得练习!",
        #     1,
        #     50,
        #     30,
        #     [
        #         "动作一:双手哑铃弯举",
        #         "动作方法: 双手各握一哑铃;掌心向前 将哑铃向上弯举 上弯举至顶峰状态,收紧肱二头肌，稍停 然后控制还原 到初始状态，重复以上动作。",
        #         "1.gif"
        #     ],
        #     [
        #         "动作二:哑铃交替弯举",
        #         "动作方法: 双手持哑铃垂于体侧，掌心相对，两肘靠身体两侧 以肘关节为支点，向上弯举 同时前臂外旋掌心朝上，举至最高点收紧肱二头肌，稍停 然后控制还原 到初始状态，重复以上动作。",
        #         "2.gif"
        #     ]
        # ]
        self.data_dir = data_dir

        self.cover = Utils.files_in_dir(self.data_dir, ['.jpg', '.jpeg', '.tiff', '.bmp', '.png'], True)
        files = Utils.files_in_dir(self.data_dir, ['.json'], True)
        # print('dd', self.cover, files)
        if files:
            file = files[0]
            # MyJson.write(data, file)/{data_dir}.json
            data = MyJson.read(file)
            self.resume = data[0]
            self.notice = data[1:5]
            self.action = data[5:]
            # print(data)

        if self.cover or files:
            # 子控件失效的设置
            self.pb_style.setEnabled(True)
            self.pb_model.setEnabled(True)
            self.pb_next.setEnabled(True)
            self.pb_prev.setEnabled(True)

    # 初始化数据前的清理
    def clear(self):
        self.data_dir = None
        self.is_carousel = False  # 轮播还是静态展示
        self.is_acting = False  # 开始锻炼还是展示封面
        self.title = ''  # 标题
        self.resume = ''  # 简介
        self.notice.clear()  # 每天所有锻炼动作的总体要求，以及组数，次数，休息时间
        self.action.clear()  # 每天的所有锻炼动作，名称、要领、动图示范
        self.cur_act = 0  # 当前动作
        self.cover.clear()  # 封面图
        self.cur_cov = 0
        self.timer.stop()

        self.lb_title.clear()
        self.lb_resume.clear()  # 每个锻炼计划的标题及意义
        self.lb_notice.clear()  # 当日提示
        self.lb_gist.clear()  # 锻炼步骤
        self.lb_img.clear()  # 锻炼动图
        self.movie.stop()  # 锻炼动图

        # 子控件失效的设置
        self.pb_style.setText("显示封面")
        self.pb_model.setText("翻看")
        self.pb_style.setEnabled(False)
        self.pb_prev.setEnabled(False)
        self.pb_next.setEnabled(False)
        self.pb_model.setEnabled(False)
        # for children in self.toolbar.findChildren(QWidget):
        #     children.setEnabled(False)

    def slot_tools_clicked(self, pb: QPushButton):
        # sender = self.toolbar.sender()
        name = pb.text()
        print(name)
        if name in ['显示封面', '显示动作']:
            self.is_acting = bool(1 - self.is_acting)  # 取反
            pb.setText('显示动作') if self.is_acting else pb.setText('显示封面')
            self.start(self.is_acting)
        elif name == '前图':
            self.prev()
        elif name == '后图':
            self.next()
        elif name in ['轮播', '翻看']:
            self.is_carousel = bool(1 - self.is_carousel)  # 取反
            if self.is_carousel:
                pb.setText('轮播')
            else:
                pb.setText('翻看')

            # 子控件失效的设置
            self.pb_prev.setEnabled(bool(1 - self.is_carousel))
            self.pb_next.setEnabled(bool(1 - self.is_carousel))

            self.carousel(self.is_carousel)

    def select_action(self, index):
        if -1 <= index < len(self.action):
            self.cur_act = index
            self.show_me()

    # 设置展示动图还是封面图
    def start(self, flag: bool = True):
        self.is_acting = flag
        self.flush()

    # 设置轮播自动展示还是单幅图人工展示，包括动图或者封面
    def carousel(self, flag: bool = True):
        self.is_carousel = flag
        self.flush()

    # 人工展示时的前图
    def prev(self):
        if not self.is_carousel:
            if self.is_acting:
                self.cur_act = self.cur_act - 1 \
                    if self.cur_act > 0 else len(self.action) - 1
            else:
                self.cur_cov = self.cur_cov - 1 \
                    if self.cur_cov > 0 else len(self.cover) - 1

            self.flush()

    # 人工展示时的后图
    def next(self):
        if not self.is_carousel:
            if self.is_acting:
                self.cur_act = self.cur_act + 1 \
                    if self.cur_act < len(self.action) - 1 else 0
            else:
                self.cur_cov = self.cur_cov + 1 \
                    if self.cur_cov < len(self.cover) - 1 else 0

            self.flush()

    # 刷新界面数据
    def flush(self):
        self.lb_title.setText(self.title)
        self.lb_resume.setText(self.resume)
        if self.notice:
            self.lb_notice.setText(self.notice[0] + f'   共{len(self.action)}个动作！')

        if self.is_carousel:
            self._carousel()
        else:
            self.timer.stop()
            self._alone()

    # 单图展示
    def _alone(self):
        if not self.is_acting:  # 显示封面
            self.lb_gist.setVisible(False)
            if not self.cover:
                return

            self.lb_img.setPixmap(QPixmap(self.cover[self.cur_cov]))
            # self.movie.stop()
            # self.lb_img.clear()
            # self.lb_img.set_img(self.cover[self.cur_cov])
            # self.lb_img.show_center_img()
        else:  # 显示动作
            self.lb_gist.setVisible(True)
            if not self.action:
                return
            action = self.action[self.cur_act]
            self.lb_gist.setText('\n       '.join(action[:-1]))

            # self.lb_img.clear()
            self.lb_img.setMovie(self.movie)
            gif = self.data_dir + f'/{action[-1]}'
            # print(gif)
            self.movie.stop()
            self.movie.setFileName(gif)
            self.movie.start()

    # 轮播图展示
    def _carousel(self):
        period = 0
        if self.is_acting:
            if self.notice and len(self.notice) == 4:
                group, times, rest = self.notice[1:]  # 组数，次数，休息时间，每个次2秒
                period = group * (times * 2 + rest) * 1000  # 周期
                # print(group, times, rest, period)
                # period = 1000
            else:
                period = (60 + self.stay) * 1000
        else:
            # print(len(self.cover))
            if self.cover and len(self.cover) > 1:
                period = 3000  # 3秒
            else:
                return
        # print(period)
        self._motion()
        self.timer.start(period)  # 设置计时间隔并启动；单位毫秒

    def _motion(self):
        if self.is_acting:
            self.cur_act = self.cur_act + 1 \
                if self.cur_act < len(self.action) - 1 else 0
        else:
            self.cur_cov = self.cur_cov + 1 \
                if self.cur_cov < len(self.cover) - 1 else 0

        self._alone()

    def use_palette(self):
        self.setWindowTitle("设置背景图片")
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(),
                             QtGui.QBrush(QtGui.QPixmap("./res/background/bk1.jpg")))
        self.setPalette(window_pale)

    #     # 多线程执行定时任务,语音播报
    #     # self._play_music()
    #     # threading.Timer(2, self._talking, ("动作播报",)).start()  # 10秒调用函数一次
    #     # threading.Timer(0, self._update_face, ("背景音乐",)).start()  # 10秒调用函数一次


# 阴影、圆角、底图的子窗体，充当主窗体
class Canvas(QWidget):
    def __init__(self, parent):
        super(Canvas, self).__init__(parent)

        self.parent = parent
        self.title_height = 50  # 标题栏高度
        self.left_width = 150  # 左侧宽度
        self.menu_height = 40  # 列表菜单项的高度

        self.data_dir = 'e:/dumbbell'

        self.data_plan = ['一副哑铃练全身', '15图', '十八般']
        self.data_video = []  # 资源：视频文件
        self.data_menu = []  # 菜单：界面
        self.body_arm = [('示范文件', '次数时间', '动作要领', '难度')]

        files = Utils.files_in_dir('./res//background', ['.jpg'], True)
        Utils.sort_nicely(files)
        i = Utils.rand_int(0, len(files)-1-5)
        # print(i, files)
        self.bg_label = CustomBG(self, files[i], Const.MARGIN)

        self.layout_main = QHBoxLayout(self)  # 左右布局
        self.fm_left = QFrame()
        self.pb_person = EllipseButton(self, 50, 50)
        self.sub_menu = ChildMenu()
        self.listWidget = MyQListWidget(self)

        self.fm_right = QFrame()
        self.titleBar = TitleBar()
        self.stackedWidget = QStackedWidget()  # 堆栈窗体

        # 多子窗体的窗体
        # self.mdi = QMdiArea()QMdiSubWindow()
        # # 为子窗口计数
        # self.count = self.count + 1
        # # 创建一个子窗口
        # sub = QMdiSubWindow()
        # # 为子窗口添加一个TextEdit控件
        # sub.setWidget(QTextEdit())
        # self.mdi.addSubWindow(sub)
        # sub.show()
        # self.mdi.cascadeSubWindows()  # 当点击菜单栏中的Cascade时，堆叠子窗口
        # self.mdi.tileSubWindows()  # 当点击菜单栏中的Tiled时，平铺子窗口

        # # 创建一个DockWidget# 停靠窗体
        # self.items = QDockWidget()
        #
        # # 定义一些内容（放到DockWidget中）
        # self.listWidget = QListWidget()
        # self.listWidget.setFixedSize(150, 300)
        # self.listWidget.addItem('item1')
        # self.listWidget.addItem('item2')
        # self.listWidget.addItem('item3')
        # self.items.setWidget(self.listWidget)
        # # 将DockWidget加到主窗口中，默认停靠在右边
        # self.addDockWidget(Qt.RightDockWidgetArea, self.items)
        # # 给主窗口添加一些控件
        # self.setCentralWidget(QLineEdit())

        self.init_date()
        self.init_canvas_ui()
        self.init_ui()

    def init_date(self):
        # 初始化数据
        data = MyJson.read(os.path.join(self.data_dir, 'menu.json'))
        # data = None
        if data:
            self.data_menu.extend(data)
        else:
            self.data_menu.extend([
                [('./res/images/1.ico', '运动资源'), ('', '文案'), ('', '视频'), ('', '网页')],
                [('', '锻炼部位'), ('', '肩部'), ('', '背部'), ('', '胸部'), ('', '腰腹'), ('', '手臂'), ('', '腿脚')],
                [('', '个性规划'), ('', '占位')],
                [('', '数据指数'), ('', '占位')],
                [('', '设置'), ('', '占位')]
            ])

    #     data = [
    #         "       力量训练所带来的好处之一就是提高基础代谢，而基础代谢的提高则有利于脂肪的燃烧。在这组动作当中，几乎涉及全身各个部位的训练，"
    #         "在实际的训练过程中，根据自己的健身需要选择哑铃重量，对于想要塑形的女士朋友来讲，选择1.5kg左右的小哑铃。"
    #         "对于以增肌为主要目的的朋友来讲，选择可以调节的哑铃组合来不断挑战自己更合适，这时候使用大重量。"
    #         "注意事项："
    #         "热身虽然不能达到锻炼的目的，但也是不可以被忽视的环节，所以，再心急也要热身。注意安全，不管是动作本身所带来的危险隐患，还是身体上的不适都需要被注意。"
    #         "以动作的标准规范为前提完成每一个动作，在动作过程中感觉身体不适，就多休息一下，或者是停止训练，不要勉强自己。"
    #         "动作过程中，充分感受目标肌肉的发力，并有意识地去进行，在每一次的动作中都要有意识地去感受，这样会让动作达到更佳的效果。"
    #         "动作间的休息时间在30秒左右，休息时要在轻微的活动中度过，不要坐着或者躺着不动。"
    #         "注意给自己留出休息的时间，不要为了在短时间内达到某种目的就每天都去做，休息是为了更好的训练，所以，在自己的计划当中，休息也应该是单独的一项。"
    #         "最后，在动作结束时，去放松拉伸，尤其是对自己感觉比较紧的部位要重点进行。",
    #         "塑形的女士，每个动作12-20次，每次2-3组；增肌的朋友，每个动作8-12次，每次2-3组，每周3-4次。",
    # 2,
    # 20,
    # 30,
    # [
    #     "动作一：坐姿哑铃推举",
    #     "主要锻炼三角肌前束与中束"
    #     "在凳子或者健身球上坐正，挺胸收腹，双手各握哑铃举至双肩两侧，掌心向前，大小臂垂直，"
    #     "将哑铃从身体两侧向上推起至手臂伸直，但肘关节不要锁死，注意推举时两哑铃不要相碰，"
    #     "稍停后主动控制速度慢慢下放还原。",
    #     "1.gif"
    # ],
    # [
    #     "动作二：站姿哑铃侧平举",
    #     "锻炼三角肌中束"
    #     "双脚稍微打开站立，挺胸收腹，双手各握哑铃置于身体两侧。"
    #     "向侧上方平举哑铃至双肩水平，肘部微屈，稍停后慢慢下放还原。",
    #     "2.gif"
    # ],
    # [
    #     "动作三：俯身哑铃飞鸟",
    #     "锻炼三角肌后束"
    #     "双脚分开，俯身约90°，双手对握哑铃，拳心相对，手肘微屈，双臂垂直于地面。、"
    #     "臂用力向两侧伸展，同时转动手臂，使拳眼朝下，"
    #     "绷紧肘关节，肩部发力，想象整条手臂与哑铃成为一个整体在运动，"
    #     "下放时双臂缓慢往里边转边合，而不是自由下落。",
    #     "3.gif"
    # ],
    # [
    #     "动作四：俯身单臂哑铃划船",
    #     "锻炼背阔肌"
    #     "一只手臂支撑身体，另一只手持哑铃，一条腿伸直脚踩地，另一条腿跪在凳子上，上身前倾，臀部向后，弯腰并确保背部挺直，使上身几乎和地面平行。"
    #     "肩胛收缩，肘部贴紧身体，将哑铃快速上提至身体两侧，顶点稍停。"
    #     "然后将哑铃缓缓放回起始位置，同时吸气。",
    #     "4.gif"
    # ],
    # [
    #     "动作五：哑铃耸肩",
    #     "锻炼斜方肌"
    #     "站立，挺胸收腹，双手各持一只哑铃，掌心相对，双臂在身体两侧自然下垂。"
    #     "手臂保持伸直状态，肩膀尽量上提将哑铃向上拉，同时呼气。直至肩膀上提至极限。"
    #     "在顶端稍停，然后将哑铃降回起始位置，同时吸气。"
    #     "注意做动作的过程中不要借助肱二头肌或者小臂的力量，要完全依靠肩膀的上下运动来移动哑铃。",
    #     "5.gif"
    # ],
    # [
    #     "动作六：上斜哑铃飞鸟",
    #     "锻炼胸大肌上侧"
    #     "仰卧在倾斜角度约为30度的凳子上，双手各握哑铃，掌心相对，推起至两臂伸直。"
    #     "双手持哑铃平行地向两侧落下，手肘稍微弯屈，哑铃落下至感到胸部两侧肌肉有充分的拉伸感。"
    #     "顶点稍停后，胸部发力，小臂外旋，使上臂向身体中间靠拢，在最高挤压胸部保持1秒后再落下。"
    #     "动作过程中，肩膀始终后缩下沉。",
    #     "6.gif"
    # ],
    # [
    #     "动作七：哑铃俯卧撑",
    #     "锻炼胸部，使用哑铃可以增加动作幅度，除对胸部形成足够的刺激以外，对三角肌也会起到一定的作用。"
    #     "俯身，双臂位于肩部正下方，双手握住两个哑铃与双脚撑起身体，使身体从头到脚呈一条直线，"
    #     "屈肘向下俯身至胸部几乎贴近地面，双手哑铃向两侧滑动，集中胸大肌力量向上推起身体，同时哑铃向内滑动。",
    #     "7.gif"
    # ],
    # [
    #     "动作八：站姿哑铃弯举",
    #     "锻炼肱二头肌"
    #     "站立，挺胸收腹，双手各握哑铃垂于身体两侧，掌心相对。"
    #     "肱二头肌发力，向上弯举至动作顶点，同时旋转手腕至拳眼相对，稍停后缓慢下放还原。",
    #     "8.gif"
    # ],
    # [
    #     "动作九：仰卧后撑",
    #     "锻炼肱三头肌"
    #     "找一个高度适中的凳子，双手撑于凳子边缘，双腿向前伸直（感觉难度大可以屈膝）。"
    #     "绷紧肩部，手臂后侧发力做屈伸运动，背部沿长凳外侧上下移动。",
    #     "9.gif"
    # ],
    # [
    #     "动作十：哑铃单腿硬拉",
    #     "动作方法：单腿站立，挺胸收腹，非支撑腿屈膝，小腿向后，双手对握哑铃垂于身体两侧。"
    #     "挺直背部，臀部向后推的同时小哑铃贴着右腿垂直下放，右腿膝盖微屈但不能超过脚尖。"
    #     "臀部发力，挺胯起身，回到起始状态。",
    #     "10.gif"
    # ],
    # [
    #     "动作十一：台阶登凳",
    #     "锻炼目标：股四头肌、臀大肌。"
    #     "双手各握哑铃，面朝台阶站立，挺胸收腹。"
    #     "一脚置于台阶上，右腿用力下蹬，带动身体至凳上直至双脚平踏凳面，"
    #     "接着另一腿下跨步，使身体回到起始位置，双腿交替进行。",
    #     "11.gif"
    # ]]
    #
    #     print(type(data),data)
    #     MyJson.write(data, r'E:\dumbbell\运动资源\文案\11个动作在家练\11个动作在家练.json')
        # for each in self.data_menu:
        #     path = self.data_dir + f'/{each[0][1]}/{each[0][1]}.json'
        #     print(each[1:], path)
        #     MyJson.write(each[1:], path)
        # for child in each[1:]:
        #     path = self.data_dir + f'/{each[0][1]}/{child[1]}/{child[1]}.json'
        #     print(child[1], path)
        #     MyJson.write(child[1], path)

        # self.data_video.append(r'e:\家庭哑铃计划')  # 第一项是存放文件的目录
        # files = Utils.files_in_dir(self.data_video[0], ['.mp4'])
        # self.data_video.extend(files)  # 目录里所有文件
        # print(self.data_menu)

    # 主界面设置
    def init_canvas_ui(self):
        self.resize(500, 500)
        self.setObjectName('Canvas')
        # self.setStyleSheet('background-image:url(./res/images/background1.jpg);border-radius:20px;')

        # self.setAttribute(Qt.WA_StyledBackground, True)  # 子QWdiget背景透明
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)  # 设置无边框窗口
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # self.setWindowOpacity(0.9)  # 设置窗口透明度

        # 本身带上阴影特效，需要父窗体留出margin
        Utils.set_effect(self, 1, 20, 5, 5, QColor(0, 0, 0, 200))
        # the same QGraphicsEffect can not be shared by other widgets
        # 子窗体带阴影的设置
        # for children in self.findChildren(QWidget):
        #     shadow = QGraphicsDropShadowEffect(blurRadius=15, xOffset=5, yOffset=5, color=QColor(0, 0, 0, 255))
        #     children.setGraphicsEffect(shadow)

        self.setMouseTracking(True)  # 跟踪鼠标移动事件的必备
        # self.setAttribute(Qt.WA_TransparentForMouseEvents, True)  # 设置鼠标穿透

        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setSpacing(0)
        self.layout_main.addWidget(self.fm_left)
        self.layout_main.addWidget(self.fm_right)

        # 信号槽，还是发给父窗口处理
        # self.titleBar.sign_pb_prev.connect(self.sign_title_clicked)
        # self.titleBar.sign_pb_next.connect(self.sign_title_clicked)
        self.titleBar.sign_win_minimize.connect(self.parent.sign_showMinimized)
        self.titleBar.sign_win_maximize.connect(self.parent.sign_showMaximized)
        self.titleBar.sign_win_resume.connect(self.parent.sign_showNormal)
        self.titleBar.sign_win_close.connect(self.parent.close)
        self.titleBar.sign_win_move.connect(partial(self.parent.sign_move, self.left_width))
        # self.windowTitleChanged.connect(self.titleBar.setTitle)
        # self.windowIconChanged.connect(self.titleBar.setIcon)

    # 添加控件
    def init_ui(self):
        # 初始化总体界面
        # self.fm_left.setAttribute(Qt.WA_TransparentForMouseEvents, True)  # 设置鼠标穿透
        self.fm_left.setMouseTracking(True)  # 跟踪鼠标移动事件的必备
        self.pb_person.setMouseTracking(True)  # 自定义类中已经打上了
        # self.listWidget.setMouseTracking(True)
        self.fm_right.setMouseTracking(True)  # 跟踪鼠标移动事件的必备
        self.titleBar.setMouseTracking(True)
        self.stackedWidget.setMouseTracking(True)

        # region 左侧界面(上面按钮，下面QListWidget)
        # region 左侧整体
        lv_left = QVBoxLayout(self.fm_left)
        lv_left.setContentsMargins(0, 15, 0, 0)
        # lh_tmp = QHBoxLayout()
        # lh_tmp.addWidget(self.pb_person, 0, Qt.AlignCenter)
        # lv_left.addLayout(lh_tmp)
        lv_left.addWidget(self.pb_person, 0, Qt.AlignCenter)
        lv_left.addStretch()
        lv_left.addWidget(self.listWidget, 0, Qt.AlignCenter)
        lv_left.addStretch()

        # self.fm_left.setWindowOpacity(0.5)  # 设置窗口透明度
        self.fm_left.setObjectName('left_fm')
        # self.fm_left.setFixedWidth(self.left_width)  # 直接设置宽度，按钮不居中；通过样式设置则居中
        qss_left = '#left_fm{border-top-left-radius:%d;border-bottom-left-radius:%d;' \
                   'min-width: %dpx;max-width: %dpx;' \
                   'font-size:16px;font-weight:bold;font-family:Roman times;' \
                   'color: white;background: rgba(0, 0, 0, 50);' \
                   'background-position: center center}' % \
                   (Const.MARGIN, Const.MARGIN, self.left_width, self.left_width)
        self.fm_left.setStyleSheet(qss_left)
        # self.fm_left.setStyleSheet('background-image: url(./res/background/background1.jpg);'
        #                            '/*border-radius:20px;     画出圆角*/'
        #                            'background-repeat: no-repeat;       /*背景不要重复*/'
        #                            'background-position: center center;      /*图片的位置，居中，靠左对齐*/')
        # endregion

        # region 左侧图标
        # self.lb_person.setAlignment(Qt.AlignCenter)
        # self.lb_person.setIcon(QIcon('./res/images/girl1.png'))
        self.pb_person.setFixedSize(QSize(150, 150))
        self.pb_person.set('./res/images/boy.png')
        # self.pb_person.set('./res/images/girl1.png')

        # self.lb_person.setStyleSheet('border-top-left-radius:%d;'
        #                              'background: transparent;     /*全透明*/'
        #                              '/*background:rgba(0,0,0,0.1);      半透明*/' % self.margin)
        # self.lb_person.setStyleSheet("color:black;"
        #                              "color:red;"
        #                              "background-color:rgb(78,255,255);"
        #                              "border:2px;"
        #                              "border-radius:15px;"
        #                              "padding:2px 4px;")

        # self.lb_person.setStyleSheet(
        #     'min-width:  50px;max-width:  40px;'
        #     'min-height: 50px;max-height: 40px;'
        #     'border-width: 0 0 0 0;'
        #     'border-image: url(./res/images/water.png) 0 0 0 0 stretch;')
        # pix = self.get_round_pixmap(QPixmap('./res/images/1.png'), 100)
        # self.lb_person.setPixmap(pix)
        # self.tb_person.setFixedHeight(self.title_height)
        # self.tb_person.setAutoFillBackground(True)
        # endregion

        # region 列表框设置
        self.listWidget.setFrameShape(QListWidget.NoFrame)  # 去掉边框
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏滚动条
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setCursor(QCursor(Qt.ArrowCursor))
        self.listWidget.setObjectName('menu_list')
        # self.listWidget.setSpacing(10)  # 设置QListWidget中单元项的间距
        # self.listWidget.setViewportMargins(0, 0, 0, 0)
        # 通过QListWidget的当前item变化来切换QStackedWidget中的序号
        # self.listWidget.resize(365, 400)
        # 设置显示模式,一般的文本配合图标模式(也可以用Icon模式,setViewMode)
        # self.listWidget.setViewMode(QListView.IconMode)
        # self.delegate = ItemDelegate()
        # self.listWidget.setItemDelegate(self.delegate)#图标在右侧
        # # 设置QListWidget中单元项的图片大小
        # self.listWidget.setIconSize(QSize(100, 100))
        # # 设置QListWidget中单元项的间距
        # self.listWidget.setSpacing(10)
        # self.listWidget.setViewportMargins(0, 0, 0, 0)
        # # 设置自动适应布局调整（Adjust适应，Fixed不适应），默认不适应
        # self.listWidget.setResizeMode(QListWidget.Adjust)
        # # 设置不能移动
        # self.listWidget.setMovement(QListWidget.Static)

        menu_count = len(self.data_menu)
        item_count = 10 if menu_count > 10 else menu_count
        self.listWidget.setFixedHeight(self.menu_height * item_count)

        self.sub_menu.init_stack_menu(self.data_menu, self.listWidget)  # 子菜单页面初始化
        self.sub_menu.select_stack(0)

        for each in self.data_menu:
            item = QListWidgetItem(QIcon(each[0][0]), each[0][1], self.listWidget)
            #     item.setToolTip(self.data[i])
            item.setSizeHint(QSize(16777215, self.menu_height))  # 设置item的默认宽高(这里只有高度比较有用)
            item.setTextAlignment(Qt.AlignCenter)  # 文字居中

        # item = QListWidgetItem(QIcon(), '', self.listWidget)
        # item.setSizeHint(QSize(16777215, 1))
        # line = QtWidgets.QFrame()
        # line.setFixedHeight(2)
        # line.setEnabled(False)
        # line.setStyleSheet('background:transparent;background-color:rgb(155,155,155);'
        #                    'border:1px solid rgb(155,155,155)')
        # # line.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Raised)

        # self.listWidget.setItemWidget(item, line)
        # endregion
        # endregion

        # region 右侧界面设置(上边TitleBar，下边QStackedWidget)
        # region 右侧总体
        lv_right = QVBoxLayout(self.fm_right)
        lv_right.setContentsMargins(0, 0, 1, 0)
        lv_right.addWidget(self.titleBar)
        # lv_right.addStretch()
        lv_right.addWidget(self.stackedWidget)
        # lv_right.addStretch()

        self.fm_right.setObjectName('right_fm')
        # self.fm_left.setFixedWidth(self.left_width)  # 直接设置宽度，按钮不居中；通过样式设置则居中
        qss_right = '#right_fm{background: transparent;     /*全透明*/' \
                    'border-top-right-radius:%d;border-bottom-right-radius:%d;' \
                    'font-size:16px;font-weight:bold;font-family:Roman times;' \
                    'background-position: center center}' % (Const.MARGIN, Const.MARGIN)
        self.fm_right.setStyleSheet(qss_right)
        # endregion

        # region 右侧工具栏
        self.titleBar.setHeight(self.title_height)
        # self.titleBar.setStyleSheet('border-top-right-radius:15;border-bottom-right-radius:15')
        # self.titleBar.setAttribute(Qt.WA_StyledBackground, True)
        # endregion

        # region 右侧stackedWidget
        # 定义播放页面

        # region 文件列表
        lw_videos = QListWidget()
        # lw_videos.setViewMode(QListView.IconMode)  # 显示模式,Icon模式(一般文本配合图标,setViewMode)
        # lw_videos.setFrameShape(QListView.NoFrame)  # 无边框
        # lw_videos.setFlow(QListWidget.LeftToRight)  # 从左到右
        # lw_videos.setWrapping(True)  # 这三个组合可以达到和FlowLayout一样的效果
        # lw_videos.setResizeMode(QListWidget.Adjust)  # 设置自动适应布局调整（Adjust适应，Fixed不适应），默认不适应
        # lw_videos.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏滚动条
        lw_videos.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        lw_videos.setIconSize(QSize(100, 100))  # 设置QListWidget中单元项的图片大小
        lw_videos.setSpacing(10)  # 设置QListWidget中单元项的间距

        # lw_videos.setViewportMargins(0, 0, 0, 0)
        lw_videos.setMovement(QListWidget.Static)  # 设置不能移动
        lw_videos.setStyleSheet('background: transparent;     /*全透明*/'
                                'color: rgb(255, 200, 20);   /**/'
                                'font-size:22px;font-weight:bold;font-family:Roman times;')
        # lw_videos.setCursor(QCursor(Qt.ArrowCursor))

        # 连接竖着的滚动条滚动事件
        # lw_videos.verticalScrollBar().actionTriggered.connect(self.onActionTriggered)
        lw_videos.clicked.connect(self.submenu_resource)
        # item_height = 40
        # item_count = 11 if len(self.data_video) > 11 else len(self.data_video)
        # lw_videos.setFixedHeight(item_height * item_count)
        # print(lw_videos.height(), self.menu_height * item_count)

        # for each in self.data_video:
        #     item = QListWidgetItem(QIcon(), each, lw_videos)
        #     #     item.setToolTip(self.data[i])
        #     item.setSizeHint(QSize(16777215, self.menu_height))  # 设置item的默认宽高(这里只有高度比较有用)
        #     item.setTextAlignment(Qt.AlignCenter)  # 文字居中
        self.stackedWidget.addWidget(lw_videos)
        # endregion

        # region 动图播放页面
        stage = Curtain(self)
        self.stackedWidget.addWidget(stage)
        # endregion

        # 再模拟20个右侧的页面(就不和上面一起循环放了)
        # for i in range(1):
        #     # label = QLabel(f'我是页面{i}', self)
        #     # label.setAlignment(Qt.AlignCenter)
        #     label = MyQLabel('学生', self)
        #     label.resize(400, 400)
        #     # print('df fd', self.stackedWidget.size(), label.size())
        #     # 设置label的背景颜色(这里随机)
        #     # 这里加了一个margin边距(方便区分QStackedWidget和QLabel的颜色)
        #     # self.stackedWidget.setStyleSheet('background: rgb(%d, %d, %d);margin: 0px;'
        #     #                     % (randint(0, 255), randint(0, 255), randint(0, 255)))
        #     label.setStyleSheet('background: green;margin: 50px;')
        #     label.show_center_img('./res/images/1_horizontal.jpg')

        # endregion

        # endregion

    def add_lw_items(self, img_path, flag=1):
        """
        读取缩略图
        :param img_path:
        :param flag: stacked 的序号，1：gif  0：视频文件页面
        :return:
        """

        files = Utils.files_in_dir(img_path, ['.jpg', '.jpeg', '.gif', '.tiff', '.bmp', '.png'], True)
        print(files)
        return
        for f1 in files:
            exif_dict = piexif.load("d:/1/" + f1)
            thumbnail = exif_dict.pop("thumbnail")
            if thumbnail is not None:
                pix1 = QPixmap()
                pix1.loadFromData(thumbnail, "JPG")

            item1 = QListWidgetItem(QIcon(pix1.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)),
                                    os.path.split(f1)[-1])
            self.iconlist.addItem(item1)

    def init_video_display(self):
        pass

    def createIcons(self, lw):
        configButton = QtGui.QListWidgetItem(lw)
        configButton.setIcon(QtGui.QIcon('./res/images/.png'))
        configButton.setText("Configuration")
        configButton.setTextAlignment(QtCore.Qt.AlignHCenter)
        configButton.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        updateButton = QtGui.QListWidgetItem(self.contentsWidget)
        updateButton.setIcon(QtGui.QIcon(':/images/update.png'))
        updateButton.setText("Updatessss")
        updateButton.setTextAlignment(QtCore.Qt.AlignHCenter)
        updateButton.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        queryButton = QtGui.QListWidgetItem(self.contentsWidget)
        queryButton.setIcon(QtGui.QIcon(':/images/query.png'))
        queryButton.setText("Query")
        queryButton.setTextAlignment(QtCore.Qt.AlignHCenter)
        queryButton.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.contentsWidget.currentItemChanged.connect(self.changePage)

    # QListWidget current 改变时触发
    def changePage(self, current, previous):
        print(self.contentsWidget.row(current))

    def submenu_clicked(self, name):
        # print(name)
        res_names = self.data_menu[0][1:]
        res_names = [res_names[i][1] for i in range(len(res_names))]
        body_names = self.data_menu[1][1:]  # ['肩部', '手臂', '肩背', '腰腹', '腿脚']
        body_names = [body_names[i][1] for i in range(len(body_names))]
        # print(type(res_names), res_names)

        if name in res_names:
            self.stackedWidget.setCurrentIndex(0)
            widget = self.stackedWidget.currentWidget()  # 第一个是展示多个选项的列表框
            # widget = QListWidget()
            widget.clear()
            # widget.itemClicked.connect(self.submenu_resource)

            title = f'{self.data_menu[0][0][1]}/{name}'
            widget.setObjectName(title)  # 槽函数需要

            file = self.data_dir + f'/{title}/{name}.json'
            data_res = MyJson.read(file)
            #             data = '''[
            #     "       力量训练所带来的好处之一就是提高基础代谢，而基础代谢的提高则有利于脂肪的燃烧。在这组动作当中，几乎涉及全身各个部位的训练，在实际的训练过程中，根据自己的健身需要选择哑铃重量，对于想要塑形的女士朋友来讲，选择1.5kg左右的小哑铃。对于以增肌为主要目的的朋友来讲，选择可以调节的哑铃组合来不断挑战自己更合适，这时候使用大重量。
            # 注意事项：
            # 热身虽然不能达到锻炼的目的，但也是不可以被忽视的环节，所以，再心急也要热身。
            # 注意安全，不管是动作本身所带来的危险隐患，还是身体上的不适都需要被注意。以动作的标准规范为前提完成每一个动作，在动作过程中感觉身体不适，就多休息一下，或者是停止训练，不要勉强自己。
            # 动作过程中，充分感受目标肌肉的发力，并有意识地去进行，在每一次的动作中都要有意识地去感受，这样会让动作达到更佳的效果。
            # 动作间的休息时间在30秒左右，休息时要在轻微的活动中度过，不要坐着或者躺着不动
            # 注意给自己留出休息的时间，不要为了在短时间内达到某种目的就每天都去做，休息是为了更好的训练，所以，在自己的计划当中，休息也应该是单独的一项。
            # 最后，在动作结束时，去放松拉伸，尤其是对自己感觉比较紧的部位要重点进行。",
            #     "塑形的女士，每个动作12-20次，每次2-3组；增肌的朋友，每个动作8-12次，每次2-3组，每周3-4次。",
            #     2,
            #     20,
            #     30,
            #     [
            #         "动作一：坐姿哑铃推举",
            #         "主要锻炼三角肌前束与中束
            #
            # 在凳子或者健身球上坐正，挺胸收腹，双手各握哑铃举至双肩两侧，掌心向前，大小臂垂直
            # 将哑铃从身体两侧向上推起至手臂伸直，但肘关节不要锁死，注意推举时两哑铃不要相碰
            # 稍停后主动控制速度慢慢下放还原。",
            #         "1.gif"
            #     ],
            #     [
            #         "动作二：站姿哑铃侧平举",
            #         "锻炼三角肌中束
            #
            # 双脚稍微打开站立，挺胸收腹，双手各握哑铃置于身体两侧
            # 向侧上方平举哑铃至双肩水平，肘部微屈
            # 稍停后慢慢下放还原。",
            #         "2.gif"
            #     ],
            #     [
            #         "动作三：俯身哑铃飞鸟",
            #         "锻炼三角肌后束
            #
            # 双脚分开，俯身约90°，双手对握哑铃，拳心相对，手肘微屈，双臂垂直于地面
            # 双臂用力向两侧伸展，同时转动手臂，使拳眼朝下
            # 绷紧肘关节，肩部发力，想象整条手臂与哑铃成为一个整体在运动
            # 下放时双臂缓慢往里边转边合，而不是自由下落。",
            #         "3.gif"
            #     ],
            #     [
            #         "动作四：俯身单臂哑铃划船",
            #         "锻炼背阔肌
            #
            # 一只手臂支撑身体，另一只手持哑铃，一条腿伸直脚踩地，另一条腿跪在凳子上，上身前倾，臀部向后，弯腰并确保背部挺直，使上身几乎和地面平行。
            # 肩胛收缩，肘部贴紧身体，将哑铃快速上提至身体两侧，顶点稍停
            # 然后将哑铃缓缓放回起始位置，同时吸气。",
            #         "4.gif"
            #     ],
            #     [
            #         "动作五：哑铃耸肩",
            #         "锻炼斜方肌
            #
            # 站立，挺胸收腹，双手各持一只哑铃，掌心相对，双臂在身体两侧自然下垂
            # 手臂保持伸直状态，肩膀尽量上提将哑铃向上拉，同时呼气。直至肩膀上提至极限
            # 在顶端稍停，然后将哑铃降回起始位置，同时吸气。
            # 注意做动作的过程中不要借助肱二头肌或者小臂的力量，要完全依靠肩膀的上下运动来移动哑铃。",
            #         "5.gif"
            #     ],
            #     [
            #         "动作六：上斜哑铃飞鸟",
            #         "锻炼胸大肌上侧
            #
            # 仰卧在倾斜角度约为30度的凳子上，双手各握哑铃，掌心相对，推起至两臂伸直。
            # 双手持哑铃平行地向两侧落下，手肘稍微弯屈，哑铃落下至感到胸部两侧肌肉有充分的拉伸感
            # 顶点稍停后，胸部发力，小臂外旋，使上臂向身体中间靠拢，在最高挤压胸部保持1秒后再落下
            # 动作过程中，肩膀始终后缩下沉。",
            #         "6.gif"
            #     ],
            #     [
            #         "动作七：哑铃俯卧撑",
            #         "锻炼胸部，使用哑铃可以增加动作幅度，除对胸部形成足够的刺激以外，对三角肌也会起到一定的作用。
            #
            # 俯身，双臂位于肩部正下方，双手握住两个哑铃与双脚撑起身体，使身体从头到脚呈一条直线
            # 屈肘向下俯身至胸部几乎贴近地面，双手哑铃向两侧滑动
            # 集中胸大肌力量向上推起身体，同时哑铃向内滑动。",
            #         "7.gif"
            #     ],
            #     [
            #         "动作八：站姿哑铃弯举",
            #         "锻炼肱二头肌
            #
            # 站立，挺胸收腹，双手各握哑铃垂于身体两侧，掌心相对
            # 肱二头肌发力，向上弯举至动作顶点，同时旋转手腕至拳眼相对
            # 稍停后缓慢下放还原。",
            #         "8.gif"
            #     ],
            #     [
            #         "动作九：仰卧后撑",
            #         "锻炼肱三头肌
            #
            # 找一个高度适中的凳子，双手撑于凳子边缘，双腿向前伸直（感觉难度大可以屈膝）
            # 绷紧肩部，手臂后侧发力做屈伸运动，背部沿长凳外侧上下移动。",
            #         "9.gif"
            #     ],
            #     [
            #         "动作十：哑铃单腿硬拉",
            #         "动作方法：单腿站立，挺胸收腹，非支撑腿屈膝，小腿向后，双手对握哑铃垂于身体两侧
            # 挺直背部，臀部向后推的同时小哑铃贴着右腿垂直下放，右腿膝盖微屈但不能超过脚尖
            # 臀部发力，挺胯起身，回到起始状态。",
            #         "10.gif"
            #     ],
            #     [
            #         "动作十一：台阶登凳",
            #         "锻炼目标：股四头肌、臀大肌
            #
            # 双手各握哑铃，面朝台阶站立，挺胸收腹
            # 一脚置于台阶上，右腿用力下蹬，带动身体至凳上直至双脚平踏凳面
            # 接着另一腿下跨步，使身体回到起始位置
            # 双腿交替进行。",
            #         "11.gif"
            #     ]
            # ]'''
            #             file = r'E:\dumbbell\运动资源\文案\11个动作在家练'

            # print('dd', title, file, data_res)
            # path, f = os.path.split(file)
            # ll = Utils.files_in_dir(path, ['.mp4'])
            # MyJson.write(data, file)

            for each in data_res:
                item = None
                if name == '文案':
                    item = QListWidgetItem(QIcon(each[0]), each[1], widget)
                    item.setToolTip(each[1])
                elif name == '视频' or name == '网页':
                    item = QListWidgetItem(QIcon(), each, widget)
                    item.setToolTip(each)
                item.setSizeHint(QSize(16777215, self.menu_height))  # 设置item的默认宽高(这里只有高度比较有用)
                item.setTextAlignment(Qt.AlignCenter)  # 文字居中
        elif name in body_names:
            self.submenu_body(name)
            # print(self.stackedWidget.count())
            # print(type())
        # elif name == :
        #     pass
        # elif name == :
        #     pass
        # elif name == :
        #     pass
        #
        # elif name == 'q':
        #     pass
        else:
            pass

    def submenu_resource(self):
        lw = self.stackedWidget.currentWidget()
        name = lw.objectName()
        text = lw.currentItem().text()
        path = self.data_dir + f'/{name}/{text}'
        print(name, text, path)

        if '文案' in name:
            # imgs = Utils.files_in_dir(path, ['.jpg', '.jpeg', '.tiff', '.bmp', '.png'])
            # gifs = Utils.files_in_dir(path, ['.gif'])
            # json = Utils.files_in_dir(path, ['.json'])
            # print(imgs, json)
            # print(gifs)
            self.stackedWidget.setCurrentIndex(1)
            curtain = self.stackedWidget.widget(1)
            # print(type(curtain))
            curtain.clear()
            curtain.set_title(text)
            curtain.data_serialize(path)
            curtain.start(False)
        elif '视频' in name:
            # print('动态拉伸', path)
            os.startfile(path)  # 利用系统调用默认程序打开本地文件

    def submenu_body(self, name):
        self.stackedWidget.setCurrentIndex(1)
        curtain = self.stackedWidget.widget(1)
        # print(type(curtain))
        # curtain = Curtain()

        path = self.data_dir + f'/{self.data_menu[1][0][1]}' + f'/{name}'
        # print('this is body', path)

        curtain.clear()
        curtain.set_title(name)
        curtain.data_serialize(path)
        curtain.start()

    # def sign_title_clicked(self):
    #     sender = self.sender()
    #     # print(sender.text())

    # def slot_list_row_changed(self):
    #     cur_row = self.listWidget.currentRow()
    #     pos = self.listWidget.pos()
    #
    #     child_menu_pos = QPoint(self.menu_height * cur_row, self.left_width)
    #
    #     # self.stacked_menu.setCurrentIndex(cur_row)
    #     print(cur_row)
    #
    #     # 通过QListWidget的当前item变化来切换QStackedWidget中的序号
    #     # self.stackedWidget.setCurrentIndex(cur_row // 2)

    # def paintEvent(self, event):
    #     return
    #     # # 主窗体无边框时是加载不了样式的，仅在子控件上实现样式。
    #     # # 要在主窗体本身实现样式，需要在paintEvent事件中加上如下代码，设置底图也是一样的
    #     # opt = QStyleOption()
    #     # opt.initFrom(self)
    #     # p = QPainter(self)
    #     # p.setRenderHint(QPainter.Antialiasing)  # 反锯齿
    #     # self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
    #     # # super(Canvas, self).paintEvent(event)
    #
    #     # 不通过样式，直接设置圆角，通用，且不继承于子控件
    #     painter = QPainter(self)
    #     painter.setRenderHint(QPainter.Antialiasing)  # 反锯齿
    #
    #     # 显示全图充满
    #     # img_new = Utils.img_center(self.width(), self.height(),
    #     #                            './res//background/bk5.jpg')
    #     # painter.setBrush(QBrush(img_new))  # 设置底图的方式之一
    #     # painter.setBrush(QBrush(QPixmap.fromImage(img_new)))  # 设置底图的方式之一
    #     # painter.setBrush(QBrush(Qt.blue))
    #     painter.setPen(Qt.transparent)
    #
    #     rect = self.rect()
    #     rect.setWidth(rect.width() - 1)
    #     rect.setHeight(rect.height() - 1)
    #     painter.drawRoundedRect(rect, 20, 20)
    #     # 也可用QPainterPath 绘制代替 painter.drawRoundedRect(rect, 15, 15)
    #     # painterPath= QPainterPath()
    #     # painterPath.addRoundedRect(rect, 15, 15)
    #     # painter.drawPath(painterPath)
    #
    #     # 直接设置底图，与圆角的画刷设置不能同时
    #     # pix = QPixmap('./res/images/background11.jpg')
    #     # painter.drawPixmap(self.rect(), pix)
    #
    #     # super(testShadow, self).paintEvent(event)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super(Canvas, self).resizeEvent(a0)
        self.bg_label.update()

    # def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
    #     if a0 == 'menu_list':
    #         print('great')
    #     if a1.type() == QtCore.QEvent.HoverMove:
    #         print('鼠标移动到按钮上')
    #         return True
    #     elif a1.type() == QtCore.QEvent.MouseMove:
    #         print('按钮被点击')
    #         return True

    # def enterEvent(self, a0: QtCore.QEvent):
    #     print('enter', a0.pos())
    #     return super().enterEvent(a0)
    #
    # def leaveEvent(self, a0: QtCore.QEvent):
    #     print('leave', a0.pos())
    #     return super().enterEvent(a0)


# 主窗体的影子
class MainWin(QWidget):

    # region 主窗口的影子，不用再改
    def __init__(self, *args, **kwargs):
        super(MainWin, self).__init__(*args, **kwargs)

        self.resize(1500, 1000)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)  # 设置无边框窗口
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # self.setAttribute(Qt.WA_StyledBackground, True)  # 子QWdiget背景透明
        self.setMouseTracking(True)  # 跟踪鼠标移动事件的必备

        self.LOCATION = Const.CENTER
        # self.dragPosition = 0  # 拖动时坐标

        self.canvas = Canvas(self)

        # child = ChildMenu(self)
        # child.show()
        # child.move(self.x()+100, self.y()+300)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(Const.MARGIN, Const.MARGIN,
                                  Const.MARGIN, Const.MARGIN)  # 给阴影留下位置
        # layout.setContentsMargins(0, 0, 0, 0)  # 给阴影留下位置
        layout.addWidget(self.canvas)
        # layout.addWidget(child)
        Utils.center_win(self)

    def sign_showMinimized(self):
        self.showMinimized()

    def sign_showMaximized(self):
        """最大化,要先去除上下左右边界,如果不去除则边框地方会有空隙"""
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.showMaximized()

    def sign_showNormal(self):
        """还原,要先保留上下左右边界,否则没有边框无法调整"""
        self.layout().setContentsMargins(Const.MARGIN, Const.MARGIN,
                                         Const.MARGIN, Const.MARGIN)
        super(MainWin, self).showNormal()

    # def nativeEvent(self):
    #     pass

    def mousePressEvent(self, event: QMouseEvent):
        # if event.button() == Qt.LeftButton:#也可以
        if event.buttons() == Qt.LeftButton:
            if self.LOCATION != Const.CENTER:
                self.mouseGrabber()  # 得到正在捕获键盘事件的窗口
            else:
                pass
                # self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()

    def mouseReleaseEvent(self, event: QMouseEvent):
        # if event.buttons() == Qt.LeftButton:#就不行
        if event.button() == Qt.LeftButton:
            if self.LOCATION is not Const.CENTER:  # 非边线附近一律恢复鼠标形状
                self.setCursor(QtGui.QCursor(Qt.ArrowCursor))
            self.unsetCursor()

    def cursor_location(self, pos_current):
        """
            给光标标定位
            :param pos_current:相对位置
            :return:
            """
        x, y = pos_current.x(), pos_current.y()  # 相对于无边框窗口左上角的位置
        # print(f'x={x}  y={y}')
        width = self.width() - Const.PADDING  # 无边框窗口的宽减去边距
        height = self.height() - Const.PADDING  # 无边框窗口的长减去边距

        if x < Const.PADDING and y < Const.PADDING:  # 左上角内侧
            self.LOCATION = Const.TL_CORNER
            self.setCursor(QCursor(Qt.SizeFDiagCursor))  # 设置鼠标形状
        elif x > width and y > height:  # 右下角内侧
            self.LOCATION = Const.BR_CORNER
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif x < Const.PADDING and y > height:  # 左下角内侧
            self.LOCATION = Const.BL_CORNER
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif x > width and y < Const.PADDING:  # 右上角内侧
            self.LOCATION = Const.TR_CORNER
            self.setCursor(QCursor(Qt.SizeBDiagCursor))

        elif x < Const.PADDING:  # 左边内侧
            self.LOCATION = Const.LEFT
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif x > width:  # 右边内侧
            self.LOCATION = Const.RIGHT
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif y < Const.PADDING:  # 上边
            self.LOCATION = Const.TOP
            self.setCursor(QCursor(Qt.SizeVerCursor))
        elif y > height:  # 下边
            self.LOCATION = Const.BOTTOM
            self.setCursor(QCursor(Qt.SizeVerCursor))

        else:  # 中间 默认
            self.LOCATION = Const.CENTER
            self.setCursor(QCursor(Qt.ArrowCursor))

        # print(self.LOCATION)

    def mouseMoveEvent(self, event: QMouseEvent):
        mouse_pos = event.globalPos()
        top_left = self.mapToGlobal(self.rect().topLeft())
        # top_left = self.pos
        bottom_right = self.mapToGlobal(self.rect().bottomRight())

        # print(self.LOCATION)

        # if event.buttons() and event.button() != Qt.LeftButton:  # 也不行
        if not event.buttons():
            self.cursor_location(event.pos())
        else:
            if event.buttons() == Qt.LeftButton:
                # print('left press')
                if self.LOCATION is Const.CENTER:
                    pass
                    # print('center')
                    # self.move(event.globalPos() - self.dragPosition)  # 将窗口移动到指定位置
                else:
                    geo = QtCore.QRect(top_left, bottom_right)

                    if self.LOCATION == Const.LEFT:
                        # if bottom_right.x() - mouse_pos.x() > self.minimumWidth():#不需要，有setmin、max、fix决定
                        # geo.setWidth(bottom_right.x() - mouse_pos.x())  # 自动计算的
                        geo.setX(mouse_pos.x())
                    elif self.LOCATION is Const.RIGHT:
                        geo.setWidth(mouse_pos.x() - top_left.x())
                    elif self.LOCATION is Const.TOP:
                        geo.setY(mouse_pos.y())
                    elif self.LOCATION == Const.BOTTOM:
                        geo.setHeight(mouse_pos.y() - top_left.y())
                    elif self.LOCATION == Const.TL_CORNER:
                        geo.setX(mouse_pos.x())
                        geo.setY(mouse_pos.y())
                    elif self.LOCATION == Const.TR_CORNER:
                        geo.setWidth(mouse_pos.x() - top_left.x())
                        geo.setY(mouse_pos.y())
                    elif self.LOCATION == Const.BL_CORNER:
                        geo.setX(mouse_pos.x())
                        geo.setHeight(mouse_pos.y() - top_left.y())
                    elif self.LOCATION == Const.BR_CORNER:
                        geo.setWidth(mouse_pos.x() - top_left.x())
                        geo.setHeight(mouse_pos.y() - top_left.y())
                    # else:  # is Const.CENTER
                    #     pass
                    self.setGeometry(geo)  # 设置影子的父窗口的位置

            # else:
            #     print('other press')
        # QEvent的accept（）和ignore（）一般不会用到，因为不如直接调用QWidget类的事件处理函数直接，而且作用是一样的
        # 唯有在closeEvent（）中必须调用accept（）或ignore（）。
        event.ignore()

    def close(self):
        self.canvas.sub_menu.close()
        super(MainWin, self).close()

    def sign_move(self, x_offset, pos):
        if self.windowState() == Qt.WindowMaximized or self.windowState() == Qt.WindowFullScreen:
            # 最大化或者全屏则不允许移动
            return

        # if self._widget is None:
        #     return

        pos_new = copy.copy(pos)
        pos_new.setX(pos.x() - x_offset)  # 减去左侧列表框占用的
        # print('this', pos_new.x(), pos.x())

        super(MainWin, self).move(pos_new)
    # endregion


if __name__ == '__main__':
    app = QApplication(sys.argv)

    g_style = StyleSheet()  # 包围窗体，定义在前
    w = MainWin()  # 添加在中间
    # w = Canvas(None)
    # w = ChildMenu(None)
    # w = Curtain(None)
    # w.show()
    g_style.set(app)  # 包围窗体，设置在后

    sys.exit(app.exec_())

    # w = WinInfo()
    # w.get_all_win()
