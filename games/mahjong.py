#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Project: PyCharm
# @File    : mahjong.py
# @Author  : tiger
# @Email   : shdorado@126.com
# @Time    : 2020/5/22 0:14

# from gevent import monkey
#
# monkey.patch_all()  # 必须放到被打补丁者的前面，如time，socket模块之前# 必须写在最上面，这句话后面的所有阻塞全部能够识别了
# import gevent#协程
# from gevent.pool import Pool
# from functools import partial
# from multiprocessing import Process#进程
import threading  # 线程

import sys
import os
import random
from utilities import Utils
import win32api

from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from PIL import Image, ImageQt, ImageFilter
# from PIL.ImageQt import ImageQt
import numpy as np
import time
from custTitle import FrameLessWindow
from games.majing import Mahjong, MjData


class PilPic:
    # 一、照片去色
    @staticmethod
    def white_black(pic, save_file):
        img = Image.open(pic)
        img_01 = img.convert("L")
        img_01.save(save_file)
        return img_01

    # 二、照片模糊
    @staticmethod
    def blurred(pic, radius, save_file):
        img = Image.open(pic)
        img_02 = img.filter(ImageFilter.GaussianBlur(radius=radius))
        img_02.save(save_file)
        return img_02

    # 三、照片旋转 90°
    @staticmethod
    def rotate(pic, rad, save_file):
        img = Image.open(pic)
        img_03 = img.rotate(rad)
        img_03.save(save_file)
        return img_03

    # 四、照片翻转
    @staticmethod
    def turn(pic, flag=Image.FLIP_LEFT_RIGHT, save_file=None):
        img = Image.open(pic)
        img_04 = img.transpose(flag)
        img_04.save(save_file)
        return img_04

    # 五、照片缩略图
    @staticmethod
    def zoom(pic, size=(120, 120), save_file=None):
        img = Image.open(pic)
        img_05 = img.copy()
        img_05.thumbnail(size)
        img_05.save(save_file)
        return img_05


# 多进程+协程。4个玩家的智能算法用4个进程，充分利用多cpu，
# 杠碰、吃胡等用多协程实现。
# COROUTINE_NUMBER = 2000  # 协程池数量
# pool = Pool(COROUTINE_NUMBER)  # 使用协程池


