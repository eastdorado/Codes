#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import random
import os
import copy
import time
from functools import partial
from PyQt5 import QtWidgets, QtGui, QtCore
from utilities import Utils, MyLog, BitMark

sys.setrecursionlimit(100000)  # 这里设置递归深度为十万


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

    def update_me(self, coord=None, style_fm=3, hidden=False):
        self.is_hide = hidden  # 默认是明牌
        self.coord = copy.deepcopy(coord) if coord else self.coord
        # 3 red  4 blue； 其他任意是原色，隐藏就是背面
        self._style_fm = style_fm if style_fm in [3, 4] else \
            0 if self.is_hide else (self.ID // 12) + 1  # 默认是红色内框

        # print(self._style_fm, self.colors[self._style_fm])
        self.update()

    def delete(self) -> None:
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setParent(None)
        # layout.removeWidget(wg)
        self.deleteLater()

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
    #     # self._hide = False
    #     # self.state = 4  # 蓝框
    #     # self.update()
    #     # self._parent.chess_clicked(self)  # 传回当前棋子

    # def animation_me(self, path=None):
    #     if not path:
    #         return
    #
    #     # 动画设置
    #     animation = QtCore.QPropertyAnimation(self, b"pos", self._parent)
    #     # length = len(path)
    #     # delay = 1/length
    #     # for i in range(length):
    #     #     animation.setKeyValueAt(i*delay, path[i])
    #
    #     animation.setKeyValueAt(0, QtCore.QPoint(150, 150))
    #     animation.setKeyValueAt(0.25, QtCore.QPoint(550, 150))
    #     animation.setKeyValueAt(0.5, QtCore.QPoint(550, 550))
    #     animation.setKeyValueAt(0.75, QtCore.QPoint(150, 550))
    #     animation.setKeyValueAt(1, QtCore.QPoint(150, 150))
    #
    #     animation.setDuration(5000)
    #     # animation.setLoopCount(3)
    #
    #     # animation.start()
    #
    #     animation2 = QtCore.QPropertyAnimation(self, b"pos", self._parent)
    #
    #     animation2.setKeyValueAt(0, QtCore.QPoint(0, 0))
    #     animation2.setKeyValueAt(0.25, QtCore.QPoint(0, 700))
    #     animation2.setKeyValueAt(0.5, QtCore.QPoint(700, 700))
    #     animation2.setKeyValueAt(0.75, QtCore.QPoint(700, 0))
    #     animation2.setKeyValueAt(1, QtCore.QPoint(0, 0))
    #
    #     animation2.setDuration(5000)
    #     # animation2.setLoopCount(3)
    #
    #     # animation2.start()
    #
    #     animation_group1 = QtCore.QSequentialAnimationGroup(self._parent)  # 设置一个动画组
    #     # QSequentialAnimationGroup # 串行动画，多个动画挨个执行
    #     # QParallelAnimationGroup  # 并行动画，多个动画一块执行
    #     animation_group1.addAnimation(animation)  # 添加动画
    #     # animation_group1.addPause(5000) #串行动画暂时时间，串行
    #
    #     pasuse_animation = QtCore.QPauseAnimation()  # 暂停动画
    #     pasuse_animation.setDuration(3000)  # 设置暂停时间
    #     animation_group1.addAnimation(pasuse_animation)  # 添加动画
    #
    #     animation_group1.addAnimation(animation2)  # 添加动画
    #     animation_group1.start()  # 动画组开始执行
    #
    #     # red_btn.clicked.connect(animation_group1.pause)
    #     # green_btn.clicked.connect(animation_group1.resume)

    @staticmethod
    def army_building():
        # 创建全副军队
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
        p.drawPixmap(rect, QtGui.QPixmap("E:/Codes/res/background/t3.png"))

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


class UnionSet(object):
    def __init__(self):
        self.parent = {}

    def init(self, key):
        if key not in self.parent:
            self.parent[key] = key

    def find(self, key):
        self.init(key)
        while self.parent[key] != key:
            self.parent[key] = self.parent[self.parent[key]]
            key = self.parent[key]
        return key

    def join(self, key1, key2):
        p1 = self.find(key1)
        p2 = self.find(key2)
        if p1 != p2:
            self.parent[p2] = p1


class AStarRoute(object):
    """采用二叉堆的 A星算法"""

    def __init__(self):
        self.map2d_w = 5
        self.map2d_h = 12

        self.map2d = []
        self.map2d_size = self.map2d_w * self.map2d_h  # 地图节点数目
        self.can_search = False  #

        self.start = None
        self.end = None

        self.impasse = 4  # 死路的权重
        self.value = [1, 2, 3, self.impasse]  # 权重范围

        self.open_list = []
        self.close_list = []

    def init_map2d(self, board, start, end):
        """初始化地图数据"""
        # [row, col , g, h, v, father]
        # row，col-坐标 g-当前路径成本 h-估算成本 v-节点的权重 father-父节点
        self.map2d.clear()
        self.open_list.clear()
        self.close_list.clear()

        self.start = start  # 初始化起点的序号
        self.end = end  # 初始化终点的序号

        self.open_list.append(self.start)  # 起点放进列表

        if not board or not (-1 < self.start < self.map2d_size and -1 < self.end < self.map2d_size):
            self.can_search = False
            return
        else:
            self.can_search = True

        # 地图上所有站点的权重设置
        for row in range(self.map2d_h):
            for col in range(self.map2d_w):
                h = (abs(self.end // self.map2d_h - row) + abs(self.end % self.map2d_w - col)) * 10  # 计算h值
                value = 0
                if board[row][col][0] == 1 and board[row][col][0] is None:
                    # 可通行性：铁路兵站且无棋子，可通行
                    value = 2
                else:  # 其它站点全都不可通行
                    value = self.impasse  # 非铁路兵站当做不通行

                # [row, col , g, h, v, father]
                # row，col-坐标 g-当前路径成本 h-估算成本 v-节点的权重 father-父节点
                self.map2d.append([row, col, 0, h, value, None])

        self.map2d[self.start][4] = 2  # 起点权重的重新设置
        self.map2d[self.end][4] = 3  # 终点权重的重新设置
        # print(self.map2d)

    # 序号变行列号
    def sid2coord(self, sid):
        return [sid // self.map2d_w, sid % self.map2d_w]

    # 行列号变序号
    def coord2sid(self, coord):
        """
        行列号变报数
        @param coord:
        @return:
        """
        return coord[0] * self.map2d_w + coord[1]

    def _get_f(self, node):
        assert 0 <= node < self.map2d_size
        return self.map2d[node][2] + self.map2d[node][3]  # 价值

    # region 插入和删除 open list的项目
    def _insert(self, num):
        current_id = 0
        parent_id = 0

        if num in self.open_list:
            current_id = self.open_list.index(num)
            parent_id = (current_id - 1) // 2
        else:
            self.open_list.append(num)
            current_id = len(self.open_list) - 1
            parent_id = (current_id - 1) // 2

        """把新增在最后的小数往上移动"""
        while current_id > 0:
            if self._get_f(self.open_list[parent_id]) <= self._get_f(self.open_list[current_id]):  # f值比较
                break
            else:
                self.open_list[parent_id], self.open_list[current_id] = \
                    self.open_list[current_id], self.open_list[parent_id]

                current_id = parent_id
                parent_id = (current_id - 1) // 2

    def _delate(self, num):
        """删除特定数，并下沉"""
        if num not in self.open_list:
            print(f'delate {num} : it is not in open list')
            return None

        temp = self.open_list.pop()
        if num == temp:  # 是最末的最大数
            return num

        ind = self.open_list.index(num)
        self.open_list[ind] = temp  # 用最后一项覆盖当前位置
        # print(self.open_list)
        self._shift_down(ind)  # 可以不用调用吗？
        # print(self.open_list)
        return num

    def _shift_down(self, ind):
        """父节点根据大小往下沉"""
        current_id = ind
        child_left_id = current_id * 2 + 1
        child_right_id = current_id * 2 + 2

        last_id = len(self.open_list) - 1

        while child_left_id <= last_id:  # 叶子节点不需要处理
            # 如果当前节点只有左孩子没有右孩子
            if child_left_id == last_id:
                if self._get_f(self.open_list[current_id]) <= self._get_f(self.open_list[-1]):  # f值比较
                    break
                else:
                    self.open_list[current_id], self.open_list[-1] = \
                        self.open_list[-1], self.open_list[current_id]
                    break
            # 如果当前节点既有左孩子又有右孩子
            else:
                litter_id = child_left_id \
                    if self._get_f(self.open_list[child_left_id]) <= self._get_f(self.open_list[child_right_id]) \
                    else child_right_id
                if self._get_f(self.open_list[current_id]) <= self._get_f(self.open_list[litter_id]):
                    break
                else:
                    self.open_list[litter_id], self.open_list[current_id] \
                        = self.open_list[current_id], self.open_list[litter_id]
                    current_id = litter_id
                    child_left_id = current_id * 2 + 1
                    child_right_id = current_id * 2 + 2

    # endregion

    def deal_neighbours(self, node_id):
        """处理邻居"""
        node_row = self.map2d[node_id][0]
        node_col = self.map2d[node_id][1]

        for i in range(node_row - 1, node_row + 2):
            if i < 0 or i >= self.map2d_h:  # 越界检测
                continue
            for j in range(node_col - 1, node_col + 2):
                if j < 0 or j >= self.map2d_w:  # 越界检测
                    continue
                if i == node_row and j == node_col:  # 自身检测
                    continue

                if (i + j - node_row - node_col) not in [-1, 1]:  # 四个角忽略，不走对角线
                    continue

                neighbour_id = i * self.map2d_w + j

                if self.map2d[neighbour_id][4] == self.impasse:  # 避开障碍物
                    continue

                if neighbour_id in self.close_list:  # 已经处理过了
                    continue

                path = abs(node_row - i) + abs(node_col - j)
                value = 10 if path == 1 else 14  # 不容许对角线通过，14则可以

                new_g = self.map2d[neighbour_id][4] * value + self.map2d[node_id][2]  # 计算跨越的代价

                if neighbour_id not in self.open_list:  # 新考察对象
                    self.map2d[neighbour_id][5] = node_id  # 更新其父亲
                    if neighbour_id == self.end:  # 已经找到终点了
                        return 1
                    self.map2d[neighbour_id][2] = new_g  # 首先更新g值
                    self._insert(neighbour_id)  # 再根据f值大小排序插入
                else:
                    if new_g < self.map2d[neighbour_id][2]:  # 更小的g值
                        self.map2d[neighbour_id][5] = node_id  # 更新其父亲
                        self.map2d[neighbour_id][2] = new_g  # 必须更新g值
                        # self._delate(neighbour_id)    # 已经处理过了，不重复添加
                        self._insert(neighbour_id)  # 先删后插，以保持排序
                    else:
                        continue  # 父亲、g值不必改变

        # if node_id in self.open_list:
        # self._insert(node_id)
        self._delate(node_id)
        self.close_list.append(node_id)

        return 0

    # 获得最短路径
    def searching(self):
        path = []
        if not self.can_search:
            return path

        if self.map2d[self.end][4] != self.impasse:  # 判断寻路终点是否是障碍
            # 2.主循环逻辑
            while True:
                if not self.open_list:
                    print('山重水复疑无路')
                    break

                if self.deal_neighbours(self.open_list[0]):  # 找到终点了
                    son_id = self.end
                    while True:
                        if son_id != self.start:
                            path.append(son_id)
                            son_id = self.map2d[son_id][5]  # 找父亲
                        else:
                            path.append(son_id)
                            return list(reversed(path))
        else:
            print('世上只有套路，本没有路')

        self.can_search = False
        return path

    def get_path(self, board, coord_start=[0, 0], coord_end=[11, 4]):
        s = self.coord2sid(coord_start)
        e = self.coord2sid(coord_end)

        self.init_map2d(board, s, e)

        path = []
        for each in self.searching():
            path.append(self.sid2coord(each))

        return path

    # def get_min_node(self):
    #     if not self.open_list:
    #         return None
    #
    #     node = self.open_list[0]
    #     for each in self.open_list:
    #         f = self._get_f(each)
    #         print(f)
    #         if self._get_f(node) > f:  # 等于时怎么办？
    #             node = each
    #     print(self._get_f(node))
    #     return node


# 军棋（陆战棋）
class LandBattleChess(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LandBattleChess, self).__init__(parent)
        # region ui 参数及设置
        self.parent = parent
        self.setFixedSize(700, 980)
        self.move(600, 20)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)  # 无边框

        self.margin = 20
        self.border = 3  # 框线宽度
        self.space_w = 40  # 棋子间隔
        self.space_h = 15
        self.front = 60  # 楚河汉街
        self.chess_w = round((self.width() - 2 * self.margin - 4 * self.space_w) / 5)
        self.chess_h = round((self.height() - 2 * self.margin - 11 * self.space_h - self.front) / 12)
        self.half_w, self.half_h = round(self.chess_w / 2), round(self.chess_h / 2)
        self.line_w = self.width() - 2 * self.margin - self.chess_w  # 铁路横线段的长度
        self.line_h = self.height() - 2 * self.margin - self.chess_h  # 铁路纵线段的长度

        self.toolbar = MyToolbar(self)
        file_name = os.path.split(__file__)[-1].split(".")[0]  # 当前文件名称
        self.log = MyLog(log_file=f'{file_name}.txt', log_tags="")
        # endregion

        # region 游戏参数及设置
        self.aStar = AStarRoute()  # 计算最短路径算法
        # 棋盘地图："兵站类型、九宫邻居列表、棋子控件"
        self.board = [[[1, None, None] for _ in range(5)] for _ in range(12)]
        self.railway = [[1, 0], [1, 1], [1, 2], [1, 3], [1, 4],
                        [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [7, 4], [8, 4], [9, 4], [10, 4],
                        [10, 3], [10, 2], [10, 1], [10, 0],
                        [9, 0], [8, 0], [7, 0], [6, 0], [5, 0], [4, 0], [3, 0], [2, 0],
                        [5, 1], [5, 2], [5, 3], [6, 1], [6, 2], [6, 3]]  # 所有32个铁路站点
        self.setting = BitMark(16)  # 设置区的属性标志位

        self.bastion = []  # 双方的堡垒
        self.dark_room = []  # 暗牌坐标列表
        self.seen_card = []  # 显牌，按顺序加入
        self.lot = 0  # 手数
        self.enemies = [[], []]  # 可攻击的敌手棋子集合，击杀或同归于尽

        self.tmp = None  # 临时位置，按下时画临时的蓝框用
        self.last = None  # 最终落下的棋子位置，棋子红框用，或翻牌的棋子位置
        self.selected = None  # 鼠标选中的我方棋子
        self.rect_blue = None  # 窗口蓝框
        self.rect_red = []  # 窗口红框,可能两个
        # endregion

        self._init_board()

    # region 数据的初始化及界面区
    def _init_board(self):
        # region 站点的属性设置

        # 1:铁路兵站32个，一步多站 2:公路兵站14个，一步一站
        # 3:行营10个 4:大本营4个 0:界外无效

        # 32个铁路兵站，默认都是 1  Railway station

        # 14个公路兵站  depot  Highway station
        self.board[0][0][0] = 2
        self.board[0][2][0] = 2
        self.board[0][4][0] = 2
        self.board[2][2][0] = 2
        self.board[3][1][0] = 2
        self.board[3][3][0] = 2
        self.board[4][2][0] = 2
        self.board[7][2][0] = 2
        self.board[8][1][0] = 2
        self.board[8][3][0] = 2
        self.board[9][2][0] = 2
        self.board[11][0][0] = 2
        self.board[11][2][0] = 2
        self.board[11][4][0] = 2
        # 10个行营 Line camp
        self.board[2][1][0] = 3
        self.board[2][3][0] = 3
        self.board[3][2][0] = 3
        self.board[4][1][0] = 3
        self.board[4][3][0] = 3
        self.board[7][1][0] = 3
        self.board[7][3][0] = 3
        self.board[8][2][0] = 3
        self.board[9][1][0] = 3
        self.board[9][3][0] = 3
        # 4个大本营 base camp
        self.board[0][1][0] = 4
        self.board[0][3][0] = 4
        self.board[11][1][0] = 4
        self.board[11][3][0] = 4
        # self.log.debug('地图站点属性设置后', self.board)
        # endregion

        self._init_neighbours()

        # region 系统设置
        self.setting[0] = 1  # 玩家先手，0 ai先手   me_first = False
        self.setting[1] = 1  # 大本营不吃子  base_camp = False
        self.setting[2] = 1  # 玩家阵营  0是红方,1是蓝方
        self.setting[3] = 1  # 移动动画

        self.setting[8] = 0  # 已经开局
        # endregion

        # self.enemies[0].clear()
        # self._find_route(1, 0)
        # self.log.debug('route:', self.enemies[0])

        # railway = [[1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [2, 0], [2, 4],
        #            [3, 0], [3, 4], [4, 0], [4, 4], [5, 0], [5, 1], [5, 2],
        #            [5, 3], [5, 4], [6, 0], [6, 1], [6, 2], [6, 3], [6, 4],
        #            [7, 0], [7, 4], [8, 0], [8, 4], [9, 0], [9, 4],
        #            [10, 0], [10, 1], [10, 2], [10, 3], [10, 4]]
        # for each in railway:
        #     self._search_route(each[0], each[1])

        self.replay()

    def _init_neighbours(self):
        """ 连通图设置，各点的邻居设置。"""

        # tmp = []  # 所有铁路站点的合集
        neighbours = []

        for row in range(12):
            for col in range(5):
                # if self.board[row][col][0] == 1:  # 铁路站点
                #     tmp.append([row, col])

                neighbours.clear()
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if self._invalid_coord([row + i, col + j]):  # 界外
                            continue
                        if i == 0 and j == 0:  # 自己
                            continue
                        # 本身不是行营，对角也不是行营
                        if self.board[row][col][0] != 3 and i * j != 0 and \
                                self.board[row + i][col + j][0] != 3:
                            continue

                        neighbours.append([row + i, col + j])

                # 复合类型一定要用深拷贝，否则都是一个数据
                self.board[row][col][1] = copy.deepcopy(neighbours)

        # 中间四个铁路站点要断开一路
        self.board[5][1][1].pop(self.board[5][1][1].index([6, 1]))
        self.board[5][3][1].pop(self.board[5][3][1].index([6, 3]))
        self.board[6][1][1].pop(self.board[6][1][1].index([5, 1]))
        self.board[6][3][1].pop(self.board[6][3][1].index([5, 3]))
        # self.log.debug(f'地图：{len(self.board[2][3][1])}个', self.board[2][3][1])

    def _clear(self):
        # region 游戏数据清零
        for r in range(12):
            for c in range(5):
                if self.board[r][c][2]:  # 清理棋子控件
                    self.board[r][c][2].delete()
                self.board[r][c][2] = None

        # region 小黑屋/暗牌初始化，翻棋时的mark
        self.dark_room = [i for i in range(60)]  # 小黑屋去掉行营位置，其他位置放棋子
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

        self.seen_card.clear()
        self.bastion = ['红雷', '红雷', '红雷', '红旗', '蓝雷', '蓝雷', '蓝雷', '蓝旗']

        self.lot = 0
        self.selected = None
        self.last = None
        self.tmp = None
        self.rect_blue = None  # 窗口蓝框
        self.rect_red = []  # 窗口红框,可能两个

        self.setting[8] = 0  # 尚未开始。

    def _draw_sites(self, qp: QtGui.QPainter):
        # 绘制棋盘底图

        off = 26
        for j in range(12):
            for i in range(5):
                qp.setPen(QtGui.QPen(QtGui.QColor(55, 55, 55), 2, QtCore.Qt.SolidLine))

                x = self.margin + self.half_w + i * (self.chess_w + self.space_w)
                y = self.margin + self.half_h + j * (self.chess_h + self.space_h)
                y = y if j < 6 else y + self.front

                if self.board[j][i][0] < 3:  # 兵站
                    rect = QtCore.QRect(x - off, y - off // 2, off * 2, off)
                    qp.setBrush(QtGui.QBrush(QtGui.QColor(0, 155, 0)))
                    qp.drawRect(rect)
                    dx, dy = off - 8, off // 2 - 8
                    rect = QtCore.QRect(x - dx, y - dy, 2 * dx, 2 * dy)
                    if self.board[j][i][0] == 1:  # 铁路兵站
                        qp.setBrush(QtGui.QBrush(QtCore.Qt.darkGray))
                    else:  # 公路兵站
                        qp.setBrush(QtGui.QBrush(QtCore.Qt.gray))
                    qp.drawRect(rect)

                elif self.board[j][i][0] == 3:  # 行营
                    off1 = off - 5
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
        # 铁路
        qp.setPen(pen)
        pts = [QtCore.QPoint(self.margin + self.half_w,
                             self.margin + self.half_h + self.chess_h + self.space_h),
               QtCore.QPoint(self.margin + self.half_w + self.line_w,
                             self.margin + self.half_h + self.chess_h + self.space_h),
               QtCore.QPoint(self.margin + self.half_w + self.line_w,
                             self.margin + self.half_h + self.front + 10 * (self.chess_h + self.space_h)),
               QtCore.QPoint(self.margin + self.half_w,
                             self.margin + self.half_h + self.front + 10 * (self.chess_h + self.space_h)),
               QtCore.QPoint(self.margin + self.half_w,
                             self.margin + self.half_h + self.chess_h + self.space_h)]
        qp.drawPolyline(QtGui.QPolygon(pts))

        qp.drawLine(self.margin + self.half_w,
                    self.margin + self.half_h + 5 * (self.chess_h + self.space_h),
                    self.margin + self.half_w + self.line_w,
                    self.margin + self.half_h + 5 * (self.chess_h + self.space_h))
        qp.drawLine(self.margin + self.half_w,
                    self.margin + self.half_h + self.front + 6 * (self.chess_h + self.space_h),
                    self.margin + self.half_w + self.line_w,
                    self.margin + self.half_h + self.front + 6 * (self.chess_h + self.space_h))
        qp.drawLine(self.margin + self.half_w + 2 * (self.chess_w + self.space_w),
                    self.margin + self.half_h + 5 * (self.chess_h + self.space_h),
                    self.margin + self.half_w + 2 * (self.chess_w + self.space_w),
                    self.margin + self.half_h + self.front + 6 * (self.chess_h + self.space_h))

    def _draw_box(self, qp: QtGui.QPainter):
        # 在空的兵站上画蓝框或者红框，置零就是擦除蓝红框
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

        for each in self.rect_red:
            qp.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), w_line, QtCore.Qt.SolidLine))
            qp.setBrush(QtGui.QBrush())  # 空画刷，就是透明
            qp.drawRoundedRect(each, 5.0, 5.0)

    def _flush_box(self, coord_last=None, coord_shadow=None, coord_blue=None):
        """ 红框易位(可选)，附近红框也可以设置；蓝框消失(必然)
        @param coord_last: 新红框的坐标
        @param coord_shadow: 红框的附框坐标，也就是 start，自动擦除旧的，有没有新框看赋值
        @param coord_blue: 新蓝框的位置
        """

        # region 处理蓝框
        # print('旧蓝框:', self.selected, '    红框:', self.last, '    新蓝框:', coord_blue)
        if self.selected:  # 首先无条件擦除旧蓝框并归零
            chess = self.board[self.selected[0]][self.selected[1]][2]
            if chess:
                if self.selected == self.last:  # 机器翻出我方棋子又被选中,需要恢复红框
                    chess.update_me()  # 默认红框
                else:
                    chess.update_me(None, 0)  # 清除蓝框
        self.selected = None

        if coord_blue:  # 需要则画上新蓝框
            chess = self.board[coord_blue[0]][coord_blue[1]][2]
            if chess:
                chess.update_me(style_fm=4)  # 蓝框

            self.selected = copy.deepcopy(coord_blue)
        # endregion

        if coord_last:
            self.rect_red.clear()

            # region 处理影子红框
            if coord_shadow:  # 新位置画红框，替代了旧的附框
                x, y = self.get_pos(coord_shadow)
                self.rect_red.append(QtCore.QRect(x + 3, y + 3, self.chess_w - 3, self.chess_h - 3))
            else:  # 翻棋时则不需要影子，旧的附框自动被清除
                ...  # 清除窗口红框

            self.update()  # start位置也画红框
            # endregion

            if self.last:  # 擦除过时红框
                chess = self.board[self.last[0]][self.last[1]][2]
                if chess:  # 有棋子，说明是移动棋子
                    chess.update_me(style_fm=0)
                else:  # 说明前面双方同归于尽了，没有棋子了，则窗口里自动擦除：rect——red清零即可以
                    ...

            chess = self.board[coord_last[0]][coord_last[1]][2]  # 迎接新红框
            if chess:
                chess.update_me(coord_last)  # 红框并更新，一定要更新
            else:  # 没有棋子说明双方也同归于尽了，则窗口里画框
                x, y = self.get_pos(coord_last)
                self.rect_red.append(QtCore.QRect(x + 3, y + 3, self.chess_w - 3, self.chess_h - 3))

            self.last = copy.deepcopy(coord_last)  # 换位

    # endregion

    # region 消息槽区

    def paintEvent(self, e: QtGui.QPaintEvent) -> None:
        qp = QtGui.QPainter()
        qp.begin(self)

        qp.setRenderHint(QtGui.QPainter.Antialiasing)  # 抗锯齿
        qp.drawPixmap(0, 0, QtGui.QPixmap("E:/Codes/res/background/background2.jpg"))

        # region 纵横线
        qp.setPen(QtGui.QPen(QtGui.QColor(50, 50, 50), 2, QtCore.Qt.SolidLine))
        for j in range(12):
            x = self.margin + self.half_w
            y = self.margin + self.half_h + j * (self.chess_h + self.space_h)
            y = y if j < 6 else y + self.front
            qp.drawLine(x, y, x + self.line_w, y)

        for i in range(0, 5, 2):
            x = self.margin + self.half_w + i * (self.chess_w + self.space_w)
            y = self.margin + self.half_h
            qp.drawLine(x, y, x, y + self.line_h)

        for i in range(1, 5, 2):
            x = self.margin + self.half_w + i * (self.chess_w + self.space_w)
            y = self.margin + self.half_h
            qp.drawLine(x, y, x, y + 5 * (self.chess_h + self.space_h))
            qp.drawLine(x, y + self.front + 6 * (self.chess_h + self.space_h), x, y + self.line_h)
        # endregion

        # region 斜线
        qp.drawLine(self.margin + self.half_w,
                    self.margin + self.half_h + self.chess_h + self.space_h,
                    self.margin + self.half_w + self.line_w,
                    self.margin + self.half_h + 5 * (self.chess_h + self.space_h))
        qp.drawLine(self.margin + self.half_w + self.line_w, self.margin + self.half_h + self.chess_h + self.space_h,
                    self.margin + self.half_w, self.margin + self.half_h + 5 * (self.chess_h + self.space_h))

        pts = [QtCore.QPoint(self.margin + self.half_w + 2 * (self.chess_w + self.space_w),
                             self.margin + self.chess_h + self.space_h + self.half_h),
               QtCore.QPoint(self.margin + self.half_w + self.line_w,
                             self.margin + 3 * (self.chess_h + self.space_h) + self.half_h),

               QtCore.QPoint(self.margin + self.half_w + 2 * (self.chess_w + self.space_w),
                             self.margin + 5 * (self.chess_h + self.space_h) + self.half_h),
               QtCore.QPoint(self.margin + self.half_w,
                             self.margin + 3 * (self.chess_h + self.space_h) + self.half_h),
               QtCore.QPoint(self.margin + self.half_w + 2 * (self.chess_w + self.space_w),
                             self.margin + self.chess_h + self.space_h + self.half_h)]
        qp.drawPolyline(QtGui.QPolygon(pts))

        qp.drawLine(self.margin + self.half_w,
                    self.margin + self.half_h + self.front + 6 * (self.chess_h + self.space_h),
                    self.margin + self.half_w + self.line_w,
                    self.margin + self.half_h + self.front + 10 * (self.chess_h + self.space_h))
        qp.drawLine(self.margin + self.half_w + self.line_w,
                    self.margin + self.half_h + self.front + 6 * (self.chess_h + self.space_h),
                    self.margin + self.half_w,
                    self.margin + self.half_h + self.front + 10 * (self.chess_h + self.space_h))

        pts = [QtCore.QPoint(self.margin + self.half_w + 2 * (self.chess_w + self.space_w),
                             self.margin + self.half_h + self.front + 6 * (self.chess_h + self.space_h)),
               QtCore.QPoint(self.margin + self.half_w + self.line_w,
                             self.margin + self.half_h + self.front + 8 * (self.chess_h + self.space_h)),
               QtCore.QPoint(self.margin + self.half_w + 2 * (self.chess_w + self.space_w),
                             self.margin + self.half_h + self.front + 10 * (self.chess_h + self.space_h)),
               QtCore.QPoint(self.margin + self.half_w,
                             self.margin + self.half_h + self.front + 8 * (self.chess_h + self.space_h)),
               QtCore.QPoint(self.margin + self.half_w + 2 * (self.chess_w + self.space_w),
                             self.margin + self.half_h + self.front + 6 * (self.chess_h + self.space_h))]
        qp.drawPolyline(QtGui.QPolygon(pts))
        # endregion

        # 铁路
        self._draw_railway(qp, QtGui.QPen(QtGui.QColor(50, 50, 50), 12, QtCore.Qt.SolidLine))
        self._draw_railway(qp, QtGui.QPen(QtGui.QColor(255, 255, 255), 5, QtCore.Qt.DotLine))

        self._draw_sites(qp)  # 棋子位置
        self._draw_box(qp)  # 画蓝红框

        # region 测试
        # # self.log.debug(self.enemies)
        # qp.setPen(QtGui.QPen(QtGui.QColor(50, 50, 250), 5, QtCore.Qt.DotLine))
        # pts = []
        #
        # # p = QtCore.QPoint(self.margin + half_w, self.margin + half_h+self.chess_h + self.space_h)
        # # pts.append(p)
        #
        # for each in self.enemies[0][:]:
        #     x = self.margin + self.half_w + each[1] * (self.chess_w + self.space_w)
        #     y = self.margin + self.half_h + each[0] * (self.chess_h + self.space_h) if each[0] < 6 else \
        #         self.margin + self.half_h + self.front + each[0] * (self.chess_h + self.space_h)
        #     pts.append(QtCore.QPoint(x, y))
        # # pts.append(p)
        # qp.drawPolyline(QtGui.QPolygon(pts))
        # endregion

        qp.end()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super(LandBattleChess, self).resizeEvent(a0)

        # pb.setObjectName('测试')
        # pb.setStyleSheet(f'{self.qss_pb[0]}{self.qss_pb[1]}')
        # pb.move(40, 50)

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        """ 仅显示蓝框，有棋子则棋子刷蓝框，空位则父窗口刷蓝框
        @param e:
        @return:
        """

        ret = self.get_coord(e.pos())
        if ret is None:
            return

        row, col, dx, dy = ret

        chess_hit = self.board[row][col][2]
        if not chess_hit:  # 点击了无棋子的兵站或兵营
            self.rect_blue = QtCore.QRect(dx + 3, dy + 3, self.chess_w - 3, self.chess_h - 3)
            self.update()
        else:
            self.tmp = [row, col]
            _, coord, hidden, _ = chess_hit.get_info()
            # print(coord, row, col, hidden)

            chess_hit.update_me(None, 4, hidden)  # 蓝框

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        # 逻辑：两套系统last-prev, start-end
        # 点中棋子则——自己棋子，当成start，标蓝，无其他动作;如果暗棋，则当做Last和prev
        #         ——对方棋子，当成end，先路径检测，再战斗检测，最后可能移动
        # 点中空白则移动自己棋子，当成end，先路径检测，再移动

        # region 各个方框的显示与擦除
        self.rect_blue = None  # 清除蓝框
        self.update()

        if self.tmp:  # 先无条件擦除蓝框
            chess = self.board[self.tmp[0]][self.tmp[1]][2]
            _, coord, hidden, _ = chess.get_info()
            chess.update_me(None, 0, hidden)  # 擦除蓝框
            self.tmp = None

        if self.last:  # 无条件显示红框
            chess = self.board[self.last[0]][self.last[1]][2]
            if chess:
                chess.update_me()  # 红框，采用默认值即可

        # endregion

        ret = self.get_coord(e.pos())
        if ret is None:
            return

        # region 处理有效点击事件
        row, col, dx, dy = ret
        node_cur = self.board[row][col]  # 当前站点数据
        coord_cur = [row, col]  # 当前站点坐标

        # 点击了空白位置，还要判断当前棋子能否移动到这个位置
        if node_cur[2] is None:
            if not self.selected:  # 没有选中棋子，不能移动到空白处
                return

            node_sel = self.board[self.selected[0]][self.selected[1]]
            path = self.search_way(self.selected, coord_cur)  # 判断上次选中棋子能否移动到当前位置
            # self.log.debug(self.selected, coord_cur, path)

            # 路径不通，选中棋子不能移动到当前位置处，或者选中的是地雷、军旗，也不能移动
            if not path or node_sel[2].get_info()[3] in ['地雷', '军旗']:
                self._flush_box()
                return  # 需要重新选中棋子

            # 能移动
            else:
                self.move_chess(self.selected, coord_cur, path, 2)  # 则首先移动选中的棋子

        # 点中了棋子
        else:
            info_cur = node_cur[2].get_info()

            # 第一次点暗棋，如机器先手，则不会执行到这步
            if self.last is None:
                self.last = coord_cur  # coord
                self.setting[2] = info_cur[0] // 12  # 选择玩家阵营

                node_cur[2].update_me()  # 红框，采用默认值即可
                # print("我是蓝方" if self.me else '我是红方')
                self.dark_room.pop(self.dark_room.index(row * 5 + col))  # 明牌弹出小黑屋
                self.mark_locus(coord_cur)
                self.call_ai()  # 呼叫 AI 走棋

            # 暗棋需要翻转
            elif info_cur[2]:
                if self.selected:  # 属于误操作，无效
                    self._flush_box()  # 红蓝框
                    return

                self._flush_box(coord_cur)  # 红蓝框
                # 明牌弹出小黑屋
                self.dark_room.pop(self.dark_room.index(self.aStar.coord2sid(coord_cur)))
                self.mark_locus(coord_cur)
                self.call_ai()  # 呼叫 AI 走棋

            # 点击的棋子是玩家的
            elif info_cur[0] // 12 == self.setting[2]:
                # print(f'点击了我方{rank}', coord, [row, col])
                if coord_cur == self.selected:  # 实现选中与取消的切换，蓝框的间隔出现
                    self._flush_box()
                else:
                    self._flush_box(coord_blue=coord_cur)  # 当前点击一定是蓝的，清除过时蓝框

            # 判断能否吃掉对方棋子
            else:
                if not self.selected:
                    return

                path = self.search_way(self.selected, coord_cur)
                # 路径不通，不能战斗；或者战斗出现异常，则忽略操作，并清除当前项
                if not path or not self.strike_foes(self.selected, coord_cur, path):
                    self._flush_box()

        # endregion

    def slot_pb_clicked(self, ctl):
        """
        工具栏命令
        @param ctl:
        """
        text = ctl.text()
        # print(text)
        if text == '新局':
            print('不能的')
            self.replay()

        elif text == '悔棋':
            # self.log.debug('手数:', self.lot, len(self.seen_card), self.seen_card)
            if self.lot > 0:
                locus_ai = self.seen_card.pop()
                locus_me = self.seen_card.pop()
                self.lot -= 2

                self.last = None
                self.rect_red.clear()
                # self.log.debug(locus_me, locus_ai)

                # 处理 AI 的棋
                if len(locus_ai) == 1:  # 翻出的棋子
                    chess = self.board[locus_ai[0][0]][locus_ai[0][1]][2]
                    if chess:
                        chess.update_me(None, 0, True)  # 隐藏去框
                        self.dark_room.append(self.aStar.coord2sid(locus_ai[0]))  # 重新打入黑屋
                    # self.log.debug(chess._rank)
                else:  # 移动或战斗的两个棋子
                    ...

                # 处理我的棋
                if len(locus_me) == 1:
                    chess = self.board[locus_me[0][0]][locus_me[0][1]][2]
                    if chess:
                        chess.update_me(None, -1, True)  # 隐藏去框
                        self.dark_room.append(self.aStar.coord2sid(locus_me[0]))  # 重新打入黑屋
                else:
                    ...
                    # chess_a = self.board[locus_me[0][0]][locus_me[0][1]][2]
                    # chess_d = self.board[locus_me[1][0]][locus_me[1][1]][2]
                    # # 复位
                    # # if chess_a and not chess_d
                    # chess_a.update_me(None, 0, True)  # 隐藏去框
                    # chess_d.update_me(None, 0, True)  # 隐藏去框
                    #
                    # coord_a = locus_me[0]
                    # coord_d = locus_me[1]
                    # self._flush_box(coord_a, coord_d)

                if self.lot > 0:
                    locus = self.seen_card[-1]
                    # self.log.debug(locus)
                    if len(locus) == 1:
                        self._flush_box(locus[0])
                    else:
                        self._flush_box(locus[0], locus[1])
                # else:
                #     self.last = None

        else:
            self.close()

    def slot_move_win(self, pos):
        """
        拖曳工具栏可以移动主窗体
        @param pos:
        """
        self.move(self.pos() + pos)

    def __str__(self):
        """
        打印对象时的输出
        @return:
        """
        return '翻棋 Flip chess 玩法。'

    __repr__ = __str__

    # endregion

    # region 业务逻辑区
    # 新局开始，随机布子
    def replay(self):
        self._clear()  # 游戏数据清零

        # region 游戏数据初始化

        # region 军队初始化
        army = Chess.army_building()
        random.shuffle(army)
        # print(len(army), army)
        # endregion

        # 把士兵安放到棋盘地图上
        for each in self.dark_room:
            row = each // 5
            col = each % 5
            # print(each, row, col)

            self.board[row][col][2] = Chess(self, army.pop(), [row, col])  # 棋局的棋子分布图

            x = self.margin + col * (self.chess_w + self.space_w)
            y = self.margin + row * (self.chess_h + self.space_h)
            if row >= 6:
                y += self.front

            self.board[row][col][2].setGeometry(x, y, self.chess_w, self.chess_h)
            self.board[row][col][2].show()

        # self.log.debug('棋子分布完毕', self.board)

        self.setting[8] = True

        # endregion

        # region 开始游戏
        if not self.setting[0]:  # 机器先手
            last = self._ai_open_chess()
            if last:
                # print(last)
                chess = self.board[last[0]][last[1]][2]
                chess.update_me()  # 红框，采用默认值即可
                info = chess.get_info()
                self.setting[2] = 1 - info[0] // 12  # 选择玩家阵营
                print("AI是红方" if self.setting[2] else 'AI是蓝方')
        # endregion

        # while True:
        #     self._AI_open_chess()

    def mark_locus(self, *args) -> None:
        """
        记录轨迹，方便悔棋
        @param args: 包含一个或两个棋子坐标，要么翻牌的，要么移动的
        """

        self.seen_card.append(list(args))
        self.lot += 1
        # self.log.debug(args, type(args), self.seen_card)

    # 轮到 AI 下棋
    def call_ai(self):
        # 电脑走起
        self._ai_open_chess()  # AI翻棋
        # 吃棋

    def _ai_open_chess(self):
        # AI 翻棋
        if self.dark_room:  # 还有暗棋，可以翻开
            index = Utils.rand_int(0, len(self.dark_room) - 1)
            # 明牌弹出小黑屋，切换到当前翻出的位置
            coord_cur = self.aStar.sid2coord(self.dark_room.pop(index))
            # print(self.last, index, self.dark_room)
            self._flush_box(coord_cur)
            self.mark_locus(coord_cur)

    def victory(self):
        if '红旗' not in self.bastion:
            print("红方军旗被夺，蓝方胜！")
        elif '蓝旗' not in self.bastion:
            print("蓝方军旗被夺，红方胜！")
        else:
            ...

    # 行列号的合法性
    @staticmethod
    def _invalid_coord(coord: list = None) -> bool:
        """
        行列号的越界判断
        @param coord: 行列号
        @return:
        """
        # 坐标有效性判断
        return False if coord and 0 <= coord[0] < 12 and 0 <= coord[1] < 5 else True

    # 屏幕位置转换成 行列号
    def get_coord(self, pos):
        """
        屏幕位置转换成 行列号
        获得鼠标点击处的行列号和棋子的左上角屏幕位置
        @param pos:
        @return: 行列号，棋子左上角 x，y
        """

        x, y = pos.x(), pos.y()
        y = y if y < (self.height() - self.front) // 2 else y - self.front  # 下半区

        row = (y - self.margin + self.space_h // 2) // (self.chess_h + self.space_h)
        col = (x - self.margin + self.space_w // 2) // (self.chess_w + self.space_w)

        dx = self.margin + col * (self.chess_w + self.space_w)  # 棋子的左边界
        dy = self.margin + row * (self.chess_h + self.space_h)  # 棋子的上边界

        # print('鼠标点击了 in', row, col)
        if dx <= x <= dx + self.chess_w and dy <= y <= dy + self.chess_h:  # 点击在棋子范围内了
            dy = dy if row < 6 else dy + self.front
            return row, col, dx, dy
        else:
            return None

    # 获得棋子左上角的屏幕坐标
    def get_pos(self, coord: list) -> list:
        """
        把行列号转换成棋子左上角的屏幕坐标
        @param coord: 行列号列表
        @return: x,y 左上角
        """
        # if self._invalid_coord(coord):
        #     return None

        x = self.margin + coord[1] * (self.chess_w + self.space_w)  # 棋子的左边界
        y = self.margin + coord[0] * (self.chess_h + self.space_h)  # 棋子的上边界
        # x = self.margin + self.half_w + coord[1] * (self.chess_w + self.space_w) # 棋子中心x
        # y = self.margin + self.half_h + coord[0] * (self.chess_h + self.space_h) # 棋子中心y

        y = y if coord[0] < 6 else y + self.front

        return x, y

    # 获得铁路上的通行性
    def _search_railway(self, coord_attacker, coord_defender):
        """
        铁路兵站上的可通行性
        @param coord_attacker: 进攻方行列号
        @param coord_defender: 防守方行列号
        @return: path,通行路径上的所有兵站，不通为空
        """

        if self._invalid_coord(coord_attacker) or \
                self._invalid_coord(coord_defender) or \
                coord_attacker == coord_defender:
            return []

        node_a = self.board[coord_attacker[0]][coord_attacker[1]]
        node_d = self.board[coord_defender[0]][coord_defender[1]]

        if not node_a[2] or node_a[0] != 1:  # 没有棋子 or 非铁路兵站
            return []

        # 邻居关系已经在父函数里处理过了，这里不会出现
        if node_d[0] == 1 and coord_defender in node_a[1]:
            return [coord_attacker, coord_defender]  # 直接是铁路上的好邻居

        if node_a[2].get_info()[-1] == '工兵':  # 满铁路可走，所有铁路兵站
            path = self.aStar.get_path(self.board, coord_attacker, coord_defender)
            self.log.debug('工兵的铁路最短路径:', path)
            return path

        else:  # 不是工兵，不能拐弯
            # 在铁路上的8个拐角点上，则横竖都是通行的路
            # if coord_attacker in [[1, 0], [1, 4], [5, 0], [5, 4], [6, 0], [6, 4], [10, 0], [10, 4]]:
            row_a, row_d = coord_attacker[0], coord_defender[0]
            col_a, col_d = coord_attacker[1], coord_defender[1]
            path = [coord_attacker]

            if row_a == row_d:  # 同在横线上
                step = 1 if row_d - row_a > 0 else -1
                for i in range(row_a + step, row_d, step):  # 因为肯定不是邻居，差肯定大于1
                    if self.board[row_a][i][2]:  # 有棋子，不通行
                        return []
                    else:
                        path.append([row_a, i])

                path.append(coord_defender)
                return path  # 两兵站之间没有棋子，可以直达

            elif col_a == col_d:  # 同在纵线上
                step = 1 if col_d - col_a > 0 else -1
                for i in range(col_a + step, col_d, step):  # 因为肯定不是邻居，差肯定大于1
                    if self.board[i][col_a][2]:  # 有棋子，不通行
                        return []
                    else:
                        path.append([i, col_a])

                path.append(coord_defender)
                return path  # 两兵站之间没有棋子，可以直达

            else:  # 防守方肯定不在铁路线上
                return []

            # for i in range(5):
            #     if i != col:  # 本身除外
            #         self.enemies[1].append([row, i])  # 横线都加上
            #
            # if col == 2:  # 中间2站点
            #     r = 5 if row == 6 else 6
            #     self.enemies[1].append([r, 2])  # 竖线仅一点要加上
            # else:  # 边线上的点
            #     for i in range(1, 11):
            #         if i != row:  # 本身除外
            #             self.enemies[1].append([i, col])  # 竖线点都要加上

        # else:  # 要么横向要么竖向
        #     for each in neighbours:
        #         st, nb, _ = self.board[each[0]][each[1]]
        #         if st != 1:  # 不是铁路邻居
        #             continue
        #         if each[0] == row:  # 横向铁路线上搜索
        #             for i in range(5):
        #                 if i != col:  # 本身除外
        #                     self.enemies[1].append([row, i])
        #         else:  # 纵向铁路线上搜索
        #             for i in range(1, 11):
        #                 if i != row:  # 本身除外
        #                     self.enemies[1].append([i, col])
        #         break
        #
        #     return True if coord_attacker in [[5, 2], [6, 2]] and \
        #                    coord_defender in [[5, 2], [6, 2]] \
        #         else False  # 中间两兵站，互为邻居，额外加上一个

        # self.log.debug(f'站点 ：{coord_attacker}')

    # 先路径检测，再战斗检测，最后可能移动
    # 纯粹的路径连通性，含有棋子障碍物的情况
    def search_way(self, coord_start, coord_end):
        """
        纯粹的路径连通性检测，不涉及棋子判断
        @param coord_start:
        @param coord_end:
        @return: 路径点的列表，空列表代表不连通
        """

        path = []
        if self._invalid_coord(coord_start) or self._invalid_coord(coord_end):
            # self.log.debug('坐标不合法')
            return path

        style, neighbours, _ = self.board[coord_start[0]][coord_start[1]]  # 进攻方棋子或选中的棋子

        # 通达性检核
        if coord_end in neighbours:  # 首先都在邻居里搜寻，不在则不可通达，返回
            path.extend([coord_start, coord_end])
        else:
            # self.log.debug('不是邻居关系。', coord_start, coord_end, neighbours)
            if style == 1:  # 如果是铁路兵站，扩展的通达性
                path.extend(self._search_railway(coord_start, coord_end))
                # path = self.aStar.get_path(self.board, coord_start, coord_end)
                # self.log.debug('铁路路径:', path)

        return path

    # 裁判   =0：同归于尽  <0：失败  >0：胜利 -2-3-4:异常
    def judge(self, id_attacker: int, id_defender: int) -> int:
        """
            战斗胜负判断
            @param id_attacker: 攻击方棋子的 id
            @param id_defender: 防守方棋子的 id
            @return: 类型码 0：同归于尽  <0：失败  >0：胜利 -2-3-4:异常
            """
        if not 0 <= id_attacker < 24 or not 0 <= id_defender < 24:
            # self.log.debug('棋子id异常')
            return -3  # 异常

        if (id_attacker < 12 and id_defender < 12) or \
                (id_attacker > 11 and id_defender > 11):
            # self.log.debug('自家人火并')
            return -2  # 同伴

        ret = -4
        a = id_attacker % 12  # 进攻方
        d = id_defender % 12  # 防守方

        if a < 9 and d < 9:
            comp = d - a  # 越小军衔越大
            # self.log.debug(f'军衔差{comp}级')
            ret = 0 if comp == 0 else 1 if comp > 0 else -1

        if a is Chess.ORDER.index('军旗'):
            # self.log.debug('军旗不能进攻')
            return -1

        if d is Chess.ORDER.index('军旗'):  # 比炸弹优先，炸弹炸不了
            if a == Chess.ORDER.index('工兵'):
                if id_attacker < 12:
                    if '蓝雷' not in self.bastion:  # 蓝方地雷已光
                        self.bastion.pop(self.bastion.index('蓝旗'))  # 可以夺去蓝方军旗
                        ret = 1
                    else:
                        # self.log.debug('先排除蓝方所有地雷')
                        ret = -1
                else:
                    if '红雷' not in self.bastion:  # 红方地雷已光
                        self.bastion.pop(self.bastion.index('红旗'))  # 可以夺去蓝方军旗
                        ret = 1
                    else:
                        # self.log.debug('先排除红方所有地雷')
                        ret = -1
            else:
                # self.log.debug('只有工兵才能扛旗')
                ret = -1

        elif a == Chess.ORDER.index('炸弹') or d == Chess.ORDER.index('炸弹'):  # 比地雷优先
            ret = 0

        elif a is Chess.ORDER.index('地雷'):
            # self.log.debug('地雷不能进攻')
            return -1

        elif d is Chess.ORDER.index('地雷'):
            if a == Chess.ORDER.index('工兵'):
                if id_attacker < 12:  # red
                    self.bastion.pop(self.bastion.index('蓝雷'))  # 蓝方地雷 -1
                else:
                    self.bastion.pop(self.bastion.index('红雷'))  # 弹出红方地雷， -1
                ret = 1
            else:
                # self.log.debug('请用工兵排雷')
                ret = -1

        return ret

    # 搏斗
    def strike_foes(self, coord_attacker, coord_defender, path):
        """ 处理吃棋，必须是两个棋子
        @param path:
        @param coord_attacker:
        @param coord_defender:
        @return:
        """

        if self._invalid_coord(coord_attacker) or self._invalid_coord(coord_defender):
            # self.log.debug('坐标不合法')
            return False

        node_a = self.board[coord_attacker[0]][coord_attacker[1]]  # 进攻方棋子或选中的棋子
        node_d = self.board[coord_defender[0]][coord_defender[1]]  # 防守方棋子或前进的位置

        # 兵站必须有棋子
        if node_a[2] is None or node_d[2] is None:
            # self.log.debug('站上无人')
            return False

        # 对方在行营里，不可战斗，除非最后
        if node_d[0] == 3:
            # self.log.debug('对方在行营 line camp 里')
            return False

        # 对方在大本营里，且设置为不可战斗
        if node_d[0] == 4 and not self.setting[1]:
            # self.log.debug('敌人在大本营 base camp 里, 且不容许吃大本营里的子')
            return False

        # 可以搏斗了
        info_a = node_a[2].get_info()  # 棋子的信息
        info_d = node_d[2].get_info()

        result = self.judge(info_a[0], info_d[0])

        if result not in [-1, 0, 1]:
            return False

        # 打不动，按兵不动
        elif result == -1:
            # self.log.debug('打不动，罢兵。')
            return False

        self.move_chess(coord_attacker, coord_defender, path, result)  # 移动棋子

        return True

    def anti(self, coord_attacker, coord_defender, path, st):
        chess_a = self.board[coord_attacker[0]][coord_attacker[1]][2]  # 进攻方棋子或选中的棋子
        chess_d = self.board[coord_defender[0]][coord_defender[1]][2]  # 防守方棋子

        # 棋子移动动画
        if not chess_a or not path:
            # self.log.debug('无法动画移动')
            return
        if st != 2 and not chess_d:
            # self.log.debug('动画类型不匹配，无法动画移动')
            return

        # region 基本动画设置
        anim = QtCore.QPropertyAnimation(chess_a, b"pos", self)

        length = len(path)
        delay = 1 / length
        for i in range(length):
            xy = self.get_pos(path[i])
            pt = QtCore.QPoint(xy[0], xy[1])
            anim.setKeyValueAt(i * delay, pt)

        # anim.setStartValue(path[0])
        xy = self.get_pos(path[-1])
        anim.setEndValue(QtCore.QPoint(xy[0], xy[1]))
        anim.setDuration(250 * length)
        # anim.setLoopCount(3)
        # anim.setEasingCurve(QtCore.QEasingCurve.OutBounce)  # 设置动画的节奏 动画曲线/InQuad

        # endregion

        # region 后续动画

        # 移动到空位置后的动画
        if st == 2:
            anim.finished.connect(partial(self._anti_over, coord_attacker, coord_defender, st))  # 动画完成时
            # 参数 DeleteWhenStopped停止时动画将自动删除；KeepWhenStopped  停止时不会删除动画
            anim.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

        # 战而胜之后，按顺序播放一组动画
        elif st == 1:
            anim1 = QtCore.QPropertyAnimation(chess_d, b'pos', self)
            xy = self.get_pos(coord_defender)
            anim1.setStartValue(QtCore.QPoint(xy[0], xy[1]))
            xy = self.get_pos([coord_defender[0], -3]) if chess_d.get_info()[0] < 12 \
                else self.get_pos([coord_defender[0], 5])  # 左红右蓝
            # self.log.debug([coord_defender[0], -3], xy)
            anim1.setEndValue(QtCore.QPoint(xy[0], xy[1]))
            anim1.setDuration(1000)
            anim1.finished.connect(partial(self._anti_over, coord_attacker, coord_defender, st))  # 动画完成时

            anim_gp_s = QtCore.QSequentialAnimationGroup(
                self)  # 串行动画QSequentialAnimationGroup# 并行动画QParallelAnimationGroup
            anim_gp_s.addAnimation(anim)
            anim_gp_s.addAnimation(anim1)
            anim_gp_s.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

        # 同归于尽后，先顺序播放后同时播放
        elif st == 0:
            anim_gp_p = QtCore.QParallelAnimationGroup(self)  # 并行动画QParallelAnimationGroup
            anim.finished.connect(anim_gp_p.start)  # 动画完成时接下一段动画组

            anim1 = QtCore.QPropertyAnimation(chess_a, b'pos', self)  # 攻方消失
            xy = self.get_pos(coord_defender)
            anim1.setStartValue(QtCore.QPoint(xy[0], xy[1]))
            xy = self.get_pos([coord_defender[0], -3]) if chess_a.get_info()[0] < 12 \
                else self.get_pos([coord_defender[0], 5])  # 左红右蓝
            anim1.setEndValue(QtCore.QPoint(xy[0], xy[1]))
            anim1.setDuration(1000)
            # anim1.finished.connect(partial(self._anti_over, coord_attacker, coord_defender, st, False))  # 动画完成时

            anim2 = QtCore.QPropertyAnimation(chess_d, b'pos', self)  # 守方消失
            xy = self.get_pos(coord_defender)
            anim2.setStartValue(QtCore.QPoint(xy[0], xy[1]))
            xy = self.get_pos([coord_defender[0], -3]) if chess_d.get_info()[0] < 12 \
                else self.get_pos([coord_defender[0], 5])  # 左红右蓝
            anim2.setEndValue(QtCore.QPoint(xy[0], xy[1]))
            anim2.setDuration(1000)
            anim2.finished.connect(partial(self._anti_over, coord_attacker, coord_defender, st))  # 动画完成时

            anim_gp_p.addAnimation(anim1)
            anim_gp_p.addAnimation(anim2)
            anim_gp_p.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

        # endregion

    def _anti_over(self, coord_attacker, coord_defender, st):
        """
        动画结束的收尾，自动呼叫 ai
        @param coord_attacker:
        @param coord_defender:
        @param st:
        """

        # chess_a = self.board[coord_attacker[0]][coord_attacker[1]][2]
        # chess_d = self.board[coord_defender[0]][coord_defender[1]][2]

        if st > 0:  # 保留攻击方棋子
            # if st == 1:
            #     self.board[coord_defender[0]][coord_defender[1]][2].delete()

            chess = self.board[coord_attacker[0]][coord_attacker[1]][2]
            self.board[coord_defender[0]][coord_defender[1]][2] = chess
        else:  # 棋子都不留
            # self.board[coord_attacker[0]][coord_attacker[1]][2].delete()
            # self.board[coord_defender[0]][coord_defender[1]][2].delete()
            self.board[coord_defender[0]][coord_defender[1]][2] = None

        self.board[coord_attacker[0]][coord_attacker[1]][2] = None
        self._flush_box(coord_defender, coord_attacker)  # 棋子红框处理和坐标更新
        self.mark_locus(coord_attacker, coord_defender)
        self.call_ai()  # 呼叫 AI 走棋

    def move_chess(self, coord_attacker, coord_defender, path, st=0):
        """
            移动棋子，并删除相关棋子
            @param coord_attacker:
            @param coord_defender:
            @param path: 铁路移动路径
            @param st: 标志位 0：双亡，1：吃棋 2：移动
            @return:
        """

        if self._invalid_coord(coord_attacker) or self._invalid_coord(coord_defender):
            # self.log.debug('坐标不合法')
            return

        chess = self.board[coord_attacker[0]][coord_attacker[1]][2]  # 进攻方棋子或选中的棋子
        chess_d = self.board[coord_defender[0]][coord_defender[1]][2]  # 防守方棋子
        if not chess:
            # self.log.debug('进攻方无棋子')
            return

        if self.setting[3]:  # 动画移动棋子
            self.anti(coord_attacker, coord_defender, path, st)

        else:  # 无动画
            if st > 0:  # 直接移动棋子
                x, y = self.get_pos(coord_defender)
                chess.move(x, y)
                self.board[coord_defender[0]][coord_defender[1]][2] = chess

                if st == 1:  # 吃棋
                    chess_d.delete()  # 删除被吃的棋子

            else:  # 双亡
                # chess.delete()  # 删除进攻方棋子
                # chess_d.delete()  # 删除防守方棋子
                self.board[coord_defender[0]][coord_defender[1]][2] = None

            self.board[coord_attacker[0]][coord_attacker[1]][2] = None
            self._flush_box(coord_attacker, coord_defender)  # 棋子红框处理和坐标更新
            self.call_ai()  # 呼叫 AI 走棋

    # def _find_enemies(self, row, col):
    #     self.enemies[0].clear()
    #     st, neighbours, _ = self.board[row][col]
    #     if st != 1:  # 非铁路
    #         return
    #
    #     if [row, col] not in self.enemies[0]:
    #         self.enemies[0].append([row, col])
    #
    #     # self.lot += 1
    #     # print(st, self.lot)
    #     if not neighbours:
    #         return
    #
    #     for each in neighbours:
    #         st_n, nb, _ = self.board[each[0]][each[1]]
    #
    #         if st_n != 1:  # 不是铁路上的邻居
    #             continue
    #
    #         if [row, col] == each:  # 回头了
    #             continue
    #
    #         if each in self.enemies[0]:
    #             continue
    #
    #         self.enemies[0].append(each)
    #
    #         # print(st_n, each)
    #         self._find_route(each[0], each[1])
    #
    # def checking(self, site_start, site_end):
    #     """ 处理吃棋，必须是两个棋子 """
    #
    #     if self._invalid_coord(site_end) or self._invalid_coord(site_start):
    #         print('坐标不合法')
    #         return
    #
    #     node_s = self.board[site_start[0]][site_start[1]]  # 进攻方棋子或选中的棋子
    #     node_e = self.board[site_end[0]][site_end[1]]  # 防守方棋子或前进的位置
    #
    #     if node_e[0] in [3, 4]:  # 对方在行营或者大本营里，不可战斗
    #         print('在营里')
    #         return
    #
    #     if node_s[2] is None:  # 必须有棋子
    #         print('攻击方无子')
    #         return
    #
    #     info_e = node_e[2].get_info()
    #     if info_e[3] in ['地雷', '军旗']:
    #         print('地雷、军旗不可攻击。', info_e)
    #         return
    #
    #     path = None
    #     # 通达性检核
    #     if site_end not in node_s[1]:  # 首先都在邻居里搜寻，不在则不可通达，返回
    #         print('不是邻居关系。', site_end, node_s)
    #         if node_s[0] == 1:  # 再判断铁路通达性，不通需返回
    #             path = self.aStar.get_path(self.board, site_start, site_end)
    #             if not path:
    #                 return
    #         else:
    #             return
    #     print('铁路最短路径:', path)
    #
    #     # 可以通达，可以战斗
    #     ret = self.fight(node_s[2], node_e[2])  # 同阵营棋子战斗也处理在内
    #     print(ret)
    #     if ret < 0:  # 按兵不动
    #         print('打不动，罢兵。')
    #         return
    #     elif ret == 0:  # 同归于尽
    #         node_s[2].delete()
    #         node_e[2].delete()
    #         self.board[site_start[0]][site_start[1]][2] = None
    #         self.board[site_end[0]][site_end[1]][2] = None
    #     else:  # 战而胜之
    #         # node_e[2].delete()
    #         self.move_chess(site_start, site_end)  # #####################################################
    #         # node_s[2].update_me(site_end, -1)  # 更新坐标
    #         # self.board[site_start[0]][site_start[1]][2] = None
    #         # self.board[site_end[0]][site_end[1]][2] = node_s[2]

    # # 获得所有可抵达的敌人
    # def get_enemies(self, coord):
    #     if not self._valid_coord(coord):
    #         return None
    #     row, col = coord
    #
    #     chess = self.board[row][col][2]
    #     ret = chess.get_info()
    #     if ret[3] in ['地雷', '军旗']:  # 不能移动吃子的
    #         return None
    #
    #     self.enemies[0].clear()
    #     self.enemies[1].clear()
    #
    #     # if self.board[row][col] in [2, 4]:  # 2: 公路兵站14个，一步一站  4:大本营4个
    #     #     self._search_foes_near(row, col)
    #     #
    #     # elif self.board[row][col] == 3:  # 3:行营10个
    #     #     self._search_foes_near(row, col)
    #     #
    #     #     if self._valid_coord(row - 1, col - 1):
    #     #         self._fight_foe(row, col, row - 1, col - 1)
    #     #     if self._valid_coord(row - 1, col + 1):
    #     #         self._fight_foe(row, col, row - 1, col + 1)
    #     #     if self._valid_coord(row + 1, col - 1):
    #     #         self._fight_foe(row, col, row + 1, col - 1)
    #     #     if self._valid_coord(row + 1, col + 1):
    #     #         self._fight_foe(row, col, row + 1, col + 1)
    #
    #     if self.board[row][col][0] == 1:  # 缺省1: 铁路兵站32个，一步多站   0:界外无效
    #         ...
    #     else:  # 非铁路，邻居已定
    #         neighbours = self.board[row][col][1]
    #         self.log.debug(neighbours)
    #         for each in neighbours:
    #             self._fight_foe(row, col, each[0], each[1])
    #
    # def _search_foes_on_railway(self, row, col):
    #     # 搜索铁路上的敌人
    #     if self._valid_coord(row, col - 1):
    #         self._fight_foe(row, col, row, col - 1)
    #     if self._valid_coord(row, col + 1):
    #         self._fight_foe(row, col, row, col + 1)
    #     if self._valid_coord(row - 1, col):
    #         self._fight_foe(row, col, row - 1, col)
    #     if self._valid_coord(row + 1, col):
    #         self._fight_foe(row, col, row + 1, col)
    #
    # def fight(self, chess, chess_foe):
    #     # 与敌人战斗
    #     if not chess or not chess_foe:
    #         return -4
    #
    #     ret = chess.get_info()
    #     ret_foe = chess_foe.get_info()
    #
    #     if abs(ret[0] - ret_foe[0]) < 12:  # 自己人 错误的
    #         return -3
    #
    #     return self.judge(ret[0], ret_foe[0])
    #     # if result == 0:
    #     #     self.enemies[1].append(chess_foe)  #
    #     # elif result > 0:
    #     #     self.enemies[0].append(chess_foe)

    # def _update_frame(self, showing=False):
    #     # 各种方框的显示与擦除
    #     if showing:
    #         ...
    #     else:
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
    # endregion


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
