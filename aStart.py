#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @项目名称: python
# @File    : aStart.py
# @Time    : 2020/3/27 14:01
# @Author  : big
# @Email   : shdorado@126.com

import sys
import random
import math
import time

from PyQt5 import QtCore, QtGui, QtWidgets


class Node:
    def __init__(self, index, value, father=None):
        self.index = index
        self.value = value
        self.father = father
        self.child_left = None
        self.child_right = None


class MaxHeap:
    """最大堆：父比子大"""
    heap = []

    @staticmethod
    def show_heap():
        print(MaxHeap.heap)

    # region 基本操作
    # region 插入元素
    @staticmethod
    def insert(num):
        MaxHeap.heap.append(num)
        MaxHeap.shift_up()

    @staticmethod
    def shift_up():
        """把新增在最后的大数节点往上移动"""
        current_id = len(MaxHeap.heap) - 1
        parent_id = (current_id - 1) // 2
        while current_id > 0:
            if MaxHeap.heap[parent_id] >= MaxHeap.heap[current_id]:
                break
            else:
                MaxHeap.heap[parent_id], MaxHeap.heap[current_id] = MaxHeap.heap[current_id], MaxHeap.heap[parent_id]
                current_id = parent_id
                parent_id = (current_id - 1) // 2

    # endregion

    # region 删除元素
    @staticmethod
    def delate(num):
        """删除特定数，并下沉"""
        temp = MaxHeap.heap.pop()
        if num == temp:  # 是最末的最小数
            return
        if num not in MaxHeap.heap:
            print('not in heap')
            return
        ind = MaxHeap.heap.index(num)
        MaxHeap.heap[ind] = temp
        MaxHeap.shift_down(ind)

    @staticmethod
    def shift_down(ind):
        """把最末的数作为根，再根据大小往下沉"""
        current_id = ind
        child_id_left = current_id * 2 + 1
        child_id_right = current_id * 2 + 2
        while current_id < len(MaxHeap.heap) - 1:
            # 如果当前节点为叶子节点，shift_down完成
            if current_id * 2 + 1 > len(MaxHeap.heap) - 1:
                break
            # 如果当前节点只有左孩子没有右孩子
            if current_id * 2 + 1 == len(MaxHeap.heap) - 1:
                if MaxHeap.heap[current_id] > MaxHeap.heap[-1]:
                    break
                else:
                    MaxHeap.heap[current_id], MaxHeap.heap[-1] = MaxHeap.heap[-1], MaxHeap.heap[current_id]
                    break
            # 如果当前节点既有左孩子又有右孩子
            if MaxHeap.heap[current_id] > max(MaxHeap.heap[child_id_left], MaxHeap.heap[child_id_right]):
                break
            else:
                if MaxHeap.heap[child_id_right] > MaxHeap.heap[child_id_left]:
                    MaxHeap.heap[child_id_right], MaxHeap.heap[current_id] = MaxHeap.heap[current_id], MaxHeap.heap[
                        child_id_right]
                    current_id = child_id_right
                    child_id_left = current_id * 2 + 1
                    child_id_right = current_id * 2 + 2
                else:
                    MaxHeap.heap[child_id_left], MaxHeap.heap[current_id] = MaxHeap.heap[current_id], MaxHeap.heap[
                        child_id_left]
                    current_id = child_id_left
                    child_id_left = current_id * 2 + 1
                    child_id_right = current_id * 2 + 2

    # endregion
    # endregion

    # region 基础排序
    @staticmethod
    def extract_max():
        """弹出最大的根，并重新构建"""
        num = MaxHeap.heap[0]
        try:
            MaxHeap.delate(num)
            return num
        except:
            return num

    @staticmethod
    def heap_sort(arr):
        for n in arr:  # 形成大堆
            MaxHeap.insert(n)
        for i in range(len(arr)):  # 大堆重新赋值给源
            arr[i] = MaxHeap.extract_max()

    @staticmethod
    def heapify(arr):
        """从最后一个父节点倒推，一个个下沉，省去所有叶子的运算"""
        MaxHeap.heap = arr
        n = (len(arr) - 1) // 2
        while n >= 0:
            MaxHeap.shift_down(n)
            n -= 1

    @staticmethod
    def heap_sort2(arr):
        """返回列表的绝对排序过的新列表"""
        MaxHeap.heapify(arr)
        res = []
        for i in range(len(arr)):
            res.append(MaxHeap.extract_max())
        return res

    @staticmethod
    def heap_sort3(arr):
        """原地堆排序，直接在源数据上操作"""
        MaxHeap.heapify(arr)
        for i in range(len(arr) - 1, -1, -1):
            MaxHeap.heap[i], MaxHeap.heap[0] = MaxHeap.heap[0], MaxHeap.heap[i]  # 将堆顶元素与堆尾元素互换
            MaxHeap.shift_down(0)
    # endregion


