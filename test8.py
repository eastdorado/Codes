#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ctypes import *
# from ctypes import cdll, Structure
from ctypes.wintypes import HWND, DWORD

import win32api
from enum import IntEnum, unique, Enum
import sys, os
from PIL import Image, ImageQt
from utilities import BackLabel, Utils, EllipseButton, CircleImage

import cgitb  # 相当管用

cgitb.enable(format='text')  # 解决 pyqt5 异常只要进入事件循环,程序就崩溃,而没有任何提示


# class WINDOWCOMPOSITIONATTRIB(IntEnum):
#     WCA_UNDEFINED = 0
#     WCA_NCRENDERING_ENABLED = 1
#     WCA_NCRENDERING_POLICY = 2
#     WCA_TRANSITIONS_FORCEDISABLED = 3
#     WCA_ALLOW_NCPAINT = 4
#     WCA_CAPTION_BUTTON_BOUNDS = 5
#     WCA_NONCLIENT_RTL_LAYOUT = 6
#     WCA_FORCE_ICONIC_REPRESENTATION = 7
#     WCA_EXTENDED_FRAME_BOUNDS = 8
#     WCA_HAS_ICONIC_BITMAP = 9
#     WCA_THEME_ATTRIBUTES = 10
#     WCA_NCRENDERING_EXILED = 11
#     WCA_NCADORNMENTINFO = 12
#     WCA_EXCLUDED_FROM_LIVEPREVIEW = 13
#     WCA_VIDEO_OVERLAY_ACTIVE = 14
#     WCA_FORCE_ACTIVEWINDOW_APPEARANCE = 15
#     WCA_DISALLOW_PEEK = 16
#     WCA_CLOAK = 17
#     WCA_CLOAKED = 18
#     WCA_ACCENT_POLICY = 19
#     WCA_FREEZE_REPRESENTATION = 20
#     WCA_EVER_UNCLOAKED = 21
#     WCA_VISUAL_OWNER = 22
#     WCA_LAST = 23
#
#
# class WINDOWCOMPOSITIONATTRIBDATA(Structure):
#     _fields_ = [('Attrib', WINDOWCOMPOSITIONATTRIB),
#                 ('pvData', c_void_p),  # PVOID
#                 ('cbData', c_ulong), ]  # SIZE_T
#
#
# class ACCENT_STATE(IntEnum):
#     ACCENT_DISABLED = 0
#     ACCENT_ENABLE_GRADIENT = 1
#     ACCENT_ENABLE_TRANSPARENTGRADIENT = 2
#     ACCENT_ENABLE_BLURBEHIND = 3
#     ACCENT_INVALID_STATE = 4
#
#
# class ACCENT_POLICY(Structure):
#     _fields_ = [('AccentState', ACCENT_STATE),
#                 ('AccentFlags', DWORD * 1),
#                 ('GradientColor', c_ulong),
#                 ('AnimationId', c_ulong), ]
#
#
# # typedef BOOL(WINAPI*pfnSetWindowCompositionAttribute)(HWND, struct WINDOWCOMPOSITIONATTRIBDATA*)
#
# def get_com(self, hWnd):
#     # Utils.call_dll(self)
#     hUser = win32api.GetModuleHandle("user32.dll")
#     if hUser:
#         print('user32.dll')
#         setWindowCompositionAttribute = win32api.GetProcAddress(hUser, "SetWindowCompositionAttribute")
#         # setWindowCompositionAttribute = (pfnSetWindowCompositionAttribute)setWindowCompositionAttribute
#         print(type(setWindowCompositionAttribute))
#
#         if setWindowCompositionAttribute:
#             accent = ACCENT_POLICY(ACCENT_STATE.ACCENT_ENABLE_BLURBEHIND, 0, 0, 0)
#             data = WINDOWCOMPOSITIONATTRIBDATA()
#             data.dwAttrib = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY
#             data.pvData = accent
#             data.cbData = sizeof(accent)
#             setWindowCompositionAttribute(hWnd, data)


