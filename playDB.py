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
import copy
import math
import pyttsx3
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from functools import partial
from enum import IntEnum, unique
import numpy as np
import piexif
from utilities import Utils, EllipseButton, StyleSheet, MyJson
import cv2

# import cgitb  # �൱����

# cgitb.enable(format='text')  # ��� pyqt5 �쳣ֻҪ�����¼�ѭ��,����ͱ���,��û���κ���ʾ


# sys.setrecursionlimit(10000)


class VideoDisplay(QWidget):
    def __init__(self, *args, **kwargs):
        super(VideoDisplay, self).__init__(*args, **kwargs)
        self.parent = args[0]

        # Ĭ����ƵԴΪ���
        self.ui.radioButtonCam.setChecked(True)
        self.isCamera = True

        # �źŲ�����
        ui.Open.clicked.connect(self.Open)
        ui.Close.clicked.connect(self.Close)
        ui.radioButtonCam.clicked.connect(self.radioButtonCam)
        ui.radioButtonFile.clicked.connect(self.radioButtonFile)

        # ����һ���ر��¼�����Ϊδ����
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
            # ��������rtsp��ʽ����֧�ֵ�
            # cap = cv2.VideoCapture("rtsp://admin:Supcon1304@172.20.1.126/main/Channels/1")
            self.cap = cv2.VideoCapture("rtsp://admin:Supcon1304@172.20.1.126:554/h264/ch1/main/av_stream")

        # ������Ƶ��ʾ�߳�
        th = threading.Thread(target=self.Display)
        th.start()

    def Close(self):
        # �ر��¼���Ϊ�������ر���Ƶ����
        self.stopEvent.set()

    def Display(self):
        self.ui.Open.setEnabled(False)
        self.ui.Close.setEnabled(True)

        while self.cap.isOpened():
            success, frame = self.cap.read()
            # RGBתBGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.ui.DispalyLabel.setPixmap(QPixmap.fromImage(img))

            if self.isCamera:
                cv2.waitKey(1)
            else:
                cv2.waitKey(int(1000 / self.frameRate))

            # �жϹر��¼��Ƿ��Ѵ���
            if True == self.stopEvent.is_set():
                # �ر��¼���Ϊδ�����������ʾlabel
                self.stopEvent.clear()
                self.ui.DispalyLabel.clear()
                self.ui.Close.setEnabled(False)
                self.ui.Open.setEnabled(True)
                break


class ItemDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.decorationPosition = QtWidgets.QStyleOptionViewItem.Right
        super(ItemDelegate, self).paint(painter, option, index)


# Բ��ͼƬ��ť
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


