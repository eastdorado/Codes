#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @项目名称: python
# @File    : test4.py
# @Time    : 2020/1/24 13:18
# @Author  : big
# @Email   : shdorado@126.com

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QCursor, QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QGraphicsOpacityEffect, \
    QGraphicsBlurEffect, QGraphicsPixmapItem, QGraphicsItem
import sys
import math
from enum import Enum, IntEnum, unique


# @unique  # 装饰器可以帮助我们检查保证value没有重复值
class Const(IntEnum):
    # 继承于Enum的枚举类中的Key不能相同，Value可以相，要Value也不能相同，那么在导入Enum的同时，需要导入unique函数
    # 枚举项可以用来比较，使用==，或者is。枚举类不能用来实例化对象,在类外部不能修改Value值
    OTHER = '0'
    CENTER = '0'
    TOP = 1
    BOTTOM = '2'
    LEFT = 3
    RIGHT = 4
    TL_CORNER = 5  # 左上角
    TR_CORNER = 6  # 右上角
    BL_CORNER = 7
    BR_CORNER = 8

    PADDING = 50  # 边距
    MARGIN = 15  # 四周边距


PADDING = 50  # 边距


# sys.setrecursionlimit(10000)


class ShadowWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ShadowWidget, self).__init__(parent)
        self.pixmaps = []

        # # 设置具体阴影
        # shadowEffect = QGraphicsDropShadowEffect(self)
        # shadowEffect.setOffset(0, 0)
        # # 阴影颜色
        # shadowEffect.setColor(QColor(38, 78, 119, 127))
        # # 阴影半径
        # shadowEffect.setBlurRadius(22)
        # self.setGraphicsEffect(shadowEffect)
        #
        # opacityEffect = QGraphicsOpacityEffect()
        # opacityEffect.setOpacity(0.2)
        # label0 = QtWidgets.QLabel()
        # label0.setPixmap(QPixmap(":/image/1.jpg").scaled(300, 200))
        # label0.setGraphicsEffect(opacityEffect)
        # self.layout().addWidget(label0)
        #
        # blurEffect = QGraphicsBlurEffect()
        # blurEffect.setBlurRadius(5)
        # pixmapItem = QGraphicsPixmapItem()
        # pixmapItem.setPixmap(QPixmap(":/image/1.jpg").scaled(300, 200))
        # pixmapItem.setGraphicsEffect(blurEffect)
        # pixmapItem.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        #
        # ui->graphicsView->setScene(new
        # QGraphicsScene);
        # ui->graphicsView->scene()->addItem(pixmapItem);
        #

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.SHADOW_WIDTH = 0  # 边框距离
        self.isLeftPressDown = False  # 鼠标左键是否按下
        self.LOCATION = Const.OTHER
        self.dragPosition = 0  # 拖动时坐标
        self.Numbers = type('Enum', (), dict(UP=0, DOWN=1, LEFT=2, RIGHT=3, LEFTTOP=4,
                                             LEFTBOTTOM=5, RIGHTBOTTOM=6, RIGHTTOP=7, NONE=8))  # 枚举参数
        print(type(self.Numbers))
        # self.setMinimumHeight(500)  # 窗体最小高度
        # self.setMinimumWidth(800)  # 窗体最小宽度
        self.dir = self.Numbers.NONE  # 初始鼠标状态
        self.setMouseTracking(True)

    # 绘制边框阴影
    def drawShadow(self, painter):
        # 绘制左上角、左下角、右上角、右下角、上、下、左、右边框
        self.pixmaps.append("./res/images/left_top.png")
        self.pixmaps.append("./img/border/left_bottom.png")
        self.pixmaps.append("./img/border/right_top.png")
        self.pixmaps.append("./img/border/right_bottom.png")
        self.pixmaps.append("./img/border/top_mid.png")
        self.pixmaps.append("./img/border/bottom_mid.png")
        self.pixmaps.append("./img/border/left_mid.png")
        self.pixmaps.append("./img/border/right_mid.png")
        painter.drawPixmap(0, 0, self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[0]))  # 左上角
        painter.drawPixmap(self.width() - self.SHADOW_WIDTH, 0, self.SHADOW_WIDTH, self.SHADOW_WIDTH,
                           QPixmap(self.pixmaps[2]))  # 右上角
        painter.drawPixmap(0, self.height() - self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.SHADOW_WIDTH,
                           QPixmap(self.pixmaps[1]))  # 左下角
        painter.drawPixmap(self.width() - self.SHADOW_WIDTH, self.height() - self.SHADOW_WIDTH, self.SHADOW_WIDTH,
                           self.SHADOW_WIDTH, QPixmap(self.pixmaps[3]))  # 右下角
        painter.drawPixmap(0, self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.height() - 2 * self.SHADOW_WIDTH,
                           QPixmap(self.pixmaps[6]).scaled(self.SHADOW_WIDTH,
                                                           self.height() - 2 * self.SHADOW_WIDTH))  # 左
        painter.drawPixmap(self.width() - self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.SHADOW_WIDTH,
                           self.height() - 2 * self.SHADOW_WIDTH, QPixmap(self.pixmaps[7]).scaled(self.SHADOW_WIDTH,
                                                                                                  self.height() - 2 * self.SHADOW_WIDTH))  # 右
        painter.drawPixmap(self.SHADOW_WIDTH, 0, self.width() - 2 * self.SHADOW_WIDTH, self.SHADOW_WIDTH,
                           QPixmap(self.pixmaps[4]).scaled(self.width() - 2 * self.SHADOW_WIDTH,
                                                           self.SHADOW_WIDTH))  # 上
        painter.drawPixmap(self.SHADOW_WIDTH, self.height() - self.SHADOW_WIDTH, self.width() - 2 * self.SHADOW_WIDTH,
                           self.SHADOW_WIDTH, QPixmap(self.pixmaps[5]).scaled(self.width() - 2 * self.SHADOW_WIDTH,
                                                                              self.SHADOW_WIDTH))  # 下

    # 枚举参数

    def enum(self, **enums):
        return type('Enum', (), enums)

    def region(self, cursorGlobalPoint):
        # 获取窗体在屏幕上的位置区域，tl为topleft点，rb为rightbottom点
        rect = self.rect()
        tl = self.mapToGlobal(rect.topLeft())
        br = self.mapToGlobal(rect.bottomRight())

        x = cursorGlobalPoint.x()
        y = cursorGlobalPoint.y()

        if tl.x() <= x <= tl.x() + PADDING and tl.y() <= y <= tl.y() + PADDING:
            # 左上角内侧
            self.dir = self.Numbers.LEFTTOP
            self.setCursor(QCursor(Qt.SizeFDiagCursor))  # 设置鼠标形状
        elif br.x() - PADDING <= x <= br.x() and br.y() - PADDING <= y <= br.y():
            # 右下角内侧
            self.dir = self.Numbers.RIGHTBOTTOM
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif tl.x() <= x <= tl.x() + PADDING and br.y() - PADDING <= y <= br.y():
            # 左下角内侧
            self.dir = self.Numbers.LEFTBOTTOM
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif br.x() - PADDING <= x <= br.x() and tl.y() <= y <= tl.y() + PADDING:
            # 右上角内侧
            self.dir = self.Numbers.RIGHTTOP
            self.setCursor(QCursor(Qt.SizeBDiagCursor))

        elif tl.x() - PADDING <= x <= tl.x() + PADDING:
            # 左边内侧
            self.dir = self.Numbers.LEFT
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif br.x() - PADDING <= x <= br.x():
            # 右边内侧
            self.dir = self.Numbers.RIGHT
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif tl.y() <= y <= tl.y() + PADDING:
            # 上边
            self.dir = self.Numbers.UP
            self.setCursor(QCursor(Qt.SizeVerCursor))
        elif br.y() - PADDING <= y <= br.y():
            # 下边
            self.dir = self.Numbers.DOWN
            self.setCursor(QCursor(Qt.SizeVerCursor))
        else:
            # 默认
            self.dir = self.Numbers.NONE
            self.setCursor(QtGui.QCursor(Qt.ArrowCursor))
        print(self.dir)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.isLeftPressDown = False
            if self.dir != self.Numbers.NONE:  # 非边线附件的一律改回鼠标形状
                self.releaseMouse()
                self.setCursor(QtGui.QCursor(Qt.ArrowCursor))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.isLeftPressDown = True
            if self.dir != self.Numbers.NONE:
                self.mouseGrabber()  # 得到正在捕获键盘事件的窗口
            else:
                self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        # print(type(event))
        gloPoint = event.globalPos()
        rect = self.rect()
        tl = self.mapToGlobal(rect.topLeft())
        rb = self.mapToGlobal(rect.bottomRight())

        if not self.isLeftPressDown:
            self.region(gloPoint)
        else:
            if (self.dir != self.Numbers.NONE):
                rmove = QtCore.QRect(tl, rb)
                if (self.dir == self.Numbers.LEFT):
                    # if (rb.x() - gloPoint.x() <= self.minimumWidth()):
                    #     rmove.setX(tl.x())
                    # else:
                        rmove.setX(gloPoint.x())
                elif (self.dir == self.Numbers.RIGHT):
                    rmove.setWidth(gloPoint.x() - tl.x())
                elif (self.dir == self.Numbers.UP):
                    if (rb.y() - gloPoint.y() <= self.minimumHeight()):
                        rmove.setY(tl.y())
                    else:
                        rmove.setY(gloPoint.y())
                elif (self.dir == self.Numbers.DOWN):
                    rmove.setHeight(gloPoint.y() - tl.y())
                elif (self.dir == self.Numbers.LEFTTOP):
                    if (rb.x() - gloPoint.x() <= self.minimumWidth()):
                        rmove.setX(tl.x())
                    else:
                        rmove.setX(gloPoint.x())
                    if (rb.y() - gloPoint.y() <= self.minimumHeight()):
                        rmove.setY(tl.y())
                    else:
                        rmove.setY(gloPoint.y())
                elif (self.dir == self.Numbers.RIGHTTOP):
                    rmove.setWidth(gloPoint.x() - tl.x())
                    rmove.setY(gloPoint.y())
                elif (self.dir == self.Numbers.LEFTBOTTOM):
                    rmove.setX(gloPoint.x())
                    rmove.setHeight(gloPoint.y() - tl.y())
                elif (self.dir == self.Numbers.RIGHTBOTTOM):
                    rmove.setWidth(gloPoint.x() - tl.x())
                    rmove.setHeight(gloPoint.y() - tl.y())
                else:
                    pass
                self.setGeometry(rmove)
            else:
                self.move(event.globalPos() - self.dragPosition)
                event.accept()

    def paintEvent(self, event):
        # 四周都有阴影的
        m = 9
        path = QtGui.QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRect(m, m, self.width() - m * 2, self.height() - m * 2)
        painter = QtGui.QPainter(self)
        # painter.setRenderHint(QPainter.Antialiasing, True)
        painter.fillPath(path, QtGui.QBrush(Qt.white))

        color = QColor(100, 100, 100, 30)
        # for(int i=0; i<10; i++)

        for i in range(m):
            path = QtGui.QPainterPath()
            path.setFillRule(Qt.WindingFill)
            path.addRoundedRect(m - i, m - i, self.width() - (m - i) * 2, self.height() - (m - i) * 2, 1, 1)

            al = 90 - math.sqrt(i) * 30
            print(al)
            color.setAlpha(int(al))
            painter.setPen(QtGui.QPen(color, 1, Qt.SolidLine))
            painter.drawRoundedRect(QtCore.QRect(m - i, m - i, self.width() - (m - i) * 2, self.height() - (m - i) * 2),
                                    0, 0)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    shadow = ShadowWidget()
    shadow.show()
    sys.exit(app.exec_())