# class Tile(QtWidgets.QFrame):
#     _W, _H = 30, 40
#     _s1, _s2, _s3 = 2.3, 2.1, 2
#     g_W, g_H = _W * _s1, _H * _s1  # 普通牌的width, height
#     g_W_d, g_H_d = _W * _s2, _H * _s2  # 叫牌的宽高
#     g_W_s, g_H_s = _W * _s3, _H * _s3  # 废牌的宽高
#
#     # def __init__(self, parent=None, ID=0, kind=1, index=-1):
#     #     """
#     #     卡牌
#     #     :param parent:
#     #     :param ID: 牌号
#     #     :param kind: 每家的正牌 —— 0：东方牌 1:南方牌、影子牌 2:西方牌 3:北方牌
#     #                  每家的叫牌(第14张牌) —— 4:东 5 6 7北
#     #                 每家的明牌 ——   8:东方 9:南方卧牌 10 11
#     #                 每家的死牌 —— 12:东方 13:南方 14:西方 15:北方
#     #     :param index: 牌的槽位，在牌面中的位置，回传用
#     #     """
#     #     # 加一个suppress规则:
#     #     # noinspection PyArgumentList
#     #     super(Tile, self).__init__(parent)
#     #
#     #     self.parent = parent
#     #     self.ID = ID
#     #     self.kind = kind
#     #     self.index = index
#     #     self.is_ejected = False  # 弹出标志
#     #     self.lb = QtWidgets.QLabel(self)
#     #
#     #     self._create()
#     #     self.setVisible(False)
#     #
#     # def _create(self):
#     #     self.lb.setScaledContents(True)  # 让图片自适应label大小
#     #     name, pic_file = DataMj.get_name_pic(self.ID)
#     #
#     #     if self.kind == 0:
#     #         self.setFixedSize(30, 80)
#     #         pic_file = './res/images/tile_right.png'
#     #         self.lb.setGeometry(0, 0, self.width(), self.height())
#     #         self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)  # 事件穿透，鼠标不起作用
#     #
#     #         # tmp = self.alphabg2white_PIL(self.pic_file)
#     #         # bg = self.pil2pixmap(tmp)
#     #         # bg = QtGui.QPixmap.fromImage(bg1)
#     #
#     #         # bg = Image.open(pic_file).transpose(Image.ROTATE_270)
#     #         # # DataMj.pil2_pixmap(bg)
#     #         # lb.setPixmap(bg.scaled(width+10, height+60, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
#     #         self.lb.setPixmap(QtGui.QPixmap(pic_file))
#     #
#     #     elif self.kind == 1:
#     #         self.setMouseTracking(True)  # 跟踪鼠标移动
#     #         self.setFixedSize(Tile.g_W, Tile.g_H)
#     #         self.lb.setGeometry(7, 25, int(Tile.g_W * 0.8), int(Tile.g_H * 0.7))
#     #         self.lb.setMouseTracking(True)  # 跟踪鼠标移动
#     #         self.lb.setPixmap(QtGui.QPixmap(pic_file))
#     #
#     #     elif self.kind == 2:
#     #         self.setFixedSize(30, 80)
#     #         pic_file = './res/images/tile_left.png'
#     #         self.lb.setGeometry(0, 0, self.width(), self.height())
#     #         self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)  # 事件穿透，鼠标不起作用
#     #         self.lb.setPixmap(QtGui.QPixmap(pic_file))
#     #
#     #     elif self.kind == 3:
#     #         self.setFixedSize(65, 85)
#     #         pic_file = './res/images/tile_top.png'
#     #         # self.setFixedSize(80, 85)
#     #         # pic_file = r'E:\python\games\res\ma_yellow\face-down-128px.png'
#     #         self.lb.setGeometry(0, 0, self.width(), self.height())
#     #         self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)  # 事件穿透，鼠标不起作用
#     #         self.lb.setPixmap(QtGui.QPixmap(pic_file))
#     #
#     #     elif self.kind == 4:  # 东方叫牌
#     #         self.setFixedSize(int(Tile.g_H_d * 0.9), int(Tile.g_W_d * 1.1))
#     #         self.lb.setGeometry(6, 5, int(Tile.g_H_d * 0.9 * 0.8), int(Tile.g_W_d * 0.7))
#     #
#     #         if pic_file:
#     #             im = Image.open(pic_file)
#     #             out = im.transpose(Image.ROTATE_90)  # 逆时针旋转 90
#     #             # img = im.resize(100, 100)  # 将图片重新设置尺寸
#     #             # out.save('./tmp.png')
#     #             self.lb.setPixmap(DataMj.pil2pixmap(out))
#     #
#     #     elif self.kind == 5:  # 南方叫牌
#     #         self.setFixedSize(Tile.g_W_d, Tile.g_H_d)
#     #         self.lb.setGeometry(7, 7, int(Tile.g_W_d * 0.8), int(Tile.g_H_d * 0.65))
#     #
#     #         if pic_file:
#     #             # im = Image.open(pic_file)
#     #             # out = im.transpose(Image.FLIP_TOP_BOTTOM)  # 进行上下颠倒
#     #             self.lb.setPixmap(QtGui.QPixmap(pic_file))
#     #
#     #     elif self.kind == 6:  # 西方叫牌
#     #         self.setFixedSize(int(Tile.g_H_d * 0.9), int(Tile.g_W_d * 1.1))
#     #         self.lb.setGeometry(6, 5, int(Tile.g_H_d * 0.9 * 0.8), int(Tile.g_W_d * 0.7))
#     #
#     #         if pic_file:
#     #             im = Image.open(pic_file)
#     #             out = im.transpose(Image.ROTATE_270)  # 逆时针旋转 270
#     #             self.lb.setPixmap(DataMj.pil2pixmap(out))
#     #
#     #     elif self.kind == 7:  # 北方叫牌 即正打出的第14张牌
#     #         self.setFixedSize(Tile.g_W_d, Tile.g_H_d)
#     #         self.lb.setGeometry(7, 7, int(Tile.g_W_d * 0.8), int(Tile.g_H_d * 0.65))
#     #
#     #         if pic_file:
#     #             im = Image.open(pic_file)
#     #             out = im.transpose(Image.FLIP_TOP_BOTTOM)  # 进行上下颠倒
#     #             self.lb.setPixmap(DataMj.pil2pixmap(out))
#     #
#     #     elif self.kind == 8:
#     #         self.setFixedSize(Tile.g_W_s * 0.75, Tile.g_H_s * 0.75)
#     #         pic_width, pic_height = int(Tile.g_W_s * 0.75 * 0.8), int(Tile.g_H_s * 0.75 * 0.7)
#     #         self.lb.setGeometry(5, 5, pic_width, pic_height)
#     #         self.lb.setPixmap(QtGui.QPixmap(pic_file))
#     #
#     #     elif self.kind == 9:
#     #         self.setFixedSize(Tile.g_tile_height * 0.75, Tile.g_tile_width * 0.75)
#     #         pic_width, pic_height = int(Tile.g_width * 0.75 * 0.8), int(Tile.g_height * 0.75 * 0.7)
#     #         self.lb.setGeometry(5, 5, pic_height, pic_width)
#     #         self.lb.setPixmap(QtGui.QPixmap(pic_file))
#     #
#     # def resurfacing(self, ID, kind=5):
#     #     """
#     #     相当于摸了一张牌到热牌位置
#     #     更换皮肤和牌号，槽位不变。仅针对热牌和影子牌，其他牌建议用互换法
#     #     :param kind:
#     #     :param ID: 要复制的牌卡牌号
#     #     :return:
#     #     """
#     #
#     #     if DataMj.is_valid(ID):
#     #         pic_file = DataMj.get_name_pic(ID)[1]
#     #         if pic_file:
#     #             if kind == 4:  # 东方叫牌
#     #                 im = Image.open(pic_file)
#     #                 out = im.transpose(Image.ROTATE_90)  # 逆时针旋转 90
#     #                 self.lb.setPixmap(DataMj.pil2pixmap(out))
#     #             # elif kind == 5:
#     #             #     self.lb.setPixmap(QtGui.QPixmap(pic_file))
#     #             elif kind == 6:
#     #                 im = Image.open(pic_file)
#     #                 out = im.transpose(Image.ROTATE_270)  # 逆时针旋转 270
#     #                 self.lb.setPixmap(DataMj.pil2pixmap(out))
#     #             elif kind == 7:
#     #                 im = Image.open(pic_file)
#     #                 out = im.transpose(Image.FLIP_TOP_BOTTOM)  # 进行上下颠倒
#     #                 self.lb.setPixmap(DataMj.pil2pixmap(out))
#     #             else:
#     #                 self.lb.setPixmap(QtGui.QPixmap(pic_file))
#     #
#     #             self.lb.repaint()
#     #             self.ID = ID
#
#     def __init__(self, parent=None, tile_id=0, kind=1, index=-1):
#         """
#         卡牌
#         :param parent:
#         :param tile_id: 牌号
#         :param kind: 每家的正牌 —— 0：东方牌 1:南方牌、影子牌 2:西方牌 3:北方牌
#                      每家的叫牌(第14张牌) —— 4:东 5 6 7北
#                     每家的明牌 ——   8:东方 9:南方卧牌 10 11
#                     每家的死牌 —— 12:东方 13:南方 14:西方 15:北方
#         :param index: 牌的槽位，在牌面中的位置，回传用
#         """
#         # 加一个suppress规则:
#         # noinspection PyArgumentList
#         super(Tile, self).__init__(parent)
#
#         self.parent = parent
#         self.ID = tile_id
#         self.kind = kind
#         self.index = index
#         self.is_ejected = False  # 弹出标志
#         self.lb = QtWidgets.QLabel(self)
#
#         self._create()
#         # self.setVisible(False)
#
#     def _create(self):
#         self.lb.setScaledContents(True)  # 让图片自适应label大小
#         name, pic_file = DataMj.get_name_pic(self.ID)
#
#         if self.kind == 0:
#             self.setFixedSize(30, 80)
#             pic_file = './res/images/tile_right.png'
#             self.lb.setGeometry(0, 0, self.width(), self.height())
#             self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)  # 事件穿透，鼠标不起作用
#
#             # tmp = self.alphabg2white_PIL(self.pic_file)
#             # bg = self.pil2pixmap(tmp)
#             # bg = QtGui.QPixmap.fromImage(bg1)
#
#             # bg = Image.open(pic_file).transpose(Image.ROTATE_270)
#             # # DataMj.pil2_pixmap(bg)
#             # lb.setPixmap(bg.scaled(width+10, height+60, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
#             self.lb.setPixmap(QtGui.QPixmap(pic_file))
#
#         elif self.kind == 1:
#             self.setMouseTracking(True)  # 跟踪鼠标移动
#             self.setFixedSize(Tile.g_W, Tile.g_H)
#             self.lb.setGeometry(7, 25, int(Tile.g_W * 0.8), int(Tile.g_H * 0.7))
#             self.lb.setMouseTracking(True)  # 跟踪鼠标移动
#             self.lb.setPixmap(QtGui.QPixmap(pic_file))
#
#         elif self.kind == 2:
#             self.setFixedSize(30, 80)
#             pic_file = './res/images/tile_left.png'
#             self.lb.setGeometry(0, 0, self.width(), self.height())
#             self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)  # 事件穿透，鼠标不起作用
#             self.lb.setPixmap(QtGui.QPixmap(pic_file))
#
#         elif self.kind == 3:
#             self.setFixedSize(65, 85)
#             pic_file = './res/images/tile_top.png'
#             # self.setFixedSize(80, 85)
#             # pic_file = r'E:\python\games\res\ma_yellow\face-down-128px.png'
#             self.lb.setGeometry(0, 0, self.width(), self.height())
#             self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)  # 事件穿透，鼠标不起作用
#             self.lb.setPixmap(QtGui.QPixmap(pic_file))
#
#         elif self.kind == 4:  # 东方叫牌
#             self.setFixedSize(Tile.g_H_d * 0.9, Tile.g_W_d * 1.1)
#             self.lb.setGeometry(6, 5, int(Tile.g_H_d * 0.9 * 0.8), int(Tile.g_W_d * 0.7))
#
#             # if pic_file:
#             #     im = Image.open(pic_file)
#             #     out = im.transpose(Image.ROTATE_90)  # 逆时针旋转 90
#             #     # img = im.resize(100, 100)  # 将图片重新设置尺寸
#             #     # out.save('./tmp.png')
#             #     self.lb.setPixmap(DataMj.pil2pixmap(out))
#
#         elif self.kind == 5:  # 南方叫牌
#             self.setFixedSize(Tile.g_W_d, Tile.g_H_d)
#             self.lb.setGeometry(7, 7, int(Tile.g_W_d * 0.8), int(Tile.g_H_d * 0.65))
#
#             if pic_file:
#                 # im = Image.open(pic_file)
#                 # out = im.transpose(Image.FLIP_TOP_BOTTOM)  # 进行上下颠倒
#                 self.lb.setPixmap(QtGui.QPixmap(pic_file))
#
#         elif self.kind == 6:  # 西方叫牌
#             self.setFixedSize(Tile.g_H_d * 0.9, Tile.g_W_d * 1.1)
#             self.lb.setGeometry(6, 5, int(Tile.g_H_d * 0.9 * 0.8), int(Tile.g_W_d * 0.7))
#
#             # if pic_file:
#             #     im = Image.open(pic_file)
#             #     out = im.transpose(Image.ROTATE_270)  # 逆时针旋转 270
#             #     self.lb.setPixmap(DataMj.pil2pixmap(out))
#
#         elif self.kind == 7:  # 北方叫牌 即正打出的第14张牌
#             self.setFixedSize(Tile.g_W_d, Tile.g_H_d)
#             self.lb.setGeometry(7, 7, int(Tile.g_W_d * 0.8), int(Tile.g_H_d * 0.65))
#
#             # if pic_file:
#             #     im = Image.open(pic_file)
#             #     out = im.transpose(Image.FLIP_TOP_BOTTOM)  # 进行上下颠倒
#             #     self.lb.setPixmap(DataMj.pil2pixmap(out))
#
#         elif self.kind == 8:
#             self.setFixedSize(Tile.g_W_s * 0.75, Tile.g_H_s * 0.75)
#             pic_width, pic_height = int(Tile.g_W_s * 0.75 * 0.8), int(Tile.g_H_s * 0.75 * 0.7)
#             self.lb.setGeometry(5, 5, pic_width, pic_height)
#             self.lb.setPixmap(QtGui.QPixmap(pic_file))
#
#         elif self.kind == 9:
#             self.setFixedSize(Tile.g_tile_height * 0.75, Tile.g_tile_width * 0.75)
#             pic_width, pic_height = int(Tile.g_width * 0.75 * 0.8), int(Tile.g_height * 0.75 * 0.7)
#             self.lb.setGeometry(5, 5, pic_height, pic_width)
#             self.lb.setPixmap(QtGui.QPixmap(pic_file))
#
#     def resurfacing(self, ID, kind=5):
#         """
#         相当于摸了一张牌到热牌位置
#         更换皮肤和牌号，槽位不变。仅针对热牌和影子牌，其他牌建议用互换法
#         :param kind:
#         :param ID: 要复制的牌卡牌号
#         :return:
#         """
#
#         if DataMj.is_valid(ID):
#             pic_file = DataMj.get_name_pic(ID)[1]
#             if pic_file:
#                 if kind == 4:  # 东方叫牌
#                     im = Image.open(pic_file)
#                     out = im.transpose(Image.ROTATE_90)  # 逆时针旋转 90
#                     self.lb.setPixmap(DataMj.pil2pixmap(out))
#                 # elif kind == 5:
#                 #     self.lb.setPixmap(QtGui.QPixmap(pic_file))
#                 elif kind == 6:
#                     im = Image.open(pic_file)
#                     out = im.transpose(Image.ROTATE_270)  # 逆时针旋转 270
#                     self.lb.setPixmap(DataMj.pil2pixmap(out))
#                 elif kind == 7:
#                     im = Image.open(pic_file)
#                     out = im.transpose(Image.FLIP_TOP_BOTTOM)  # 进行上下颠倒
#                     self.lb.setPixmap(DataMj.pil2pixmap(out))
#                 else:
#                     self.lb.setPixmap(QtGui.QPixmap(pic_file))
#
#                 self.lb.repaint()
#                 self.ID = ID
#
#     def release_me(self):
#         self.lb.deleteLater()
#         self.deleteLater()
#
#     def mousePressEvent(self, e):
#         # print('mousePress')
#         if not self.parent.can_discard:  # 禁止打牌
#             return
#
#         if not self.is_ejected:  # 弹起来，提示预计要打的牌
#             name = DataMj.get_name_pic(self.ID)[0]
#             # print(str(sys._getframe().f_lineno), name, self.index)
#
#             tile = self.parent.tile_ejected  # 原来弹起的要归位
#             if tile:
#                 tile.move(tile.x(), tile.y() + 50)
#                 tile.is_ejected = False
#             self.parent.tile_ejected = self  # 当下的要弹起
#             self.move(self.x(), self.y() - 50)
#             self.is_ejected = True
#         else:  # 弹起时点击，就出牌了
#             self.move(self.x(), self.y() + 50)
#             self.is_ejected = False
#             self.parent.tile_ejected = None
#
#             self.parent.discard(self)
#         # print('mousePress')
#         if not self.parent.can_discard:  # 禁止打牌
#             return
#
#     def paintEvent(self, event):
#         qp = QtGui.QPainter()
#         pic = None
#
#         if self.kind == 1:
#             pic = './res/images/tile_bottom.png'
#         elif self.kind == 4 or self.kind == 6:
#             pic = './res/images/tile_hot_h.png'
#         elif self.kind == 5 or self.kind == 7:
#             pic = './res/images/tile_hot_v.png'
#
#         qp.begin(self)
#         # qp.drawPixmap(self.rect(), QtGui.QPixmap(self.pic_file), QtCore.QRect())
#         qp.drawPixmap(self.rect(), QtGui.QPixmap(pic), QtCore.QRect())
#         # qp.setBrush(QtGui.QColor(10, 10, 10))
#
#         qp.end()
#
#     def __str__(self):
#         return f'牌{self.index}: {DataMj.get_name_pic(self.ID)}'
#
#     __repr__ = __str__
#     '''
#     __repr__ = __str__ 使用时可保证在控制台>>> m 时 任然输出
#     '''
class Tile(QtWidgets.QLabel):
    def __init__(self, width, height, pic_file=None, kind=1, parent=None):
        """
        卡牌
        :param parent:
        :param ID: 牌号
        :param kind: 每家的正牌 —— 0：东方牌 1:南方牌、影子牌 2:西方牌 3:北方牌
                     每家的叫牌(第14张牌) —— 4:东 5 6 7北
                    每家的明牌 ——   8:东方 9:南方卧牌 10 11
                    每家的死牌 —— 12:东方 13:南方 14:西方 15:北方
        :param index: 牌的槽位，在牌面中的位置，回传用
        """
        # 加一个suppress规则:
        # noinspection PyArgumentList
        super(Tile, self).__init__(parent)
        self.parent = parent
        self.width = width
        self.height = height
        self.pic = pic_file
        self.kind = kind

        self.setScaledContents(True)  # 让图片自适应label大小
        self.setMouseTracking(True)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.resize(self.width, self.height)
        save_file = './tmp.png'
        if self.kind == 0:  # 东座
            PilPic.rotate(self.pic, 90, save_file)
        elif self.kind == 1:
            save_file = self.pic
        elif self.kind == 2:  # 西座
            PilPic.rotate(self.pic, -90, save_file)
        else:
            PilPic.turn(self.pic, Image.FLIP_TOP_BOTTOM, save_file)

        self.setPixmap(Utils.img_center(self.width, self.height, save_file))

        super(Tile, self).resizeEvent(a0)

    def __str__(self):
        return f'牌{self.index}: {MjData.get_name_pic(self.ID)}'

    __repr__ = __str__  # __repr__ = __str__ 使用时可保证在控制台>>> m 时 任然输出