class MyQLabel(QLabel):
    clicked = pyqtSignal()  # �Զ��嵥���ź�
    DoubleClicked = pyqtSignal()  # �Զ���˫���ź�

    def __init__(self, *args, **kwargs):
        super(MyQLabel, self).__init__(*args, **kwargs)
        # self.setFixedSize(200, 200)
        self.setMouseTracking(True)  # ����ƶ�����
        # self.setScaledContents(True)  # ͼƬ����ӦQLabel��С

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
            # self.setAutoFillBackground(True)  # /Widget���ӱ���ͼƬʱ�����һ��Ҫ��
            # wide = min(width, height)
            # pix = QtGui.QPixmap(img).scaled(wide, wide, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
            # self.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(img_new)))
            # self.setIconSize(QtCore.QSize(wide, wide))
            # self.setFlat(True)  # ��������ܹ�ʵ�ְ�ť͸������pngͼƬʱ������
            # border = 0  # �����߿�ȡ�����Ч��

            qss = '''
                color: %s;
                background-color: %s;
                background: transparent;     /*ȫ͸��*/
                background-image:url(%s);
                background-position: center center;      /*ͼƬ��λ�ã����У��������*/
                background-repeat: no-repeat;       /*������Ҫ�ظ�*/

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
        painter.drawRoundedRect(0, 0, size.width(), size.height(), 99, 99)
        image = QPixmap(pix_src.scaled(size))
        image.setMask(mask)

        return image

    def set_img(self, img_file):
        self.img = img_file

    # ��ͼƬ������ȫ����ʾ���������ڱΣ��Ҿ��У����
    def show_center_img(self):
        if not self.img:
            return

        img = QImage(self.img)
        sw, sh = self.width(), self.height()
        ratio_w = img.width() / sw
        ratio_h = img.height() / sh

        is_w = True if ratio_w < ratio_h else False
        # print(sw, sh, is_w)

        img_new = img.scaledToWidth(sh) if is_w else img.scaledToHeight(sw)
        # img_new = img.scaled(sw, sh, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # print(img_new.size(), img.size())

        self.setPixmap(QPixmap.fromImage(img_new))
        self.setAlignment(Qt.AlignCenter)

    # def show_circle_img(self, img_file, scale=1.0):
    #     assert img_file, "��������"
    #
    #     #     # ��ʾԲ��ͼ��
    #     #     label.setStyleSheet('min-width:  100px;max-width:  100px;'
    #     #                     'min-height: 100px;max-height: 100px;'
    #     #                     'border-radius: 50px;border-width: 0 0 0 0;'
    #     #                     'border-image: url(./res/images/water.png) 0 0 0 0 stretch')
    #
    #     # ������Բ�ĳ��ᡢ����
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
    #     path.addEllipse(0, 0, sw, sh)  # ������Բ
    #     painter.setClipPath(path)
    #
    #     painter.drawPixmap(0, 0, sw, sh, pix)
    #     # self.setPixmap(img_file)

    # ��д��굥���¼�
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super(MyQLabel, self).resizeEvent(a0)
        self.show_center_img()

    def mousePressEvent(self, QMouseEvent):  # ����
        self.clicked.emit()

    # ��д���˫���¼�
    def mouseDoubleClickEvent(self, QMouseEvent):  # ˫��
        self.DoubleClicked.emit()

    # ��widget���ܻ���Ӱ
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


class TitleBar(QWidget):
    StyleSheet = """
    /*������*/
    TitleBar {
        /*background: transparent;     ȫ͸��*/
        /*background-color: skyblue;   */
        /*background-color:rgba(0,0,0,0.1)      ��͸��*/
        border-top-right-radius:15;
        /*background-image:url(./res/background/bk5.jpg);*/
        background-repeat: no-repeat;       /*������Ҫ�ظ�*/
        background-position: center center;      /*ͼƬ��λ�ã����У��������*/
    }
    /*��С����󻯹رհ�ťͨ��Ĭ�ϱ���*/
    #buttonMinimum,#buttonMaximum,#buttonClose {
        /*background-color: skyblue;*/
        /*background:rgba(0,0,0,0.3)      ��͸��*/
        border:none;    /*ȫ͸��*/
        color:red
    }
    /*��ͣ*/
    #buttonMinimum:hover,#buttonMaximum:hover {
        /*background-color: green;*/
        /*color: red;���������ǰ�����Ч��*/
        background:rgba(0,0,0,0.2)     /*��͸��*/
    }
    /*��갴�²���*/
    #buttonMinimum:pressed,#buttonMaximum:pressed {
        /*background-color: Firebrick;*/
        /*color: blue;���������ǰ�����Ч��*/
        background:rgba(0,0,0,0.4)      /*��͸��*/
    }
    #buttonClose:hover {
        color: red;
        /*background-color: gray;*/
        /*background:rgba(0,0,0,0.4)      ��͸��*/
    }
    #buttonClose:pressed {
        color: red;
        /*background-color: Firebrick;*/
        /*background:rgba(0,0,0,0.4)      ��͸��*/
    }
    """

    # region �ź�������
    sign_pb_prev = pyqtSignal()  # ǰһ��
    sign_pb_next = pyqtSignal()  # ��һ��
    sign_win_minimize = pyqtSignal()  # ������С���ź�
    sign_win_maximize = pyqtSignal()  # ��������ź�
    sign_win_resume = pyqtSignal()  # ���ڻָ��ź�
    sign_win_close = pyqtSignal()  # ���ڹر��ź�
    sign_win_move = pyqtSignal(QPoint)  # �����ƶ�

    # endregion

    def __init__(self, *args, **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)

        self.setStyleSheet(TitleBar.StyleSheet)

        self.setMouseTracking(True)
        # ����͸�����ؼ���͸��
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_StyledBackground, True)  # ֧��qss���ñ���
        self.mPos = None
        self.iconSize = 20  # ͼ���Ĭ�ϴ�С
        # ����Ĭ�ϱ�����ɫ,���������ܵ������ڵ�Ӱ�쵼��͸��
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(palette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        # ����
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # ������ͼ��
        self.lb_icon = QLabel(self)
        self.lb_icon.setPixmap(QtGui.QPixmap('./res/images/star.png'))
        # self.lb_icon.setScaledContents(True)
        # self.lb_icon.setFixedWidth(100)
        # self.lb_icon.setStyleSheet('background: transparent; ')
        layout.addWidget(self.lb_icon)

        # pb_prev = QPushButton('ǰһ��', self, clicked=self.sign_pb_prev.emit)
        # pb_prev.setStyleSheet('color:red')
        # ���ڱ���
        layout.addStretch()
        self.lb_title = QLabel(self.tr('�˶�����'), self)
        self.lb_title.setMargin(2)
        self.lb_title.setStyleSheet(
            'color: red;font-size:24px;font-weight:bold;font-family:Roman times;')
        # pb_next = QPushButton('��һ��')
        # layout.addWidget(pb_prev)
        layout.addWidget(self.lb_title)
        # layout.addWidget(pb_next)
        # layout.addStretch()
        # �м�������
        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # ����Webdings��������ʾͼ��
        font = self.font() or QFont()
        font.setFamily('Webdings')

        # ��С����ť
        self.min_button = QPushButton(
            '0', self, clicked=self.sign_win_minimize.emit, font=font, objectName='buttonMinimum')
        # self.min_button.setAutoFillBackground(False)
        # self.min_button.setStyleSheet("background-color: rgb(28, 255, 3);")
        # self.min_button.setAutoDefault(False)
        # self.min_button.setDefault(False)
        # self.min_button.setFlat(False)
        layout.addWidget(self.min_button)
        # ���/��ԭ��ť
        self.buttonMaximum = QPushButton(
            '1', self, clicked=self.showMaximized, font=font, objectName='buttonMaximum')
        layout.addWidget(self.buttonMaximum)
        # �رհ�ť
        self.buttonClose = QPushButton(
            'r', self, clicked=self.sign_win_close.emit, font=font, objectName='buttonClose')
        layout.addWidget(self.buttonClose)
        # ��ʼ�߶�
        self.setHeight()

    def showMaximized(self):
        if self.buttonMaximum.text() == '1':
            # ���
            self.buttonMaximum.setText('2')
            self.sign_win_maximize.emit()
        else:  # ��ԭ
            self.buttonMaximum.setText('1')
            self.sign_win_resume.emit()

    def setHeight(self, height=38):
        """���ñ������߶�"""
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        # �����ұ߰�ť�Ĵ�С
        self.min_button.setMinimumSize(height, height)
        self.min_button.setMaximumSize(height, height)
        self.buttonMaximum.setMinimumSize(height, height)
        self.buttonMaximum.setMaximumSize(height, height)
        self.buttonClose.setMinimumSize(height, height)
        self.buttonClose.setMaximumSize(height, height)

    def setTitle(self, title):
        """���ñ���"""
        self.titleLabel.setText(title)

    def setIcon(self, icon):
        """����ͼ��"""
        self.iconLabel.setPixmap(icon.pixmap(self.iconSize, self.iconSize))

    def setIconSize(self, size):
        """����ͼ���С"""
        self.iconSize = size

    def mouseDoubleClickEvent(self, event):
        super(TitleBar, self).mouseDoubleClickEvent(event)
        self.showMaximized()

    def mousePressEvent(self, event):
        """������¼�"""
        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()  # widget�������Ͻ�����ڵ�����Ļ�����Ͻǵģ�x=0,y=0��ƫ��λ��
            # pos = QtGui.QMouseEvent()
            # self.mPos = event.globalPos()  # ���ƫ�������Ļ���Ͻǣ�x=0,y=0����λ��
        event.accept()

    def mouseReleaseEvent(self, event):
        """��굯���¼�"""
        self.mPos = None
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.mPos:
            # ��Ҫ�����������غ��ȥ���������margins
            self.sign_win_move.emit(self.mapToGlobal(event.pos() - self.mPos - QPoint(15, 15)))
            # self.sign_win_move.emit(event.globalPos() - self.mPos)
        event.accept()

    def enterEvent(self, event):
        self.setCursor(QCursor(Qt.PointingHandCursor))  # �������ͼ��
        super(TitleBar, self).enterEvent(event)
        event.accept()

    def leaveEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))
        event.accept()

    def wheelEvent(self, event):
        event.accept()


@unique  # @unique װ�������԰������Ǽ�鱣֤valueû���ظ�ֵ
class Const(IntEnum):
    # �̳���Enum��ö�����е�Key������ͬ��Value�����࣬
    # ҪValueҲ������ͬ����ô�ڵ���Enum��ͬʱ����Ҫ����unique����
    # ö������������Ƚϣ�ʹ��==������is��ö���಻������ʵ��������,�����ⲿ�����޸�Valueֵ
    CENTER = '0'
    TOP = 1
    BOTTOM = '2'
    LEFT = 3
    RIGHT = 4
    TL_CORNER = 5  # ���Ͻ�
    TR_CORNER = 6  # ���Ͻ�
    BL_CORNER = 7
    BR_CORNER = 8

    PADDING = 20  # �����ٱ߿�ı߾࣬>=margin
    MARGIN = 15  # ���ܱ߾�


class ChildMenu(QWidget):
    def __init__(self):
        super(ChildMenu, self).__init__()
        self.parent = None
        self.menu_data = [
            [(QIcon(), '�˶���Դ'), (QIcon(), '�İ�'), (QIcon(), '��Ƶ'), (QIcon(), '��ҳ')],
            [(QIcon(), '������λ'), (QIcon(), '�ֱ�'), (QIcon(), '�米'), (QIcon(), '����'), (QIcon(), '�Ȳ�')],
            [(QIcon(), '���Թ滮'), (QIcon(), 'ռλ')],
            [(QIcon(), '����ָ��'), (QIcon(), 'ռλ')],
            [(QIcon(), '����'), (QIcon(), 'ռλ')]
        ]
        self.button_width = 40
        self.button_spacing = 10
        self.button_margin = 10
        self.stack_index = 0
        # self.setFixedHeight(self.parent.parent.menu_height)
        # self.resize(800, 60)
        self.stacked_menu = QStackedWidget()
        # self.raise_()  # ���������д����ö�

        # self.setMouseTracking(True)
        # self.stacked_menu.setMouseTracking(True)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)  # �����ޱ߿򴰿�
        # self.setWindowModality(Qt.ApplicationModal)# �����ö�
        # self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool |  # ����������ǰ��
        #                     Qt.MSWindowsFixedSizeDialogHint |
        #                     Qt.WindowCloseButtonHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # ���ô��ڱ���͸��

        self.setObjectName('child')
        self.setStyleSheet('QWidget#child {'
                           'background-color: #0f0 ;'
                           'border-top-right-radius:10;'
                           'border-bottom-right-radius:10;}')
        self.stacked_menu.setObjectName('stack')
        self.stacked_menu.setStyleSheet('#stack {background: transparent;     /*ȫ͸��*/'
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
        sender = self.sender()  # ��ȡ���Ϳؼ�
        self.parent.parent.submenu_clicked(sender.text())

    def select_stack(self, stack_index):
        self.stack_index = stack_index
        self.stacked_menu.setCurrentIndex(stack_index)

        # �ѱ�Ŀؼ������أ������ܸı��С��
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
        pos = self.mapFromGlobal(QCursor.pos())  # ���������λ��
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
        assert isinstance(self.parent, Canvas), '�б�ĸ����岻��ȷ'
        self.child = self.parent.sub_menu
        assert isinstance(self.child, ChildMenu), '�б���Ӳ˵����岻��ȷ'

        self.cur_row = -1  # ���б�־
        self.is_done = False  # �������
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
        # size = self.sizeHint()  # �ߴ�
        # size = item.sizeHint()
        row = self.row(item)
        # row1 = e.pos().y() // size.height()
        if row != self.cur_row:  # �����ˣ����²˵�
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
            # ������Ҫ������������ʵ��ó�
            y += (self.mapToGlobal(self.pos()) - self.pos()).y()
            x += self.mapToGlobal(self.pos()).x()

            self.child.move(x, y)
            # self.child.setWindowModality(Qt.ApplicationModal)

            # self._animation.stop()
            # self._animation.setStartValue(QRect(x, y, 0, ch))
            # self._animation.setEndValue(QRect(x, y, cw, ch))
            # self._animation.start()
            # ���� QAbstractAnimation.KeepWhenStopped  ֹͣʱ����ɾ������
            #     QAbstractAnimation.DeleteWhenStopped   ֹͣʱ�������Զ�ɾ��

            self.child.show()  # frameGeometry������ʾ����

        # e.ignore()

    def leaveEvent(self, e: QtCore.QEvent):
        # here the code for mouse leave
        # print('list leave')
        self.setCursor(Qt.ArrowCursor)
        self.cur_row = -1
        self.is_done = False
        pos = self.mapFromGlobal(QCursor.pos())  # ���������λ��
        # pos = e.pos()
        # print(type(pos), pos)
        if pos.x() >= self.parent.left_width:
            # self.child.grabMouse()  # �õ����ڲ�������¼��Ĵ���
            # ������괩͸
            # self.parent.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            # self.child.setWindowModality(Qt.ApplicationModal)
            pass
        else:
            self.child.hide()

        e.accept()

    #     # # ��ȡitem��button
    #     # button = self.sender()
    #     # # ��ȡ��ť�����listwwdget������
    #     # # listwidget ����ڴ�������� ��ȥ button ����ڴ��������
    #     # buttonpos = button.mapToGlobal(QPoint(0, 0)) - self.listwidget.mapToGlobal(QPoint(0, 0))
    #     # # ��ȡ������
    #     # item = self.listwidget.indexAt(buttonpos)
    #     # print(item)
    #     # # ��ȡλ��
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
    # #     # accept()        # ��ʾ�¼��Ѵ�������Ҫ�򸸴��ڴ���
    # #     # buttons()  # �����ĸ���갴������ס�ˡ�
    # #     # ignore()        # ��ʾ�¼�δ���������򸸴��ڴ���
    #
    # # def hoverLeaveEvent(self, event):
    # #     print('Leave')
    # #
    # # def hoverMoveEvent(self, event):
    # #     print('Moving')
    #
    # """��д����¼���ʵ�ִ����϶���"""

    # item.setText(name)  # ����
    # item_name = item.text()  # ��ȡ
    # item.setData(Qt.UserRole, name)  # ����
    # item_name = item.data(Qt.UserRole)  # ��ȡ
    #
    # try:
    #     if event.buttons() and Qt.LeftButton:
    #         self.parent.move(event.globalPos() - self.parent.m_DragPosition)  # move�������ƶ���ָ��λ��
    #         event.accept()
    # except AttributeError:
    #     pass
    # event.ignore()

    # def mouseReleaseEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.m_drag = False
    #         self.unsetCursor()

    # �˵�������ʾ

    # def contextMenuEvent(self, event):
    #     pos = event.globalPos()
    #     print('�Ҽ��˵�')
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
    #     self._contextMenu.addAction('�˵�1', self.hello)
    #     self._contextMenu.addAction('�˵�2', self.hello)
    #     self._contextMenu.addAction('�˵�3', self.hello)
    #     self._contextMenu.addAction('�˵�4', self.hello)
    #     self._contextMenu.addAction('�˵�5', self.hello)
    #     self._contextMenu.addAction('�˵�6', self.hello)

    def initAnimation(self, control):
        # ��ť����
        self._animation = QPropertyAnimation(control, b'geometry', self)
        self._animation.setEasingCurve(QEasingCurve.Linear)
        self._animation.setDuration(300)
        # easingCurve �޸ĸñ�������ʵ�ֲ�ͬ��Ч��
        # s = self._animation.loopCount()  # ���ض�����ѭ������
        # print(s)


# ����Ļ��/����
class Curtain(QWidget):
    def __init__(self, parent):
        super(Curtain, self).__init__(parent)
        self.parent = parent
        # self.setAttribute(Qt.WA_TranslucentBackground)  # ���ô��ڱ���͸��
        self.use_palette()

        self.data_dir = None
        self.is_carousel = False  # �ֲ�չʾ���ǵ���ͼչʾ
        self.is_acting = False  # ����ͼ���Ƿ���ͼ
        self.title = ''  # ����
        self.resume = ''  # ���
        self.notice = []  # ÿ�����ж�������������Ҫ���Լ���������������Ϣʱ��
        self.action = []  # ÿ������ж������������ơ�Ҫ�졢��ͼʾ��
        self.cur_act = 0  # ��ǰ����
        self.cover = []  # ����ͼ
        self.cur_cov = 0

        self.stay = 60  # ����֮��ͣ��������
        # self.engine = pyttsx3.init()  # ��ʼ��������
        self.timer = QTimer(self)  # ��ʼ��һ����ʱ��

        self.pb_style = QPushButton('��ʾ����')
        self.pb_prev = QPushButton("ǰͼ")
        self.pb_next = QPushButton("��ͼ")
        self.pb_model = QPushButton('����')

        self.lb_title = QLabel()  # ÿ�������ƻ��ı���
        self.lb_resume = QLabel()  # ÿ�������ƻ��ı��⼰����
        self.lb_notice = QLabel()  # ������ʾ
        self.lb_gist = QLabel()  # ��������
        self.lb_img = QLabel()  # ������ͼ
        self.movie = QMovie()  # ������ͼ

        self.init_ui()
        # self.clear()
        # self.data_serialize(r'E:\dumbbell\plan\16ͼ')
        # self.start()

        Utils.center_win(self)

    def init_ui(self):
        # font = QtGui.QFont('΢���ź�', 15)
        # self.setFont(font)
        self.timer.timeout.connect(self._motion)  # ÿ�μ�ʱ��ʱ��ʱ�����ź�

        # region �Զ��幤����
        toolbar = QFrame()
        toolbar.setObjectName('w')
        toolbar.setAttribute(Qt.WA_TranslucentBackground)  # ���ô��ڱ���͸��
        toolbar.setFrameStyle(QFrame.NoFrame | QFrame.Raised)  # Box
        # ./res/background/bk5.jpg
        Utils.bg_trans('./tmp.png', 200, 100, (255, 255, 255, 100))
        toolbar.setStyleSheet(
            "background-image:url(./tmp.png); /*  */"
            "/*background-color: cyan;   */"
            "/*color:red;  */"
            "font-size:24px;font-weight:bold;font-family:΢���ź�;")

        lh = QHBoxLayout(toolbar)

        lb = QLabel('ռλ')
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

        # region ������
        self.lb_title.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.lb_title.setAlignment(Qt.AlignCenter)
        self.lb_title.setStyleSheet(
            "background:white;color:rgba(255,0,0,255);"
            "font-size:26px;font-weight:bold;font-family:΢���ź�;")

        self.lb_resume.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.lb_resume.setWordWrap(True)
        self.lb_resume.setStyleSheet(
            "background:white;color:rgba(0,255,0,255);"
            "font-size:24px;font-weight:bold;font-family:΢���ź�;")

        self.lb_notice.setAlignment(Qt.AlignCenter)
        self.lb_notice.setWordWrap(True)
        self.lb_notice.setStyleSheet(
            "background:white;color:blue;"
            "font-size:24px;font-weight:bold;font-family:΢���ź�;")

        self.lb_gist.setVisible(False)
        self.lb_gist.setWordWrap(True)
        # self.lb_gist.setMinimumWidth(100)
        self.lb_gist.setStyleSheet(
            "background:white;color:green;border: 2px solid gray;"
            "font-size:24px;font-weight:bold;font-family:΢���ź�;")

        self.lb_img.setMinimumSize(400, 400)
        self.lb_img.setMaximumSize(800, 800)
        self.lb_img.setAlignment(Qt.AlignCenter)
        self.lb_img.setStyleSheet("background: transparent;     /*ȫ͸��*/;"
                                  "border: 0px solid green")
        # self.lb_img.setScaledContents(True)

        self.movie.setScaledSize(self.lb_img.size())  # ����GIFλ���Լ���С�� labelһ��
        # speed = self.movie.speed()
        # print(speed)
        # self.movie.setSpeed(100)
        # self.movie.setSpeed(self.movie.speed() -100)
        # self.engine.setProperty('rate', self.engine.getProperty('rate') - 50)  # ��������
        # self.engine.setProperty('volume', self.engine.getProperty('volume') + 5)  # ��������

        # voices = self.engine.getProperty('voices')  # ѡ������
        # # for voice in voices:
        # #     print(voice.id, voice.languages)
        # self.engine.setProperty("voice", voices[0].id)
        # endregion

        # region �ܲ���
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

    # ��ʼ������
    def data_serialize(self, data_dir):
        # data = [
        #     "       �󲿷ֵĳ�ѧ�߶���ѡ�����������е���������嵫ȴ��֪������ĸ�����λ�Ķ���������"
        #     "����С��Ҳ�����������15�����嶯������������Ҫ��������",
        #     "ÿ������Ϊһ�飬ÿ��1-2���ӣ������Ϣ30s���ǵ���ϰ!",
        #     1,
        #     50,
        #     30,
        #     [
        #         "����һ:˫���������",
        #         "��������: ˫�ָ���һ����;������ǰ ������������� �����������״̬,�ս��Ŷ�ͷ������ͣ Ȼ����ƻ�ԭ ����ʼ״̬���ظ����϶�����",
        #         "1.gif"
        #     ],
        #     [
        #         "������:���彻�����",
        #         "��������: ˫�ֳ����崹����࣬������ԣ����⿿�������� ����ؽ�Ϊ֧�㣬������� ͬʱǰ���������ĳ��ϣ�������ߵ��ս��Ŷ�ͷ������ͣ Ȼ����ƻ�ԭ ����ʼ״̬���ظ����϶�����",
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
            # �ӿؼ�ʧЧ������
            self.pb_style.setEnabled(True)
            self.pb_model.setEnabled(True)
            self.pb_next.setEnabled(True)
            self.pb_prev.setEnabled(True)

    # ��ʼ������ǰ������
    def clear(self):
        self.data_dir = None
        self.is_carousel = False  # �ֲ����Ǿ�̬չʾ
        self.is_acting = False  # ��ʼ��������չʾ����
        self.title = ''  # ����
        self.resume = ''  # ���
        self.notice.clear()  # ÿ�����ж�������������Ҫ���Լ���������������Ϣʱ��
        self.action.clear()  # ÿ������ж������������ơ�Ҫ�졢��ͼʾ��
        self.cur_act = 0  # ��ǰ����
        self.cover.clear()  # ����ͼ
        self.cur_cov = 0
        self.timer.stop()

        self.lb_title.clear()
        self.lb_resume.clear()  # ÿ�������ƻ��ı��⼰����
        self.lb_notice.clear()  # ������ʾ
        self.lb_gist.clear()  # ��������
        self.lb_img.clear()  # ������ͼ
        self.movie.stop()  # ������ͼ

        # �ӿؼ�ʧЧ������
        self.pb_style.setText("��ʾ����")
        self.pb_model.setText("����")
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
        if name in ['��ʾ����', '��ʾ����']:
            self.is_acting = bool(1 - self.is_acting)  # ȡ��
            pb.setText('��ʾ����') if self.is_acting else pb.setText('��ʾ����')
            self.start(self.is_acting)
        elif name == 'ǰͼ':
            self.prev()
        elif name == '��ͼ':
            self.next()
        elif name in ['�ֲ�', '����']:
            self.is_carousel = bool(1 - self.is_carousel)  # ȡ��
            if self.is_carousel:
                pb.setText('�ֲ�')
            else:
                pb.setText('����')

            # �ӿؼ�ʧЧ������
            self.pb_prev.setEnabled(bool(1 - self.is_carousel))
            self.pb_next.setEnabled(bool(1 - self.is_carousel))

            self.carousel(self.is_carousel)

    def select_action(self, index):
        if -1 <= index < len(self.action):
            self.cur_act = index
            self.show_me()

    # ����չʾ��ͼ���Ƿ���ͼ
    def start(self, flag: bool = True):
        self.is_acting = flag
        self.flush()

    # �����ֲ��Զ�չʾ���ǵ���ͼ�˹�չʾ��������ͼ���߷���
    def carousel(self, flag: bool = True):
        self.is_carousel = flag
        self.flush()

    # �˹�չʾʱ��ǰͼ
    def prev(self):
        if not self.is_carousel:
            if self.is_acting:
                self.cur_act = self.cur_act - 1 \
                    if self.cur_act > 0 else len(self.action) - 1
            else:
                self.cur_cov = self.cur_cov - 1 \
                    if self.cur_cov > 0 else len(self.cover) - 1

            self.flush()

    # �˹�չʾʱ�ĺ�ͼ
    def next(self):
        if not self.is_carousel:
            if self.is_acting:
                self.cur_act = self.cur_act + 1 \
                    if self.cur_act < len(self.action) - 1 else 0
            else:
                self.cur_cov = self.cur_cov + 1 \
                    if self.cur_cov < len(self.cover) - 1 else 0

            self.flush()

    # ˢ�½�������
    def flush(self):
        self.lb_title.setText(self.title)
        self.lb_resume.setText(self.resume)
        if self.notice:
            self.lb_notice.setText(self.notice[0] + f'   ��{len(self.action)}��������')

        if self.is_carousel:
            self._carousel()
        else:
            self.timer.stop()
            self._alone()

    # ��ͼչʾ
    def _alone(self):
        if not self.is_acting:  # ��ʾ����
            self.lb_gist.setVisible(False)
            if not self.cover:
                return

            self.lb_img.setPixmap(QPixmap(self.cover[self.cur_cov]))
            # self.movie.stop()
            # self.lb_img.clear()
            # self.lb_img.set_img(self.cover[self.cur_cov])
            # self.lb_img.show_center_img()
        else:  # ��ʾ����
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

    # �ֲ�ͼչʾ
    def _carousel(self):
        period = 0
        if self.is_acting:
            if self.notice and len(self.notice) == 4:
                group, times, rest = self.notice[1:]  # ��������������Ϣʱ�䣬ÿ����2��
                period = group * (times * 2 + rest) * 1000  # ����
                # print(group, times, rest, period)
                # period = 1000
            else:
                period = (60 + self.stay) * 1000
        else:
            # print(len(self.cover))
            if self.cover and len(self.cover) > 1:
                period = 3000  # 3��
            else:
                return
        # print(period)
        self._motion()
        self.timer.start(period)  # ���ü�ʱ�������������λ����

    def _motion(self):
        if self.is_acting:
            self.cur_act = self.cur_act + 1 \
                if self.cur_act < len(self.action) - 1 else 0
        else:
            self.cur_cov = self.cur_cov + 1 \
                if self.cur_cov < len(self.cover) - 1 else 0

        self._alone()

    def use_palette(self):
        self.setWindowTitle("���ñ���ͼƬ")
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(),
                             QtGui.QBrush(QtGui.QPixmap("./res/background/bk1.jpg")))
        self.setPalette(window_pale)

    #     # ���߳�ִ�ж�ʱ����,��������
    #     # self._play_music()
    #     # threading.Timer(2, self._talking, ("��������",)).start()  # 10����ú���һ��
    #     # threading.Timer(0, self._update_face, ("��������",)).start()  # 10����ú���һ��


# ��Ӱ��Բ�ǡ���ͼ���Ӵ��壬�䵱������
class Canvas(QWidget):
    def __init__(self, parent):
        super(Canvas, self).__init__(parent)

        self.parent = parent
        self.title_height = 50  # �������߶�
        self.left_width = 150  # �����
        self.menu_height = 60  # �б�˵���ĸ߶�

        self.data_dir = 'e:/dumbbell'

        self.data_plan = ['һ��������ȫ��', '15ͼ', 'ʮ�˰�']
        self.data_video = []  # ��Դ����Ƶ�ļ�
        self.data_menu = []  # �˵�������
        self.body_arm = [('ʾ���ļ�', '����ʱ��', '����Ҫ��', '�Ѷ�')]

        # self.bg_label = QLabel()

        self.layout_main = QHBoxLayout(self)  # ���Ҳ���
        self.fm_left = QFrame()
        self.pb_person = EllipseButton(self, 50, 50)
        self.sub_menu = ChildMenu()
        self.listWidget = MyQListWidget(self)

        self.fm_right = QFrame()
        self.titleBar = TitleBar()
        self.stackedWidget = QStackedWidget()  # ��ջ����

        # ���Ӵ���Ĵ���
        # self.mdi = QMdiArea()QMdiSubWindow()
        # # Ϊ�Ӵ��ڼ���
        # self.count = self.count + 1
        # # ����һ���Ӵ���
        # sub = QMdiSubWindow()
        # # Ϊ�Ӵ������һ��TextEdit�ؼ�
        # sub.setWidget(QTextEdit())
        # self.mdi.addSubWindow(sub)
        # sub.show()
        # self.mdi.cascadeSubWindows()  # ������˵����е�Cascadeʱ���ѵ��Ӵ���
        # self.mdi.tileSubWindows()  # ������˵����е�Tiledʱ��ƽ���Ӵ���

        # # ����һ��DockWidget# ͣ������
        # self.items = QDockWidget()
        #
        # # ����һЩ���ݣ��ŵ�DockWidget�У�
        # self.listWidget = QListWidget()
        # self.listWidget.setFixedSize(150, 300)
        # self.listWidget.addItem('item1')
        # self.listWidget.addItem('item2')
        # self.listWidget.addItem('item3')
        # self.items.setWidget(self.listWidget)
        # # ��DockWidget�ӵ��������У�Ĭ��ͣ�����ұ�
        # self.addDockWidget(Qt.RightDockWidgetArea, self.items)
        # # �����������һЩ�ؼ�
        # self.setCentralWidget(QLineEdit())

        self.init_date()
        self.init_canvas_ui()
        self.init_ui()

    def init_date(self):
        # ��ʼ������
        data = MyJson.read(os.path.join(self.data_dir, 'menu.json'))
        # data = None
        if data:
            self.data_menu.extend(data)
        else:
            self.data_menu.extend([
                [('./res/images/1.ico', '�˶���Դ'), ('', '�İ�'), ('', '��Ƶ'), ('', '��ҳ')],
                [('', '������λ'), ('', '�粿'), ('', '����'), ('', '�ز�'), ('', '����'), ('', '�ֱ�'), ('', '�Ƚ�')],
                [('', '���Թ滮'), ('', 'ռλ')],
                [('', '����ָ��'), ('', 'ռλ')],
                [('', '����'), ('', 'ռλ')]
            ])

        # print(self.data_menu)
        # MyJson.write(self.data_menu, f'{self.data_dir}/menu.json')
        # for each in self.data_menu:
        #     path = self.data_dir + f'/{each[0][1]}/{each[0][1]}.json'
        #     print(each[1:], path)
        #     MyJson.write(each[1:], path)
        # for child in each[1:]:
        #     path = self.data_dir + f'/{each[0][1]}/{child[1]}/{child[1]}.json'
        #     print(child[1], path)
        #     MyJson.write(child[1], path)

        # self.data_video.append(r'e:\��ͥ����ƻ�')  # ��һ���Ǵ���ļ���Ŀ¼
        # files = Utils.files_in_dir(self.data_video[0], ['.mp4'])
        # self.data_video.extend(files)  # Ŀ¼�������ļ�
        # print(self.data_menu)

    # ����������
    def init_canvas_ui(self):
        self.resize(500, 500)
        self.setObjectName('Canvas')
        # self.setStyleSheet('background-image:url(./res/images/background1.jpg);border-radius:20px;')

        # self.setAttribute(Qt.WA_StyledBackground, True)  # ��QWdiget����͸��
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)  # �����ޱ߿򴰿�
        # self.setAttribute(Qt.WA_TranslucentBackground)  # ���ô��ڱ���͸��
        # self.setWindowOpacity(0.9)  # ���ô���͸����

        # ���������Ӱ��Ч����Ҫ����������margin
        Utils.set_effect(self, 1, 20, 5, 5, QColor(0, 0, 0, 200))
        # the same QGraphicsEffect can not be shared by other widgets
        # �Ӵ������Ӱ������
        # for children in self.findChildren(QWidget):
        #     shadow = QGraphicsDropShadowEffect(blurRadius=15, xOffset=5, yOffset=5, color=QColor(0, 0, 0, 255))
        #     children.setGraphicsEffect(shadow)

        self.setMouseTracking(True)  # ��������ƶ��¼��ıر�
        # self.setAttribute(Qt.WA_TransparentForMouseEvents, True)  # ������괩͸

        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setSpacing(0)
        self.layout_main.addWidget(self.fm_left)
        self.layout_main.addWidget(self.fm_right)

        # �źŲۣ����Ƿ��������ڴ���
        self.titleBar.sign_pb_prev.connect(self.sign_title_clicked)
        self.titleBar.sign_pb_next.connect(self.sign_title_clicked)
        self.titleBar.sign_win_maximize.connect(self.parent.sign_showMaximized)
        self.titleBar.sign_win_resume.connect(self.parent.sign_showNormal)
        self.titleBar.sign_win_close.connect(self.parent.close)
        self.titleBar.sign_win_move.connect(partial(self.parent.sign_move, self.left_width))
        # self.windowTitleChanged.connect(self.titleBar.setTitle)
        # self.windowIconChanged.connect(self.titleBar.setIcon)

    # ��ӿؼ�
    def init_ui(self):
        # ��ʼ���������
        # self.fm_left.setAttribute(Qt.WA_TransparentForMouseEvents, True)  # ������괩͸
        self.fm_left.setMouseTracking(True)  # ��������ƶ��¼��ıر�
        self.pb_person.setMouseTracking(True)  # �Զ��������Ѿ�������
        # self.listWidget.setMouseTracking(True)
        self.fm_right.setMouseTracking(True)  # ��������ƶ��¼��ıر�
        self.titleBar.setMouseTracking(True)
        self.stackedWidget.setMouseTracking(True)

        # region ������(���水ť������QListWidget)
        # region �������
        lv_left = QVBoxLayout(self.fm_left)
        lv_left.setContentsMargins(0, 15, 0, 0)
        # lh_tmp = QHBoxLayout()
        # lh_tmp.addWidget(self.pb_person, 0, Qt.AlignCenter)
        # lv_left.addLayout(lh_tmp)
        lv_left.addWidget(self.pb_person, 0, Qt.AlignCenter)
        lv_left.addStretch()
        lv_left.addWidget(self.listWidget, 0, Qt.AlignCenter)
        lv_left.addStretch()

        # self.fm_left.setWindowOpacity(0.5)  # ���ô���͸����
        self.fm_left.setObjectName('left_fm')
        # self.fm_left.setFixedWidth(self.left_width)  # ֱ�����ÿ�ȣ���ť�����У�ͨ����ʽ���������
        qss_left = '#left_fm{border-top-left-radius:%d;border-bottom-left-radius:%d;' \
                   'min-width: %dpx;max-width: %dpx;' \
                   'font-size:16px;font-weight:bold;font-family:Roman times;' \
                   'color: white;background: rgba(0, 0, 0, 80);' \
                   'background-position: center center}' % \
                   (Const.MARGIN, Const.MARGIN, self.left_width, self.left_width)
        self.fm_left.setStyleSheet(qss_left)
        # self.fm_left.setStyleSheet('background-image: url(./res/background/background1.jpg);'
        #                            '/*border-radius:20px;     ����Բ��*/'
        #                            'background-repeat: no-repeat;       /*������Ҫ�ظ�*/'
        #                            'background-position: center center;      /*ͼƬ��λ�ã����У��������*/')
        # endregion

        # region ���ͼ��
        # self.lb_person.setAlignment(Qt.AlignCenter)
        # self.lb_person.setIcon(QIcon('./res/images/girl1.png'))
        # self.pb_person.setFixedSize(QSize(self.left_width, 40))
        self.pb_person.set('./res/images/girl1.png')

        # self.lb_person.setStyleSheet('border-top-left-radius:%d;'
        #                              'background: transparent;     /*ȫ͸��*/'
        #                              '/*background:rgba(0,0,0,0.1);      ��͸��*/' % self.margin)
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

        # region �б������
        self.listWidget.setFrameShape(QListWidget.NoFrame)  # ȥ���߿�
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # ���ع�����
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setCursor(QCursor(Qt.ArrowCursor))
        self.listWidget.setObjectName('menu_list')
        # self.listWidget.setSpacing(10)  # ����QListWidget�е�Ԫ��ļ��
        # self.listWidget.setViewportMargins(0, 0, 0, 0)
        # ͨ��QListWidget�ĵ�ǰitem�仯���л�QStackedWidget�е����
        # self.listWidget.resize(365, 400)
        # ������ʾģʽ,һ����ı����ͼ��ģʽ(Ҳ������Iconģʽ,setViewMode)
        # self.listWidget.setViewMode(QListView.IconMode)
        # self.delegate = ItemDelegate()
        # self.listWidget.setItemDelegate(self.delegate)#ͼ�����Ҳ�
        # # ����QListWidget�е�Ԫ���ͼƬ��С
        # self.listWidget.setIconSize(QSize(100, 100))
        # # ����QListWidget�е�Ԫ��ļ��
        # self.listWidget.setSpacing(10)
        # self.listWidget.setViewportMargins(0, 0, 0, 0)
        # # �����Զ���Ӧ���ֵ�����Adjust��Ӧ��Fixed����Ӧ����Ĭ�ϲ���Ӧ
        # self.listWidget.setResizeMode(QListWidget.Adjust)
        # # ���ò����ƶ�
        # self.listWidget.setMovement(QListWidget.Static)

        menu_count = len(self.data_menu)
        item_count = 10 if menu_count > 10 else menu_count
        self.listWidget.setFixedHeight(self.menu_height * item_count)

        self.sub_menu.init_stack_menu(self.data_menu, self.listWidget)  # �Ӳ˵�ҳ���ʼ��
        self.sub_menu.select_stack(0)

        for each in self.data_menu:
            item = QListWidgetItem(QIcon(each[0][0]), each[0][1], self.listWidget)
            #     item.setToolTip(self.data[i])
            item.setSizeHint(QSize(16777215, self.menu_height))  # ����item��Ĭ�Ͽ��(����ֻ�и߶ȱȽ�����)
            item.setTextAlignment(Qt.AlignCenter)  # ���־���

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

        # region �Ҳ��������(�ϱ�TitleBar���±�QStackedWidget)
        # region �Ҳ�����
        lv_right = QVBoxLayout(self.fm_right, spacing=0)
        lv_right.setContentsMargins(0, 0, 1, 0)
        lv_right.addWidget(self.titleBar)
        # lv_right.addStretch()
        lv_right.addWidget(self.stackedWidget)
        # lv_right.addStretch()

        self.fm_right.setObjectName('right_fm')
        # self.fm_left.setFixedWidth(self.left_width)  # ֱ�����ÿ�ȣ���ť�����У�ͨ����ʽ���������
        qss_right = '#right_fm{background: transparent;     /*ȫ͸��*/' \
                    'border-top-right-radius:%d;border-bottom-right-radius:%d;' \
                    'font-size:16px;font-weight:bold;font-family:Roman times;' \
                    'background-position: center center}' % (Const.MARGIN, Const.MARGIN)
        self.fm_right.setStyleSheet(qss_right)
        # endregion

        # region �Ҳ๤����
        self.titleBar.setHeight(self.title_height)
        # self.titleBar.setStyleSheet('border-top-right-radius:15;border-bottom-right-radius:15')
        # self.titleBar.setAttribute(Qt.WA_StyledBackground, True)
        # endregion

        # region �Ҳ�stackedWidget
        # ���岥��ҳ��

        # region �ļ��б�
        lw_videos = QListWidget()
        # lw_videos.setViewMode(QListView.IconMode)  # ��ʾģʽ,Iconģʽ(һ���ı����ͼ��,setViewMode)
        # lw_videos.setFrameShape(QListView.NoFrame)  # �ޱ߿�
        # lw_videos.setFlow(QListWidget.LeftToRight)  # ������
        # lw_videos.setWrapping(True)  # ��������Ͽ��Դﵽ��FlowLayoutһ����Ч��
        # lw_videos.setResizeMode(QListWidget.Adjust)  # �����Զ���Ӧ���ֵ�����Adjust��Ӧ��Fixed����Ӧ����Ĭ�ϲ���Ӧ
        # lw_videos.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # ���ع�����
        lw_videos.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        lw_videos.setIconSize(QSize(100, 100))  # ����QListWidget�е�Ԫ���ͼƬ��С
        lw_videos.setSpacing(10)  # ����QListWidget�е�Ԫ��ļ��

        # lw_videos.setViewportMargins(0, 0, 0, 0)
        lw_videos.setMovement(QListWidget.Static)  # ���ò����ƶ�
        lw_videos.setStyleSheet('/*background: transparent;     ȫ͸��*/'
                                'color: rgb(255, 200, 20);'
                                'font-size:22px;font-weight:bold;font-family:Roman times;')
        # lw_videos.setCursor(QCursor(Qt.ArrowCursor))

        # �������ŵĹ����������¼�
        # lw_videos.verticalScrollBar().actionTriggered.connect(self.onActionTriggered)
        lw_videos.clicked.connect(self.submenu_resource)
        # item_height = 40
        # item_count = 11 if len(self.data_video) > 11 else len(self.data_video)
        # lw_videos.setFixedHeight(item_height * item_count)
        # print(lw_videos.height(), self.menu_height * item_count)

        # for each in self.data_video:
        #     item = QListWidgetItem(QIcon(), each, lw_videos)
        #     #     item.setToolTip(self.data[i])
        #     item.setSizeHint(QSize(16777215, self.menu_height))  # ����item��Ĭ�Ͽ��(����ֻ�и߶ȱȽ�����)
        #     item.setTextAlignment(Qt.AlignCenter)  # ���־���
        self.stackedWidget.addWidget(lw_videos)
        # endregion

        # region ��ͼ����ҳ��
        stage = Curtain(self)
        self.stackedWidget.addWidget(stage)
        # endregion

        # ��ģ��20���Ҳ��ҳ��(�Ͳ�������һ��ѭ������)
        # for i in range(1):
        #     # label = QLabel(f'����ҳ��{i}', self)
        #     # label.setAlignment(Qt.AlignCenter)
        #     label = MyQLabel('ѧ��', self)
        #     label.resize(400, 400)
        #     # print('df fd', self.stackedWidget.size(), label.size())
        #     # ����label�ı�����ɫ(�������)
        #     # �������һ��margin�߾�(��������QStackedWidget��QLabel����ɫ)
        #     # self.stackedWidget.setStyleSheet('background: rgb(%d, %d, %d);margin: 0px;'
        #     #                     % (randint(0, 255), randint(0, 255), randint(0, 255)))
        #     label.setStyleSheet('background: green;margin: 50px;')
        #     label.show_center_img('./res/images/1_horizontal.jpg')

        # endregion

        # endregion

    def add_lw_items(self, img_path, flag=1):
        """
        ��ȡ����ͼ
        :param img_path:
        :param flag: stacked ����ţ�1��gif  0����Ƶ�ļ�ҳ��
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

    # QListWidget current �ı�ʱ����
    def changePage(self, current, previous):
        print(self.contentsWidget.row(current))

    def submenu_clicked(self, name):
        # print(name)
        res_names = self.data_menu[0][1:]
        res_names = [res_names[i][1] for i in range(len(res_names))]
        body_names = self.data_menu[1][1:]  # ['�粿', '�ֱ�', '�米', '����', '�Ƚ�']
        body_names = [body_names[i][1] for i in range(len(body_names))]
        # print(type(res_names), res_names)

        if name in res_names:
            self.stackedWidget.setCurrentIndex(0)
            widget = self.stackedWidget.currentWidget()  # ��һ����չʾ���ѡ����б��
            # widget = QListWidget()
            widget.clear()
            # widget.itemClicked.connect(self.submenu_resource)

            title = f'{self.data_menu[0][0][1]}/{name}'
            widget.setObjectName(title)  # �ۺ�����Ҫ

            file = self.data_dir + f'/{title}/{name}.json'
            data_res = MyJson.read(file)
            # print(title, file, data_res)
            # path, f = os.path.split(file)
            # ll = Utils.files_in_dir(path, ['.mp4'])
            # MyJson.write(ll, file)
            for each in data_res:
                item = None
                if name == '�İ�':
                    item = QListWidgetItem(QIcon(each[0]), each[1], widget)
                    item.setToolTip(each[1])
                elif name == '��Ƶ' or name == '��ҳ':
                    item = QListWidgetItem(QIcon(), each, widget)
                    item.setToolTip(each)
                item.setSizeHint(QSize(16777215, self.menu_height))  # ����item��Ĭ�Ͽ��(����ֻ�и߶ȱȽ�����)
                item.setTextAlignment(Qt.AlignCenter)  # ���־���
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

        if '�İ�' in name:
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
        elif '��Ƶ' in name:
            # print('��̬����', path)
            os.startfile(path)  # ����ϵͳ����Ĭ�ϳ���򿪱����ļ�

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

    def sign_title_clicked(self):
        sender = self.sender()
        # print(sender.text())

    def slot_list_row_changed(self):
        cur_row = self.listWidget.currentRow()
        pos = self.listWidget.pos()

        child_menu_pos = QPoint(self.menu_height * cur_row, self.left_width)

        # self.stacked_menu.setCurrentIndex(cur_row)
        print(cur_row)

        # ͨ��QListWidget�ĵ�ǰitem�仯���л�QStackedWidget�е����
        # self.stackedWidget.setCurrentIndex(cur_row // 2)

    def paintEvent(self, event):
        # # �������ޱ߿�ʱ�Ǽ��ز�����ʽ�ģ������ӿؼ���ʵ����ʽ��
        # # Ҫ�������屾��ʵ����ʽ����Ҫ��paintEvent�¼��м������´��룬���õ�ͼҲ��һ����
        # opt = QStyleOption()
        # opt.initFrom(self)
        # p = QPainter(self)
        # p.setRenderHint(QPainter.Antialiasing)  # �����
        # self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
        # # super(Canvas, self).paintEvent(event)

        # ��ͨ����ʽ��ֱ������Բ�ǣ�ͨ�ã��Ҳ��̳����ӿؼ�
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # �����

        # ��ʾȫͼ����
        img = QImage('./res//background/bk5.jpg')
        w, h = self.width(), self.height()
        ratio_w = img.width() / w
        ratio_h = img.height() / h

        is_w = True if ratio_w < ratio_h else False
        img_new = img.scaledToWidth(h) if is_w else img.scaledToHeight(w)

        painter.setBrush(QBrush(QPixmap.fromImage(img_new)))  # ���õ�ͼ�ķ�ʽ֮һ
        # painter.setBrush(QBrush(Qt.blue))
        painter.setPen(Qt.transparent)

        rect = self.rect()
        rect.setWidth(rect.width() - 1)
        rect.setHeight(rect.height() - 1)
        painter.drawRoundedRect(rect, 20, 20)
        # Ҳ����QPainterPath ���ƴ��� painter.drawRoundedRect(rect, 15, 15)
        # painterPath= QPainterPath()
        # painterPath.addRoundedRect(rect, 15, 15)
        # painter.drawPath(painterPath)

        # ֱ�����õ�ͼ����Բ�ǵĻ�ˢ���ò���ͬʱ
        # pix = QPixmap('./res/images/background11.jpg')
        # painter.drawPixmap(self.rect(), pix)

        # super(testShadow, self).paintEvent(event)

    # def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
    #     super(Canvas, self).resizeEvent(a0)
    #     Utils.setBg(self, self.bg_label, './res//background/bk5.jpg')

    # def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
    #     if a0 == 'menu_list':
    #         print('great')
    #     if a1.type() == QtCore.QEvent.HoverMove:
    #         print('����ƶ�����ť��')
    #         return True
    #     elif a1.type() == QtCore.QEvent.MouseMove:
    #         print('��ť�����')
    #         return True

    # def enterEvent(self, a0: QtCore.QEvent):
    #     print('enter', a0.pos())
    #     return super().enterEvent(a0)
    #
    # def leaveEvent(self, a0: QtCore.QEvent):
    #     print('leave', a0.pos())
    #     return super().enterEvent(a0)


# �������Ӱ��
class MainWin(QWidget):

    # region �����ڵ�Ӱ�ӣ������ٸ�
    def __init__(self, *args, **kwargs):
        super(MainWin, self).__init__(*args, **kwargs)

        self.resize(1500, 1000)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)  # �����ޱ߿򴰿�
        self.setAttribute(Qt.WA_TranslucentBackground)  # ���ô��ڱ���͸��
        # self.setAttribute(Qt.WA_StyledBackground, True)  # ��QWdiget����͸��
        self.setMouseTracking(True)  # ��������ƶ��¼��ıر�

        self.LOCATION = Const.CENTER
        # self.dragPosition = 0  # �϶�ʱ����

        self.canvas = Canvas(self)

        # child = ChildMenu(self)
        # child.show()
        # child.move(self.x()+100, self.y()+300)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(Const.MARGIN, Const.MARGIN,
                                  Const.MARGIN, Const.MARGIN)  # ����Ӱ����λ��
        # layout.setContentsMargins(0, 0, 0, 0)  # ����Ӱ����λ��
        layout.addWidget(self.canvas)
        # layout.addWidget(child)
        Utils.center_win(self)

    def sign_showMaximized(self):
        """���,Ҫ��ȥ���������ұ߽�,�����ȥ����߿�ط����п�϶"""
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.showMaximized()

    def sign_showNormal(self):
        """��ԭ,Ҫ�ȱ����������ұ߽�,����û�б߿��޷�����"""
        self.layout().setContentsMargins(self.Const.MARGIN, self.Const.MARGIN,
                                         self.Const.MARGIN, self.Const.MARGIN)
        super(MainWin, self).showNormal()

    # def nativeEvent(self):
    #     pass

    def mousePressEvent(self, event: QMouseEvent):
        # if event.button() == Qt.LeftButton:#Ҳ����
        if event.buttons() == Qt.LeftButton:
            if self.LOCATION != Const.CENTER:
                self.mouseGrabber()  # �õ����ڲ�������¼��Ĵ���
            else:
                pass
                # self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()

    def mouseReleaseEvent(self, event: QMouseEvent):
        # if event.buttons() == Qt.LeftButton:#�Ͳ���
        if event.button() == Qt.LeftButton:
            if self.LOCATION is not Const.CENTER:  # �Ǳ��߸���һ�ɻָ������״
                self.setCursor(QtGui.QCursor(Qt.ArrowCursor))
            self.unsetCursor()

    def cursor_location(self, pos_current):
        """
            �����궨λ
            :param pos_current:���λ��
            :return:
            """
        x, y = pos_current.x(), pos_current.y()  # ������ޱ߿򴰿����Ͻǵ�λ��
        # print(f'x={x}  y={y}')
        width = self.width() - Const.PADDING  # �ޱ߿򴰿ڵĿ��ȥ�߾�
        height = self.height() - Const.PADDING  # �ޱ߿򴰿ڵĳ���ȥ�߾�

        if x < Const.PADDING and y < Const.PADDING:  # ���Ͻ��ڲ�
            self.LOCATION = Const.TL_CORNER
            self.setCursor(QCursor(Qt.SizeFDiagCursor))  # ���������״
        elif x > width and y > height:  # ���½��ڲ�
            self.LOCATION = Const.BR_CORNER
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif x < Const.PADDING and y > height:  # ���½��ڲ�
            self.LOCATION = Const.BL_CORNER
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif x > width and y < Const.PADDING:  # ���Ͻ��ڲ�
            self.LOCATION = Const.TR_CORNER
            self.setCursor(QCursor(Qt.SizeBDiagCursor))

        elif x < Const.PADDING:  # ����ڲ�
            self.LOCATION = Const.LEFT
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif x > width:  # �ұ��ڲ�
            self.LOCATION = Const.RIGHT
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif y < Const.PADDING:  # �ϱ�
            self.LOCATION = Const.TOP
            self.setCursor(QCursor(Qt.SizeVerCursor))
        elif y > height:  # �±�
            self.LOCATION = Const.BOTTOM
            self.setCursor(QCursor(Qt.SizeVerCursor))

        else:  # �м� Ĭ��
            self.LOCATION = Const.CENTER
            self.setCursor(QCursor(Qt.ArrowCursor))

        # print(self.LOCATION)

    def mouseMoveEvent(self, event: QMouseEvent):
        mouse_pos = event.globalPos()
        top_left = self.mapToGlobal(self.rect().topLeft())
        # top_left = self.pos
        bottom_right = self.mapToGlobal(self.rect().bottomRight())

        # print(self.LOCATION)

        # if event.buttons() and event.button() != Qt.LeftButton:  # Ҳ����
        if not event.buttons():
            self.cursor_location(event.pos())
        else:
            if event.buttons() == Qt.LeftButton:
                # print('left press')
                if self.LOCATION is Const.CENTER:
                    pass
                    # print('center')
                    # self.move(event.globalPos() - self.dragPosition)  # �������ƶ���ָ��λ��
                else:
                    geo = QtCore.QRect(top_left, bottom_right)

                    if self.LOCATION == Const.LEFT:
                        # if bottom_right.x() - mouse_pos.x() > self.minimumWidth():#����Ҫ����setmin��max��fix����
                        # geo.setWidth(bottom_right.x() - mouse_pos.x())  # �Զ������
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
                    self.setGeometry(geo)  # ����Ӱ�ӵĸ����ڵ�λ��

            # else:
            #     print('other press')
        # QEvent��accept������ignore����һ�㲻���õ�����Ϊ����ֱ�ӵ���QWidget����¼�������ֱ�ӣ�����������һ����
        # Ψ����closeEvent�����б������accept������ignore������
        event.ignore()

    def close(self):
        self.canvas.sub_menu.close()
        super(MainWin, self).close()

    def sign_move(self, x_offset, pos):
        if self.windowState() == Qt.WindowMaximized or self.windowState() == Qt.WindowFullScreen:
            # ��󻯻���ȫ���������ƶ�
            return

        # if self._widget is None:
        #     return

        pos_new = copy.copy(pos)
        pos_new.setX(pos.x() - x_offset)  # ��ȥ����б��ռ�õ�
        # print('this', pos_new.x(), pos.x())

        super(MainWin, self).move(pos_new)
    # endregion


if __name__ == '__main__':
    app = QApplication(sys.argv)

    g_style = StyleSheet()  # ��Χ���壬������ǰ
    w = MainWin()  # ������м�
    # w = Canvas(None)
    # w = ChildMenu(None)
    # w = Curtain(None)
    # w.show()
    g_style.set(app)  # ��Χ���壬�����ں�

    sys.exit(app.exec_())

    # w = WinInfo()
    # w.get_all_win()
