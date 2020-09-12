#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from functools import partial
from utilities import Utils, BackLabel
import numpy as np
import cgitb  # 相当管用

cgitb.enable(format='text')  # 解决 pyqt5 异常只要进入事件循环,程序就崩溃,而没有任何提示


class Stone(QtWidgets.QWidget):  # 棋子
    def __init__(self, parent=None, lot=0, coord=(0, 0)):
        super(Stone, self).__init__(parent)
        self.parent = parent

        self.coord = coord  # 坐标
        self.lot = lot  # 手数，可能为多次打劫，奇数为黑子，偶数为白子
        self.kill_list = []  # 吃掉的棋子
        # self.state = 0  # 0空子/死子；1黑子；2白子
        # self.liberty = 0  # 气数

        self.ko = 0  # 打劫，=被提时的手数
        self._pic = None  # 棋子图片
        self._size = None  # 棋子尺寸
        self.is_show_lot = None  # 显示手数
        self.is_cur_lot = True  # 是最后一手

        self._set_ui()

    def _set_ui(self):
        # self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setMouseTracking(True)

        e = QtWidgets.QGraphicsDropShadowEffect()
        offset = 5
        e.setBlurRadius(15)  # 阴影半径，虚化程度，不能大于圆角半径
        e.setOffset(offset, offset)  # 阴影宽度
        color = QtGui.QColor(80, 80, 80, 250) if self.lot % 2 else QtGui.QColor(20, 20, 20, 250)
        e.setColor(color)  # 阴影颜色
        self.setGraphicsEffect(e)

    # 悔棋用,恢复
    def get_kill_list(self):
        return self.kill_list

    def update_me(self, size, is_show_lot, is_cur_lot=True, kill_list=None):
        self._pic = './res/images/goB.png' if self.lot % 2 else './res/images/goW3.png'  # white go1.png'
        # size = 500
        self._size = size
        self.is_show_lot = is_show_lot
        self.is_cur_lot = is_cur_lot  # 要不要擦除最后一手的红圈圈
        if kill_list:
            self.kill_list.extend(kill_list)
            # print('update_me', kill_list)

        self.update()
        self.resize(size, size)

    # 删除自己，悔棋用
    def delete_me(self):
        # 恢复死亡名单

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        # self.setParent(None)
        # lo = widget.parent().layout()
        # lo.removeWidget(obj)
        self.deleteLater()

    # 被吃了，依旧保留，隐藏
    def kill_me(self):
        self.setVisible(False)

    def clear_me(self):
        ...
        # self.state = 0
        # self.liberty = 0
        # self.lots = 0
        # self.ko = 0
        # if isinstance(self.pic, QtWidgets.QLabel):
        #     self.pic.setVisible(False)
        #     self.pic.setPixmap(QtGui.QPixmap("./res/images/goD.png"))
        #     # self.pic.setPixmap(QtGui.QPixmap(""))  # 移除label上的图片
        # else:
        #     print('clear:not label')

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        super(Stone, self).paintEvent(event)
        # print('stone paint')
        # 不通过样式，直接设置圆角，通用，且不继承于子控件
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)  # 设置抗锯齿

        img_new = Utils.img_center(self.width(), self.height(), self._pic)
        painter.setBrush(QtGui.QBrush(img_new))  # 设置底图的方式之一

        painter.setPen(QtCore.Qt.transparent)  # 无边框

        rect = QtCore.QRect(0, 0, self._size, self._size)
        painter.drawRoundedRect(rect, self.width() // 2, self.height() // 2)

        # 数字
        if self.is_show_lot and not self.is_cur_lot:
            painter.setPen(QtGui.QColor(20, 155, 244, 255))
            painter.setFont(QtGui.QFont("Arial", 12))
            painter.drawText(rect, QtCore.Qt.AlignCenter, f'{self.lot}')

        # 画圆
        if self.is_cur_lot:
            # 判断是书写笔还是橡皮
            # mode = QPainter.CompositionMode_SourceOver if self.is_draw \
            #     else QPainter.CompositionMode_Clear  # 橡皮擦设置为擦除并为透明色。
            # painter.setCompositionMode(mode)
            # print(mode)
            # 然后画图。
            # pen = QtGui.QPen(QtGui.QColor(255, 122, 110, 255))  # 设置颜色
            pen = QtGui.QPen(QtCore.Qt.red)  # 设置颜色
            pen.setWidth(3)  # 设置边框宽度
            painter.setPen(pen)  # 添加描边边框
            painter.setBrush(QtCore.Qt.NoBrush)
            # print(rect)
            off = 6
            rt = QtCore.QRectF(rect.width() / 2-off, rect.height() / 2-off, 2*off, 2*off)
            painter.drawEllipse(rt)


MARGIN = 10


# 棋盘
class GoBoard(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(GoBoard, self).__init__(parent)
        self.parent = parent

        self.board_lines = 19  # 棋盘规格
        self.board_map = np.zeros((self.board_lines, self.board_lines, 2), dtype=int)
        # state(0:空  1:黑子 2:白子 3:劫 4:禁着点), stone_lot
        # print(self.board_map)
        self.side = 40  # 边空大小，显示坐标
        self.grid = 0  # 棋格大小
        self.stone_size = [0, 0]  # 棋子大小, 棋子大小的一半

        self.has_coord = False  # 不显示坐标
        self.has_lot = False  # 不显示手数

        self.stone_stream = []  # 实战流程
        self.lot_cur = 0  # 当前手数
        self.stone_rope = []  # 大龙，算气用的，死活用
        self.kill_list = []  # 死亡名单
        # self.stone_rope_liberty = [0, 0, 0, 0]  # 大龙总气数、外气、内气、公气

        # self.stone_prev = None  # 记录前一个点
        # self.killed = [[]]  # 每一手吃掉的棋子串
        # self.cur_stone = [0]*2     # 当前落点，可以悔棋

        # 棋盘数据定义
        # self.go_board = [[Stone() for i in range(self.board_size)] for j in range(self.board_size)]

        # self.setMinimumSize(self.BOARD_SIZE + self.BOARD_SIDE, self.BOARD_SIZE + self.BOARD_SIDE)
        # self.bg = BackLabel(self, './res/images/wenli4.jpg', 0)
        # self.bg.setStyleSheet('background: transparent;')

        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(800, 800)
        self.setMouseTracking(True)  # 跟踪鼠标移动
        # self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        # self.setStyleSheet('background-color:BurlyWood')  # Tan
        self.setStyleSheet('background-image:url(./res/images/wenli4.jpg)')
        Utils.set_effect(self, 1, 25, MARGIN, MARGIN, QtCore.Qt.darkGray)

        self.update_board()

    # 重回所有棋子，棋盘大小改变时调用
    def _flush_stones(self):
        length = len(self.stone_stream)
        if length > 0:
            for i in range(length - 1):  # 棋子重绘
                stone = self.stone_stream[i]
                stone.update_me(self.stone_size[0], self.has_lot, False)
                x = self.side + stone.coord[1] * self.grid - self.stone_size[1]
                y = self.side + stone.coord[0] * self.grid - self.stone_size[1]
                stone.move(x, y)

            stone = self.stone_stream[-1]
            stone.update_me(self.stone_size[0], self.has_lot)  # 画圈
            x = self.side + stone.coord[1] * self.grid - self.stone_size[1]
            y = self.side + stone.coord[0] * self.grid - self.stone_size[1]
            stone.move(x, y)

    # 更新棋盘
    def update_board(self):
        w = min(self.width(), self.height())
        self.grid = round((w - 2 * self.side) / (self.board_lines - 1))  # 棋格大小
        self.stone_size[0] = self.grid - 4  # 棋子大小
        self.stone_size[1] = self.stone_size[0] // 2  # 棋子大小的一半
        # print(self.grid, self.stone_half)

        self._flush_stones()  # 重画棋子
        self.update()  # 重画棋盘线

        # 初始化棋盘数据
        # for i in range(self.board_lines):
        #     for j in range(self.board_lines):
        #         lb = QtWidgets.QLabel(self)
        #
        #         # e2 = QtWidgets.QGraphicsDropShadowEffect()
        #         # e2.setBlurRadius(20)  # 阴影半径，虚化程度，不能大于圆角半径
        #         # e2.setOffset(5, 5)  # 阴影宽度
        #         # e2.setColor(QtGui.QColor(0, 0, 0, 200))  # 阴影颜色
        #         # lb.setGraphicsEffect(e2)
        #
        #         lb.setMouseTracking(True)  # 也能获取鼠标移动事件
        #         lb.setVisible(False)
        #         lb.setPixmap(QtGui.QPixmap("./res/images/goD.png"))
        #         lb.setScaledContents(True)  # 让图片自适应label大小
        #         lb.setMaximumSize(QtCore.QSize(self.chess_half_size * 2, self.chess_half_size * 2))
        #         lb.move(self.margins + self.chess_half_size - self.chess_half_size + j * self.grid_size,
        #                 self.margins + self.chess_half_size - self.chess_half_size + i * self.grid_size)
        #         self.go_board[i][j].pic = lb  # 棋子图片占位

    # 判断在棋盘外部
    def in_board(self, row, col):
        """
        落子在棋盘格内
        :param row: 行
        :param col: 列
        :return:
        """
        return 0 <= row < self.board_lines and 0 <= col < self.board_lines

    # 计算棋子的气，包含一串
    def get_liberty(self, row, col):
        self.stone_rope.clear()
        return self._cal_liberty(row, col)

    def _cal_liberty(self, row, col):
        """
        外部第一次调用前必须先调用
        self.stone_rope.clear()
        :param row: 行
        :param col: 列
        :return: 棋子或者相连大龙的气
        """

        if not self.in_board(row, col):
            return 0  # -1 出边了，等于少一气

        kind = self.board_map[row][col][0]
        if kind == 0:  # 空
            return 0  # -1

        if (row, col) in self.stone_rope:  # 处理过
            return 0
        else:
            self.stone_rope.append((row, col))

        liberty = 0

        offset = [-1, 0, 1, 0, 0, -1, 0, 1]
        for i in range(0, len(offset), 2):
            row1, col1 = row + offset[i], col + offset[i + 1]
            # print(i, row1, col1)

            if self.in_board(row1, col1):
                kind1 = self.board_map[row1][col1][0]
                if kind1 == 0:  # 空子
                    if (row1, col1) not in self.stone_rope:  # 未处理过
                        self.stone_rope.append((row1, col1))
                        liberty += 1
                elif kind1 == kind:
                    liberty += self._cal_liberty(row1, col1)

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

    # 落子处理

    # 提通，吃子
    def _take(self, row, col, state, stone):
        """
            上下左右看对方棋子有没有被杀死的，可以判断出连环劫的情况，
            返回被吃的死子串，保存在 kill_list 中
            :param row:
            :param col:
            :return:
        """

        kind = 2 if state == 1 else 1  # 黑白颠倒

        self.kill_list.clear()  # 死亡名单，保存所有死子的手数

        # 上下左右都计算一遍，看对方有没有死棋
        offset = [-1, 1, 0, 0]
        length = len(offset)
        for i in range(length):
            j = length - i - 1
            row_near, col_near = row + offset[i], col + offset[j]
            # print(i, row_near, col_near)
            if not self.in_board(row_near, col_near):
                # return -1
                continue

            if kind != self.board_map[row_near][col_near][0]:  # 不是对方的子
                # return -1
                continue

            liberty = self.get_liberty(row_near, col_near)
            if liberty > 0:  # 不是死子，不需提去
                # return -1
                continue

            # 气=0，
            count_dead = len(self.stone_rope)
            if count_dead > 1:  # 提多个死子
                for each in self.stone_rope:
                    lot = self.board_map[each[0], each[1], 1]
                    self.board_map[each[0], each[1]] = [0, 0]
                    stone_dead = self.stone_stream[lot - 1]
                    stone_dead.kill_me()
                    self.kill_list.append(lot)
            elif count_dead == 1:  # 可能是打劫
                state, lot = self.board_map[self.stone_rope[0][0], self.stone_rope[0][1]]
                stone_dead = self.stone_stream[lot - 1]
                if stone_dead.ko == self.lot_cur - 1:  # 说明对方刚打了劫，不能接着打
                    # print(dead_chess.ko)
                    return 0  # 恢复原状，不能接着打劫
                else:  # 说明刚寻完劫，可以接着打，即提子
                    self.board_map[self.stone_rope[0][0], self.stone_rope[0][1]] = [0, 0]
                    stone.ko = self.lot_cur  # 标记为当前手数
                    stone_dead.kill_me()
                    self.kill_list.append(lot)  # 虚子落地

        return 1

    # 落子，判断禁入点以及打劫等情况
    def set_chess(self, row, col):
        """ 先判断有没有在提对方子，其中要判断是不是打单劫。
            么有提子则看是不是禁入点。
            都不是，则落子无悔
        :param row:
        :param col:
        :return:
        """
        # 已经判断过了
        # if not self.in_board(row, col):
        #     return -1

        # state = self.board_map[row, col, 0]
        # if state > 2:  # 有子，返回
        #     return -1
        # else:

        # 先根据手数虚拍一子，再判断合法否，并没有产生控件，以便恢复

        # 放上新棋子
        self.lot_cur += 1

        state = 2 - self.lot_cur % 2
        self.board_map[row][col] = [state, self.lot_cur]

        st = Stone(self, self.lot_cur, (row, col))
        # st.update_me(self.stone_size[0], self.has_lot, True, self.kill_list)
        self.stone_stream.append(st)

        msg = '黑子' if state == 1 else '白子'

        # 先提对方死子
        ret = self._take(row, col, state, st)
        # print(ret)
        if ret == 0:  # 判断对方才打劫
            print(f'{msg}先寻劫，禁入点')
            self.board_map[row, col] = [0, 0]  # 虚子羽化
            self.stone_stream.pop()
            st.delete_me()
            self.lot_cur -= 1
            return -3
        else:
            if not self.kill_list:  # 没有提子，再判断是不是不入气点
                if self.get_liberty(row, col) == 0:  # 自己不能填死自己(应氏规则可以)
                    print(f'{msg}不入气，禁入点')
                    self.board_map[row][col] = [0, 0]  # 恢复
                    self.stone_stream.pop()
                    st.delete_me()
                    self.lot_cur -= 1
                    return -3

        if self.lot_cur > 1:  # 擦除圆圈
            # print(self.lot_cur)
            prev = self.stone_stream[self.lot_cur - 2]
            # print(type(prev))
            prev.update_me(self.stone_size[0], self.has_lot, False)

        # 放上新棋子
        # st = Stone(self, self.lot_cur, (row, col))
        st.update_me(self.stone_size[0], self.has_lot, True, self.kill_list)

        x = self.side + col * self.grid - self.stone_size[1]
        y = self.side + row * self.grid - self.stone_size[1]
        # print(x, y, e.pos().x(), e.pos().y())
        st.move(x, y)
        st.show()
        # self.stone_stream.append(st)

        self.parent.set_lot(self.lot_cur)

        # print(self.board_map)

        return 0

    def slot_checked(self, wg):
        # wg = QtWidgets.QCheckBox()
        # print(wg.text())
        if wg.text() == '显示坐标':
            self.has_coord = wg.isChecked()
            self.update()  # 重画棋盘
        else:  # 显示手数
            self.has_lot = wg.isChecked()
            self._flush_stones()  # 重画棋子

        # self.max_lib()

    def _find(self, row, col, state):
        # if self.board_map[row][col][0] != 0:
        #     return

        # self.board_map[row][col] = [state, self.lot_cur]
        self.lot_cur += 2
        stone = Stone(self, self.lot_cur, (row, col))
        stone.update_me(self.stone_size[0], True, False, self.kill_list)
        self.stone_stream.append(stone)
        x = self.side + col * self.grid - self.stone_size[1]
        y = self.side + row * self.grid - self.stone_size[1]
        stone.move(x, y)
        stone.show()

        lib1 = self.get_liberty(row, col)
        # print(row, col, lib1)

        offset = [-1, 1, 0, 0]
        length = len(offset)
        for i in range(length):
            j = length - i - 1
            row_near, col_near = row + offset[i], col + offset[j]
            # print(i, j, row_near, col_near)
            if not self.in_board(row_near, col_near):
                continue

            if self.board_map[row_near][col_near][0] != 0:
                continue

            self.board_map[row_near][col_near] = [state, self.lot_cur]
            lib2 = self.get_liberty(row_near, col_near)
            print(lib1, lib2)
            if lib2 <= lib1:
                self.board_map[row_near][col_near] = [0, 0]
            else:
                self._find(row_near, col_near, state)

    def max_lib(self):
        row = Utils.rand_int(0, self.board_lines - 1)
        col = Utils.rand_int(0, self.board_lines - 1)

        # self.lot_cur += 1
        state = 1  # 2 - self.lot_cur % 2
        self.board_map[row][col] = [state, self.lot_cur]
        self._find(row, col, state)
        print(self.get_liberty(row, col))
        # self.stone_stream[0].update_me(self.stone_size[0], False, True)

    # 悔棋
    def slot_withdraw(self):
        if self.lot_cur > 0:
            self.lot_cur -= 1
            stone = self.stone_stream.pop()
            row, col = stone.coord
            self.board_map[row][col] = [0, 0]

            kill_list = stone.get_kill_list()
            for each in kill_list:
                dead_stone = self.stone_stream[each - 1]
                row, col = dead_stone.coord
                lot = dead_stone.lot
                self.board_map[row][col] = [2 - lot % 2, lot]
                dead_stone.setVisible(True)

            stone.delete_me()

            self.parent.set_lot(self.lot_cur)

    # 画棋盘线
    def paintEvent(self, event):
        # print('paint')
        offset = self.side

        qp = QtGui.QPainter()
        qp.begin(self)
        # 画棋盘线
        pen = QtGui.QPen(QtGui.QColor(50, 50, 50), 3, QtCore.Qt.SolidLine)
        qp.setPen(pen)

        width = (self.board_lines - 1) * self.grid

        for i in range(self.board_lines):
            qp.drawLine(offset, offset + i * self.grid,
                        offset + width, offset + i * self.grid)
            qp.drawLine(offset + i * self.grid, offset,
                        offset + i * self.grid, offset + width)

            # 写出坐标
            if self.has_coord:
                # pen = QtGui.QPen(QtCore.Qt.blue, 2, QtCore.Qt.SolidLine)
                # qp.setPen(pen)
                font = QtGui.QFont('微软雅黑', 10)
                # font.setPointSize(18)
                # font.setBold(True)
                qp.setFont(font)

                rect = QtCore.QRect(
                    self.side + width + self.stone_size[1],
                    self.side + i * self.grid - self.side // 2,
                    self.side, self.side)
                qp.drawText(rect, int(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter), str(self.board_lines - i))

                rect = QtCore.QRect(
                    self.side + i * self.grid - self.side // 2,
                    self.side + width + self.stone_size[1], self.side, self.side)
                qp.drawText(rect, int(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter), chr(ord('A') + i))

        # 画星位
        radius = 5
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20), 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(QtGui.QColor(10, 10, 10))

        if self.board_lines >= 15:  # 15路围棋盘
            qp.drawEllipse(QtCore.QRect(offset + 3 * self.grid - radius,
                                        offset + 3 * self.grid - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_lines - 1) // 2 * self.grid - radius,
                                        offset + 3 * self.grid - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_lines - 4) * self.grid - radius,
                                        offset + 3 * self.grid - radius,
                                        radius * 2, radius * 2))

            qp.drawEllipse(QtCore.QRect(offset + 3 * self.grid - radius,
                                        offset + (self.board_lines - 1) // 2 * self.grid - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_lines - 1) // 2 * self.grid - radius,
                                        offset + (self.board_lines - 1) // 2 * self.grid - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_lines - 4) * self.grid - radius,
                                        offset + (self.board_lines - 1) // 2 * self.grid - radius,
                                        radius * 2, radius * 2))

            qp.drawEllipse(QtCore.QRect(offset + 3 * self.grid - radius,
                                        offset + (self.board_lines - 4) * self.grid - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_lines - 1) // 2 * self.grid - radius,
                                        offset + (self.board_lines - 4) * self.grid - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_lines - 4) * self.grid - radius,
                                        offset + (self.board_lines - 4) * self.grid - radius,
                                        radius * 2, radius * 2))
        elif self.board_lines >= 13:  # 13路围棋盘
            qp.drawEllipse(QtCore.QRect(offset + 3 * self.grid - radius,
                                        offset + 3 * self.grid - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_lines - 4) * self.grid - radius,
                                        offset + 3 * self.grid - radius,
                                        radius * 2, radius * 2))

            qp.drawEllipse(QtCore.QRect(offset + (self.board_lines - 1) // 2 * self.grid - radius,
                                        offset + (self.board_lines - 1) // 2 * self.grid - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + 3 * self.grid - radius,
                                        offset + (self.board_lines - 4) * self.grid - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_lines - 4) * self.grid - radius,
                                        offset + (self.board_lines - 4) * self.grid - radius,
                                        radius * 2, radius * 2))
        elif self.board_lines >= 9:  # 9路围棋盘
            qp.drawEllipse(QtCore.QRect(offset + 2 * self.grid - radius,
                                        offset + 2 * self.grid - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_lines - 3) * self.grid - radius,
                                        offset + 2 * self.grid - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_lines - 1) // 2 * self.grid - radius,
                                        offset + (self.board_lines - 1) // 2 * self.grid - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + 2 * self.grid - radius,
                                        offset + (self.board_lines - 3) * self.grid - radius,
                                        radius * 2, radius * 2))
            qp.drawEllipse(QtCore.QRect(offset + (self.board_lines - 3) * self.grid - radius,
                                        offset + (self.board_lines - 3) * self.grid - radius,
                                        radius * 2, radius * 2))
        qp.end()

    def mousePressEvent(self, e):
        col = round((e.pos().x() - self.side) / self.grid)
        row = round((e.pos().y() - self.side) / self.grid)

        # print(row, col, self.stone_half)
        if not self.in_board(row, col):  # 盘外
            return
        if self.board_map[row][col][0] != 0:  # 非空子
            lib = self.get_liberty(row, col)
            # print('气数：', lib, row, col)
            self.parent.set_lib(lib)
            return

        self.set_chess(row, col)  # 落子判断，禁入点以及打劫情况

    def enterEvent(self, e):  # 鼠标移入label
        # print('enterEvent', type(self))
        self.setCursor(QtCore.Qt.PointingHandCursor)  # 设置光标为：手指

    def resizeEvent(self, event):
        # print('res')
        # w = min(self.parent.width(), self.parent.height())
        # self.setMaximumSize(w, w)
        # self.bg.update()
        # print('resizeEvent')
        self.update_board()
        ...

    # # def mouseDoubleClickEvent(self, e):
    # #     print('mouse double clicked')
    # #
    # # def focusInEvent(self, e):
    # #     print('focusInEvent')
    # #
    # # def focusOutEvent(self, e):
    # #     print('focusOutEvent')
    # #
    # # def moveEvent(self, e):
    # #     print('moveEvent')
    #
    # def leaveEvent(self, e):  # 鼠标离开label
    #     # 定义鼠标的样式
    #     # self.setCursor(QtCore.Qt.PointingHandCursor)  # 设置光标为：等待
    #     # self.setCursor(QtCore.Qt.SizeAllCursor)  # 设置光标为：移动
    #     # print('leaveEvent')
    #     if self.prev_stone:
    #         stone = self.go_board[self.prev_stone[0]][self.prev_stone[1]]
    #         if stone.state == 0:  # 空子
    #             stone.pic.setVisible(False)
    #     self.prev_stone = None
    #
    # def mouseMoveEvent(self, e):
    #     col = (e.pos().x() - self.margins) // self.grid_size
    #     row = (e.pos().y() - self.margins) // self.grid_size
    #
    #     if not self.isInBorad(row, col):
    #         return
    #
    #     if self.prev_stone:
    #         if self.prev_stone == (row, col):  # 同一个棋子上移动就退出
    #             return
    #         # print('mouseMoveEvent')
    #         stone = self.go_board[self.prev_stone[0]][self.prev_stone[1]]
    #         if stone.state == 0:  # 空子
    #             stone.pic.setVisible(False)
    #     self.prev_stone = (row, col)
    #
    #     self.go_board[row][col].pic.setVisible(True)