class MahjongTable(QtWidgets.QFrame):
    def __init__(self, parent):
        super(MahjongTable, self).__init__(parent)

        self.parent = parent
        self.w_border = 5
        self.w_middle = 5
        self.margin = self.w_border * 2 + self.w_middle
        self.tile_w = 52
        self.tile_h = 80

        self.mahjong = Mahjong(self)

        self.lh_main = QtWidgets.QHBoxLayout(self)
        self.count = 0

        self.init_board()

    def slot_playing(self):
        # self.mahjong.clear_round()
        # self.mahjong.shuffling()
        # self.mahjong.deal()
        # self.mahjong.playing()
        self.update()

    def _show_south(self, card):
        card = [[4, 0], [6, 0], [19, 0], [22, 0], [23, 0], [23, 0], [23, 0],
                [24, 0], [36, 0], [39, 0], [40, 0], [41, 0], [41, 0], [6, 0]]
        # 南座
        x = 170
        pics = self.mahjong.data.card2pics(card)

        if not pics:
            return
        print(pics, card)

        for i in range(len(pics) - 1):
            # 南座
            tile = Tile(self.tile_w, self.tile_h, pics[i], 1, self)
            tile.move(x + i * self.tile_w, 910)

        tile = Tile(self.tile_w, self.tile_h, pics[-1], 1, self)
        tile.move(80 + x + i * self.tile_w, 910)
        # print(self.height())

    def _show_north(self, card):
        # 北座
        x = 170
        pics = self.mahjong.data.card2pics(card)
        if not pics:
            return

        tile = Tile(self.tile_w, self.tile_h, pics[-1], 3, self)
        tile.move(x, self.margin)

        for i in range(len(pics) - 1):
            tile = Tile(self.tile_w, self.tile_h, pics[i], 3, self)
            tile.move(80 + x + i * self.tile_w, self.margin)

    def _show_east(self, card):
        # 东座
        x = 160
        pics = self.mahjong.data.card2pics(card)
        if not pics:
            return

        tile = Tile(self.tile_h, self.tile_w, pics[-1], 0, self)
        tile.move(1000, 120)

        for i in range(len(pics) - 1):
            tile = Tile(self.tile_h, self.tile_w, pics[i], 0, self)
            tile.move(1000, 200 + i * self.tile_w)

    def _show_west(self, card):
        # 西座
        x = 160
        pics = self.mahjong.data.card2pics(card)
        if not pics:
            return

        for i in range(len(pics) - 1):
            tile = Tile(self.tile_h, self.tile_w, pics[i], 2, self)
            tile.move(self.margin, 120 + i * self.tile_w)

        tile = Tile(self.tile_h, self.tile_w, pics[-1], 2, self)
        tile.move(self.margin, 200 + i * self.tile_w)

    def show_cards(self):
        # print(self.mahjong.card_players[0][0])
        # if not self.mahjong.begin:
        if self.mahjong.data.is_valid(self.mahjong.card_players[0][0][0]):
            # print('ddd', self.mahjong.card_players[0])
            self._show_south(self.mahjong.card_players[1])
            # self._show_north(self.mahjong.card_players[3])
            # self._show_east(self.mahjong.card_players[0])
            # self._show_west(self.mahjong.card_players[2])

    def init_board(self):
        # 仅设置桌面
        # self.resize(self.parent.width(), self.parent.height())
        # self.setLineWidth(self.w_border)
        # self.setMidLineWidth(self.w_middle)
        # self.setFrameStyle(QtWidgets.QFrame.Raised | QtWidgets.QFrame.Box)
        # self.setFrameRect(QtCore.QRect(10, 10, 80, 80))

        # self.setMouseTracking(True)  # 跟踪鼠标移动
        # self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        # self.setStyleSheet('background-image:url(./res/images/mahjongdesk.jpg)')
        # self.setStyleSheet('background-color:#CC6600')  # Tan
        # self.setStyleSheet('background-color:blue')  # Tan

        lb = QtWidgets.QLabel(self)
        lb.setPixmap(QtGui.QPixmap('./res/images/mahjongdesk.jpg'))
        lb.setScaledContents(True)  # 让图片自适应label大小

        # 总体框架
        self.lh_main.setContentsMargins(0, 0, 0, 0)
        self.lh_main.addWidget(lb)

    def resizeEvent(self, event):
        self.count += 1
        ...

        self._show_south(None)

    @staticmethod
    def img_ex(img):
        a = cv2.imread(img)
        h, w = a.shape[:2]
        print(h, w)
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]])  # 先确定图片的四个顶点的坐标，逆时针
        cv2.circle(a, (0, h - 1), 36, (0, 290, 0), -1)

        pts1 = np.float32([[0, 0], [0, h - 64], [w - 1, h - 64], [w - 1, 0]])  # 把图片的四个顶点的坐标变成
        M = cv2.getPerspectiveTransform(pts, pts1)  # 先得确定透视变换的系数：
        dst = cv2.warpPerspective(a, M, (128, 128))  # 对原图进行这个变换
        cv2.imwrite('0.png', dst)  # 保存图片

    # 立体字
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        # self.show_cards()
        # self._show_south(None)
        return

        p = QtGui.QPainter(self)
        msg = "麻将大王"
        p.setPen(QtGui.QPen(QtCore.Qt.darkGray))
        # p.drawText(rect, msg, Qt.AlignCenter)
        x, y = 100, 100
        ft = QtGui.QFont("华文行楷", 62, QtGui.QFont.Bold)
        p.setFont(ft)
        for i in range(5):
            x += 1
            y += 1
            p.drawText(x, y, msg)
            i += 1

        p.setPen(QtGui.QPen(QtCore.Qt.black))
        p.drawText(x, y, msg)


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_win()

        # TODO(tiger) Change this to use relations
        self.table = MahjongTable(self)
        self.bench = QtWidgets.QWidget()

        hl = QtWidgets.QHBoxLayout(self)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(0)
        hl.addWidget(self.table)
        hl.addWidget(self.bench)

        self.init_bench()

    def init_bench(self):
        self.bench.setFixedWidth(100)

        lv = QtWidgets.QVBoxLayout(self.bench)
        pb = QtWidgets.QPushButton('开始打牌')
        pb.clicked.connect(self.table.slot_playing)
        lv.addWidget(pb)

    def init_win(self):
        self.setWindowTitle('麻将乐园')

        self.move(self.width() * (-2), 0)  # 先将窗口放到屏幕外，可避免移动窗口时的闪烁现象。
        self.show()

        height_title = self.frameGeometry().height() - self.geometry().height()

        # # 获取显示器分辨率大小
        desktop = QtWidgets.QApplication.desktop()
        height = desktop.availableGeometry().height()
        width = desktop.availableGeometry().width()
        # screenRect = desktop.screenGeometry()

        # self.setFixedSize(1200, height-100)
        # print(height, height_title)
        self.resize(1200, height - height_title)
        self.move(width // 2 - 600, 2)

        # Utils.center_win(self)

    # def resizeEvent(self, event):
    #     palette = QtGui.QPalette()
    #     pix = QtGui.QPixmap('./res/images/background.jpg')
    #     pix = pix.scaled(self.width(), self.height())
    #     palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
    #     self.setPalette(palette)

    # 图片的透视变换


if __name__ == '__main__':
    # 字体大小自适应分辨率
    app = None
    v_compare = QtCore.QVersionNumber(5, 6, 0)
    v_current, _ = QtCore.QVersionNumber.fromString(QtCore.QT_VERSION_STR)  # 获取当前Qt版本
    if QtCore.QVersionNumber.compare(v_current, v_compare) >= 0:
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # Qt从5.6.0开始，支持High-DPI
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication(sys.argv)
        font = QtGui.QFont("宋体")
        pointsize = font.pointSize()
        font.setPixelSize(pointsize * 90 // 72)
        app.setFont(font)

    # mainWnd = FrameLessWindow()
    # mainWnd.setWindowTitle('测试标题栏')
    # mainWnd.setWindowIcon(QtGui.QIcon('./res/images/tu.png'))
    #
    # height = app.desktop().screenGeometry().height()
    # screenRect = desktop.screenGeometry()
    # desktopRect = desktop.availableGeometry()
    # print(screenRect, desktopRect)

    # height = QtWidgets.QDesktopWidget().screenGeometry().height()
    # mainWnd.resize(QtCore.QSize(1200, height))
    #
    # mainWnd.setWidget(MainWindow())  # 把自己的窗口添加进来
    # mainWnd.show()
    # mainWnd.center()

    win = MainWindow()
    # win = MahjongTable(None)
    # win.show()
    # win.slot_playing()
    # win.update()

    sys.exit(app.exec_())