class MinHeap:
    """最小堆：父比子小"""
    heap = []

    @staticmethod
    def show_heap():
        print(MinHeap.heap)

    # region 基本操作
    # region 插入元素
    @staticmethod
    def insert(num):
        MinHeap.heap.append(num)
        MinHeap.shift_up()
        # MinHeap.show_heap()

    @staticmethod
    def shift_up():
        """把新增在最后的小数往上移动"""
        current_id = len(MinHeap.heap) - 1
        parent_id = (current_id - 1) // 2
        while current_id > 0:
            if MinHeap.heap[parent_id] <= MinHeap.heap[current_id]:
                break
            else:
                MinHeap.heap[parent_id], MinHeap.heap[current_id] = MinHeap.heap[current_id], MinHeap.heap[parent_id]
                current_id = parent_id
                parent_id = (current_id - 1) // 2

    # endregion

    # region 删除元素
    @staticmethod
    def delate(num):
        """删除特定数，并下沉"""
        temp = MinHeap.heap.pop()
        if num == temp:  # 是最末的最大数
            return
        if num not in MinHeap.heap:
            print('not in heap')
            return
        ind = MinHeap.heap.index(num)
        MinHeap.heap[ind] = temp
        MinHeap.shift_down(ind)

    @staticmethod
    def shift_down(ind):
        """父节点根据大小往下沉"""
        current_id = ind
        child_left_id = current_id * 2 + 1
        child_right_id = current_id * 2 + 2
        while child_left_id <= len(MinHeap.heap) - 1:
            # 如果当前节点为叶子节点，shift_down完成
            # if child_left_id > len(MinHeap.heap) - 1:
            #     break

            # 如果当前节点只有左孩子没有右孩子
            if child_left_id == len(MinHeap.heap) - 1:
                if MinHeap.heap[current_id] < MinHeap.heap[-1]:
                    break
                else:
                    MinHeap.heap[current_id], MinHeap.heap[-1] = MinHeap.heap[-1], MinHeap.heap[current_id]
                    break
            # 如果当前节点既有左孩子又有右孩子
            else:
                litter_id = child_left_id \
                    if MinHeap.heap[child_left_id] <= MinHeap.heap[child_right_id] else child_right_id
                if MinHeap.heap[current_id] <= MinHeap.heap[litter_id]:
                    break
                else:
                    MinHeap.heap[litter_id], MinHeap.heap[current_id] \
                        = MinHeap.heap[current_id], MinHeap.heap[litter_id]
                    current_id = litter_id
                    child_left_id = current_id * 2 + 1
                    child_right_id = current_id * 2 + 2

    # endregion
    # endregion

    # region 基础排序
    @staticmethod
    def extract_min():
        """弹出最小的根，并重新构建"""
        num = MinHeap.heap[0]
        try:
            MinHeap.delate(num)
            return num
        except:
            return num

    @staticmethod
    def heap_sort(arr):
        for n in arr:  # 形成大堆
            MinHeap.insert(n)
        for i in range(len(arr)):  # 大堆重新赋值给源
            arr[i] = MinHeap.extract_min()

    @staticmethod
    def heapify(arr):
        """从最后一个父节点倒推，一个个下沉，省去所有叶子的运算"""
        MinHeap.heap = arr
        n = (len(arr) - 1) // 2
        while n >= 0:
            MinHeap.shift_down(n)
            n -= 1

    @staticmethod
    def heap_sort2(arr):
        """返回列表的绝对排序过的新列表"""
        MinHeap.heapify(arr)
        res = []
        for i in range(len(arr)):
            res.append(MinHeap.extract_min())
        return res

    @staticmethod
    def heap_sort3(arr):
        """原地堆排序，直接在源数据上操作"""
        MinHeap.heapify(arr)
        for i in range(len(arr) - 1, -1, -1):
            MinHeap.heap[i], MinHeap.heap[0] = MinHeap.heap[0], MinHeap.heap[i]  # 将堆顶元素与堆尾元素互换
            MinHeap.shift_down(0)
    # endregion