class MainWin(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWin, self).__init__(*args, **kwargs)
        self.go = GoBoard(self)

        self.platform = QtWidgets.QFrame()
        self.cb_coord = QtWidgets.QCheckBox('显示坐标')
        self.cb_lot = QtWidgets.QCheckBox('显示手数')
        self.cb_coord.stateChanged.connect(partial(self.go.slot_checked, self.cb_coord))
        self.cb_lot.stateChanged.connect(partial(self.go.slot_checked, self.cb_lot))

        self.lb_lot = QtWidgets.QLabel('当前手数：0')
        self.lb_lib = QtWidgets.QLabel('所选棋子的气数：0')
        self.pb_withdraw = QtWidgets.QPushButton('悔棋')
        self.pb_withdraw.clicked.connect(self.go.slot_withdraw)
        lv = QtWidgets.QVBoxLayout(self.platform)
        lv.addWidget(self.cb_coord)
        lv.addWidget(self.cb_lot)
        lv.addWidget(self.lb_lot)
        lv.addWidget(self.lb_lib)
        lv.addWidget(self.pb_withdraw)
        lv.addStretch()

        self.resize(1200, 800)
        lh = QtWidgets.QHBoxLayout(self)
        # lh.setContentsMargins(0, 0, 0, 0)
        lh.setSpacing(10)
        lh.addWidget(self.go)
        lh.addWidget(self.platform)

        Utils.center_win(self)

    def set_lot(self, lot):
        self.lb_lot.setText(f'当前手数：{lot}')

    def set_lib(self, lib):
        self.lb_lib.setText(f'所选棋子的气数：{lib}')

    def __str__(self):
        return '1'

    __repr__ = __str__


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())
