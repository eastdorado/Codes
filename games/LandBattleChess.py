#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import random
import os
from functools import partial
from PyQt5 import QtWidgets, QtGui, QtCore
from utilities import Utils, MyLog, BitMark, BitSet


class Chess(QtWidgets.QFrame):
    ORDER = ('司令', '军长', '师长', '旅长', '团长', '营长',
             '连长', '排长', '工兵', '地雷', '炸弹', '军旗')

    # CODE = r'ABCCDDEEFFGGGHHHIIIJJJKKL'  # 红方编码

    FORM = ('军旗', '司令', '军长',
            '师长', '师长', '旅长', '旅长', '团长', '团长', '营长', '营长', '炸弹', '炸弹',
            '连长', '连长', '连长', '排长', '排长', '排长', '工兵', '工兵', '工兵',
            '地雷', '地雷', '地雷')  # 红方25 个
    qss_pb = ['border:0px solid green; border-radius:8px;padding: 2px 4px;',  # 共性
              # 'hover{background-color:rgb(44 , 137 , 255)};'
              # 'pressed{background-color:rgb(14 , 135 , 228);padding-left:3px;padding-top:3px};',

              # 'background:qlineargradient('  # 显示背面
              # 'spread: pad, x1: 0, y1: 1, x2: 0, y2: 0,'
              # 'stop:0 #00ff00, stop:0.5 #505050, stop:0.98 #00ff00);',
              'background:rgb(0, 155, 0);',
              # 'background:qlineargradient('  # 显示红方
              # 'spread: pad, x1: 0, y1: 1, x2: 0, y2: 0,'
              # 'stop:0 #ff0000, stop:0.5 #505050, stop:0.98 #ff0000);',
              'background:rgb(200, 0, 0);',
              # 'background:qlineargradient('  # 显示蓝方
              # 'spread: pad, x1: 0, y1: 1, x2: 0, y2: 0,'
              # 'stop:0 #0000ff, stop:0.5 #505050, stop:0.98 #0000ff);',
              'background:rgb(0, 0, 200);',
              'color:white;'  # 鼠标弹起时
              'font-family:"宋体";font-size:35px;font-weight:bold;'
              ]
    colors = (QtGui.QColor(105, 155, 5),  # 背面底色
              QtGui.QColor(214, 105, 5),  # 红方底色
              QtGui.QColor(30, 105, 160),  # 蓝方底色
              QtCore.Qt.red, QtCore.Qt.blue)  # 外框 红色或蓝色

    def __init__(self, parent, index, coord):
        super(Chess, self).__init__(parent)
        self._parent = parent
        self._style_fm = 0  # 内框类型，0:用底色清除内框 1:红框 2:蓝框
        self._width_fm = 3  # 红蓝外框的宽度
        self._radius = 8  # 圆角半径
        self._deep = 4  # 文字的阴影深度
        self._rank = self.ORDER[index % 12]  # 军衔

        self.ID = index  # 棋子标识
        self.coord = coord  # 坐标
        self.is_hide = True

        self.init_ui()

    def init_ui(self):
        # self.setFixedSize(160, 130)
        # self.setLineWidth(10)
        # self.setMidLineWidth(10)
        # self.setFrameShape(QtWidgets.QFrame.Panel)
        # self.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.setFrameStyle(QtWidgets.QFrame.Raised | QtWidgets.QFrame.StyledPanel)
        # self.setFrameRect(QtCore.QRect(10, 10, 80, 80))

        # self.setStyleSheet(f'{self.qss_pb[0]}{self.qss_pb[1]}')
        # self.setStyleSheet(f'background:rgb(0,155,0);border-radius:{self.radius}px;')

        # self.setMouseTracking(True)
        Utils.set_effect(self, 1, 10, 5, 5, QtGui.QColor(100, 100, 100))

    def get_info(self):
        return self.ID, self.coord, self.is_hide, self._rank

    def update_me(self, coord=None, style_fm=1, hidden=False):
        self.is_hide = hidden  # 默认是明牌
        self.coord = coord if coord else self.coord
        self._style_fm = style_fm + 2 if style_fm in [1, 2] else \
            0 if self.is_hide else (self.ID // 12) + 1  # 默认是红色内框
        # print(self._style_fm)
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        rect = self.rect()
        p = QtGui.QPainter()
        p.begin(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)  # 抗锯齿

        # region 填充阵营底色
        color = self.colors[0] if self.is_hide else self.colors[1] if self.ID < 12 else self.colors[2]
        p.setBrush(QtGui.QBrush(color))
        p.setPen(QtGui.QPen(color, 1, QtCore.Qt.SolidLine))
        p.drawRoundedRect(rect, self._radius, self._radius)
        # endregion

        # region 画红、蓝框、底色框
        rect.setX(rect.x() + self._width_fm)
        rect.setY(rect.y() + self._width_fm)
        rect.setWidth(rect.width() - self._width_fm)
        rect.setHeight(rect.height() - self._width_fm)
        p.setPen(QtGui.QPen(self.colors[self._style_fm], 2 * self._width_fm, QtCore.Qt.SolidLine))
        p.drawRoundedRect(rect, self._radius, self._radius)
        # endregion

        # region 立体名字
        if not self.is_hide:  # 不是暗牌
            rect = self.rect()
            p.setFont(QtGui.QFont("微软雅黑", 20, QtGui.QFont.Normal))
            # 绘制阴文
            p.setPen(QtGui.QPen(QtCore.Qt.darkGray, 1, QtCore.Qt.SolidLine))

            rect.setX(rect.x() - self._deep)
            rect.setY(rect.y() - self._deep)
            for i in range(self._deep):
                rect.setX(rect.x() + 1)
                rect.setY(rect.y() + 1)
                p.drawText(rect, QtCore.Qt.AlignCenter, self._rank)
            # 绘制阳文
            p.setPen(QtGui.QPen(QtCore.Qt.white))
            p.drawText(rect, QtCore.Qt.AlignCenter, self._rank)
        # endregion

        # 颜色渐变线
        # for i in range(self.border):
        #     c = (self.border - i) * 8
        #     # print(type(c), c)
        #
        #     r = color.red() + c if color.red() > 10 else 0
        #     g = color.green() + c if color.green() > 10 else 0
        #     b = color.blue() + c if color.blue() > 10 else 0
        #     new_color = QtGui.QColor(r, g, b)
        #     # print(r, g, b)
        #     p.setPen(QtGui.QPen(new_color, 1, QtCore.Qt.SolidLine))
        #
        #     # rect = self.rect()
        #     # rect.setX(rect.x()+i)
        #     # rect.setY(rect.y()+i)
        #     # rect.setWidth(rect.width() - i)
        #     # rect.setHeight(rect.height() - i)
        #     #
        #     # p.drawRoundedRect(rect, self.radius, self.radius)
        #
        #     # p.drawLine(self.radius - i, i, self.width() - self.radius + i, i)
        #     p.drawLine(i, i, self.width() - i, i)
        #     # p.drawLine(i, self.radius - i, i, self.height() - self.radius + i)
        #     p.drawLine(i, i, i, self.height() - i)
        #
        #     r = color.red() - c if color.red() > 10 else 0
        #     g = color.green() - c if color.green() > 10 else 0
        #     b = color.blue() - c if color.blue() > 10 else 0
        #     new_color = QtGui.QColor(r, g, b)
        #     p.setPen(QtGui.QPen(new_color, 1, QtCore.Qt.SolidLine))
        #
        #     p.setPen(QtGui.QPen(new_color, 1, QtCore.Qt.SolidLine))
        #     # p.drawLine(self.radius - i, self.height() - i, self.width() - self.radius + i, self.height() - i)
        #     # p.drawLine(self.width() - i, self.radius - i, self.width() - i, self.height() - self.radius + i)
        #     p.drawLine(i, self.height() - i, self.width() - i, self.height() - i)
        #     p.drawLine(self.width() - i, i, self.width() - i, self.height() - i)
        p.end()

    # def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
    #     self._hide = False
    #     self.state = 4  # 蓝框
    #     self.update()
    #     # self._parent.chess_clicked(self)  # 传回当前棋子

    @staticmethod
    def army_building():
        return [Chess.ORDER.index(soldier) for soldier in Chess.FORM] + \
               [Chess.ORDER.index(soldier) + 12 for soldier in Chess.FORM]
        # id_red = list(Chess.CODE.lower())
        # id_blue = list(Chess.CODE.upper())
        # return [soldier for soldier in id_red] + [soldier for soldier in id_blue]


class MyToolbar(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyToolbar, self).__init__(parent)

        self.parent = parent
        self._pre_pos = None

        self._init_ui()

    def _init_ui(self):
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)  # 无边框
        self.setObjectName('tool')
        # self.setStyleSheet('background-color:rgba(0,200,0,255);')
        self.setFixedSize(self.parent.width(), self.parent.front)
        self.move(0, (self.parent.height() - self.height()) // 2 + 4)
        Utils.set_effect(self, 2, 0.7)  # 背景半透明

        lh = QtWidgets.QHBoxLayout(self)

        pb = QtWidgets.QPushButton('新局', self)
        pb.setStyleSheet('background-color:rgba(10,210,210,155); color:rgba(20,10,255,255);'
                         'font-size:25px;font-weight:bold;font-family:新宋体;border-radius:5;')
        pb.setFixedSize(60, 30)
        # pb.move(180, self.height() // 2 - 15)
        pb.clicked.connect(partial(self.parent.slot_pb_clicked, pb))
        # lh.addStretch()
        lh.addWidget(pb)

        pb = QtWidgets.QPushButton('悔棋', self)
        pb.setStyleSheet('background-color:rgba(10,210,210,155); color:rgba(20,10,255,255);'
                         'font-size:25px;font-weight:bold;font-family:新宋体;border-radius:5;')
        pb.setFixedSize(60, 30)
        # pb.move(180, self.height() // 2 - 15)
        pb.clicked.connect(partial(self.parent.slot_pb_clicked, pb))
        # lh.addStretch()
        lh.addWidget(pb)

        pb = QtWidgets.QPushButton('退出', self)
        pb.setStyleSheet('background-color:rgba(10,210,210,155); color:rgba(20,10,255,255);'
                         'font-size:25px;font-weight:bold;font-family:新宋体;border-radius:5;')
        pb.setFixedSize(60, 30)
        # pb.move(320, self.height() // 2 - 15)
        pb.clicked.connect(partial(self.parent.slot_pb_clicked, pb))
        # lh.addSpacerItem(QtWidgets.QSpacerItem(220, 50))
        lh.addWidget(pb)
        # lh.addStretch()

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):  # 重写移动事件
        # 必须加s，否则不起作用
        if e.buttons() == QtCore.Qt.LeftButton and self._pre_pos:
            # self.move(self.pos() + self._endPos)
            self.parent.slot_move_win(e.pos() - self._pre_pos)
        e.accept()

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        if e.button() == QtCore.Qt.LeftButton:
            self._pre_pos = e.pos()
        e.accept()

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent):
        if e.button() == QtCore.Qt.LeftButton:
            self._pre_pos = False
        e.accept()

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))  # 更改鼠标图标

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        p = QtGui.QPainter()
        p.begin(self)

        # 主窗体加载不了样式时需要这样
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)  # 反锯齿
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, p, self)
        super(MyToolbar, self).paintEvent(a0)

        rect = self.rect()
        # # pix = Utils.img_center(rect.width, rect.height, r'E:/Neworld/res/background/t3.jpg')
        # # painter.setBrush(QtGui.QBrush(pix))  # 设置底图的方式之一
        # # painter.drawRoundedRect(rect, 20, 20)
        p.drawPixmap(rect, QtGui.QPixmap("E:/Neworld/res/background/t3.png"))

        # 设置字体、大小、字符间距等
        font = QtGui.QFont("华文隶书", 24, QtGui.QFont.Normal)
        # font.setPointSize(18)
        # font.setFamily("Microsoft YaHei")
        # font.setWeight(QtGui.QFont.Bold)
        # font.setBold(True)
        font.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, 10)
        p.setFont(font)

        p.setPen(QtGui.QPen(QtGui.QColor(5, 5, 5), 2, QtCore.Qt.SolidLine))
        p.drawText(rect, QtCore.Qt.AlignCenter, "楚河     汉界")
        p.end()