class MyBinaryTree(object):
    def __init__(self, btree):

        for each in btree:
            MinHeap.insert(each)
        # MinHeap.heap = btree
        self.Btree = MinHeap.heap

        # MaxHeap.heap = self.Btree
        # MinHeap.heap_sort3(self.Btree)
        # res = self.Heap.heap_sort2(self.Btree)
        # print(res)
        # MaxHeap.show_heap()

        # self.Heap.insert(11)
        MinHeap.delate(2)
        # self.Heap.show_heap()
        # print(self.Btree)

        self.Count = len(self.Btree)
        self.Depth = int(math.log2(self.Count)) + 1 if self.Count > 0 else 0  # 深度 n个节点的完全二叉树的深度
        self.Breadth = pow(2, self.Depth) - 1  # 广度，最底层需要的格数,即完全二叉树的节点数

    def draw_node(self, qp, grid_w, grid_h, index):
        depth = int(math.log2(index + 1) if index >= 0 else 0)  # 所在层数
        depth_max = self.Depth - 1  # 深度

        grid_first = pow(2, depth_max - depth)  # 左边距
        grid_mid = 2 * grid_first  # 中间的间隔

        first_index = pow(2, depth) - 1  # 左边第一项序号
        # last_index = first_index + pow(2, depth) - 1  # pow(2, depth+1) - 2
        # # 右边序号

        cur_grid_x = grid_first + grid_mid * (index - first_index) + 1  # 树左移一格
        cur_grid_y = depth + 1  # 节点所在的格子

        x = cur_grid_x * grid_w - grid_w // 2  # 圆心的屏幕坐标
        y = cur_grid_y * grid_h - grid_h // 2

        ride = 25  # 圆半径
        rect = QtCore.QRect(x - ride, y - ride, 2 * ride, 2 * ride)

        qp.setPen(QtCore.Qt.darkBlue)
        qp.setBrush(QtGui.QColor(173, 216, 230))

        # 画圆
        qp.drawEllipse(rect)

        # 画数字
        font = QtGui.QFont('Decorative', 20)
        font.setBold(True)
        qp.setFont(font)
        qp.drawText(rect, QtCore.Qt.AlignCenter, str(self.Btree[index]))

        # 画连线
        pen = QtGui.QPen(QtGui.QColor(0, 150, 0), 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)

        if index == 0:
            return

        X = grid_first * grid_w
        R = math.sqrt(pow(X, 2) + grid_h * grid_h)
        scale = ride / R
        dx = round(scale * X)
        dy = round(scale * grid_h)

        if index % 2:  # 在左边
            qp.drawLine(x + dx, y - dy, x - dx + X, y + dy - grid_h)
        else:  # 在右边
            qp.drawLine(x - dx, y - dy, x + dx - X, y + dy - grid_h)

    def draw_tree(self, qp, canvas_size):
        col = QtGui.QColor(0, 0, 0)
        col.setNamedColor('#d0d0d0')
        # pen = QPen()
        qp.setPen(col)

        if self.Depth == 0:
            return
        grid_w = canvas_size.width() // self.Breadth  # 画布方格尺寸
        grid_h = canvas_size.height() // self.Depth  # 画布方格尺寸

        for y in range(self.Depth):
            for x in range(self.Breadth):
                # qp.setBrush(col)
                qp.drawRect(
                    round(
                        grid_w * x),
                    round(
                        grid_h * y),
                    round(grid_w),
                    round(grid_h))

        for i in range(self.Count):
            self.draw_node(qp, grid_w, grid_h, i)


