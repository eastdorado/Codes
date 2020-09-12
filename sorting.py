#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Project: PyCharm
# @File    : sorting.py
# @Author  : tiger
# @Email   : shdorado@126.com
# @Time    : 2020/3/29 15:21

import sys
import random
import math

from PyQt5 import QtCore, QtGui, QtWidgets


class Sorting(object):
    arr = []

    def __init__(self):
        super(Sorting, self).__init__()

    @staticmethod
    def bubbleSort(arr):
        """ 冒泡排序 """
        for i in range(1, len(arr)):
            for j in range(0, len(arr) - i):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    @staticmethod
    def selectionSort(arr):
        """ 选择排序 """
        for i in range(len(arr) - 1):
            # 记录最小数的索引
            minIndex = i
            for j in range(i + 1, len(arr)):
                if arr[j] < arr[minIndex]:
                    minIndex = j
            # i 不是最小数时，将 i 和最小数进行交换
            if i != minIndex:
                arr[i], arr[minIndex] = arr[minIndex], arr[i]
        return arr

    @staticmethod
    def insertionSort(arr):
        """ 插入排序 """
        for i in range(len(arr)):
            preIndex = i - 1
            current = arr[i]
            while preIndex >= 0 and arr[preIndex] > current:
                arr[preIndex + 1] = arr[preIndex]
                preIndex -= 1
            arr[preIndex + 1] = current
        return arr

    @staticmethod
    def shellSort(arr):
        """ 希尔排序 """
        import math
        gap = 1
        while (gap < len(arr) / 3):
            gap = gap * 3 + 1
        while gap > 0:
            for i in range(gap, len(arr)):
                temp = arr[i]
                j = i - gap
                while j >= 0 and arr[j] > temp:
                    arr[j + gap] = arr[j]
                    j -= gap
                arr[j + gap] = temp
            gap = math.floor(gap / 3)
        return arr

    @staticmethod
    def mergeSort(arr):
        """ 归并排序 """
        import math
        if (len(arr) < 2):
            return arr
        middle = math.floor(len(arr) / 2)
        left, right = arr[0:middle], arr[middle:]
        return Sorting.merge(Sorting.mergeSort(left), Sorting.mergeSort(right))

    @staticmethod
    def merge(left, right):
        result = []
        while left and right:
            if left[0] <= right[0]:
                result.append(left.pop(0));
            else:
                result.append(right.pop(0));
        while left:
            result.append(left.pop(0));
        while right:
            result.append(right.pop(0));
        return result

    @staticmethod
    def quickSort(arr, left=None, right=None):
        """ 快速排序 """
        left = 0 if not isinstance(left, (int, float)) else left
        right = len(arr) - 1 if not isinstance(right, (int, float)) else right
        if left < right:
            partitionIndex = Sorting.partition(arr, left, right)
            Sorting.quickSort(arr, left, partitionIndex - 1)
            Sorting.quickSort(arr, partitionIndex + 1, right)
        return arr

    @staticmethod
    def partition(arr, left, right):
        pivot = left
        index = pivot + 1
        i = index
        while i <= right:
            if arr[i] < arr[pivot]:
                Sorting.swap(arr, i, index)
                index += 1
            i += 1
        Sorting.swap(arr, pivot, index - 1)
        return index - 1

    @staticmethod
    def swap(arr, i, j):
        arr[i], arr[j] = arr[j], arr[i]

    @staticmethod
    def buildMaxHeap(arr):
        """ 堆排序 """
        import math
        for i in range(math.floor(len(arr) / 2), -1, -1):
            Sorting.heapify(arr, i)

    @staticmethod
    def heapify(arr, i):
        left = 2 * i + 1
        right = 2 * i + 2
        largest = i
        arrLen = len(arr)
        if left < arrLen and arr[left] > arr[largest]:
            largest = left
        if right < arrLen and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            Sorting.swap(arr, i, largest)
            Sorting.heapify(arr, largest)

    @staticmethod
    def swap(arr, i, j):
        arr[i], arr[j] = arr[j], arr[i]

    @staticmethod
    def heapSort(arr):
        global arrLen
        arrLen = len(arr)
        Sorting.buildMaxHeap(arr)
        for i in range(len(arr) - 1, 0, -1):
            Sorting.swap(arr, 0, i)
            arrLen -= 1
            Sorting.heapify(arr, 0)
        return arr

    @staticmethod
    def countingSort(arr, maxValue):
        """ 计数排序 """
        bucketLen = maxValue + 1
        bucket = [0] * bucketLen
        sortedIndex = 0
        arrLen = len(arr)
        for i in range(arrLen):
            if not bucket[arr[i]]:
                bucket[arr[i]] = 0
            bucket[arr[i]] += 1
        for j in range(bucketLen):
            while bucket[j] > 0:
                arr[sortedIndex] = j
                sortedIndex += 1
                bucket[j] -= 1
        return arr

    @staticmethod
    def radixSort(A):
        """ 基数排序一般用于长度相同的元素组成的数组 """
        # A = [random.randint(1, 9999) for i in range(10000)]
        for k in range(4):  # 4轮排序
            s = [[] for i in range(10)]
            for i in A:
                s[(i // (10 ** k)) % 10].append(i)
            A = [a for b in s for a in b]
        return A

    @staticmethod
    def toInt(str_num):
        """ 字符串转数字算法实现 """
        number = 0  # 强制初始化
        for i in range(0, len(str_num), 1):
            digit = int(str_num[i])
            number += digit * pow(10, i)
            print(f'{i}:{digit}, all={number}')
            # number = (char)( - 48) + * number * 10    # 逐一取字符转换为数字，并升权放入number
        return number


class BucketSort(object):
    """范围为1-M的桶排序 """

    def _max(self, oldlist):
        _max = oldlist[0]
        for i in oldlist:
            if i > _max:
                _max = i
        return _max

    def _min(self, oldlist):
        _min = oldlist[0]
        for i in oldlist:
            if i < _min:
                _min = i
        return _min

    def sort(self, oldlist):
        _max = self._max(oldlist)
        _min = self._min(oldlist)
        s = [0 for i in range(_min, _max + 1)]
        for i in oldlist:
            s[i - _min] += 1
        current = _min
        n = 0
        for i in s:
            while i > 0:
                oldlist[n] = current
                i -= 1
                n += 1
            current += 1

    def __call__(self, oldlist):
        self.sort(oldlist)
        return oldlist


class GeneticAlgorithm(object):
    # chromosome = None   # 染色体，二进制数，位数各异

    @staticmethod
    def init(group_size, len1, len2):
        """
        种群初始化，随机生成0与1组成的染色体
        :param group_size: 种群规模
        :param len1: 染色体1长度
        :param len2: 染色体2长度
        :return: 初始化的种群
        """
        group = []
        for i in range(group_size):
            chromosome = ''
            for j in range(len1 + len2):
                chromosome += str(random.randint(0, 1))
            group.append(chromosome)
        return group

    @staticmethod
    def func(group, len1, len2):
        """
            适应度函数 max[ f(x1,x2) = 21.5+x1*sin(4*pi*x1 + x2*sin(20*pi*x2) ]
                          -3.0 <= x1 <= 12.1    4.1 <= x2 <= 5.8
            根据染色体长度，将整段染色体分隔成两个小染色体，
            然后转换成10进制，带入函数，结果就是适应度f，以求最大的f
            :param group: 种群
            :param len1: 染色体1的长度
            :param len2:
            :return: 种群中各染色体的适应度
        """
        eva = []
        for i in range(len(group)):
            temp1 = ''.decode(group[i][:len1])
            temp2 = ''.decode(group[i][len1:])
            x_1 = -3.0 + temp1 * (12.1 + 3.0) / (pow(2, len1) - 1)
            x_2 = 4.1 + temp2 * (5.8 - 4.1) / (pow(2, len2) - 1)
            temp = 21.5 + x_1 * math.sin(4 * math.pi * x_1) + x_2 * math.sin(20 * math.pi * x_2)

            temp = 0 if temp < 0 else temp
            eva.append(temp)

        return eva

    @staticmethod
    def selection(group, len1, len2):
        """
            轮盘赌选择淘汰的个体，概率跟适应度正相关
            :param group:
            :param len1:
            :param len2:
            :return: 优胜劣汰后的新种群
        """
        eva = GeneticAlgorithm.func(group, len1, len2)
        sum_eva = sum(eva)
        prob = []
        temp = 0
        new_group = []
        for e in eva:
            temp += e/sum_eva
            prob.append(temp)   # 台阶状的数字列表
        for i in range(len(prob)):
            rand = random.random()
            j = 0
            while j < len(group):
                if rand < prob[j]:
                    new_group.append(group[j])
                    break
                else:
                    break


class Population:
    # 种群的设计
    def __init__(self, size, chrom_size, cp, mp, gen_max):
        # 种群信息合
        self.individuals = []  # 个体集合
        self.fitness = []  # 个体适应度集
        self.selector_probability = []  # 个体选择概率集合
        self.new_individuals = []  # 新一代个体集合

        self.elitist = {'chromosome': [0, 0], 'fitness': 0, 'age': 0}  # 最佳个体的信息

        self.size = size  # 种群所包含的个体数
        self.chromosome_size = chrom_size  # 个体的染色体长度
        self.crossover_probability = cp  # 个体之间的交叉概率
        self.mutation_probability = mp  # 个体之间的变异概率

        self.generation_max = gen_max  # 种群进化的最大世代数
        self.age = 0  # 种群当前所处世代

        # 随机产生初始个体集，并将新一代个体、适应度、选择概率等集合以 0 值进行初始化
        v = 2 ** self.chromosome_size - 1
        for i in range(self.size):
            self.individuals.append([random.randint(0, v), random.randint(0, v)])
            self.new_individuals.append([0, 0])
            self.fitness.append(0)
            self.selector_probability.append(0)

    # 基于轮盘赌博机的选择
    def decode(self, interval, chromosome):
        '''将一个染色体 chromosome 映射为区间 interval 之内的数值'''
        d = interval[1] - interval[0]
        n = float(2 ** self.chromosome_size - 1)
        return (interval[0] + chromosome * d / n)

    def fitness_func(self, chrom1, chrom2):
        '''适应度函数，可以根据个体的两个染色体计算出该个体的适应度'''
        interval = [-10.0, 10.0]
        (x, y) = (self.decode(interval, chrom1),
                  self.decode(interval, chrom2))
        n = lambda x, y: math.sin(math.sqrt(x * x + y * y)) ** 2 - 0.5
        d = lambda x, y: (1 + 0.001 * (x * x + y * y)) ** 2
        func = lambda x, y: 0.5 - n(x, y) / d(x, y)
        return func(x, y)

    def evaluate(self):
        '''用于评估种群中的个体集合 self.individuals 中各个个体的适应度'''
        sp = self.selector_probability
        for i in range(self.size):
            self.fitness[i] = self.fitness_func(self.individuals[i][0],  # 将计算结果保存在 self.fitness 列表中
                                                self.individuals[i][1])
        ft_sum = sum(self.fitness)
        for i in range(self.size):
            sp[i] = self.fitness[i] / float(ft_sum)  # 得到各个个体的生存概率
        for i in range(1, self.size):
            sp[i] = sp[i] + sp[i - 1]  # 需要将个体的生存概率进行叠加，从而计算出各个个体的选择概率

    # 轮盘赌博机（选择）
    def select(self):
        (t, i) = (random.random(), 0)
        for p in self.selector_probability:
            if p > t:
                break
            i = i + 1
        return i

    # 交叉
    def cross(self, chrom1, chrom2):
        p = random.random()  # 随机概率
        n = 2 ** self.chromosome_size - 1
        if chrom1 != chrom2 and p < self.crossover_probability:
            t = random.randint(1, self.chromosome_size - 1)  # 随机选择一点（单点交叉）
            mask = n << t  # << 左移运算符
            (r1, r2) = (chrom1 & mask, chrom2 & mask)  # & 按位与运算符：参与运算的两个值,如果两个相应位都为1,则该位的结果为1,否则为0
            mask = n >> (self.chromosome_size - t)
            (l1, l2) = (chrom1 & mask, chrom2 & mask)
            (chrom1, chrom2) = (r1 + l2, r2 + l1)
        return (chrom1, chrom2)

    # 变异
    def mutate(self, chrom):
        p = random.random()
        if p < self.mutation_probability:
            t = random.randint(1, self.chromosome_size)
            mask1 = 1 << (t - 1)
            mask2 = chrom & mask1
            if mask2 > 0:
                chrom = chrom & (~mask2)  # ~ 按位取反运算符：对数据的每个二进制位取反,即把1变为0,把0变为1
            else:
                chrom = chrom ^ mask1  # ^ 按位异或运算符：当两对应的二进位相异时，结果为1
        return chrom

    # 保留最佳个体
    def reproduct_elitist(self):
        # 与当前种群进行适应度比较，更新最佳个体
        j = -1
        for i in range(self.size):
            if self.elitist['fitness'] < self.fitness[i]:
                j = i
                self.elitist['fitness'] = self.fitness[i]
        if (j >= 0):
            self.elitist['chromosome'][0] = self.individuals[j][0]
            self.elitist['chromosome'][1] = self.individuals[j][1]
            self.elitist['age'] = self.age

    # 进化过程
    def evolve(self):
        indvs = self.individuals
        new_indvs = self.new_individuals
        # 计算适应度及选择概率
        self.evaluate()
        # 进化操作
        i = 0
        while True:
            # 选择两个个体，进行交叉与变异，产生新的种群
            idv1 = self.select()
            idv2 = self.select()
            # 交叉
            (idv1_x, idv1_y) = (indvs[idv1][0], indvs[idv1][1])
            (idv2_x, idv2_y) = (indvs[idv2][0], indvs[idv2][1])
            (idv1_x, idv2_x) = self.cross(idv1_x, idv2_x)
            (idv1_y, idv2_y) = self.cross(idv1_y, idv2_y)
            # 变异
            (idv1_x, idv1_y) = (self.mutate(idv1_x), self.mutate(idv1_y))
            (idv2_x, idv2_y) = (self.mutate(idv2_x), self.mutate(idv2_y))
            (new_indvs[i][0], new_indvs[i][1]) = (idv1_x, idv1_y)  # 将计算结果保存于新的个体集合self.new_individuals中
            (new_indvs[i + 1][0], new_indvs[i + 1][1]) = (idv2_x, idv2_y)
            # 判断进化过程是否结束
            i = i + 2  # 循环self.size/2次，每次从self.individuals 中选出2个
            if i >= self.size:
                break

        # 最佳个体保留
        # 如果在选择之前保留当前最佳个体，最终能收敛到全局最优解。
        self.reproduct_elitist()

        # 更新换代：用种群进化生成的新个体集合 self.new_individuals 替换当前个体集合
        for i in range(self.size):
            self.individuals[i][0] = self.new_individuals[i][0]
            self.individuals[i][1] = self.new_individuals[i][1]

    def run(self):
        '''根据种群最大进化世代数设定了一个循环。
        在循环过程中，调用 evolve 函数进行种群进化计算，并输出种群的每一代的个体适应度最大值、平均值和最小值。'''
        for i in range(self.generation_max):
            self.evolve()
            print(i, max(self.fitness), sum(self.fitness) / self.size, min(self.fitness))


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setup_ui()

        self.count = 5
        self.arr = [(random.randint(0, 1)) for j in range(self.count)]
        self.text = ''.join(str(i) for i in self.arr)
        # self.num = Sorting.toInt(self.text)
        # print(self.num)
        # # print(self.arr)

    def setup_ui(self):
        self.setWindowTitle('排序算法')
        self.setGeometry(0, 0, 850, 600)
        self.center()

        vl_main = QtWidgets.QVBoxLayout(self)
        btn = QtWidgets.QPushButton('排序')
        btn.clicked.connect(self.clicked)
        btn.setGeometry(100, 100, 100, 100)
        vl_main.setAlignment(QtCore.Qt.AlignTop)
        vl_main.addWidget(btn)
        # vl_main.addWidget()

        self.show()

    def clicked(self):
        # Sorting.bubbleSort(self.arr)
        # Sorting.selectionSort(self.arr)
        # Sorting.insertionSort(self.arr)
        # Sorting.shellSort(self.arr)
        # Sorting.mergeSort(self.arr)
        # Sorting.quickSort(self.arr)
        # Sorting.buildMaxHeap(self.arr)
        # Sorting.countingSort(self.arr, 100)
        # bucketSort()(self.arr)
        # Sorting.radixSort(self.arr)

        self.arr = [(random.randint(0, 1)) for j in range(self.count)]
        self.text = ''.join(str(i) for i in self.arr)
        num = random.randint(1, 100)
        bb = bin(num)
        print(f'{num} : {bb} -> {int(bb, 2)}')
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        # self.drawRectangles(qp)

        qp.end()

    def drawText(self, event, qp):
        qp.setPen(QtGui.QColor(168, 3, 34))
        qp.setFont(QtGui.QFont('Decorative', 20))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)

    def drawRectangles(self, qp):
        qp.setPen(QtGui.QColor(3, 34, 168))
        qp.setFont(QtGui.QFont('Decorative', 20))

        for i in range(self.count):
            qp.setBrush(QtGui.QColor('#87CEFA'))  # #DAA520  	#228B22
            qp.drawRect(50 + i * 60, 350 - self.arr[i] * 2, 55, self.arr[i] * 2)

            qp.drawText(50 + i * 60, 350, 60, 50, QtCore.Qt.AlignCenter, str(self.arr[i]))

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resizeEvent(self, event):
        palette = QtGui.QPalette()
        pix = QtGui.QPixmap('res/images/background.jpg')
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(palette)


if __name__ == '__main__':
    # app = QtWidgets.QApplication(sys.argv)
    # win = MainWindow()
    # sys.exit(app.exec_())

    # 种群的个体数量为 50，染色体长度为 25，交叉概率为 0.8，变异概率为 0.1,进化最大世代数为 150
    pop = Population(50, 24, 0.8, 0.1, 150)
    pop.run()