# 军棋（陆战棋）
class LandBattleChess(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LandBattleChess, self).__init__(parent)
        # region ui 参数及设置
        self.parent = parent
        self.setFixedSize(700, 980)
        self.move(600, 20)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)  # 无边框
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 背景透明
        # self.setMouseTracking(True)

        # print(self.composition)
        self.margin = 20
        self.border = 3  # 框线宽度
        self.space_w = 40  # 棋子间隔
        self.space_h = 15
        self.front = 60  # 楚河汉街
        self.chess_w = round((self.width() - 2 * self.margin - 4 * self.space_w) / 5)
        self.chess_h = round((self.height() - 2 * self.margin - 11 * self.space_h - self.front) / 12)
        self.half_w, self.half_h = round(self.chess_w / 2), round(self.chess_h / 2)
        self.line_w = self.width() - 2 * self.margin - self.chess_w
        self.line_h = self.height() - 2 * self.margin - self.chess_h
        self.toolbar = MyToolbar(self)

        file_name = os.path.split(__file__)[-1].split(".")[0]  # 当前文件名称
        self.log = MyLog(log_file=f'{file_name}.log', log_tags="")
        # endregion

        # region 游戏参数及设置
        self.board = [[1] * 5 for i in range(12)]  # 座位属性
        self.composition = [[None] * 5 for i in range(12)]  # 棋局的落子分布
        self.dark_room = None  # 暗牌坐标列表
        self.bastion = ['红雷', '红雷', '红雷', '红旗', '蓝雷', '蓝雷', '蓝雷', '蓝旗']  # 双方的堡垒
        self.lot = 0  # 手数
        self.setting = BitMark(16)  # 设置区的属性标志位
        self.enemies = [[], []]  # 可攻击的敌手棋子集合，击杀或同归于尽
        # self.base_camp = False
        # self.me = 0  # 玩家阵营  0是红方,1是蓝方
        # self.acting = False  # 还没开局

        self.tmp = None  # 临时位置，按下时画临时的蓝框用
        self.cur = None  # 选中的棋子位置，蓝框用
        self.move_start = None  # 移动的开始位置
        self.move_end = None  # 棋子移动的最终有效位置，或翻牌的棋子位置
        self.rect_blue = None  # 蓝框
        self.rect_red = None  # 红框列表
        # endregion

        self._init_board()

    def _init_board(self):
        # region 站点的属性设置
        # 缺省1:铁路兵站32个，一步多站 2:公路兵站14个，一步一站
        # 3:行营10个 4:大本营4个 0:界外无效

        # 32个铁路兵站，默认都是 1  Railway station
        # 14个公路兵站  depot  Highway station
        self.board[0][0] = 2
        self.board[0][2] = 2
        self.board[0][4] = 2
        self.board[2][2] = 2
        self.board[3][1] = 2
        self.board[3][3] = 2
        self.board[4][2] = 2
        self.board[7][2] = 2
        self.board[8][1] = 2
        self.board[8][3] = 2
        self.board[9][2] = 2
        self.board[11][0] = 2
        self.board[11][2] = 2
        self.board[11][4] = 2
        # 10个行营 Line camp
        self.board[2][1] = 3
        self.board[2][3] = 3
        self.board[3][2] = 3
        self.board[4][1] = 3
        self.board[4][3] = 3
        self.board[7][1] = 3
        self.board[7][3] = 3
        self.board[8][2] = 3
        self.board[9][1] = 3
        self.board[9][3] = 3
        # 4个大本营 base camp
        self.board[0][1] = 4
        self.board[0][3] = 4
        self.board[11][1] = 4
        self.board[11][3] = 4
        # self.log.debug(self.board)
        # endregion

        self.setting[0] = 1  # 玩家先手，0 ai先手   me_first = False
        self.setting[1] = 1  # 大本营不吃子  base_camp = False

        self.setting[2] = 1  # 玩家阵营  0是红方,1是蓝方
        self.setting[3] = 0  # 已经开局

        self.replay()

    def _draw_sites(self, qp: QtGui.QPainter):
        # 绘制棋盘底图

        off = 26
        half_w, half_h = self.half_w, self.half_h
        for j in range(12):
            for i in range(5):
                qp.setPen(QtGui.QPen(QtGui.QColor(55, 55, 55), 2, QtCore.Qt.SolidLine))

                x = self.margin + half_w + i * (self.chess_w + self.space_w)
                y = self.margin + half_h + j * (self.chess_h + self.space_h) if j < 6 else \
                    self.margin + half_h + self.front + j * (self.chess_h + self.space_h)

                if self.board[j][i] < 3:  # 兵站
                    rect = QtCore.QRect(x - off, y - off // 2, off * 2, off)
                    qp.setBrush(QtGui.QBrush(QtGui.QColor(0, 155, 0)))
                    qp.drawRect(rect)
                    dx, dy = off - 8, off // 2 - 8
                    rect = QtCore.QRect(x - dx, y - dy, 2 * dx, 2 * dy)
                    if self.board[j][i] == 1:  # 铁路兵站
                        qp.setBrush(QtGui.QBrush(QtCore.Qt.darkGray))
                    else:  # 公路兵站
                        qp.setBrush(QtGui.QBrush(QtCore.Qt.gray))
                    qp.drawRect(rect)

                elif self.board[j][i] == 3:  # 行营
                    off1 = off - 10
                    rect = QtCore.QRect(x - off1, y - off1, 2 * off1, 2 * off1)
                    qp.setBrush(QtGui.QBrush(QtGui.QColor(0, 155, 0)))
                    qp.drawEllipse(rect)
                    off1 = off1 - 8
                    rect = QtCore.QRect(x - off1, y - off1, 2 * off1, 2 * off1)
                    qp.setBrush(QtGui.QBrush(QtCore.Qt.lightGray))
                    qp.drawEllipse(rect)

                else:  # 大本营
                    rect = QtCore.QRect(x - 50, y - 16, 100, 32)
                    qp.setBrush(QtGui.QBrush(QtCore.Qt.darkYellow))
                    qp.drawRect(rect)

                    qp.setPen(QtGui.QPen(QtGui.QColor(55, 255, 255), 2, QtCore.Qt.SolidLine))
                    qp.setFont(QtGui.QFont("华文行楷", 14, QtGui.QFont.Bold))
                    if j < 6:  # 上面的字体要旋转
                        qp.save()
                        # qp.translate(x, y)  # 旋转中心
                        # qp.rotate(30)
                        qp.drawText(rect, QtCore.Qt.AlignCenter, '大本营')
                        qp.restore()
                    else:
                        qp.drawText(rect, QtCore.Qt.AlignCenter, '大本营')

    def _draw_railway(self, qp: QtGui.QPainter, pen: QtGui.QPen):
        half_w, half_h = self.half_w, self.half_h
        line_w, line_h = self.line_w, self.line_h
        # 铁路
        qp.setPen(pen)
        pts = [QtCore.QPoint(self.margin + half_w,
                             self.margin + half_h + self.chess_h + self.space_h),
               QtCore.QPoint(self.margin + half_w + line_w,
                             self.margin + half_h + self.chess_h + self.space_h),
               QtCore.QPoint(self.margin + half_w + line_w,
                             self.margin + half_h + self.front + 10 * (self.chess_h + self.space_h)),
               QtCore.QPoint(self.margin + half_w,
                             self.margin + half_h + self.front + 10 * (self.chess_h + self.space_h)),
               QtCore.QPoint(self.margin + half_w,
                             self.margin + half_h + self.chess_h + self.space_h)]
        qp.drawPolyline(QtGui.QPolygon(pts))

        qp.drawLine(self.margin + half_w,
                    self.margin + half_h + 5 * (self.chess_h + self.space_h),
                    self.margin + half_w + line_w,
                    self.margin + half_h + 5 * (self.chess_h + self.space_h))
        qp.drawLine(self.margin + half_w,
                    self.margin + half_h + self.front + 6 * (self.chess_h + self.space_h),
                    self.margin + half_w + line_w,
                    self.margin + half_h + self.front + 6 * (self.chess_h + self.space_h))
        qp.drawLine(self.margin + half_w + 2 * (self.chess_w + self.space_w),
                    self.margin + half_h + 5 * (self.chess_h + self.space_h),
                    self.margin + half_w + 2 * (self.chess_w + self.space_w),
                    self.margin + half_h + self.front + 6 * (self.chess_h + self.space_h))

    def _draw_frame(self, qp: QtGui.QPainter):
        # 在空的兵站上画蓝框框
        w_line = 6
        if self.rect_blue:
            qp.setPen(QtGui.QPen(QtGui.QColor(0, 0, 255), w_line, QtCore.Qt.SolidLine))
            qp.setBrush(QtGui.QBrush())  # 空画刷，就是透明
            qp.drawRoundedRect(self.rect_blue, 5.0, 5.0)
            # x, y, w, h = self.rect_blue.x(), self.rect_blue.y(), self.rect_blue.width(), self.rect_blue.height()
            # qp.drawLine(x-w_line, y-w_line, x+w+w_line, y-w_line)
            # qp.drawLine(x-w_line, y-w_line, x-w_line, y+h+w_line)
            # qp.drawLine(x+w+w_line, y-w_line, x+w+w_line, y+h+w_line)
            # qp.drawLine(x-w_line, y+h+w_line, x+w+w_line, y+h+w_line)
            # qp.drawLine(self.rect_blue.topLeft(), self.rect_blue.bottomLeft())
            # qp.drawLine(self.rect_blue.topLeft(), self.rect_blue.topRight())
            # qp.drawLine(self.rect_blue.bottomLeft(), self.rect_blue.bottomRight())
            # qp.drawLine(self.rect_blue.topRight(), self.rect_blue.bottomRight())

        if self.rect_red:
            qp.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), w_line, QtCore.Qt.SolidLine))
            qp.setBrush(QtGui.QBrush())  # 空画刷，就是透明
            qp.drawRoundedRect(self.rect_red, 5.0, 5.0)

        # else:  # 擦除蓝框
        #     ...

    def _where_hit(self, pos):
        # 获得鼠标点击处的行列号和左上角在窗口里的坐标
        x, y = pos.x(), pos.y()
        y = y if y < (self.height() - self.front) // 2 else y - self.front  # 下半区

        row = (y - self.margin + self.space_h // 2) // (self.chess_h + self.space_h)
        col = (x - self.margin + self.space_w // 2) // (self.chess_w + self.space_w)

        dx = self.margin + col * (self.chess_w + self.space_w)  # 棋子的左边界
        dy = self.margin + row * (self.chess_h + self.space_h)  # 棋子的上边界

        # print('鼠标点击了 in', row, col)
        if dx <= x <= dx + self.chess_w and dy <= y <= dy + self.chess_h:  # 点击在棋子范围内了
            if row > 5:
                dy += self.front

            return row, col, dx, dy
        else:
            return None

    def _clear_frame(self, clear_end=False, cur_coord=None):
        if clear_end:
            # 擦除过时红框
            chess = self.composition[self.move_end[0]][self.move_end[1]]
            chess.update_me(None, 0)

            if cur_coord:  # 迎接新红框
                self.move_end = cur_coord

        # 擦除无用的蓝框并归零，但是与自己的last红框重合时则需要继续显示
        elif self.move_start and self.move_start != self.move_end:
            chess = self.composition[self.move_start[0]][self.move_start[1]]
            chess.update_me(None, 0)
            self.move_start = None

    def paintEvent(self, e: QtGui.QPaintEvent) -> None:
        half_w, half_h = self.half_w, self.half_h
        line_w, line_h = self.line_w, self.line_h
        qp = QtGui.QPainter()
        qp.begin(self)

        qp.setRenderHint(QtGui.QPainter.Antialiasing)  # 抗锯齿
        qp.drawPixmap(0, 0, QtGui.QPixmap("E:/Neworld/res/background/background2.jpg"))

        # region 纵横线
        qp.setPen(QtGui.QPen(QtGui.QColor(50, 50, 50), 2, QtCore.Qt.SolidLine))
        for j in range(12):
            x = self.margin + half_w
            y = self.margin + half_h + j * (self.chess_h + self.space_h) if j < 6 else \
                self.margin + half_h + j * (self.chess_h + self.space_h) + self.front
            qp.drawLine(x, y, x + line_w, y)

        for i in range(0, 5, 2):
            x = self.margin + half_w + i * (self.chess_w + self.space_w)
            y = self.margin + half_h
            qp.drawLine(x, y, x, y + line_h)

        for i in range(1, 5, 2):
            x = self.margin + half_w + i * (self.chess_w + self.space_w)
            y = self.margin + half_h
            qp.drawLine(x, y, x, y + 5 * (self.chess_h + self.space_h))
            qp.drawLine(x, y + self.front + 6 * (self.chess_h + self.space_h), x, y + line_h)
        # endregion

        # region 斜线
        qp.drawLine(self.margin + half_w, self.margin + half_h + self.chess_h + self.space_h,
                    self.margin + half_w + line_w, self.margin + half_h + 5 * (self.chess_h + self.space_h))
        qp.drawLine(self.margin + half_w + line_w, self.margin + half_h + self.chess_h + self.space_h,
                    self.margin + half_w, self.margin + half_h + 5 * (self.chess_h + self.space_h))

        pts = [QtCore.QPoint(self.margin + half_w + 2 * (self.chess_w + self.space_w),
                             self.margin + self.chess_h + self.space_h + half_h),
               QtCore.QPoint(self.margin + half_w + line_w,
                             self.margin + 3 * (self.chess_h + self.space_h) + half_h),

               QtCore.QPoint(self.margin + half_w + 2 * (self.chess_w + self.space_w),
                             self.margin + 5 * (self.chess_h + self.space_h) + half_h),
               QtCore.QPoint(self.margin + half_w,
                             self.margin + 3 * (self.chess_h + self.space_h) + half_h),
               QtCore.QPoint(self.margin + half_w + 2 * (self.chess_w + self.space_w),
                             self.margin + self.chess_h + self.space_h + half_h)]
        qp.drawPolyline(QtGui.QPolygon(pts))

        qp.drawLine(self.margin + half_w,
                    self.margin + half_h + self.front + 6 * (self.chess_h + self.space_h),
                    self.margin + half_w + line_w,
                    self.margin + half_h + self.front + 10 * (self.chess_h + self.space_h))
        qp.drawLine(self.margin + half_w + line_w,
                    self.margin + half_h + self.front + 6 * (self.chess_h + self.space_h),
                    self.margin + half_w,
                    self.margin + half_h + self.front + 10 * (self.chess_h + self.space_h))

        pts = [QtCore.QPoint(self.margin + half_w + 2 * (self.chess_w + self.space_w),
                             self.margin + half_h + self.front + 6 * (self.chess_h + self.space_h)),
               QtCore.QPoint(self.margin + half_w + line_w,
                             self.margin + half_h + self.front + 8 * (self.chess_h + self.space_h)),
               QtCore.QPoint(self.margin + half_w + 2 * (self.chess_w + self.space_w),
                             self.margin + half_h + self.front + 10 * (self.chess_h + self.space_h)),
               QtCore.QPoint(self.margin + half_w,
                             self.margin + half_h + self.front + 8 * (self.chess_h + self.space_h)),
               QtCore.QPoint(self.margin + half_w + 2 * (self.chess_w + self.space_w),
                             self.margin + half_h + self.front + 6 * (self.chess_h + self.space_h))]
        qp.drawPolyline(QtGui.QPolygon(pts))
        # endregion

        # 铁路
        self._draw_railway(qp, QtGui.QPen(QtGui.QColor(50, 50, 50), 10, QtCore.Qt.SolidLine))
        self._draw_railway(qp, QtGui.QPen(QtGui.QColor(255, 255, 255), 4, QtCore.Qt.DashLine))

        self._draw_sites(qp)  # 棋子位置
        self._draw_frame(qp)  # 画蓝框框

        qp.end()

    # def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
    #     super(LandBattleChess, self).resizeEvent(a0)
    #
    #     # pb.setObjectName('测试')
    #     # pb.setStyleSheet(f'{self.qss_pb[0]}{self.qss_pb[1]}')
    #     # pb.move(40, 50)

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        ret = self._where_hit(e.pos())
        if ret is None:
            return

        row, col, dx, dy = ret

        chess_hit = self.composition[row][col]
        if not chess_hit:  # 点击了无棋子的兵站或兵营
            self.rect_blue = QtCore.QRect(dx + 3, dy + 3, self.chess_w - 3, self.chess_h - 3)
            self.update()
        else:
            self.tmp = [row, col]
            _, coord, hidden, _ = chess_hit.get_info()
            # print(coord, row, col, hidden)

            chess_hit.update_me(None, 2, hidden)  # 蓝框

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        # region 各个方框的显示与擦除
        self.rect_blue = None  # 清除蓝框
        self.update()

        if self.tmp:  # 先无条件擦除蓝框
            chess = self.composition[self.tmp[0]][self.tmp[1]]
            _, coord, hidden, _ = chess.get_info()
            chess.update_me(None, 0, hidden)  # 擦除蓝框
            self.tmp = None

        if self.move_end:  # 先无条件显示最后的红框
            chess = self.composition[self.move_end[0]][self.move_end[1]]
            chess.update_me()  # 红框，采用默认值即可
        # endregion

        ret = self._where_hit(e.pos())
        if ret is None:
            return
        row, col, dx, dy = ret
        chess_hit = self.composition[row][col]

        # 处理有效点击事件
        if chess_hit is None:  # 点击了空白位置，还要判断当前棋子能否移动到这个位置
            if False and self.move_start:  # 不能移动，则把当前的蓝框抹去
                chess_cur = self.composition[self.move_start[0]][self.move_start[1]]
                chess_cur.update_me(None, 0)

            elif self.move_start:  # 能移动则改变当前棋子  地雷、军旗不能移动
                if self.move_end:  # 擦除上次点击的红框
                    chess = self.composition[self.move_end[0]][self.move_end[1]]
                    # print(self.move_end, chess)
                    chess.update_me(None, 0)

                self.move_end = [row, col]  # 切换到当前落点
                # 记录好正确的棋子移动的起始点

                # 棋子移动
                chess_moving = self.composition[self.move_start[0]][self.move_start[1]]
                # ret = chess_moving.get_info()
                # print("棋子内部坐标与外部坐标一致否？：", ret[1], self.cur)

                self.composition[row][col] = chess_moving  # 棋子在分布图上的移动
                self.composition[self.move_start[0]][self.move_start[1]] = None  # 地图上控件置换

                chess_moving.move(dx, dy)  # 棋子在屏幕上的移动
                chess_moving.update_me(self.move_end)  # move_end 位置处棋子打上默认的红色框

                # move_start 位置也画红框
                dx1 = self.margin + self.move_start[1] * (self.chess_w + self.space_w)  # 棋子的左边界
                dy1 = self.margin + self.move_start[0] * (self.chess_h + self.space_h)  # 棋子的上边界
                dy1 = dy1 + self.front if self.move_start[0] > 5 else dy1
                self.rect_red = QtCore.QRect(dx1 + 3, dy1 + 3, self.chess_w - 3, self.chess_h - 3)
                self.update()

                self.move_start = None
                self.call_ai()  # 呼叫 AI 走棋

        else:  # 点中了棋子
            ID, coord, hidden, rank = chess_hit.get_info()
            # print(name, ID, coord, row, col)

            if self.move_end is None:  # 第一次点了棋子，如机器先手，则不用执行这步
                self.lot += 1
                self.move_end = [row, col]  # coord
                self.me = ID // 12  # 选择玩家阵营
                chess_hit.update_me()  # 红框，采用默认值即可
                # print("我是蓝方" if self.me else '我是红方')
                self.dark_room.pop(self.dark_room.index(row * 5 + col))  # 明牌弹出小黑屋

                self.call_ai()  # 呼叫 AI 走棋

            elif hidden:  # 暗棋需要翻转
                self.lot += 1
                self._clear_frame()  # 清除过时蓝框
                chess_last = self.composition[self.move_end[0]][self.move_end[1]]
                chess_last.update_me(None, 0)  # 擦除上次点击的红框

                self.move_end = coord  # 切换到当前位置
                chess_hit.update_me()  # 红框，采用默认值即可
                self.dark_room.pop(self.dark_room.index(row * 5 + col))  # 明牌弹出小黑屋

                self.call_ai()  # 呼叫 AI 走棋

            elif ID // 12 == self.me:  # 点击的棋子是玩家的
                print(f'点击了我方{rank}', coord, [row, col])
                self._clear_frame()  # 清除过时蓝框
                self.move_start = coord  # 当前点击一定是蓝的，可以覆盖红框，红框下次自动显示
                chess_hit.update_me(None, 2)  # 蓝框

            else:  # 判断能否吃掉对方棋子
                # print(ID, rank, self.me)
                # 不能吃则忽略操作，并清除当前项

                # 能吃就取代
                if self.move_start:
                    chess_start = self.composition[self.move_start[0]][self.move_start[1]]
                    info = chess_start.get_info()

                    print(info[3], rank)
                    ret = self.judge(info[0], ID)
                    print(ret)
                    if ret > 0:  # 成功吃棋，更新end
                        self._clear_frame(True, coord)
                        chess_hit.update_me()

    def slot_pb_clicked(self, ctl):
        text = ctl.text()
        # print(text)
        if text == '新局':
            print('不能的')
            self.replay()
        elif text == '悔棋':
            print('等待完善')
        else:
            self.close()

    def slot_move_win(self, pos):
        self.move(self.pos() + pos)

    # def chess_clicked(self, chess):
    #     if self.pre:
    #         self.pre.update_chess(1)
    #     self.pre = self.cur
    #     self.cur = chess
    #     print('chess')

    # 新局开始，随机布子
    def replay(self):
        # region 游戏数据清零
        self.move_start = None
        self.move_end = None
        self.tmp = None
        self.cur = None

        if self.setting[3]:  # 需要清理棋子控件
            return
            # for row in range(12):
            #     for col in range(5):
            #         chess = self.composition[row][col]
            #         chess.destroy()
            #         self.composition[row][col]= None
        # endregion

        # region 游戏数据初始化
        # region 小黑屋初始化
        # 小黑屋去掉行营位置，其他位置放棋子
        self.dark_room = [i for i in range(60)]
        self.dark_room.pop(self.dark_room.index(11))
        self.dark_room.pop(self.dark_room.index(13))
        self.dark_room.pop(self.dark_room.index(17))
        self.dark_room.pop(self.dark_room.index(21))
        self.dark_room.pop(self.dark_room.index(23))
        self.dark_room.pop(self.dark_room.index(36))
        self.dark_room.pop(self.dark_room.index(38))
        self.dark_room.pop(self.dark_room.index(42))
        self.dark_room.pop(self.dark_room.index(46))
        self.dark_room.pop(self.dark_room.index(48))
        # print(self.dark_room)
        # endregion

        # region 军队初始化
        # army = [i for i in range(50)]  # 在tiles里的id
        army = Chess.army_building()
        random.shuffle(army)
        # print(len(army), army)
        # endregion

        # region 棋子地图随机分布初始化
        # for row in range(12):
        #     for col in range(5):
        #         if self.board[row][col] == 3:  # 行营空置
        #             continue
        for each in self.dark_room:
            row = each // 5
            col = each % 5
            # print(each, row, col)

            self.composition[row][col] = Chess(self, army.pop(), [row, col])  # 棋局的棋子分布图

            x = self.margin + col * (self.chess_w + self.space_w)
            y = self.margin + row * (self.chess_h + self.space_h) if row < 6 else \
                self.margin + self.front + row * (self.chess_h + self.space_h)

            self.composition[row][col].setGeometry(x, y, self.chess_w, self.chess_h)
            self.composition[row][col].show()
        # endregion
        # endregion

        # region 开始游戏
        self.setting[3] = True

        if not self.setting[0]:  # 机器先手
            self._ai_open_chess()
            if self.move_end:
                # print(self.move_end)
                chess_end = self.composition[self.move_end[0]][self.move_end[1]]
                chess_end.update_me()  # 红框，采用默认值即可
                info = chess_end.get_info()
                self.me = 1 - info[0] // 12  # 选择玩家阵营
                print("AI是红方" if self.me else 'AI是蓝方')
        # endregion

        # while True:
        #     self._AI_open_chess()

    def call_ai(self):
        # 电脑走起
        self._ai_open_chess()
        # 吃棋

    def _ai_open_chess(self):
        # AI翻棋
        if self.dark_room:
            if self.rect_red:  # 擦除上次的移动后的红框
                self.rect_red = None  # 清除红框
                self.update()

            if self.move_end:  # 擦除上次点击的红框
                chess = self.composition[self.move_end[0]][self.move_end[1]]
                chess.update_me(None, 0)  # 擦除上次点击的红框

            index = Utils.rand_int(0, len(self.dark_room) - 1)
            coord = self.dark_room.pop(index)  # 明牌弹出小黑屋
            self.lot += 1
            row, col = coord // 5, coord % 5
            # print(row, col, coord, index, self.dark_room)

            self.move_end = [row, col]  # 切换到当前位置
            chess = self.composition[row][col]
            chess.update_me()  # 红框，采用默认值即可

    def victory(self):
        if '红旗' not in self.bastion:
            print("红方军旗被夺，蓝方胜！")
        elif '蓝旗' not in self.bastion:
            print("蓝方军旗被夺，红方胜！")
        else:
            ...

    @staticmethod
    def _valid_coord(coord=None):
        # 坐标有效性判断
        return True if coord and 0 <= coord[0] < 12 and 0 <= coord[1] < 5 else False

    # 获得所有可抵达的敌人
    def get_enemies(self, coord):
        if not self._valid_coord(coord):
            return None
        row, col = coord

        chess = self.composition[row][col]
        ret = chess.get_info()
        if ret[3] in ['地雷', '军旗']:  # 不能移动吃子的
            return None

        self.enemies[0].clear()
        self.enemies[1].clear()

        if self.board[row][col] in [2, 4]:  # 2: 公路兵站14个，一步一站  4:大本营4个
            self._search_neighbour_near(row, col)

        elif self.board[row][col] == 3:  # 3:行营10个
            self._search_neighbour_near(row, col)

            if self._valid_coord(row - 1, col - 1):
                self._fight_neighbour(row, col, row - 1, col - 1)
            if self._valid_coord(row - 1, col + 1):
                self._fight_neighbour(row, col, row - 1, col + 1)
            if self._valid_coord(row + 1, col - 1):
                self._fight_neighbour(row, col, row + 1, col - 1)
            if self._valid_coord(row + 1, col + 1):
                self._fight_neighbour(row, col, row + 1, col + 1)

        else:  # 缺省1: 铁路兵站32个，一步多站   0:界外无效
            ...


    def _search_neighbour_near(self, row, col):
        if self._valid_coord(row, col - 1):
            self._fight_neighbour(row, col, row, col - 1)
        if self._valid_coord(row, col + 1):
            self._fight_neighbour(row, col, row, col + 1)
        if self._valid_coord(row - 1, col):
            self._fight_neighbour(row, col, row - 1, col)
        if self._valid_coord(row + 1, col):
            self._fight_neighbour(row, col, row + 1, col)

    def _fight_neighbour(self, row1, col1, row2, col2):
        chess1 = self.composition[row1, col1]
        chess2 = self.composition[row2, col2]

        if not chess1 or not chess2:
            return

        ret1 = chess1.get_info()
        ret2 = chess2.get_info()

        if abs(ret1[0] - ret2[0]) < 12:  # 自己人
            return

        result = self._judge(ret1[0], ret2[0])
        if result == 0:
            self.enemies[1].append(chess2)
        elif result > 0:
            self.enemies[0].append(chess2)

    # 战斗裁判   =0：同归于尽  <0：失败  >0：胜利
    def _judge(self, id_attacker, id_defender):
        ret = 0
        a = id_attacker % 12  # 进攻方
        d = id_defender % 12  # 防守方

        if a < 9 and d < 9:
            ret = d - a  # 越小军衔越大

        if d is Chess.ORDER.index('军旗'):  # 比炸弹优先，炸弹炸不了
            if a == Chess.ORDER.index('工兵'):
                if id_attacker < 12:
                    if '蓝雷' not in self.bastion:  # 蓝方地雷已光
                        self.bastion.pop(self.bastion.index('蓝旗'))  # 可以夺去蓝方军旗
                        ret = 1
                    else:
                        ret = -1
                else:
                    if '红雷' not in self.bastion:  # 红方地雷已光
                        self.bastion.pop(self.bastion.index('红旗'))  # 可以夺去蓝方军旗
                        ret = 1
                    else:
                        ret = -1
            else:
                ret = -1

        elif a == Chess.ORDER.index('炸弹'):  # 比地雷优先
            ret = 0

        elif d is Chess.ORDER.index('地雷'):
            if a == Chess.ORDER.index('工兵'):
                if id_attacker < 12:  # red
                    self.bastion.pop(self.bastion.index('蓝雷'))  # 蓝方地雷 -1
                else:
                    self.bastion.pop(self.bastion.index('红雷'))  # 弹出红方地雷， -1
                ret = 1
            else:
                ret = -1

        return ret

    # def _update_frame(self, showing=False):
    #     # 各种方框的显示与擦除
    #     if showing:
    #         ...
    #     else:
    #         # region 各个方框的擦除
    #
    #         if self.rect_red or self.rect_blue:  # 擦除上次的移动后的红框
    #             self.rect_blue = None  # 清除蓝框
    #             self.rect_red = None  # 清除红框
    #             self.update()
    #
    #         if self.last:  # 擦除上次点击的红框
    #             chess_last = self.composition[self.last[0]][self.last[1]]
    #             chess_last.update_me(None, 0)  # 擦除上次点击的红框
    #
    #         if self.tmp:  # 先无条件擦除蓝框
    #             chess = self.composition[self.tmp[0]][self.tmp[1]]
    #             _, coord, hidden, _ = chess.get_info()
    #             chess.update_me(None, 0, hidden)  # 擦除蓝框
    #             self.tmp = None
    #
    #         if self.cur and self.cur != self.last:  # 当前的蓝框也要擦除并归零
    #             chess_cur = self.composition[self.cur[0]][self.cur[1]]
    #             chess_cur.update_me(None, 0)
    #             self.cur = None
    #         # endregion

    def __str__(self):
        return '翻棋 Flip chess 玩法。'

    __repr__ = __str__


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = LandBattleChess()
    # form = MyToolbar()
    form.show()
    sys.exit(app.exec_())

    # MyLog('test.log', 1).debug('haohao')

    # b = BitSet(3)
    # print("size=", b.size())
    # print("binstr=", b, b.show())
    # a = BitMark(8)
    # a[2] = 1
    # # a[12] = 1
    #
    # print(a)
    # a[-3] = 1
    # print(a)
    # # a.set(-3)
    # a.flip()
    # print(a, len(a), a[-3], a[4])