class ShowTree(QtWidgets.QWidget):
    def __init__(self, parent=None):
        # noinspection PyArgumentList
        super(ShowTree, self).__init__()
        self.heap = [90, 2, 85, 70, 10, 60, 80, 30, 20, 50, 40, 34, 134, 62]

        self.tree = MyBinaryTree(self.heap)

        # self.maxHeap = MaxHeap(self.heap)
        # self.initUI()

    def initUI(self):
        pass

    def clicked(self):
        pass

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.tree.draw_tree(qp, QtCore.QSize(self.width() - 50, self.height() - 50))
        qp.end()


class NewAStar(object):
    """采用二叉堆的 A星算法"""

    def __init__(self):
        self.map2d_w = 1
        self.map2d_h = 1

        self.map2d = []
        self.map2d_size = None

        self.start = None
        self.end = None

        self.impasse = None  # 死路的权重
        self.value = None  # 权重范围

        self.open_list = []
        self.close_list = []

        self.init_map2d(5, 54, 5, 54)

    def init_map2d(self, map_w=5, map_h=12, start=0, end=59):
        """初始化地图数据"""
        # [row, col , g, h, v, father]
        # row，col-坐标 g-当前路径成本 h-估算成本 v-节点的权重 father-父节点
        self.map2d.clear()
        self.open_list.clear()
        self.close_list.clear()

        self.map2d_w = map_w
        self.map2d_h = map_h
        self.start = start  # 初始化起点的序号
        self.end = end  # 初始化终点的序号
        self.map2d_size = self.map2d_w * self.map2d_h  # 地图节点数目

        self.open_list.append(self.start)  # 起点放进列表

        self.impasse = 4  # 死路
        self.value = [1, 2, 3, self.impasse]  # 权重

        for row in range(self.map2d_h):
            for col in range(self.map2d_w):
                h = (abs(self.end // self.map2d_h - row) + abs(self.end % self.map2d_w - col)) * 10  # 计算h值
                value = random.choice(self.value)

                # [row, col , g, h, v, father]
                # row，col-坐标 g-当前路径成本 h-估算成本 v-节点的权重 father-父节点
                self.map2d.append([row, col, 0, h, value, None])

        # self.map2d[self.start][4] = 2  # 起点权重
        # self.map2d[self.end][4] = 3  # 终点权重
        # print(self.map2d)

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


class MyAStar(object):
    class Point:
        """
        表示一个点
        """

        def __init__(self, row, col):
            self.row = row
            self.col = col

        def __eq__(self, other):
            if self.row == other.row and self.col == other.col:
                return True
            return False

        def __str__(self):
            return "row:" + str(self.row) + ", col:" + str(self.col)

    class Node:  # 描述AStar算法中的节点数据
        def __init__(self, point, endPoint, v=0):
            """
            :param point: 二元组
            :param endPoint: 二元组
            :param v:
            """
            self.point = point  # 自己的坐标
            self.v = v  # 节点的权重
            # 从起点移动到方格的移动代价,沿着到达该方格而生成的路径
            self.g = 0  # g值在用到的时候会重新算
            # 从指定的方格移动到终点 B 的估算成本
            self.h = (abs(endPoint.row - point.row) +
                      abs(endPoint.col - point.col)) * 10  # 计算h值
            self.f = self.g + self.h
            self.father = None  # 父节点

        def __str__(self):
            return f"{self.point} v={self.v} g={self.g} h={self.h} father:{self.father}"

    class Map2D:
        """
            说明：
                1.构造方法需要两个参数，即二维数组的宽和高
                2.成员变量w和h是二维数组的宽和高
                3.使用：‘对象[x][y]’可以直接取到相应的值
                4.数组的默认值都是0
        """

        def __init__(self, w, h):
            self.width = w  # 地图宽
            self.height = h  # 地图高

            self.start_point = MyAStar.Point(0, 0)  # 起点坐标
            self.end_point = MyAStar.Point(h - 1, w - 1)  # 终点坐标
            # self.end_point = Point(random.randint(0, h-1), random.randint(0, w-1))

            self.impasse = 4  # 死路
            value = [1, 2, 3, self.impasse]  # 权重
            self.pics = [
                r'E:\python\res\images\good.png',
                r'E:\python\res\images\tu.png',
                r'E:\python\res\images\grass.png',
                r'E:\python\res\images\water.png',
                r'E:\python\res\images\pudi.png']

            self.nodes = [[MyAStar.Node(MyAStar.Point(i, j), self.end_point, random.choice(
                value)) for j in range(w)] for i in range(h)]

            self.nodes[0][0].v = 3
            self.nodes[self.end_point.row][self.end_point.col].v = 1

        def getValue(self, i, j):
            return self.nodes[i][j].v - 1
        # def showMap(self):
        #     for y in range(self.h):
        #         for x in range(self.w):
        #             print(self.data[x][y], end=' ')
        #         print("")
        #
        # def __getitem__(self, item):
        #     return self.data[item]

    def __init__(self, map_w, map_h):
        # 创建一个10*10的地图
        self.map2d = MyAStar.Map2D(map_w, map_h)
        self.open_list = [self.map2d.nodes[self.map2d.start_point.row][self.map2d.start_point.col]]
        self.close_list = []

        self.Item_list = []
        self.Item_count = 0
        d = NewAStar(map_w, map_h)

    def find_neighbours(self, node):
        w = self.map2d.width
        h = self.map2d.height

        for i in range(node.point.row - 1, node.point.row + 2):
            if i < 0 or i >= self.map2d.height:  # 越界检测
                continue
            for j in range(node.point.col - 1, node.point.col + 2):
                if j < 0 or j >= self.map2d.width:  # 越界检测
                    continue
                if i == node.point.row and j == node.point.col:  # 自身检测
                    continue
                neighbour = self.map2d.nodes[i][j]
                if neighbour.v == self.map2d.impasse:  # 去掉障碍物
                    continue
                if self.is_in_close_list(neighbour):  # 已经处理过了
                    continue

                path = abs(node.point.row - neighbour.point.row) + \
                       abs(node.point.col - neighbour.point.col)
                value = 10 if path == 1 else 14
                new_g = neighbour.v * value + node.g  # 更新g值

                if not self.is_in_open_list(neighbour):  # 加入下一步考察对象
                    self.open_list.append(neighbour)
                    neighbour.father = node  # 更新其父亲
                    if neighbour.point == self.map2d.end_point:  # 已经找到终点了
                        return 1
                else:
                    if new_g < neighbour.g:  # 更小的值
                        neighbour.father = node
                    else:
                        continue
                neighbour.g = new_g
                neighbour.f = new_g + neighbour.h  # 更新h值
                # print(neighbour)

        if self.is_in_open_list(node):
            self.open_list.remove(node)
            self.close_list.append(node)
        # print(len(self.open_list))
        return 0

    def get_min_node(self):
        if not self.open_list:
            return None

        node = self.open_list[0]
        for each in self.open_list:
            if node.f > each.f:  # 等于时怎么办？
                node = each
        return node

    def searching(self):
        path = []
        # 判断寻路终点是否是障碍
        # if self.map2d[self.endPoint.x][self.endPoint.y] != self.passTag:
        #     return None
        # 2.主循环逻辑
        while True:
            node = self.get_min_node()
            if not node:
                print('无路可走')
                break
            if self.find_neighbours(node):
                last = self.map2d.nodes[self.map2d.end_point.row][self.map2d.end_point.col]
                while True:
                    if last:
                        path.append(last)
                        last = last.father
                    else:
                        return list(reversed(path))
        return path

    def is_in_close_list(self, node):
        for each in self.close_list:
            if node.point == each.point:
                return True
        return False

    def is_in_open_list(self, node):
        for each in self.open_list:
            if node.point == each.point:
                return True
        return False


class D2Pane(QtWidgets.QWidget):
    def __init__(self):
        super(D2Pane, self).__init__()
        self.text = "Лев Николаевич Толстой\nАнна Каренина"
        self.map_w = 5
        self.map_h = 12
        self.colors = [QtGui.QColor(211, 211, 211), QtGui.QColor(155, 155, 155),
                       QtGui.QColor(85, 85, 85), QtGui.QColor(20, 20, 20)]

        self.flag = True
        print('-----------------------------------------')
        print('开始探路1')
        start = time.perf_counter()
        self.s = NewAStar()
        # self.s = MyAStar(self.map_w, self.map_h)
        # self.s.find_neighbours(self.map2d.nodes[0][0]
        self.path = self.s.searching()
        # self.s.deal_neighbours(49)
        # print(self.s.open_list[0], ':', self.s._get_f(self.s.open_list[0]))
        # node = self.s.get_min_node()
        end = time.perf_counter()
        print(f'用时：{end - start}')
        print('-----------------------------------------')

        # self.flag = False
        # print('-----------------------------------------')
        # print('开始探路2')
        # start = time.perf_counter()
        # self.s2 = MyAStar(self.map_w, self.map_h)
        # # self.s = MyAStar(self.map_w, self.map_h)
        # # self.s.find_neighbours(self.map2d.nodes[0][0]
        # self.path2 = self.s2.searching()
        # # self.s.deal_neighbours(49)
        # # print(self.s.open_list[0], ':', self.s._get_f(self.s.open_list[0]))
        # # node = self.s.get_min_node()
        # end = time.perf_counter()
        # print(f'用时：{end - start}')
        # print('-----------------------------------------')

        self.initUI()

    def initUI(self):
        # self.setGeometry(2500, 130, 1000, 800)
        self.setWindowTitle('A星算法演示')

        # btn = QtWidgets.QPushButton('刷新', self)
        # btn.resize(btn.sizeHint())
        # btn.move(800, 0)

        # btn.clicked.connect(self.clicked)

        self.show()

    def clicked(self):
        if self.flag:
            self.s = NewAStar()
        else:
            self.s = MyAStar(self.map_w, self.map_h)
        self.path = self.s.searching()
        print(self.path)
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        # self.drawText(event, qp)
        # self.drawPoints(qp)
        # self.drawRectangles(qp)
        # self.drawLines(qp)
        # self.drawBrushes(qp)
        # self.drawBezierCurve(qp)
        self.drawMap(qp)
        # print(self.s.open_list)
        # self.drawNode(qp, self.s.open_list[0])
        # for each in self.s.open_list:
        #     self.drawNode(qp, each)
        for i in range(len(self.path)):
            self.drawNode1(qp, self.path[i])
        # for i in range(len(self.path2)):
        #     self.drawNode2(qp, self.path2[i])

        qp.end()

    def drawNode1(self, qp, node):
        # print(node)
        ride = 10
        rt_w = self.size().width() / self.map_w
        rt_h = self.size().height() / self.map_h

        qp.setBrush(QtCore.Qt.green)
        qp.drawEllipse(int(self.s.map2d[node][1] * rt_w + rt_w / 2) - ride,
                       int(self.s.map2d[node][0] * rt_h + rt_h / 2) - ride, 2 * ride, 2 * ride)

    def drawNode2(self, qp, node):
        # print(node)
        ride = 10
        rt_w = self.size().width() / self.map_w
        rt_h = self.size().height() / self.map_h

        qp.setBrush(QtCore.Qt.red)
        qp.drawEllipse(int(node.point.col * rt_w + rt_w / 2) - ride,
                       int(node.point.row * rt_h + rt_h / 2) - ride, 2 * ride, 2 * ride)

    def drawMap(self, qp):
        col = QtGui.QColor(0, 0, 0)
        col.setNamedColor('#d0d0d0')
        # pen = QPen()
        qp.setPen(col)

        rt_w = self.size().width() / self.map_w
        rt_h = self.size().height() / self.map_h

        # if self.flag:
        for i in range(self.s.map2d_size):
            y = i // self.s.map2d_w
            x = i % self.s.map2d_w
            v = self.s.map2d[i][4] - 1
            # print(f'i={i} {x,y} v={self.s.map2d[i][4]}')
            qp.setBrush(self.colors[v])
            qp.drawRect(int(rt_w * x), int(rt_h * y), int(rt_w), int(rt_h))
            # size = QtCore.QSize(int(rt_w), int(rt_h))
            # img = QtGui.QImage(self.map2d.pics[v])
            # pixImg = QtGui.QPixmap.fromImage(img.scaled(size, QtCore.Qt.IgnoreAspectRatio))
            # qp.drawPixmap(int(rt_w * x), int(rt_h * y), pixImg)

        # 起点 与 终点
        ride = 20
        side1 = int(rt_w / 2)
        side2 = int(rt_h / 2)
        qp.setBrush(QtCore.Qt.blue)
        qp.drawEllipse(side1 - ride, side2 - ride, 2 * ride, 2 * ride)

        side1 = int(rt_w * self.s.map2d[self.s.end][0] + side1)
        side2 = int(rt_h * self.s.map2d[self.s.end][1] + side2)
        qp.setBrush(QtCore.Qt.red)
        qp.drawEllipse(side1 - ride, side2 - ride, 2 * ride, 2 * ride)

        # else:
        #     for y in range(self.map_h):
        #         for x in range(self.map_w):
        #             v = self.s.map2d.getValue(y, x)
        #             qp.setBrush(self.colors[v])
        #             qp.drawRect(int(rt_w * x), int(rt_h * y), int(rt_w), int(rt_h))
        #             # size = QtCore.QSize(int(rt_w), int(rt_h))
        #             # img = QtGui.QImage(self.map2d.pics[v])
        #             # pixImg = QtGui.QPixmap.fromImage(img.scaled(size, QtCore.Qt.IgnoreAspectRatio))
        #             # qp.drawPixmap(int(rt_w * x), int(rt_h * y), pixImg)
        #     # 起点 与 终点
        #     ride = 20
        #     side1 = int(rt_w / 2)
        #     side2 = int(rt_h / 2)
        #     qp.setBrush(QtCore.Qt.blue)
        #     qp.drawEllipse(side1 - ride, side2 - ride, 2 * ride, 2 * ride)
        #     side1 = int(rt_w * self.s.map2d.end_point.col + side1)
        #     side2 = int(rt_h * self.s.map2d.end_point.row + side2)
        #     qp.setBrush(QtCore.Qt.red)
        #     qp.drawEllipse(side1 - ride, side2 - ride, 2 * ride, 2 * ride)

    def drawText(self, event, qp):
        qp.setPen(QtGui.QColor(168, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 20))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)

    def drawPoints(self, qp):
        qp.setPen(QtCore.Qt.blue)
        size = self.size()

        for i in range(1000):
            x = random.randint(1, size.width() - 1)
            y = random.randint(1, size.height() - 1)
            qp.drawPoint(x, y)

    def drawRectangles(self, qp):
        col = QtGui.QColor(0, 0, 0)
        col.setNamedColor('#d400d4')
        qp.setPen(col)

        qp.setBrush(QtGui.QColor(200, 0, 0))
        qp.drawRect(10, 15, 90, 60)

        qp.setBrush(QtGui.QColor(255, 80, 0, 160))
        qp.drawRect(130, 15, 90, 60)

        qp.setBrush(QtGui.QColor(25, 0, 90, 200))
        qp.drawRect(250, 15, 90, 60)

    def drawLines(self, qp):
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)

        qp.setPen(pen)
        qp.drawLine(20, 40, 250, 40)

        pen.setStyle(QtCore.Qt.DashLine)
        qp.setPen(pen)
        qp.drawLine(20, 80, 250, 80)

        pen.setStyle(QtCore.Qt.DashDotLine)
        qp.setPen(pen)
        qp.drawLine(20, 120, 250, 120)

        pen.setStyle(QtCore.Qt.DotLine)
        qp.setPen(pen)
        qp.drawLine(20, 160, 250, 160)

        pen.setStyle(QtCore.Qt.DashDotDotLine)
        qp.setPen(pen)
        qp.drawLine(20, 200, 250, 200)

        pen.setStyle(QtCore.Qt.CustomDashLine)
        pen.setDashPattern([1, 4, 5, 4])
        qp.setPen(pen)
        qp.drawLine(20, 240, 250, 240)

    def drawBrushes(self, qp):
        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        qp.setBrush(brush)
        qp.drawRect(10, 15, 90, 60)

        brush.setStyle(QtCore.Qt.Dense1Pattern)
        qp.setBrush(brush)
        qp.drawRect(130, 15, 90, 60)

        brush.setStyle(QtCore.Qt.Dense2Pattern)
        qp.setBrush(brush)
        qp.drawRect(250, 15, 90, 60)

        brush.setStyle(QtCore.Qt.DiagCrossPattern)
        qp.setBrush(brush)
        qp.drawRect(10, 105, 90, 60)

        brush.setStyle(QtCore.Qt.Dense5Pattern)
        qp.setBrush(brush)
        qp.drawRect(130, 105, 90, 60)

        brush.setStyle(QtCore.Qt.Dense6Pattern)
        qp.setBrush(brush)
        qp.drawRect(250, 105, 90, 60)

        brush.setStyle(QtCore.Qt.HorPattern)
        qp.setBrush(brush)
        qp.drawRect(10, 195, 90, 60)

        brush.setStyle(QtCore.Qt.VerPattern)
        qp.setBrush(brush)
        qp.drawRect(130, 195, 90, 60)

        brush.setStyle(QtCore.Qt.BDiagPattern)
        qp.setBrush(brush)
        qp.drawRect(250, 195, 90, 60)

    def drawBezierCurve(self, qp):
        """贝塞尔曲线"""
        path = QtGui.QPainterPath()
        path.moveTo(30, 30)
        path.cubicTo(30, 30, 200, 350, 350, 130)
        path.cubicTo(350, 130, 260, 450, 250, 30)

        qp.drawPath(path)


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.wg = D2Pane()
        self.setGeometry(200, 40, 1200, 1000)
        self.setupUI()

    def setupUI(self):
        vl_main = QtWidgets.QVBoxLayout()
        # self.wg = ShowTree()

        btn = QtWidgets.QPushButton('刷新')
        btn.clicked.connect(self.wg.clicked)

        vl_main.addWidget(btn)
        vl_main.addWidget(self.wg)
        self.setLayout(vl_main)

    # def resizeEvent(self, event):
    #     palette = QtGui.QPalette()
    #     pix = QtGui.QPixmap('res/background/bk4.jpg')
    #     pix = pix.scaled(self.width(), self.height())
    #     palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
    #     self.setPalette(palette)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

    # dd = []
    # for each in dd:
    #     print('dd')
