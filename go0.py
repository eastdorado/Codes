#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Project: PyCharm
# @File    : go0.py
# @Author  : tiger
# @Email   : shdorado@126.com
# @Time    : 2020/5/11 21:04

import sys

from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np


class GoTest(object):
    def __init__(self):
        super(GoTest, self).__init__()


class Stone(object):  # 棋子
    def __init__(self):
        self.state = 0  # 0空子；1黑子；2白子
        self.liberty = 0  # 气数
        self.lots = 0  # 手数，可能为多次打劫，奇数为黑子，偶数为白子
        self.ko = 0  # 打劫，=被提时的手数
        self.pic = None  # 棋子图片

    def clear(self):
        self.state = 0
        self.liberty = 0
        self.lots = 0
        self.ko = 0
        if isinstance(self.pic, QtWidgets.QLabel):
            self.pic.setVisible(False)
            self.pic.setPixmap(QtGui.QPixmap("./res/images/goD.png"))
            # self.pic.setPixmap(QtGui.QPixmap(""))  # 移除label上的图片
        else:
            print('clear:not label')


class GoBoard(QtWidgets.QFrame):  # 棋盘
    def __init__(self, parent=None):
        super(GoBoard, self).__init__(parent)
        self.parent = parent
        self.setMinimumSize(self.parent.height(), self.parent.height())

        self.setMouseTracking(True)  # 跟踪鼠标移动

        self.board_size = 19  # 棋盘大小
        # self.unit = 40  # 单位长度
        self.margins = 20  # 边界大小
        self.grid_size = int((self.height() - 2 * self.margins) // self.board_size)  # 棋格大小
        # print(self.grid_size)
        self.chess_half_size = int(self.grid_size / 2)  # 棋子大小的一半
        self.coordinated = True  # 不显示坐标
        self.prev_stone = None  # 记录前一个点

        self.route_playing = []  # 实战流程
        self.number_playing = 0  # 当前手数
        self.killed = [[]]  # 每一手吃掉的棋子串
        # self.cur_stone = [0]*2     # 当前落点，可以悔棋

        self.stone_rope = []  # 大龙
        # self.stone_rope_liberty = [0, 0, 0, 0]  # 大龙总气数、外气、内气、公气

        # 棋盘数据定义
        self.go_board = [[Stone() for i in range(self.board_size)] for j in range(self.board_size)]

        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        # self.setStyleSheet('background-color:BurlyWood')  # Tan
        self.setStyleSheet('background-image:url(./res/images/wenli41.jpg)')

        self.update_board()

    def update_board(self):

        self.margins = 20  # 边界大小
        self.grid_size = int((self.height() - 2 * self.margins) // self.board_size)  # 棋格大小
        # print(self.grid_size)
        self.chess_half_size = int(self.grid_size / 2)  # 棋子大小的一半

        # 初始化棋盘数据
        for i in range(self.board_size):
            for j in range(self.board_size):
                lb = QtWidgets.QLabel(self)

                # e2 = QtWidgets.QGraphicsDropShadowEffect()
                # e2.setBlurRadius(20)  # 阴影半径，虚化程度，不能大于圆角半径
                # e2.setOffset(5, 5)  # 阴影宽度
                # e2.setColor(QtGui.QColor(0, 0, 0, 200))  # 阴影颜色
                # lb.setGraphicsEffect(e2)

                lb.setMouseTracking(True)  # 也能获取鼠标移动事件
                lb.setVisible(False)
                lb.setPixmap(QtGui.QPixmap("./res/images/goD.png"))
                lb.setScaledContents(True)  # 让图片自适应label大小
                lb.setMaximumSize(QtCore.QSize(self.chess_half_size * 2, self.chess_half_size * 2))
                lb.move(self.margins + self.chess_half_size - self.chess_half_size + j * self.grid_size,
                        self.margins + self.chess_half_size - self.chess_half_size + i * self.grid_size)
                self.go_board[i][j].pic = lb  # 棋子图片占位

    def isInBorad(self, row, col):
        """
        落子在棋盘格内
        :param row: 行
        :param col: 列
        :return:
        """
        # 判断在棋盘外部
        return 0 <= row < self.board_size and 0 <= col < self.board_size

    def ponnuki(self, row, col):
        """
        提通，吃子
        外部调用前必须先调用
        self.stone_rope.clear()
        :param row:
        :param col:
        :return:
        """

        if not self.isInBorad(row, col):
            return -1

        stone = self.go_board[row][col]
        kind = stone.state
        if kind == 0:  # 空子
            return -1

        kind1 = 2 if kind == 1 else 1

        self.stone_rope.clear()
        if self.isInBorad(row - 1, col):
            if kind1 == self.go_board[row - 1][col].state:  # 对方的子
                liberty = self.cal_liberty(row - 1, col)
                if liberty == 0:  # 死子，需提去
                    count_dead = len(self.stone_rope)
                    if count_dead > 1:  # 提子
                        for each in self.stone_rope:
                            dead_chess = self.go_board[each[0]][each[1]]
                            dead_chess.clear()
                    elif count_dead == 1:  # 可能是打劫
                        dead_chess = self.go_board[self.stone_rope[0][0]][self.stone_rope[0][1]]
                        if dead_chess.ko == self.number_playing - 1:  # 说明刚打完劫，不能接着打
                            # print(dead_chess.ko)
                            stone.clear()  # 恢复，不能接着打劫
                            return 0
                        else:  # 说明刚寻完劫，可以接着打
                            stone.ko = self.number_playing  # 标记为当前手数
                            dead_chess.clear()

        self.stone_rope.clear()
        if self.isInBorad(row + 1, col):
            if kind1 == self.go_board[row + 1][col].state:  # 对方的子
                liberty = self.cal_liberty(row + 1, col)
                if liberty == 0:  # 死子，需提去
                    count_dead = len(self.stone_rope)
                    if count_dead > 1:  # 提子
                        for each in self.stone_rope:
                            dead_chess = self.go_board[each[0]][each[1]]
                            dead_chess.clear()
                    elif count_dead == 1:
                        dead_chess = self.go_board[self.stone_rope[0][0]][self.stone_rope[0][1]]
                        if dead_chess.ko == self.number_playing - 1:  # 说明刚打完劫，不能接着打
                            # print(dead_chess.ko)
                            stone.clear()  # 恢复，不能接着打劫
                            return 0
                        else:  # 说明刚寻完劫，可以接着打
                            stone.ko = self.number_playing  # 标记为当前手数
                            dead_chess.clear()

        self.stone_rope.clear()
        if self.isInBorad(row, col - 1):
            if kind1 == self.go_board[row][col - 1].state:  # 对方的子
                liberty = self.cal_liberty(row, col - 1)
                if liberty == 0:  # 死子，需提去
                    count_dead = len(self.stone_rope)
                    if count_dead > 1:  # 提子
                        for each in self.stone_rope:
                            dead_chess = self.go_board[each[0]][each[1]]
                            dead_chess.clear()
                    elif count_dead == 1:
                        dead_chess = self.go_board[self.stone_rope[0][0]][self.stone_rope[0][1]]
                        if dead_chess.ko == self.number_playing - 1:  # 说明刚打完劫，不能接着打
                            stone.clear()  # 恢复，不能接着打劫
                            return 0
                        else:  # 说明刚寻完劫，可以接着打
                            stone.ko = self.number_playing  # 标记为当前手数
                            dead_chess.clear()

        self.stone_rope.clear()
        if self.isInBorad(row, col + 1):
            if kind1 == self.go_board[row][col + 1].state:  # 对方的子
                liberty = self.cal_liberty(row, col + 1)
                if liberty == 0:  # 死子，需提去
                    count_dead = len(self.stone_rope)
                    if count_dead > 1:  # 提子
                        for each in self.stone_rope:
                            dead_chess = self.go_board[each[0]][each[1]]
                            dead_chess.clear()
                    elif count_dead == 1:
                        dead_chess = self.go_board[self.stone_rope[0][0]][self.stone_rope[0][1]]
                        if dead_chess.ko == self.number_playing - 1:  # 说明刚打完劫，不能接着打
                            stone.clear()  # 恢复，不能接着打劫
                            return 0
                        else:  # 说明刚寻完劫，可以接着打
                            stone.ko = self.number_playing  # 标记为当前手数
                            dead_chess.clear()

    def cal_liberty(self, row, col):
        """
        计算棋子的气，包含一串
        外部调用前必须先调用
        self.stone_rope.clear()
        :param row: 行
        :param col: 列
        :return: 棋子或者相连大龙的气
        """

        if not self.isInBorad(row, col):
            return -1

        kind = self.go_board[row][col].state
        if kind == 0:  # 空子
            return -1

        if (row, col) in self.stone_rope:  # 处理过
            return 0
        else:
            self.stone_rope.append((row, col))

        liberty = 0

        if self.isInBorad(row - 1, col):
            kind1 = self.go_board[row - 1][col].state  # 空子
            if kind1 == 0:  # 空子
                if (row - 1, col) not in self.stone_rope:  # 未处理过
                    self.stone_rope.append((row - 1, col))
                    liberty += 1
            elif kind1 == kind:
                liberty += self.cal_liberty(row - 1, col)

        if self.isInBorad(row + 1, col):
            kind1 = self.go_board[row + 1][col].state  # 空子
            if kind1 == 0:  # 空子
                if (row + 1, col) not in self.stone_rope:  # 未处理过
                    self.stone_rope.append((row + 1, col))
                    liberty += 1
            elif kind1 == kind:
                liberty += self.cal_liberty(row + 1, col)

        if self.isInBorad(row, col - 1):
            kind1 = self.go_board[row][col - 1].state  # 空子
            if kind1 == 0:  # 空子
                if (row, col - 1) not in self.stone_rope:  # 未处理过
                    self.stone_rope.append((row, col - 1))
                    liberty += 1
            elif kind1 == kind:
                liberty += self.cal_liberty(row, col - 1)

        if self.isInBorad(row, col + 1):
            kind1 = self.go_board[row][col + 1].state  # 空子
            if kind1 == 0:  # 空子
                if (row, col + 1) not in self.stone_rope:  # 未处理过
                    self.stone_rope.append((row, col + 1))
                    liberty += 1
            elif kind1 == kind:
                liberty += self.cal_liberty(row, col + 1)

        return liberty

    # def cal_owner_liberty(self, row, col):
    #     """
    #     计算本身的气
    #     :param row:
    #     :param col:
    #     :return:    本身活气数
    #     """
    #
    #     if not self.isInBorad(row, col):
    #         return 0
    #
    #     liberty = 0
    #     if self.isInBorad(row - 1, col):
    #         if self.go_board[row - 1][col].state == 0:
    #             liberty += 1
    #     if self.isInBorad(row + 1, col):
    #         if self.go_board[row + 1][col].state == 0:
    #             liberty += 1
    #     if self.isInBorad(row, col - 1):
    #         if self.go_board[row][col - 1].state == 0:
    #             liberty += 1
    #     if self.isInBorad(row, col + 1):
    #         if self.go_board[row][col + 1].state == 0:
    #             liberty += 1
    #
    #     return liberty
    #
    # def isDead(self, row, col, kind):
    #     """
    #     判断棋子死活，返回气的多少
    #     外部调用前必须先调用
    #     self.stone_rope.clear()
    #     self.stone_rope_liberty=[0]*4
    #     :param row:
    #     :param col:
    #     :param kind:
    #     :return: =0 死了； >0 还有气
    #     """
    #
    #     # if kind < 1:  # 仅计算黑白
    #     #     return -1
    #
    #     if not self.isInBorad(row, col):
    #         return 0
    #
    #     if self.go_board[row][col].state == kind:
    #         if (row, col) in self.stone_rope:  # 已经处理过了
    #             return 0
    #         else:
    #             if self.cal_owner_liberty(row, col) == 0:
    #                 self.stone_rope.append((row, col))
    #                 return self.isDead(row - 1, col, kind) + self.isDead(row + 1, col, kind) + \
    #                        self.isDead(row, col - 1, kind) + self.isDead(row, col + 1, kind)
    #             else:
    #                 return 1
    #     else:
    #         if kind == 0:  # 空子
    #             return 1
    #         else:
    #             return 0

    def set_chess(self, row, col, kind):
        """
        落子处理
        :param row:
        :param col:
        :param kind: 黑子或白子
        :return:
        """

        if not self.isInBorad(row, col):
            return -1

        # 判断是否有子
        node = self.go_board[row][col]
        if node.state != 0:
            self.stone_rope.clear()
            liberty = self.cal_liberty(row, col)
            self.parent.info.setText(f'第{self.go_board[row][col].lots + 1}手\n\n状态：{node.state}\n气数：{liberty}')
            return -1

        # 放上棋子
        node.state = kind
        node.lots = self.number_playing
        # self.cur_stone = (row, col)

        msg = '黑子' if kind == 1 else '白子'
        # 先提对方死子
        if self.ponnuki(row, col) == 0:
            print(msg, '先寻劫，禁入点')
            return -3
        # 再判断是不是不入气点
        self.stone_rope.clear()
        if self.cal_liberty(row, col) == 0:  # 自己不能填死自己(应氏规则可以)
            print(msg, '不入气，禁入点')
            node.clear()  # 恢复
            return -3

        return 0

    # 悔棋
    def slot_withdraw(self):
        if self.number_playing > 0:
            self.number_playing -= 1
            row = self.route_playing[self.number_playing] // self.board_size
            col = self.route_playing[self.number_playing] % self.board_size
            node = self.go_board[row][col]
            node.clear()
            self.route_playing.pop()
            # if self.killed[self.number_playing]:
            #     for each in self.killed[self.number_playing]:
            #
            self.killed.pop()
            self.parent.info.setText(f'第{self.number_playing}手')
            print(self.number_playing, (row, col))

    def slot_coordinated(self):
        self.coordinated = bool(1 - self.coordinated)  # 取反
        self.update()

    def paintEvent(self, event):
        offset = self.margins + self.chess_half_size

        qp = QtGui.QPainter()

        qp.begin(self)
        # 写出坐标
        if self.coordinated:
            pen = QtGui.QPen(QtCore.Qt.blue, 2, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            font = QtGui.QFont('微软雅黑', 12)
            # font.setPointSize(18)
            # font.setBold(True)
            qp.setFont(font)
            for i in range(self.board_size):
                rect = QtCore.QRect(0, self.margins + i * self.grid_size, self.margins, self.grid_size)
                qp.drawText(rect, int(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter), str(self.board_size - i))
                rect = QtCore.QRect(self.margins + self.board_size * self.grid_size,
                                    self.margins + i * self.grid_size, self.margins, self.grid_size)
                qp.drawText(rect, int(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter), str(self.board_size - i))

                rect = QtCore.QRect(self.margins + i * self.grid_size, 0, self.grid_size, self.margins)
                qp.drawText(rect, int(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter), chr(ord('A') + i))
                rect = QtCore.QRect(self.margins + i * self.grid_size,
                                    self.margins + self.board_size * self.grid_size, self.grid_size, self.grid_size)
                qp.drawText(rect, int(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter), chr(ord('A') + i))

        # 画棋盘线
        # pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        pen = QtGui.QPen(QtGui.QColor(50, 50, 50), 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)

        for i in range(self.board_size):
            qp.drawLine(offset, offset + i * self.grid_size,
                        offset + (self.board_size - 1) * self.grid_size, offset + i * self.grid_size)
            qp.drawLine(offset + i * self.grid_size, offset,
                        offset + i * self.grid_size, offset + (self.board_size - 1) * self.grid_size)
        # 画星位
        radius = 3
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20), 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(QtGui.QColor(10, 10, 10))

        if self.board_size >= 15:  # 15路围棋盘
            qp.drawEllipse(QtCore.QRect(offset + 3 * self.grid_size - radius,
                                        offset + 3 * self.grid_size - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_size - 1) // 2 * self.grid_size - radius,
                                        offset + 3 * self.grid_size - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_size - 4) * self.grid_size - radius,
                                        offset + 3 * self.grid_size - radius,
                                        radius * 2, radius * 2))

            qp.drawEllipse(QtCore.QRect(offset + 3 * self.grid_size - radius,
                                        offset + (self.board_size - 1) // 2 * self.grid_size - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_size - 1) // 2 * self.grid_size - radius,
                                        offset + (self.board_size - 1) // 2 * self.grid_size - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_size - 4) * self.grid_size - radius,
                                        offset + (self.board_size - 1) // 2 * self.grid_size - radius,
                                        radius * 2, radius * 2))

            qp.drawEllipse(QtCore.QRect(offset + 3 * self.grid_size - radius,
                                        offset + (self.board_size - 4) * self.grid_size - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_size - 1) // 2 * self.grid_size - radius,
                                        offset + (self.board_size - 4) * self.grid_size - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_size - 4) * self.grid_size - radius,
                                        offset + (self.board_size - 4) * self.grid_size - radius,
                                        radius * 2, radius * 2))
        elif self.board_size >= 13:  # 13路围棋盘
            qp.drawEllipse(QtCore.QRect(offset + 3 * self.grid_size - radius,
                                        offset + 3 * self.grid_size - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_size - 4) * self.grid_size - radius,
                                        offset + 3 * self.grid_size - radius,
                                        radius * 2, radius * 2))

            qp.drawEllipse(QtCore.QRect(offset + (self.board_size - 1) // 2 * self.grid_size - radius,
                                        offset + (self.board_size - 1) // 2 * self.grid_size - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + 3 * self.grid_size - radius,
                                        offset + (self.board_size - 4) * self.grid_size - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_size - 4) * self.grid_size - radius,
                                        offset + (self.board_size - 4) * self.grid_size - radius,
                                        radius * 2, radius * 2))
        elif self.board_size >= 9:  # 9路围棋盘
            qp.drawEllipse(QtCore.QRect(offset + 2 * self.grid_size - radius,
                                        offset + 2 * self.grid_size - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_size - 3) * self.grid_size - radius,
                                        offset + 2 * self.grid_size - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_size - 1) // 2 * self.grid_size - radius,
                                        offset + (self.board_size - 1) // 2 * self.grid_size - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + 2 * self.grid_size - radius,
                                        offset + (self.board_size - 3) * self.grid_size - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_size - 3) * self.grid_size - radius,
                                        offset + (self.board_size - 3) * self.grid_size - radius,
                                        radius * 2, radius * 2))
        qp.end()

    def mousePressEvent(self, e):
        col = (e.pos().x() - self.margins) // self.grid_size
        row = (e.pos().y() - self.margins) // self.grid_size
        # print(row, col)

        if not self.isInBorad(row, col):
            return

        kind = 2 - (1 + self.number_playing) % 2  # 根据手数判断是黑子或白子
        if self.set_chess(row, col, kind) == 0:  # 可以落子
            self.prev_stone = None  # 去影子
            lb = self.go_board[row][col].pic
            # lb.setFixedSize(QtCore.QSize(self.chess_half_size * 2, self.chess_half_size * 2))
            file = "./res/images/goB.png" if kind == 1 else "./res/images/goW3.png"
            lb.setPixmap(QtGui.QPixmap(file))
            # lb.setScaledContents(True)  # 让图片自适应label大小
            # self.setStyleSheet("border-image:url(./res/images/gochess1.jpg) 4 4 4 4 stretch stretch;")
            # lb.setGeometry(cur_pos.x(), cur_pos.y(), 50, 50)
            lb.setVisible(True)

            info = self.parent.info
            info.setText(f'第{self.go_board[row][col].lots + 1}手')

            self.route_playing.append(row * self.board_size + col)  # 历史记录
            self.killed.append([])
            self.number_playing += 1

    def enterEvent(self, e):  # 鼠标移入label
        # print('enterEvent', type(self))
        self.setCursor(QtCore.Qt.PointingHandCursor)  # 设置光标为：手指

    # def mouseDoubleClickEvent(self, e):
    #     print('mouse double clicked')
    #
    # def focusInEvent(self, e):
    #     print('focusInEvent')
    #
    # def focusOutEvent(self, e):
    #     print('focusOutEvent')
    #
    # def moveEvent(self, e):
    #     print('moveEvent')

    def leaveEvent(self, e):  # 鼠标离开label
        # 定义鼠标的样式
        # self.setCursor(QtCore.Qt.PointingHandCursor)  # 设置光标为：等待
        # self.setCursor(QtCore.Qt.SizeAllCursor)  # 设置光标为：移动
        # print('leaveEvent')
        if self.prev_stone:
            stone = self.go_board[self.prev_stone[0]][self.prev_stone[1]]
            if stone.state == 0:  # 空子
                stone.pic.setVisible(False)
        self.prev_stone = None

    def mouseMoveEvent(self, e):
        col = (e.pos().x() - self.margins) // self.grid_size
        row = (e.pos().y() - self.margins) // self.grid_size

        if not self.isInBorad(row, col):
            return

        if self.prev_stone:
            if self.prev_stone == (row, col):  # 同一个棋子上移动就退出
                return
            # print('mouseMoveEvent')
            stone = self.go_board[self.prev_stone[0]][self.prev_stone[1]]
            if stone.state == 0:  # 空子
                stone.pic.setVisible(False)
        self.prev_stone = (row, col)

        self.go_board[row][col].pic.setVisible(True)

    def resizeEvent(self, event):
        # print('resizeEvent')
        self.update_board()


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        # TODO(tiger) Change this to use relations
        self._setup_ui()
        self._chess_init()

    def _chess_init(self):
        # 总体框架
        hl_main = QtWidgets.QHBoxLayout(self)
        self.setLayout(hl_main)

        self.chess = GoBoard(self)
        wg_right = QtWidgets.QWidget()
        wg_right.setFixedWidth(200)
        vl_right = QtWidgets.QVBoxLayout(wg_right)
        hl_main.addWidget(self.chess)
        hl_main.addWidget(wg_right)

        # 控制区
        hl_control_panel = QtWidgets.QHBoxLayout()
        pb_withdraw = QtWidgets.QPushButton("悔棋")
        pb_manual = QtWidgets.QPushButton("坐标")
        pb_withdraw.clicked.connect(self.chess.slot_withdraw)
        pb_manual.clicked.connect(self.chess.slot_coordinated)
        hl_control_panel.addWidget(pb_withdraw)
        hl_control_panel.addWidget(pb_manual)
        vl_right.addLayout(hl_control_panel)

        # 信息区
        font = QtGui.QFont('NSimSun')
        font.setPointSize(15)
        font.setWeight(50)
        self.info = QtWidgets.QTextBrowser()
        self.info.setAlignment(QtCore.Qt.AlignLeft)
        self.info.setFont(font)
        vl_right.addWidget(self.info)

    def _setup_ui(self):
        self.setWindowTitle('围棋智能')
        self.setGeometry(0, 0, 900, 750)
        self._center()

    def _center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resizeEvent(self, event):
        # self.chess.resizeEvent(event)

        palette = QtGui.QPalette()
        pix = QtGui.QPixmap('res/background/background.jpg')
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(palette)


if __name__ == '__main__':
    # 字体大小自适应分辨率
    v_compare = QtCore.QVersionNumber(5, 26, 0)
    v_current, _ = QtCore.QVersionNumber.fromString(QtCore.QT_VERSION_STR)  # 获取当前Qt版本
    if QtCore.QVersionNumber.compare(v_current, v_compare) >= 0:
        print(v_current.toString(), _)
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # Qt从5.6.0开始，支持High-DPI
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication(sys.argv)
        font = QtGui.QFont("宋体")
        pointsize = font.pointSize()
        font.setPixelSize(pointsize * 90 // 72)
        app.setFont(font)

    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

    # Chess = np.dtype([('state', np.uint8), ('liberty', np.uint16), ('pic', np.object)])
    # a = np.zeros([2, 3], dtype=Chess)
    #
    # # b = np.array(range(2, 6), dtype=np.object)
    # # a = np.arange(1, 6)
    # node = Node()
    # node.state = 1
    # node.liberty = 2
    # node.pic = None
    # # print(node)
    # # print(a.size, type(a))
    # # print('a=', a)
    # a[0][0]['pic'] = node
    # print('a[0]=', a[0], type(a[0][0]['pic'].state))
    # print(b.dtype)
    # print(a.astype('float16'))
