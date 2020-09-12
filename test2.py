#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @项目名称: python
# @File    : test2.py
# @Time    : 2020/1/13 18:19
# @Author  : big
# @Email   : shdorado@126.com

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QBitmap
from PyQt5 import QtCore, QtGui, QtWidgets


class DropListWidget(QtWidgets.QListWidget):
    # 可以拖进来的QListWidget
    def __init__(self, *args, **kwargs):
        super(DropListWidget, self).__init__(*args, **kwargs)
        self.resize(400, 400)
        self.setAcceptDrops(True)
        # 设置从左到右、自动换行、依次排列
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        # item的间隔
        self.setSpacing(5)

    def makeItem(self, size, cname):
        item = QtWidgets.QListWidgetItem(self)
        item.setData(QtCore.Qt.UserRole + 1, cname)  # 把颜色放进自定义的data里面
        item.setSizeHint(size)
        label = QtWidgets.QLabel(self)  # 自定义控件
        label.setMargin(2)  # 往内缩进2
        label.resize(size)
        pixmap = QPixmap(size.scaled(96, 96, QtCore.Qt.IgnoreAspectRatio))  # 调整尺寸
        pixmap.fill(QtGui.QColor(cname))
        label.setPixmap(pixmap)
        self.setItemWidget(item, label)

    def dragEnterEvent(self, event):
        mimeData = event.mimeData()
        if not mimeData.property('myItems'):
            event.ignore()
        else:
            event.acceptProposedAction()

    def dropEvent(self, event):
        # 获取拖放的items
        items = event.mimeData().property('myItems')
        event.accept()
        for item in items:
            # 取出item里的data并生成item
            self.makeItem(QtCore.QSize(100, 100), item.data(QtCore.Qt.UserRole + 1))


class DragListWidget(QtWidgets.QListWidget):
    # 可以往外拖的QListWidget
    def __init__(self, *args, **kwargs):
        super(DragListWidget, self).__init__(*args, **kwargs)
        self.resize(400, 400)
        # 隐藏横向滚动条
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # 不能编辑
        self.setEditTriggers(self.NoEditTriggers)
        # 开启拖功能
        self.setDragEnabled(True)
        # 只能往外拖
        self.setDragDropMode(self.DragOnly)
        # 忽略放
        self.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        # ****重要的一句（作用是可以单选，多选。Ctrl、Shift多选，可从空白位置框选）****
        # ****不能用ExtendedSelection,因为它可以在选中item后继续框选会和拖拽冲突****
        self.setSelectionMode(self.ContiguousSelection)
        # 设置从左到右、自动换行、依次排列
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        # item的间隔
        self.setSpacing(5)
        # 橡皮筋(用于框选效果)
        self._rubberPos = None
        self._rubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)

        self.initItems()

    # 实现拖拽的时候预览效果图
    # 这里演示拼接所有的item截图(也可以自己写算法实现堆叠效果)
    def startDrag(self, supportedActions):
        items = self.selectedItems()
        drag = QtGui.QDrag(self)
        mimeData = self.mimeData(items)
        # 由于QMimeData只能设置image、urls、str、bytes等等不方便
        # 这里添加一个额外的属性直接把item放进去,后面可以根据item取出数据
        mimeData.setProperty('myItems', items)
        drag.setMimeData(mimeData)
        pixmap = QPixmap(self.viewport().visibleRegion().boundingRect().size())
        pixmap.fill(QtCore.Qt.transparent)
        painter = QPainter()
        painter.begin(pixmap)
        for item in items:
            rect = self.visualRect(self.indexFromItem(item))
            painter.drawPixmap(rect, self.viewport().grab(rect))
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(self.viewport().mapFromGlobal(QtGui.QCursor.pos()))
        drag.exec_(supportedActions)

    def mousePressEvent(self, event):
        # 列表框点击事件,用于设置框选工具的开始位置
        super(DragListWidget, self).mousePressEvent(event)
        if event.buttons() != QtCore.Qt.LeftButton or self.itemAt(event.pos()):
            return
        self._rubberPos = event.pos()
        self._rubberBand.setGeometry(QtCore.QRect(self._rubberPos, QtCore.QSize()))
        self._rubberBand.show()

    def mouseReleaseEvent(self, event):
        # 列表框点击释放事件,用于隐藏框选工具
        super(DragListWidget, self).mouseReleaseEvent(event)
        self._rubberPos = None
        self._rubberBand.hide()

    def mouseMoveEvent(self, event):
        # 列表框鼠标移动事件,用于设置框选工具的矩形范围
        super(DragListWidget, self).mouseMoveEvent(event)
        if self._rubberPos:
            pos = event.pos()
            lx, ly = self._rubberPos.x(), self._rubberPos.y()
            rx, ry = pos.x(), pos.y()
            size = QtCore.QSize(abs(rx - lx), abs(ry - ly))
            self._rubberBand.setGeometry(
                QtCore.QRect(QtCore.QPoint(min(lx, rx), min(ly, ry)), size))

    def makeItem(self, size, cname):
        item = QtWidgets.QListWidgetItem(self)
        item.setData(QtCore.Qt.UserRole + 1, cname)  # 把颜色放进自定义的data里面
        item.setSizeHint(size)
        label = QtWidgets.QLabel(self)  # 自定义控件
        label.setMargin(2)  # 往内缩进2
        label.resize(size)
        pixmap = QPixmap(size.scaled(96, 96, QtCore.Qt.IgnoreAspectRatio))  # 调整尺寸
        pixmap.fill(QtGui.QColor(cname))
        label.setPixmap(pixmap)
        self.setItemWidget(item, label)

    def initItems(self):
        size = QtCore.QSize(100, 100)
        for cname in QtGui.QColor.colorNames():
            self.makeItem(size, cname)


class PixWindow(QWidget):  # 不规则窗体
    def __init__(self, parent=None):
        super(PixWindow, self).__init__(parent)

        self.pix = QBitmap('res/b0.png')  # 蒙版
        print(type(self.pix))
        windowWidth = 400
        windowHeight = 400
        # self.resize(windowWidth, windowHeight)
        self.pix = QBitmap(self.pix.scaled(int(windowWidth), int(windowHeight)))
        print(type(self.pix))
        self.resize(self.pix.size())
        self.setMask(self.pix)
        # self.setMask(self.pix.mask())

        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)  # 设置无边框和置顶窗口样式

    def paintEvent(self, event):  # 绘制窗口
        paint = QPainter(self)
        paint.drawPixmap(0, 0, self.pix.width(), self.pix.height(), QPixmap('res/images/background9.jpg'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = PixWindow()
    form.show()

    # app.setStyleSheet("""QListWidget {
    #     outline: 0px;
    #     background-color: transparent;
    # }
    # QListWidget::item:selected {
    #     border-radius: 2px;
    #     border: 1px solid rgb(0, 170, 255);
    # }
    # QListWidget::item:selected:!active {
    #     border-radius: 2px;
    #     border: 1px solid transparent;
    # }
    # QListWidget::item:selected:active {
    #     border-radius: 2px;
    #     border: 1px solid rgb(0, 170, 255);
    # }
    # QListWidget::item:hover {
    #     border-radius: 2px;
    #     border: 1px solid rgb(0, 170, 255);
    # }""")
    # wa = DragListWidget()
    # wa.show()
    # wo = DropListWidget()
    # wo.show()

    sys.exit(app.exec_())

