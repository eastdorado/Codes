#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class QLabel_scro(QLabel):
    """
    滚动条的按钮
    """
    move_scroll = pyqtSignal()  # 定义一个信号
    widget_bottom = 0  # 这里是获得 scro（滚动条） 高度的值
    last_move = 0  # 这个是用来存放上一次移动了滚动按钮的顶点值的值

    def __init__(self, *args):
        super(QLabel_scro, self).__init__(*args)

    # 鼠标点击
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:  # 只接受左键点击
            self._drag = True  # 这个是用来判断是否被点击
            self._DragPosition = e.globalPos() - self.pos()  # 这个是获得滚动按钮的顶点值距离中心点的值
            e.accept()
            self.setCursor(QCursor(Qt.PointingHandCursor))  # 改变鼠标指针

    # 鼠标释放
    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._drag = False  # 将是否点击变成 false
            self.setCursor(QCursor(Qt.ArrowCursor))  # 改变鼠标指针

    def mouseMoveEvent(self, e):
        if self.last_move == 0:  # 判断是否为0 （第一次启动要变成这个，不然会报错，因为函数在类这个全局中创建了）
            self.last_move = self.pos().y()  # 将值变成按钮顶点的值
        self.demove = self.pos().y() - self.last_move  # 这里是移动后的值减去上一次移动的值
        self.move_scroll.emit()  # 传到信号
        self.last_move = self.pos().y()  # 获得当前的值
        yx = (e.globalPos() - self._DragPosition).y()  # 这里是将当前按钮的中心点减去滚动按钮的顶点值距离中心点的值就可以获得当前按钮的顶点值
        _yx = yx + self.height()  # 这里是将顶点的值加上自身的高度就等于底端的值了
        if _yx <= self.widget_bottom and yx >= 0:  # 给按钮的移动限制范围 （就是底端的值不能超过滚动条的高度，顶点的值不能小于0）
            self.move(0, yx)  # 符合就移动
            e.accept()


class QS(QScrollArea):

    def __init__(self, *args):
        super(QS, self).__init__(*args)

    def wheelEvent(self, e):
        pass  # 这里是取消了原有的滚动条滚动时的操作 以免出现滚动了而我们自己的滚动条按钮没有变化


class Ui_Form(QWidget):
    def __init__(self, parent=None):
        super(Ui_Form, self).__init__(parent=None)
        self.setObjectName("self")
        self.resize(600, 600)
        self.scroll_area = QS(self)  # 建立滚动范围
        self.scroll_area.setGeometry(0, 0, 400, 400)
        self.scroll_area.setWidgetResizable(True)  # 将自动调整大小关闭
        self.scroll_bar = self.scroll_area.verticalScrollBar()  # 重要的一步，获取滚动范围的滚动条！！！

        self.scroll_contents = QWidget()  # 创建一个可以被滚动的视口
        self.scroll_contents.setGeometry(0, 0, 400, 800)
        self.scroll_contents.setMinimumSize(380, 1000)  # 可要可不要

        self.label_1 = QLabel(self.scroll_contents)
        self.label_1.move(50, 100)
        self.label_1.setText("HelloRyan")

        self.label_2 = QLabel(self.scroll_contents)
        self.label_2.move(50, 200)
        self.label_2.setText("你好")

        self.label_3 = QLabel(self.scroll_contents)
        self.label_3.move(50, 300)
        self.label_3.setText("-----------")

        self.label_4 = QLabel(self.scroll_contents)
        self.label_4.move(50, 400)
        self.label_4.setText("542543255235432543252")

        self.label_5 = QLabel(self.scroll_contents)
        self.label_5.move(50, 500)
        self.label_5.setText("5432543262542")

        self.label_6 = QLabel(self.scroll_contents)
        self.label_6.move(50, 600)
        self.label_6.setText("4325432532")

        self.scroll_area.setWidget(self.scroll_contents)
        self.scroll_area.installEventFilter(self)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)
        # ----------------------------------------------------

        self.scro = QWidget(self)  # 创建滚动条
        self.scro.setGeometry(QRect(500, 20, 10, self.scroll_area.height()))
        self.scro.setObjectName("widget")
        self.scro.setStyleSheet("QWidget{background-color:#fff;}")
        self.scro_w = QLabel_scro(self.scro)  # 创建滚动按钮
        self.scro_w.widget_bottom = self.scro.height()  # 将滚动条的高度传到到滚动按钮 这一步是为了适应改变了滚动条高度的问题和对于滚动按钮的限制
        self.scro_w.setGeometry(QRect(0, 0, 10, 81))
        self.scro_w.setStyleSheet("QLabel{background-color:#d7d7d7;border-radius:5px;}\n"
                                  "QLabel:hover{background-color:#b3b3b3;}")
        self.scro_w.setObjectName("label")

        self.scro_w.move_scroll.connect(self.Move)  # 连接事件
        # self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 将滚动范围的滚动条关闭

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("self", "self"))

    def wheelEvent(self, e):
        y = self.scro_w.pos().y()  # 获得滚动按钮的顶点位置
        _y = y + self.scro_w.height()  # 获得滚动按钮的底部位置
        if e.angleDelta().y() < 0:  # 这个是获得鼠标滚轮的值 它的值只有 120 和 -120 由此来判断是向上还是向下移动
            if _y <= self.scro_w.widget_bottom and y >= 0:  # 限制范围
                if (_y + 10) >= self.scro_w.widget_bottom:  # 因为以10的值来增加肯定会超出滚动条的范围的，所以这个是预先判断下一次向下滚动是否会超过滚动条的高度
                    self.scro_w.move(0, self.scro_w.widget_bottom - self.scro_w.height())  # 如果超过就取当按钮到底部时按钮的顶部位置
                    self.scroll_bar.setValue(
                        623)  # 这里面的值是滚动范围的滚动条的最大值，如果不知道最大值是多少请自行使用下面被注释的# print(self.scroll_bar.value())来查看
                else:
                    self.scro_w.move(0, y + 10)  # 如果不是就将滚动按钮移动位置
                    self.scroll_bar.setValue(self.scroll_bar.value() + 20)  # 同时移动滚动范围的滚动条
        else:
            if _y <= self.scro_w.widget_bottom and y >= 0:  # 限制范围
                if (y - 10) <= 0:  # 同样的预先判断下一次向上滚动是否会超过 0
                    self.scro_w.move(0, 0)  # 这里就很简单了，就直接给 0 即可
                    self.scroll_bar.setValue(0)  # 同样的给上滚动范围的滚动条的值
                else:
                    self.scro_w.move(0, y - 10)  # 如果不是就将滚动按钮移动位置
                    self.scroll_bar.setValue(self.scroll_bar.value() - 20)  # 同时移动滚动范围的滚动条的值

    def Move(self):
        # self.scroll_bar.setValue(self.scroll_bar.value() + (self.scro_w.demove * 2))  # 给滚动条的值移动滚动条使可视区域改变 （这里的乘2要根据你自己来判断是否要或者不要）
        self.scroll_bar.setValue(self.scroll_bar.value() + self.scro_w.demove)  # 一般是不要的，不知道这里的算法为什么有问题
        # print(self.scroll_bar.value())


import numpy as np

if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # ex = Ui_Form()
    # ex.show()
    # sys.exit(app.exec_())
    a = [88, 99]
    b, c = a
    print(b, c, a)
    b = 2 - 9 % 2
    print(b, c, a)