class MyEffect(QtWidgets.QGraphicsEffect):
    def __init__(self, *args, **kwargs):
        super(MyEffect, self).__init__(*args, **kwargs)

        self.item = QGraphicsItem()


# 带小三角的窗口
class ArrowWidget(QtWidgets.QWidget):
    SHADOW_WIDTH = 15  # 窗口阴影宽度
    BORDER_RADIUS = 5  # 窗口边角的弧度
    TRIANGLE_WIDTH = 15  # 小三角的宽度
    TRIANGLE_HEIGHT = 10  # 小三角的高度

    def __init__(self, *args, **kwargs):
        super(ArrowWidget, self).__init__(*args, **kwargs)

        self.start_pos = 0
        self.triangle_width = 0
        self.triangle_height = 0

        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)  # 设置无边框窗口
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        # 设置阴影边框
        Utils.set_effect(self, 1, self.SHADOW_WIDTH, 0, 0, QtCore.Qt.gray)

        self.setFixedSize(150, 200)

    # 设置小三角起始位置;
    def set_start_pos(self, start_pox):
        self.start_pos = start_pox

    # 设置小三角宽和高
    def set_triangle(self, width, height):
        self.triangle_width = width
        self.triangle_height = height

    # 设置中间区域widget
    def set_center_widget(self, widget):
        lh = QtWidgets.QHBoxLayout(self)
        lh.addWidget(widget)
        lh.setSpacing(0)
        lh.setContentsMargins(self.SHADOW_WIDTH, self.SHADOW_WIDTH + self.TRIANGLE_HEIGHT,
                              self.SHADOW_WIDTH, self.SHADOW_WIDTH)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255))

        #  小三角区域
        trianglePolygon = QPolygon()
        trianglePolygon.setPoint(0, QPoint(self.start_pos, self.triangle_height + self.SHADOW_WIDTH))
        trianglePolygon.setPoint(1, QPoint(self.start_pos + self.triangle_width // 2, self.SHADOW_WIDTH))
        trianglePolygon.setPoint(2, QPoint(self.start_pos + self.triangle_width,
                                           self.triangle_height + self.SHADOW_WIDTH))
        # 小三角区域
        rect = QRect(self.SHADOW_WIDTH,
                     self.triangle_height + self.SHADOW_WIDTH,
                     self.width() - self.SHADOW_WIDTH * 2,
                     self.height() - self.SHADOW_WIDTH * 2 - self.triangle_height)

        drawPath = QPainterPath()
        drawPath.addRoundedRect(rect, self.BORDER_RADIUS, self.BORDER_RADIUS)

        # Rect + Triangle
        drawPath.addPolygon(trianglePolygon)
        painter.drawPath(drawPath)


class AeroButton(QPushButton):
    def __init__(self, a, b, c, parent=None):
        super(AeroButton, self).__init__(parent)
        # self.setEnabled(True)
        self.a = a
        self.b = b
        self.c = c
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
        # painter_path.addRoundedRect(1, 1, button_rect.width() - 2, button_rect.height() - 2, self.roundness, self.roundness)
        painter_path.addEllipse(1, 1, button_rect.width() - 2, button_rect.height() - 2)
        painter.setClipPath(painter_path)
        if self.isEnabled():
            if not self.pressed and self.hovered is False:
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


class MainWin(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWin, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        # self.use_palette()

        pb = CircleImage(self)
        pb.set_me('./res/images/white go-1.png', QSize(500, 500), 0x0)
        # pb.set_me('./res/images/white go-1.png', QRect(10, 10, 50, 50), 0x0)
        # pb = EllipseButton(self)
        # pb.setFixedSize(300, 300)
        # pb.set('./res/images/white go1.png')

        e2 = QtWidgets.QGraphicsDropShadowEffect()
        e2.setBlurRadius(20)  # 阴影半径，虚化程度，不能大于圆角半径
        e2.setOffset(5, 5)  # 阴影宽度
        e2.setColor(QtGui.QColor(0, 0, 0, 180))  # 阴影颜色
        pb.setGraphicsEffect(e2)

        # go_board = QtWidgets.QFrame()
        # Utils.set_effect(go_board, 1, 15, 5, 5, QColor(220, 120, 100, 230))
        #
        # self.lb_bg = BackLabel(go_board, 'res/images/wenli41.jpg', 25, 25)
        # self.lb_bg.update()
        # e1 = QtWidgets.QGraphicsBlurEffect()
        # e1.setBlurRadius(20)
        # e1.setBlurHints(QtWidgets.QGraphicsBlurEffect.QualityHint)
        # self.lb_bg.setGraphicsEffect(e1)
        # Utils.set_effect(self.lb_bg, 3, QColor(222, 222, 0, 120), 5)

        # self.lb_bg.setScaledContents(True)

        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)  # 设置无边框窗口
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # self.setStyleSheet('background: rgba(255, 255, 255, 0);  /*半透明*/')

        self.setObjectName('w')

        #         self.pb = QPushButton('试看天下')
        #         self.pb.setFixedHeight(100)
        #         qss = '''
        #             QPushButton{/*默认显示*/
        #                 border-radius:40px;/*圆角弧度(为正方形边长一半时就是圆形)*/
        #                 background-color:rgba(0,255,0,255);/*背景色*/
        #             }
        #             QPushButton:hover{/*鼠标悬停*/
        #                 background-color:rgba(0,0,255,255);
        #             }
        #             QPushButton:pressed{/*鼠标按下*/
        #                 background-color:rgba(255,0,0,255);
        #             }
        #         '''
        #         qss1 = 'QPushButton{background: darkgray;' \
        #                'font-size: 20px;' \
        #                'color: blue;' \
        #                'text-shadow: 3px 3px 2px black, -3px -3px 2px white; }' \
        #                'QPushButton:hover {text-shadow: 3px 3px 2px white, -3px -3px 2px black;}'
        #         '''text-shadow: 0 1px 0 #eee; 凹进效果
        # text-shadow: 0 -1px 0 #123; 凹进效果
        # text-shadow: 0 -1px 1px #eee; 凸出效果
        # text-shadow: 0 1px 1px #123; 凸出效果'''
        #         qss2 = '''/*按钮普通态*/
        # QPushButton
        # {
        #     /*字体为微软雅黑*/
        #     font-family:Microsoft Yahei;
        #     /*字体大小为20点*/
        #     font-size:20pt;
        #     /*字体颜色为白色*/
        #     color:white;
        #     /*背景颜色*/
        #     background-color:rgb(14 , 150 , 254);
        #     /*边框圆角半径为8像素*/
        #     border-radius:8px;
        # }
        #
        # /*按钮停留态*/
        # QPushButton:hover
        # {
        #     /*背景颜色*/
        #     background-color:rgb(44 , 137 , 255);
        # }
        #
        # /*按钮按下态*/
        # QPushButton:pressed
        # {
        #     /*背景颜色*/
        #     background-color:rgb(14 , 135 , 228);
        #     /*左内边距为3像素，让按下时字向右移动3像素*/
        #     padding-left:3px;
        #     /*上内边距为3像素，让按下时字向下移动3像素*/
        #     padding-top:3px;
        # }'''
        #         self.pb.setStyleSheet(qss2)
        # self.pb.setStyleSheet('background-image:url(./res/background/bk3.jpg); /*  */'
        #                       'border-radius:15px;     /*画出圆角*/')

        # w = ArrowWidget()
        # w.set_start_pos(60)
        # w.set_triangle(20, 12)
        # w.setFixedSize(QSize(150, 80))
        # textLabel = QLabel("ArrowWidget")
        # textLabel.setAlignment(Qt.AlignCenter)
        # w.set_center_widget(textLabel)
        # w.show()

        lv = QVBoxLayout(self)
        # lv.addWidget(pb)
        # lv.addWidget(self.lb_bg)
        # lv.addWidget(go_board)

        # self.get_com()

    def paintEvent(self, e: QPaintEvent):
        self.text = '好好享受'
        # self._text.setHtml('<b>R(' + str(self._id) + ')</b>')
        self.font = QtGui.QFont("Ubuntu Mono")
        qp = QtGui.QPainter()

        metrics = QFontMetrics(self.font)
        path = QPainterPath()
        pen = QPen(Qt.red)  # 你的轮廓颜色

        pen_width = 2  # 你的轮廓大小

        pen.setWidth(pen_width)

        # 以下代码用于获取字体绘制中的居中的位置，因此绘制出来都是居中的字体
        length = metrics.width(self.text)
        w = self.width()
        px = (length - w) / 2
        if px < 0:
            px = -px
        py = (self.height() - metrics.height()) / 2 + metrics.ascent()
        if py < 0:
            py = -py

        # print(px, py)

        path.addText(px, py, self.font, self.text)  # 将绘制字体的路径添加到path中
        qp.setRenderHint(QPainter.Antialiasing)  # 开启抗锯齿，不然看起来很难看
        qp.strokePath(path, pen)  # 描边
        # qp.drawPath(path) # 画边
        qp.fillPath(path, QBrush(Qt.white))  # 填充path，其中QBrush可以设置填充颜色

    def resizeEvent(self, a0: QResizeEvent) -> None:
        super(MainWin, self).resizeEvent(a0)
        # self.lb_bg.update()
        # self.lb_bg.resize(self.width() - 300, self.height() - 200)
        # self.lb_bg.setPixmap(Utils.img_center(self.lb_bg.width(),
        #                                       self.lb_bg.height(),
        #                                       './res/images/wenli.jpg'))
        # Utils.setBg(self, self.lb_bg, './res/background/bk2.jpg')
        # self.lb_bg.setAlignment(Qt.AlignCenter)
        # self.lb_bg.resize(self.width() // 2, self.height() // 2)
        # pix = Utils.img_center(self.lb_bg.width(), self.lb_bg.height(),
        #                        './res/background/bk1.jpg')
        # print('here',type(pix))
        # self.lb_bg.setPixmap(pix)
        # self.lb_bg.setPixmap(QPixmap('./res/background/bk1.jpg'))

        # self.pb.resize(200, 800)
        # self.pb.setStyleSheet('border-radius:15px;     /*画出圆角*/')

    def use_palette(self):
        self.setWindowTitle("设置背景图片")
        window_pale = QPalette()
        window_pale.setBrush(self.backgroundRole(),
                             QBrush(QPixmap("./res/background/bk1.jpg")))
        self.setPalette(window_pale)


def ddd(img):
    im = Image.open(img)
    size = im.size
    print(size)
    x, y = 0, 0
    w = size[0]
    h = size[1]

    # yy 91 294  xx 30 233
    # 29 275     96 345
    # 34 254    101 321
    # region = im.crop((0, 1000, 2000, 2000))
    # region.save("./white2.png")

    hmax, hmin = 0, h

    for j in range(h):
        for i in range(w):
            point = im.getpixel((i, j))
            # im.putpixel((i, j), point)
            # print(point)
            if point[0] < 250:
                im.putpixel((i, j), (point[0]+150, point[1]+150, point[2]+150, 255))

                hmin = j if hmin > j else hmin
                hmax = j if hmax < j else hmax
                # x = i
                # y = i

            else:
                # print(point)
                ...
                # print(x)


            # y = j
        # print(x, y, im.getpixel((w//2, 93)), im.getpixel((w//2, 94)))
        # print(x, y, im.getpixel((88, h // 2)), im.getpixel((89, h // 2)))
    print(hmin, hmax)
    # im.save(r'./tmp.png')#x::89 292  yy 91 294
    #     yy 91 294  xx 30 233


if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # win = MainWin()
    # win.show()

    # w = ArrowWidget()
    # w.set_start_pos(60)
    # w.set_triangle(20, 12)
    # # w.setFixedSize(QSize(150, 80))
    # textLabel = QLabel("ArrowWidget")
    # textLabel.setAlignment(Qt.AlignCenter)
    # w.set_center_widget(textLabel)
    # w.show()

    # sys.exit(app.exec_())

    # ddd(r'E:\Neworld\res\images\timg.jpg')
    ddd(r'E:\Neworld\res\background\goW.png')
    # print(round(2.5*100))
