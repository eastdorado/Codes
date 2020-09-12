#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @项目名称: python
# @File    : multProsses.py
# @Time    : 2020/2/21 2:36
# @Author  : big
# @Email   : shdorado@126.com

import sys
import os
import multiprocessing
import time
import random
from PySide2 import QtCore, QtGui, QtWidgets
from utilities import Utils


def test1(msg):
    t_start = time.time()
    print("%s开始执行，进程号为%d" % (msg, os.getpid()))
    time.sleep(random.random() * 2)
    t_stop = time.time()
    print("%s执行完成，耗时%.2f" % (msg, t_stop - t_start))


def multpross():
    po = multiprocessing.Pool(3)
    for i in range(0, 10):
        # Pool().apply_async(要调用的目标,(传递给目标的参数元祖,))
        # 每次循环将会用空闲出来的子进程去调用目标
        po.apply_async(test1, (i,))
        # po.apply(test1, (i,))

    print("-----start-----")
    po.close()  # 关闭进程池，关闭后po不再接收新的请求
    # apply_async(func[, args[, kwds]]) ：
    # 使用非阻塞方式调用func（并行执行，堵塞方式必须等待上一个进程退出才能执行下一个进程），
    # args为传递给func的参数列表，kwds为传递给func的关键字参数列表
    # terminate()：不管任务是否完成，立即终止
    po.join()  # 主进程阻塞，等待po中所有子进程执行完成退出， 必须在close或terminate之后使用
    print("-----end-----")


def write(q):
    print("write启动(%s)，父进程为(%s)" % (os.getpid(), os.getppid()))
    for i in "python":
        q.put(i)


def read(q):
    print("read启动(%s)，父进程为(%s)" % (os.getpid(), os.getppid()))
    for i in range(q.qsize()):
        print("read从Queue获取到消息：%s" % q.get(True))


def data():
    print("(%s) start" % os.getpid())
    q = multiprocessing.Manager().Queue()
    po = multiprocessing.Pool()
    po.apply_async(write, args=(q,))

    # time.sleep(2)

    po.apply_async(read, args=(q,))
    po.close()
    po.join()

    print("(%s) end" % os.getpid())


class MutP:
    def __init__(self):
        cpu_num = Utils.GetCpuInfo()[0]
        # print(cpu_num)
        # self.pool = multiprocessing.Pool()
        self.pool = multiprocessing.Pool(processes=cpu_num)  # 根据cpu个数创建进程池里的进程个数
        # 如果不设置参数,函数会跟根据计算机的实际情况来决定要运行多少个进程，自己设置要考虑计算机的性能

    def run(self, fun, args):
        # print('run', args)
        result = self.pool.apply_async(fun, (args,))
        # print(results.get())
        # time.sleep(3)
        return result

    def end(self):
        self.pool.close()
        self.pool.join()


class Test:
    def __init__(self):
        self.data = 'dddddd'
        self.do()

    # @staticmethod
    def func(self, i):
        print(self.data, i)
        # time.sleep(0.2)
        # return i

    def do(self):
        po = MutP()
        num = 10
        results = [po.run(self.func, i) for i in range(num)]
        po.end()

        # print(results)

        # time.sleep(3)
        # for res in results:
        #     print(res.get())
        # return results


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        # self.setupUI(self)
        # self.resize(500, 375)

        # TODO 修改原始控件
        self.do()

    def func(self, i):
        print(self.data, i)
        # time.sleep(0.2)
        # return i

    def do(self):
        print('do')
        po = MutP()
        num = 10
        results = [po.run(self.func, i) for i in range(num)]
        po.end()

    def resizeEvent(self, event):
        palette = QtGui.QPalette()
        pix = QtGui.QPixmap('res/images/background.jpg')
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(palette)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
    # multpross()
    # data()
    # t = Test()
    # t.do()
