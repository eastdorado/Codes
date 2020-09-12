#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @项目名称: python
# @File    : myUi.py
# @Time    : 2019/12/30 16:41
# @Author  : big
# @Email   : shdorado@126.com

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
# from PySide2 import QtCore, QtGui, QtWidgets
from functools import partial
from ui_main import Ui_Main
from ui_card import Ui_Card
from ui_model import Ui_Model
from utilities import Utils, AnimWin, AllData
from ui_smartGo import Ui_SmartGo
from ui_test import Ui_Form

POLYGON = 4  # 等腰三角形直角边长
WIDTH = 1  # 分隔符粗细的一半

RADIUS = 17  # 窗口边角的弧度
ELLIPSE_RADIUS = 12  # 内部小圆半径
RECT = 10  # 图标长/宽的一半
TEXT_LENGTH = 100  # 文字长度


# 绘制形状不规则窗口
class Thumbnail(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Thumbnail, self).__init__(parent)

        self.ImageButton = None
        self.TextLabel = None

        self.initUi()

    def initUi(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.setFixedSize(140, 34)

        self.ImageButton = QtWidgets.QPushButton(self)
        self.ImageButton.setFixedSize(20, 20)
        self.ImageButton.setIconSize(QtCore.QSize(20, 20))
        self.ImageButton.setFlat(True)
        self.ImageButton.setStyleSheet("QPushButton{border:0px solid rgb(0, 0, 0);}")
        self.ImageButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ImageButton.move(RADIUS - RECT, RADIUS - RECT)

        self.TextLabel = QtWidgets.QLabel(self)
        self.TextLabel.setFixedSize(TEXT_LENGTH, 20)
        self.TextLabel.setAlignment(QtCore.Qt.AlignVCenter)
        self.TextLabel.setFont(QtGui.QFont("Microsoft YaHei", 14, QtGui.QFont.Normal))
        self.TextLabel.setStyleSheet("QLabel{color:rgba(255, 255, 255, 255); border:0px solid rgb(0, 0, 0);}")
        self.TextLabel.setFocusPolicy(QtCore.Qt.NoFocus)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setSpacing(0)
        layout.addWidget(self.TextLabel)
        layout.setContentsMargins(2 * RADIUS, 0, 0, 2)

    def setupThumbnail(self, icon_url, text):
        self.ImageButton.setIcon(QtGui.QIcon(icon_url))
        Elide_text = Utils.elideText(text, TEXT_LENGTH, self.TextLabel.font())
        self.TextLabel.setText(Elide_text)
        # textSize = QtGui.QFontMetrics().width(text)    # 字符超长检测
        # if textSize > TEXT_LENGTH:
        #     Elide_text = QtGui.QFontMetrics().elidedText(text, QtCore.Qt.ElideRight, TEXT_LENGTH)
        #     self.TextLabel.setText(Elide_text)

    def setIconSize(self, size):
        self.ImageButton.setIconSize(QtCore.QSize(size, size))

    def paintEvent(self, event):
        Painter = QtGui.QPainter(self)
        Painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        Painter.setPen(QtCore.Qt.NoPen)
        Painter.setBrush(QtGui.QColor(114, 164, 250, 200))

        PainterPath = QtGui.QPainterPath()
        PainterPath.addRoundedRect(QtCore.QRectF(0, 0, self.width(), self.height()), RADIUS, RADIUS)  # Rect
        PainterPath.addEllipse(RADIUS - ELLIPSE_RADIUS, RADIUS - ELLIPSE_RADIUS, ELLIPSE_RADIUS * 2,
                               ELLIPSE_RADIUS * 2)  # 除去内部小圆
        Painter.drawPath(PainterPath)

        Painter.setBrush(QtGui.QColor(255, 255, 255, 200))
        Painter.drawEllipse(RADIUS - ELLIPSE_RADIUS, RADIUS - ELLIPSE_RADIUS, ELLIPSE_RADIUS * 2,
                            ELLIPSE_RADIUS * 2)  # 内部小圆重新上色


class TestItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super(TestItemDelegate, self).__init__(parent)

        self.Img = QtGui.QIcon()
        self.Img_hover = QtGui.QIcon()

    def paint(self, painter, option, index):
        dragWidget = option.styleObject
        isDraging = dragWidget.isDraging()

        rect = option.rect

        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QtCore.Qt.NoPen)

        if option.state & (QtWidgets.QStyle.State_MouseOver | QtWidgets.QStyle.State_Selected):
            item = dragWidget.item(index.row())
            item.setIcon(item.Img_hover)

            if option.state & QtWidgets.QStyle.State_MouseOver:
                pass
            if option.state & QtWidgets.QStyle.State_Selected:
                painter.setBrush(QtGui.QColor(180, 0, 0))
                painter.drawRect(rect.topLeft().x(), rect.topLeft().y(), 4, rect.height())

                painter.setBrush(QtGui.QColor(230, 231, 234))
                painter.drawRect(rect.topLeft().x() + 4, rect.topLeft().y(), rect.width() - 4, rect.height())
        else:
            item = dragWidget.item(index.row())
            item.setIcon(item.Img)

        # begin drag
        if isDraging:
            theDragRow = dragWidget.dragRow()
            UpRow = dragWidget.highlightedRow()
            DownRow = UpRow + 1
            rowCount = dragWidget.count() - 1

            # 绘制DropIndicator
            if index.row() == UpRow and index.row() != theDragRow - 1 and index.row() != theDragRow:
                painter.setBrush(QtGui.QColor(66, 133, 244))

                if UpRow == rowCount:
                    # 到达尾部,三角形向上移动一个WIDTH的距离,以使分隔符宽度*2
                    trianglePolygon_bottomLeft = QtGui.QPolygon()
                    trianglePolygon_bottomLeft << QtCore.QPoint(rect.bottomLeft().x(),
                                                                rect.bottomLeft().y() - (POLYGON + WIDTH) + 1 - WIDTH)
                    trianglePolygon_bottomLeft << QtCore.QPoint(rect.bottomLeft().x(),
                                                                rect.bottomLeft().y() - WIDTH + 1 - WIDTH)
                    trianglePolygon_bottomLeft << QtCore.QPoint(rect.bottomLeft().x() + POLYGON,
                                                                rect.bottomLeft().y() - WIDTH + 1 - WIDTH)

                    trianglePolygon_bottomRight = QtGui.QPolygon()
                    trianglePolygon_bottomRight << QtCore.QPoint(rect.bottomRight().x() + 1,
                                                                 rect.bottomRight().y() - (POLYGON + WIDTH) + 1 - WIDTH)
                    trianglePolygon_bottomRight << QtCore.QPoint(rect.bottomRight().x() + 1,
                                                                 rect.bottomRight().y() - WIDTH + 1 - WIDTH)
                    trianglePolygon_bottomRight << QtCore.QPoint(rect.bottomRight().x() - POLYGON + 1,
                                                                 rect.bottomRight().y() - WIDTH + 1 - WIDTH)

                    painter.drawRect(rect.bottomLeft().x(), rect.bottomLeft().y() - 2 * WIDTH + 1, rect.width(),
                                     2 * WIDTH)  # rect
                    painter.drawPolygon(trianglePolygon_bottomLeft)
                    painter.drawPolygon(trianglePolygon_bottomRight)
                else:
                    # 正常情况,组成上半部分(+1是根据实际情况修正)
                    trianglePolygon_bottomLeft = QtGui.QPolygon()
                    trianglePolygon_bottomLeft << QtCore.QPoint(rect.bottomLeft().x(),
                                                                rect.bottomLeft().y() - (POLYGON + WIDTH) + 1)
                    trianglePolygon_bottomLeft << QtCore.QPoint(rect.bottomLeft().x(),
                                                                rect.bottomLeft().y() - WIDTH + 1)
                    trianglePolygon_bottomLeft << QtCore.QPoint(rect.bottomLeft().x() + POLYGON,
                                                                rect.bottomLeft().y() - WIDTH + 1)

                    trianglePolygon_bottomRight = QtGui.QPolygon()
                    trianglePolygon_bottomRight << QtCore.QPoint(rect.bottomRight().x() + 1,
                                                                 rect.bottomRight().y() - (POLYGON + WIDTH) + 1)
                    trianglePolygon_bottomRight << QtCore.QPoint(rect.bottomRight().x() + 1,
                                                                 rect.bottomRight().y() - WIDTH + 1)
                    trianglePolygon_bottomRight << QtCore.QPoint(rect.bottomRight().x() - POLYGON + 1,
                                                                 rect.bottomRight().y() - WIDTH + 1)

                    painter.drawRect(rect.bottomLeft().x(), rect.bottomLeft().y() - WIDTH + 1, rect.width(),
                                     WIDTH)  # rect
                    painter.drawPolygon(trianglePolygon_bottomLeft)
                    painter.drawPolygon(trianglePolygon_bottomRight)
            elif index.row() == DownRow and index.row() != theDragRow + 1 and index.row() != theDragRow:
                painter.setBrush(QtGui.QColor(66, 133, 244))

                if DownRow == 0:
                    # 到达头部,三角形向下移动一个WIDTH的距离,以使分隔符宽度*2
                    trianglePolygon_topLeft = QtGui.QPolygon()
                    trianglePolygon_topLeft << QtCore.QPoint(rect.topLeft().x(),
                                                             rect.topLeft().y() + (POLYGON + WIDTH) + WIDTH)
                    trianglePolygon_topLeft << QtCore.QPoint(rect.topLeft().x(), rect.topLeft().y() + WIDTH + WIDTH)
                    trianglePolygon_topLeft << QtCore.QPoint(rect.topLeft().x() + POLYGON,
                                                             rect.topLeft().y() + WIDTH + WIDTH)

                    trianglePolygon_topRight = QtGui.QPolygon()
                    trianglePolygon_topRight << QtCore.QPoint(rect.topRight().x() + 1,
                                                              rect.topRight().y() + (POLYGON + WIDTH) + WIDTH)
                    trianglePolygon_topRight << QtCore.QPoint(rect.topRight().x() + 1,
                                                              rect.topRight().y() + WIDTH + WIDTH)
                    trianglePolygon_topRight << QtCore.QPoint(rect.topRight().x() - POLYGON + 1,
                                                              rect.topRight().y() + WIDTH + WIDTH)

                    painter.drawRect(rect.topLeft().x(), rect.topLeft().y(), rect.width(), 2 * WIDTH)  # rect
                    painter.drawPolygon(trianglePolygon_topLeft)
                    painter.drawPolygon(trianglePolygon_topRight)
                else:
                    # 正常情况,组成下半部分(+1是根据实际情况修正)
                    trianglePolygon_topLeft = QtGui.QPolygon()
                    trianglePolygon_topLeft << QtCore.QPoint(rect.topLeft().x(), rect.topLeft().y() + (POLYGON + WIDTH))
                    trianglePolygon_topLeft << QtCore.QPoint(rect.topLeft().x(), rect.topLeft().y() + WIDTH)
                    trianglePolygon_topLeft << QtCore.QPoint(rect.topLeft().x() + POLYGON, rect.topLeft().y() + WIDTH)

                    trianglePolygon_topRight = QtGui.QPolygon()
                    trianglePolygon_topRight << QtCore.QPoint(rect.topRight().x() + 1,
                                                              rect.topRight().y() + (POLYGON + WIDTH))
                    trianglePolygon_topRight << QtCore.QPoint(rect.topRight().x() + 1, rect.topRight().y() + WIDTH)
                    trianglePolygon_topRight << QtCore.QPoint(rect.topRight().x() - POLYGON + 1,
                                                              rect.topRight().y() + WIDTH)

                    painter.drawRect(rect.topLeft().x(), rect.topLeft().y(), rect.width(), WIDTH)  # rect
                    painter.drawPolygon(trianglePolygon_topLeft)
                    painter.drawPolygon(trianglePolygon_topRight)

            QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)
            return
        # end drag

        # print(type(painter))
        QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)


class TestListWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, parent=None):
        super(TestListWidgetItem, self).__init__(parent)

        self.Img = QtGui.QIcon()
        self.Img_hover = QtGui.QIcon()

    def setUpIcon(self, icon, icon_hover):
        self.Img = icon
        self.Img_hover = icon_hover
        self.setIcon(self.Img)


class TestListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(TestListWidget, self).__init__(parent)

        self.startPos = QtCore.QPoint()
        self.IsDraging = False
        self.oldHighlightedRect = QtCore.QRect()
        self.theHighlightedRect = QtCore.QRect()
        self.theHighlightedRow = -1
        self.theDragRow = -1

        # setMouseTracking(true); // 注释与否没有影响
        # setDragEnabled(true); // 注释与否没有影响
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        # setDropIndicatorShown(false); // 注释与否没有影响
        # setDefaultDropAction(Qt::MoveAction); // 注释与否没有影响

    def isDraging(self):
        return self.IsDraging

    def offset(self):
        return 19

    def highlightedRow(self):
        return self.theHighlightedRow

    def dragRow(self):
        return self.theDragRow

    def myMimeType(self):
        return r"TestListWidget/text-icon-icon_hover"

    # 拖拽起点,鼠标按下时，startPos记录单击位置
    def mousePressEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.startPos = event.pos()

    # 释放鼠标时，item才会被选中
    def mouseReleaseEvent(self, event):
        # 如果鼠标释放位置和单击位置相距超过5像素，则不会触发item选中
        if (event.pos() - self.startPos).manhattanLength() > 5:
            return

        item = self.itemAt(event.pos())
        self.setCurrentItem(item)

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            # [1] 超过规定距离才会触发拖拽，防止手滑...
            if (event.pos() - self.startPos).manhattanLength() < QtWidgets.QApplication.startDragDistance():
                return
            theDragItem = self.itemAt(self.startPos)
            self.setCurrentItem(theDragItem)  # 拖拽即选中
            theDragRow = self.row(theDragItem)

            # [2] 这部分是把拖拽的数据放在QMimeData容器中（参考Qt例程puzzle，使用QByteArray和QDataStream感觉很方便）
            text = theDragItem.text()
            icon = theDragItem.Img
            icon_hover = theDragItem.Img_hover
            itemData = QtCore.QByteArray()
            dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
            dataStream.writeQString(text)
            dataStream << icon << icon_hover
            print(dataStream)
            mimeData = QtCore.QMimeData()
            mimeData.setData(self.myMimeType(), itemData)

            # [3] 设置拖拽时的缩略图，Thumbnail类(找机会我会写一篇单独的文章介绍)
            # 是继承自QWidget的类椭圆形半透明窗口，使用grab()
            # 将QWidget变成QPixmap。
            DragImage = Thumbnail(self)
            DragImage.setupThumbnail(icon_hover, text)
            # DragImage->setIconSize(18); // default: 20
            pixmap = DragImage.grab()

            drag = QtGui.QDrag(self)
            drag.setMimeData(mimeData)
            # 设置缩略图
            drag.setPixmap(pixmap)
            # 设置鼠标在缩略图上的位置
            drag.setHotSpot(QtCore.QPoint(pixmap.width() / 2, pixmap.height() / 2))

            # 拖拽开始！
            if drag.exec(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
                pass

    def dragEnterEvent(self, event):
        source = event.source()
        if source and source == self:
            # IsDraging(标志位) 判断是否正在拖拽
            self.IsDraging = True
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()

    # 当拖拽离开QListWidget时，需要update以保证DropIndicator消失
    def dragLeaveEvent(self, event):
        self.theHighlightedRow = -2
        self.update()

        # IsDraging(标志位) 判断是否正在拖拽
        self.IsDraging = False

        event.accept()

    # 拖拽移动时刷新以更新DropIndicator
    def dragMoveEvent(self, event):
        source = event.source()
        if source and source == self:
            self.oldHighlightedRect = self.theHighlightedRect
            self.theHighlightedRect = self.targetRect(event.pos())

            # offset() = 19(这个数值是我调用父类的dropEvent(event)
            # 一次一次试出来的，我觉得公式应该是19 = 40 / 2 - 1， 其中40是item行高)
            if event.pos().y() >= self.offset():
                self.theHighlightedRow = self.row(self.itemAt(event.pos() - QtCore.QPoint(0, self.offset())))
                if self.oldHighlightedRect != self.theHighlightedRect:
                    self.update()  # 刷新旧区域使DropIndicator消失
                    self.update()  # 刷新新区域使DropIndicator显示
                else:
                    self.update()
            else:
                self.theHighlightedRow = -1
                self.update()  # 仅刷新第一行

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()

    def dropEvent(self, event):
        source = event.source()
        if source and source == self:
            self.IsDraging = False  # 拖拽完成

            self.theHighlightedRow = -2
            self.update()  # 拖拽完成，刷新以使DropIndicator消失

            QtWidgets.QListWidget.dropEvent(self, event)  # 因为是拖拽即选中，所以可以直接调用父类的dropEvent(event)

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()

    def targetRect(self, position):
        # 40是item的行高
        if position.y() >= self.offset():
            return QtCore.QRect(0, (position.y() - self.offset()) / 40 * 40, self.width(), 2 * 40)
        else:
            return QtCore.QRect(0, 0, self.width(), 40)


class UiTest(Ui_Form):
    def setupUI(self, Main):
        super().setupUi(Main)

        # TODO 修改原始控件
        # Main.resize(600, 600)


class DlgTest(QtWidgets.QDialog, UiTest):
    def __init__(self, parent=None):
        super(DlgTest, self).__init__(parent)
        super().setupUI(self)

        # self.initUi()
        for item in range(11):
            # 新建个按钮
            wg = QtWidgets.QWidget()
            hl = QtWidgets.QHBoxLayout(wg)
            btn1 = QtWidgets.QPushButton("测试按钮{0}".format(item))
            btn1.clicked.connect(partial(self.slot_changed, btn1))  # 连接点击槽
            btn2 = QtWidgets.QPushButton("测试按钮{0}-1".format(item))
            btn2.clicked.connect(partial(self.slot_changed, btn2))  # 连接点击槽
            hl.addWidget(btn1)
            hl.addWidget(btn2)
            # 新建个Item
            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(QtCore.QSize(0, 40))  # 设置QListWidgetItem大小
            # 将item添加到list
            self.listWidget.addItem(item)
            # 将widget添加到item
            self.listWidget.setItemWidget(item, wg)

        self.show()

    def initUi(self):
        self.setFixedSize(250, 600)
        listwidget = TestListWidget(self)
        listwidget.setIconSize(QtCore.QSize(25, 25))
        listwidget.setFocusPolicy(QtCore.Qt.NoFocus)  # 这样可禁用tab键和上下方向键并且除去复选框
        listwidget.setFixedHeight(320)
        listwidget.setFont(QtGui.QFont("宋体", 10, QtGui.QFont.DemiBold))
        listwidget.setStyleSheet(
            # "*{outline:0px;}"  # 除去复选框
            "QListWidget{background:rgb(245, 245, 247); border:0px; margin:0px 0px 0px 0px;}"
            "QListWidget::Item{height:40px; border:0px; padding-left:14px; color:rgba(200, 40, 40, 255);}"
            "QListWidget::Item:hover{color:rgba(40, 40, 200, 255); padding-left:14px;}"
            "QListWidget::Item:selected{color:rgba(40, 40, 200, 255); padding-left:15px;}")

        delegate = TestItemDelegate()
        listwidget.setItemDelegate(delegate)

        item1 = TestListWidgetItem(listwidget)
        item1.setUpIcon(QtGui.QIcon(":/res/cross.png"), QtGui.QIcon(":/res/cross_1.png"))
        item1.setText("发现音乐")

        item2 = TestListWidgetItem(listwidget)
        item2.setUpIcon(QtGui.QIcon(":/res/cross.png"), QtGui.QIcon(":/res/cross_1.png"))
        item2.setText("私人FM")

        item3 = TestListWidgetItem(listwidget)
        item3.setUpIcon(QtGui.QIcon(":/res/cross.png"), QtGui.QIcon(":/res/cross_1.png"))
        item3.setText("朋友")

        item4 = TestListWidgetItem(listwidget)
        item4.setUpIcon(QtGui.QIcon(":/res/cross.png"), QtGui.QIcon(":/res/cross_1.png"))
        item4.setText("MV")

        item5 = TestListWidgetItem(listwidget)
        item5.setUpIcon(QtGui.QIcon(":/res/cross.png"), QtGui.QIcon(":/res/cross_1.png"))
        item5.setText("本地音乐")

        item6 = TestListWidgetItem(listwidget)
        item6.setUpIcon(QtGui.QIcon(":/res/cross.png"), QtGui.QIcon(":/res/cross_1.png"))
        item6.setText("下载管理")

        # item7 =  TestListWidgetItem(listwidget)
        # item7.setUpIcon(QtGui.QIcon(":/res/7.png"), QtGui.QIcon(":/res/7_hover.png"))
        # item7.setText("我的音乐云盘")
        #
        # item8 = TestListWidgetItem(listwidget)
        # item8.setUpIcon(QtGui.QIcon(":/res/8.png"), QtGui.QIcon(":/res/8_hover.png"))
        # item8.setText("我的收藏")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(0)
        layout.addWidget(listwidget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def slot_edit_finish(self):
        print('slot_edit_finish')

    def slot_changed(self, btn):
        print(btn.text())
        # 获取button
        button = self.sender()
        # 获取按钮相对于listwwdget的坐标
        # listwidget 相对于窗体的坐标 减去 button 相对于窗体的坐标
        buttonpos = button.mapToGlobal(QtCore.QPoint(0, 0)) - self.listWidget.mapToGlobal(QtCore.QPoint(0, 0))
        # 获取到对象
        item = self.listWidget.indexAt(buttonpos)
        # print(type(item))
        # 获取位置
        print(item.row())

    def slot_list_click(self):
        print('slot_list_click')


class Button(QtWidgets.QPushButton):

    def __init__(self, title, parent):
        super().__init__(title, parent)

    # 鼠标移动事件
    def mouseMoveEvent(self, e):

        if e.buttons() != QtCore.Qt.RightButton:
            return

        mimeData = QtCore.QMimeData()
        # 创建拖放类
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(QtCore.Qt.MoveAction)

    # 鼠标按下事件
    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if e.button() == QtCore.Qt.LeftButton:
            print('press')


# 例子类
class Example(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)

        self.button = Button('Button', self)
        self.button.move(100, 65)

        self.setWindowTitle('Click or Move')
        self.setGeometry(300, 300, 280, 150)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        position = e.pos()
        self.button.move(position)

        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()


class UiSmartGo(Ui_SmartGo):
    def setupUI(self, Main):
        super().setupUi(Main)

        # TODO 修改原始控件
        Main.resize(300, 600)
        # self.gb_orders.resize(20, 20)
        # qss = "QTabBar::tab{background-color:rbg(255,255,255,0);}" \
        #       "QTabBar::tab:selected{color:red;background-color:rbg(255,200,255);}"
        # qss = Utils.readQss(r'E:\python\res\styleSheet.qss')
        # self.tabWidget.setStyleSheet(qss)


class UiMain(Ui_Main):
    def setupUI(self, Main):
        super().setupUi(Main)

        # TODO 修改原始控件
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        # self.horizontalLayout.setSpacing(0)
        Main.setMinimumHeight(550)

        '''界面分隔'''
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.wg_left)
        splitter.addWidget(self.wg_mid)
        splitter.addWidget(self.wg_right)
        self.horizontalLayout.addWidget(splitter)

        self.vl_left.setContentsMargins(0, 0, 0, 0)
        self.vl_mid.setContentsMargins(0, 0, 0, 0)
        self.vl_right.setContentsMargins(0, 0, 0, 0)
        self.vl_left.setSpacing(0)
        self.vl_mid.setSpacing(0)
        self.vl_right.setSpacing(0)
        self.wg_left.setMinimumWidth(240)
        self.wg_left.setMaximumWidth(320)
        self.wg_mid.setMinimumWidth(280)
        self.wg_mid.setMaximumWidth(360)
        self.wg_right.setMinimumWidth(340)
        self.listWidget_left.setStyleSheet("background-color:transparent;")
        self.listWidget_mid.setStyleSheet("background-color:transparent;")
        self.listWidget_right.setStyleSheet("background-color:transparent;")
        # transparent:是Qt的一个枚举表示黑色透明 等价于rgb(0,0,0,0)

        scroll = self.listWidget_left.verticalScrollBar()
        scroll.setStyleSheet("QScrollBar{ background: #F0F0F0; width:45px ;margin-top:0px;margin-bottom:16px }"
                             "QScrollBar::handle:vertical{ background: #EAEAED; min-height: 80px ;width:30px }"
                             "QScrollBar::sub-line:vertical{height:16px;subcontrol-position:top;subcontrol-origin:margin;}"
                             "QScrollBar::add-line:vertical{height:16px;subcontrol-position:bottom;subcontrol-origin:margin;}"
                             "QScrollBar::-webkit-scrollbar{/*隐藏滚轮*/display: none;}")  # 滚动条宽度

        self.toolButton_search.setFixedWidth(20)
        self.lineEdit.setFixedWidth(300)

        self.pushButton_vault.setStyleSheet(
            'font-size:28px;font-family:STLiti;font-weight:bold;'
            'color:rgba(0, 55, 255, 1);border:none;text-align: left;'
            'qproperty-iconSize:40px 40px;'
            'qproperty-icon: url(./res/cross.png);')
        self.toolButton_add.setStyleSheet('border:none; qproperty-iconSize:30px 30px;'
                                          'qproperty-icon: url(./res/add1.png);')
        self.wg_right_title.setStyleSheet('background-color: rgb(13, 71, 161)')
        self.wg_right_title.setFixedHeight(35)
        self.hl_right.setContentsMargins(0, 0, 0, 0)
        self.toolButton_edit.setStyleSheet('border:none; qproperty-iconSize:30px 30px;'
                                           'qproperty-icon: url(./res/edit.png);')

        self.toolButton_add.clicked.connect(lambda: Main.slot_animation(self.toolButton_add))
        self.toolButton_edit.clicked.connect(lambda: Main.slot_animation(self.toolButton_edit))

        # self.listWidget_mid.clicked['QModelIndex'].connect(Main.slot_mid_clicked)
        # self.pushButton_vault.clicked.connect(Main.slot_tools_clicked)
        # self.toolButton_search.clicked.connect(Main.slot_tools_clicked)
        # self.lineEdit.textChanged['QString'].connect(Main.slot_keyword_changed)
        # self.toolButton_3.clicked.connect(Main.slot_tools_clicked)
        # self.toolButton_setting.clicked.connect(Main.slot_tools_clicked)
        # self.listWidget_left.clicked['QModelIndex'].connect(Main.slot_left_clicked)
        # self.toolButton_more.clicked.connect(Main.slot_tools_clicked)
        # self.toolButton_favority.clicked.connect(Main.slot_tools_clicked)
        # self.toolButton_add.clicked.connect(Main.slot_animation)
        # self.toolButton_edit.clicked.connect(Main.slot_animation)


class DlgField(QtWidgets.QWidget):
    '''自定义窗口'''
    # 知识点：
    # 1.为了得到返回值用到了自定义的信号/槽
    # 2.为了显示动态数字，使用了计时器

    child_delete_signal = QtCore.pyqtSignal(int)  # 自定义信号（int类型）
    child_save_signal = QtCore.pyqtSignal(str, str, bool, int)  # 自定义信号（int类型）

    def __init__(self, parent=None):
        # 加一个suppress规则:
        # noinspection PyArgumentList
        super(DlgField, self).__init__(parent)  # 这样这里的警告就消失了

        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 窗体总在最前端
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 必须放在开始，否则无焦点
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        # self.raise_()
        self.setGeometry(0, 0, 10, 10)
        self.setFont(QtGui.QFont("微软雅黑", 12, QtGui.QFont.Normal))

        self.style = 0
        self.parent = parent
        self.isSaveAble = False
        self.wg_content = QtWidgets.QWidget()
        self.vl_content = QtWidgets.QVBoxLayout(self.wg_content)

        hl_bar = QtWidgets.QHBoxLayout()
        btn_delete = QtWidgets.QPushButton('删除')
        btn_save = QtWidgets.QPushButton('保存')
        btn_exit = QtWidgets.QPushButton('退出')
        btn_delete.clicked.connect(partial(self.slot_click, btn_delete))
        btn_save.clicked.connect(partial(self.slot_click, btn_save))
        btn_exit.clicked.connect(partial(self.slot_click, btn_exit))

        hl_bar.addWidget(btn_delete)
        hl_bar.addWidget(btn_save)
        hl_bar.addWidget(btn_exit)

        layout = QtWidgets.QVBoxLayout(self)
        # layout.addLayout(self.vl_content)
        layout.addWidget(self.wg_content)
        layout.addLayout(hl_bar)
        self.setLayout(layout)

    def slot_click(self, control):
        if control.text() == '删除':
            self.child_delete_signal.emit(self.style)  # 发送信号，带参数 888
        elif control.text() == '保存':
            if not self.isSaveAble:
                self.child_save_signal.emit('', '', False, 99)  # 无需保存
            else:
                if self.style:  # 小窗口
                    self.child_save_signal.emit(self.le.text(), '', False, 1)  # 保存小节名称
                else:
                    self.child_save_signal.emit(self.le1.text(), self.le2.text(), self.cb.checkState(), 0)
        else:
            pass
        self.close()

    def slot_changed(self, control):
        self.isSaveAble = True

    def update_ui(self, text1, text2, style=2, sensitive=False):
        """
        初始化
        :param text1:
        :param text2:
        :param style: 类型 -3=标签与备注 -2=分节 -1=标题 0=密码 1=支付密码 2、3……=其余
        :param sensitive:
        :return:
        """
        self.style = style
        vl = self.layout()

        wg_new = QtWidgets.QWidget()
        vl_content = QtWidgets.QVBoxLayout(wg_new)

        wg = vl.itemAt(0).widget()
        if wg:
            # wg.setParent(None)
            wg.deleteLater()
            vl.replaceWidget(wg, wg_new, QtCore.Qt.FindDirectChildrenOnly)

        if style > 1:  # 标准窗口
            self.resize(280, 250)
            self.le1 = QtWidgets.QLineEdit()
            self.le1.setText(text1)
            self.le2 = QtWidgets.QLineEdit()
            self.le2.setText(text2)
            self.le1.textChanged.connect(self.slot_changed)
            self.le2.textChanged.connect(self.slot_changed)

            hl = QtWidgets.QHBoxLayout()
            hl.setSpacing(10)
            self.cb = QtWidgets.QCheckBox()
            self.cb.setChecked(sensitive)
            self.cb.stateChanged['int'].connect(self.slot_changed)
            # self.cb.textChanged.connect(self.slot_changed)
            hl.addWidget(self.cb)
            hl.addWidget(QtWidgets.QLabel('敏感'))
            hl.addStretch()

            vl_content.setContentsMargins(0, 0, 0, 0)
            vl_content.setSpacing(0)
            vl_content.addWidget(QtWidgets.QLabel('字段名称'))
            vl_content.addWidget(self.le1)
            vl_content.addSpacing(15)
            vl_content.addWidget(QtWidgets.QLabel('字段类型'))
            vl_content.addWidget(self.le2)
            vl_content.addSpacing(15)
            vl_content.addLayout(hl)
        elif style > -1:  # 密码，超大窗口
            self.resize(280, 340)
            self.le1 = QtWidgets.QLineEdit()
            self.le1.setText(text1)
            self.le2 = QtWidgets.QLineEdit()
            self.le2.setText(text2)
            self.le1.textChanged.connect(self.slot_changed)
            self.le2.textChanged.connect(self.slot_changed)

            hl1 = QtWidgets.QHBoxLayout()
            hl1.setSpacing(10)
            self.cb1 = QtWidgets.QCheckBox()
            self.cb1.setChecked(sensitive)
            self.cb1.stateChanged['int'].connect(self.slot_changed)
            hl1.addWidget(self.cb1)
            hl1.addWidget(QtWidgets.QLabel('敏感'))
            hl1.addStretch()    # QSpacerItem 不好删除，用label代替

            hl2 = QtWidgets.QHBoxLayout()
            hl2.setSpacing(10)
            self.cb2 = QtWidgets.QCheckBox()
            self.cb2.setChecked(False)
            self.cb2.stateChanged['int'].connect(self.slot_changed)
            hl2.addWidget(self.cb2)
            hl2.addWidget(QtWidgets.QLabel('从密码审核中排除'))
            hl2.addStretch()

            hl3 = QtWidgets.QHBoxLayout()
            hl3.setSpacing(10)
            self.cb3 = QtWidgets.QCheckBox()
            self.cb3.setChecked(False)
            self.cb3.stateChanged['int'].connect(self.slot_changed)
            self.le3 = QtWidgets.QLineEdit()
            self.le3.setText('0')
            self.le3.setEnabled(False)
            self.le3.setFixedWidth(40)
            self.le3.setValidator(QtGui.QIntValidator(0, 999))
            self.le3.textChanged.connect(self.slot_changed)
            hl3.addWidget(self.cb3)
            hl3.addWidget(QtWidgets.QLabel('有效期限'))
            hl3.addWidget(self.le3)
            hl3.addWidget(QtWidgets.QLabel('天'))
            hl3.addStretch()

            self.vl_content.setContentsMargins(0, 0, 0, 0)
            self.vl_content.setSpacing(0)
            self.vl_content.addWidget(QtWidgets.QLabel('字段名称'))
            self.vl_content.addWidget(self.le1)
            self.vl_content.addSpacing(10)    # QSpacerItem 不好删除，用label代替
            self.vl_content.addWidget(QtWidgets.QLabel('字段类型'))
            self.vl_content.addWidget(self.le2)
            self.vl_content.addSpacing(20)
            self.vl_content.addLayout(hl1)
            self.vl_content.addLayout(hl2)
            self.vl_content.addLayout(hl3)
            self.vl_content.addSpacing(20)
        else:  # 小节，小窗口
            self.resize(280, 140)
            self.le = QtWidgets.QLineEdit()
            self.le.setText(text1)
            self.le.textChanged.connect(partial(self.slot_changed, self.le))

            vl_content.setContentsMargins(0, 10, 0, 0)
            vl_content.setSpacing(5)
            vl_content.addWidget(QtWidgets.QLabel('小节名称'))
            vl_content.addWidget(self.le)
            vl_content.addStretch()

    # def focusInEvent(self, QFocusEvent):
    #     pass
    #     # print('focusInEvent')
    #
    # def focusOutEvent(self, QFocusEvent):
    #     print('focusOutEvent')
    #     self.close()

    def closeEvent(self, event):
        print('closeEvent')
        # Utils.clear_layout(self.vl_content)
        # self.wg_content.resize(10, 10)
        # self.show()
        # self.close()
        # event.ignore()


class UiCard(Ui_Card):
    def setupUI(self, Card):
        super().setupUi(Card)

        # TODO 修改原始控件
        self.setModal(QtCore.Qt.ApplicationModal)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 无边框
        self.setMinimumWidth(600)
        # self.listWidget_card.setMinimumWidth(600)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.wg_title.setStyleSheet('background-color: rgb(13, 71, 161);')
        self.wg_title.setFixedHeight(35)
        self.hl_title.setContentsMargins(0, 0, 0, 0)
        self.toolButton_title_exit.setStyleSheet('border:none;qproperty-iconSize:30px 30px;'
                                                 'qproperty-icon: url(./res/exit.png) on;')
        self.label_title.setStyleSheet('font-size:16px;font-family:微软雅黑;font-weight:bold;'
                                       'color:rgba(255, 255, 255, 1);border:none;')
        self.toolButton_title_save.setStyleSheet('font-size:15px;font-family:微软雅黑;font-weight:bold;'
                                                 'color:rgba(255, 255, 255, 1);border:none;')
        self.label_title.setText(' 添加')
        self.toolButton_title_save.setText('保存')

        self.listWidget.setStyleSheet("font-size:14px;font-family:MicrosoftYaHei;font-weight:bold;"
                                      "background-color : white;color:rgba(77,77,77,1);"
                                      "border:none; text-align: right;")
        # 拖曳
        self.listWidget.setAcceptDrops(True)
        self.listWidget.setDragEnabled(True)

        scroll = self.listWidget.verticalScrollBar()
        # op = QtWidgets.QGraphicsOpacityEffect()
        # op.setOpacity(50)
        # scroll.setGraphicsEffect(op)
        # scroll.setHidden(True)
        # scroll.setVisible(False)
        # scroll.hide()

        scroll.setStyleSheet("QScrollBar{ background: #F0F0F0; width:15px ;margin-top:0px;margin-bottom:16px }"
                             "QScrollBar::handle:vertical{ background: #EA1AED; min-height: 80px ;width:30px }"
                             "QScrollBar::sub-line:vertical{height:16px;subcontrol-position:top;subcontrol-origin:margin;}"
                             "QScrollBar::add-line:vertical{height:16px;subcontrol-position:bottom;subcontrol-origin:margin;}"
                             "QScrollBar::-webkit-scrollbar{/*隐藏滚轮*/display: none;}")  # 滚动条宽度
        # self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # self.listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)    # 水平滚动条
        self.listWidget.setVerticalScrollMode(QtWidgets.QListWidget.ScrollPerPixel)  # 设置为像素滚动
        # self.listWidget.setFrameShape(QtWidgets.QListWidget.NoFrame)
        # self.listWidget_card.resize(100, 400)
        QtWidgets.QScroller.grabGesture(self.listWidget, QtWidgets.QScroller.LeftMouseButtonGesture)  # 设置鼠标左键拖动

        self.toolButton_title_exit.clicked.connect(Card.close)

    ''' 
                     QPushButton
                     {text-align : center;
                     background-color : white;
                     font: bold;
                     border-color: gray;
                     border-width: 2px;
                     border-radius: 10px;
                     padding: 6px;
                     height : 14px;
                     border-style: outset;
                     font : 14px;}
                     QPushButton:pressed
                     {text-align : center;
                     background-color : light gray;
                     font: bold;
                     border-color: gray;
                     border-width: 2px;
                     border-radius: 10px;
                     padding: 6px;
                     height : 14px;
                     border-style: outset;
                     font : 14px;}
                     '''


class DlgCard(QtWidgets.QDialog, UiCard):
    def __init__(self, parent=None):
        super(DlgCard, self).__init__(parent)
        super().setupUI(self)

        self.parent_data = AllData()
        self.parent = parent
        self.card_id = 0  # 模板代号或者卡片序号
        self.card_data = None  # 模板数据
        self.cur_id = 0  # 当前列表项

        self.animation = None
        self.isNew = False
        self.isSaveAble = False

        self.myWin = DlgField()  # 自定义窗口
        self.myWin.child_delete_signal.connect(self.emit_delete)  # 接收自定义窗口关闭时发送过来的信号，交给 echo 函数显示
        self.myWin.child_save_signal.connect(self.emit_save)  # 接收自定义窗口关闭时发送过来的信号，交给 echo 函数显示

        self.update_card_data(self.card_id, self.isNew)
        self.create_card()
        self.show()

    def update_card_data(self, index=0, isNew=True):
        """
        根据id更新card数据
        :param index: 卡片序号
        :param isNew: 新建卡片
        :return:
        """
        self.card_id = index
        self.isNew = isNew

        # if not self.parent:
        #     AnimWin('没父亲')
        #     return

        if self.isNew:  # 根据模板添加部件
            # self.label_card.setText('添加')
            # self.card_data = self.parent.data.data_unit[self.parent.data.cur_card]
            self.card_data = self.parent_data.data_unit[self.card_id]
        else:  # 根据实际数据添加部件
            self.label_title.setText('编辑')
            # self.isNew = False
            # self.card_data = self.parent.data.data_cards[self.parent.data.cur_card]
            self.card_data = self.parent_data.data_cards[self.card_id]

        # print(self.card_data)

    def create_card(self):
        """
        根据数据创建卡片
        :return:
        """
        if not self.card_data:
            AnimWin('没有数据', self)
            return

        self.listWidget.clear()

        # 类型 -3=标签与备注 -2=分节 -1=标题 0=密码 1=支付密码 2、3……=其余
        for i in range(0, len(self.card_data)):
            self.add_card_row(self.card_data[i][0], self.card_data[i][1], self.card_data[i][2],
                              self.card_data[i][3], self.card_data[i][4])

    def add_card_row(self, text1, text2, mold=2, sensitive=False, icon_path=None):
        """
        创建卡片的每一项
        :param text1: 前标
        :param text2: 内容
        :param mold: 类型 -3=标签与备注 -2=分节 -1=标题 0=密码 1=支付密码 2、3……=其余
        :param sensitive:
        :param icon_path: 图标路径
        :return: 返回 widget
        """
        item = QtWidgets.QListWidgetItem()  # 创建QListWidgetItem对象
        item.setSizeHint(QtCore.QSize(0, 40))  # 设置QListWidgetItem大小
        wg = QtWidgets.QWidget()
        # wg.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)  # 鼠标穿透 不响应鼠标点击事件
        # wg.setObjectName(text2)

        if mold < -2:  # 底部固定的
            vl = QtWidgets.QVBoxLayout(wg)
            vl.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            vl.setContentsMargins(0, 10, 0, 0)
            vl.setSpacing(15)
            # <editor-fold desc="三个命令按钮">
            hl_field = QtWidgets.QHBoxLayout()
            hl_field.setContentsMargins(0, 0, 0, 0)
            hl_field.setSpacing(40)
            pb1 = QtWidgets.QPushButton()
            pb1.setMinimumWidth(170)
            qss = "QPushButton{border-width: 0px;border-radius: 10px;padding: 6px;" \
                  "background-color:LightGrey; color:BlueViolet;" \
                  "text-align: center;" \
                  "font-size:16px; font-family:MicrosoftYaHei; font-weight:bold;}" \
                  "QPushButton:hover{background-color:Plum;}"
            pb_field = QtWidgets.QPushButton('添加字段')
            pb_field.setStyleSheet(qss)
            pb_field.setFixedHeight(30)

            pb_node = QtWidgets.QPushButton('添加小节')
            pb_node.setStyleSheet(qss)
            pb_node.setFixedHeight(30)
            pb3 = QtWidgets.QPushButton()
            pb3.setMinimumWidth(170)

            pb_file = QtWidgets.QPushButton('添加文件')
            pb_file.setStyleSheet(qss)
            pb_file.setFixedHeight(30)
            pb5 = QtWidgets.QPushButton()
            pb5.setMinimumWidth(170)

            pb2 = QtWidgets.QPushButton('')
            hl_field.addWidget(pb1)
            # hl_field.addSpacing(20)
            hl_field.addWidget(pb_field)
            hl_field.addWidget(pb_node)
            hl_field.addWidget(pb_file)
            hl_field.addWidget(pb2)
            hl_field.setStretchFactor(pb1, 1)
            hl_field.setStretchFactor(pb2, 2)
            # </editor-fold>

            # # <editor-fold desc="添加小节">
            # hl_node = QtWidgets.QHBoxLayout()
            # hl_node.setContentsMargins(0, 0, 0, 0)
            # hl_node.setSpacing(0)
            # pb_node = QtWidgets.QPushButton('添加小节')
            # pb_node.setStyleSheet(qss)
            # pb_node.setFixedHeight(30)
            # pb3 = QtWidgets.QPushButton()
            # pb3.setMinimumWidth(170)
            # pb4 = QtWidgets.QPushButton()
            # hl_node.addWidget(pb3)
            # hl_node.addSpacing(20)
            # hl_node.addWidget(pb_node)
            # hl_node.addWidget(pb4)
            # hl_node.setStretchFactor(pb3, 1)
            # hl_node.setStretchFactor(pb4, 2)
            # # </editor-fold>
            # # <editor-fold desc="添加文件">
            # hl_file = QtWidgets.QHBoxLayout()
            # hl_file.setContentsMargins(0, 0, 0, 0)
            # hl_file.setSpacing(0)
            # pb_file = QtWidgets.QPushButton('添加文件')
            # pb_file.setStyleSheet(qss)
            # pb_file.setFixedHeight(30)
            # pb5 = QtWidgets.QPushButton()
            # pb5.setMinimumWidth(170)
            # pb6 = QtWidgets.QPushButton()
            # hl_file.addWidget(pb5)
            # hl_file.addSpacing(20)
            # hl_file.addWidget(pb_file)
            # hl_file.addWidget(pb6)
            # hl_file.setStretchFactor(pb5, 1)
            # hl_file.setStretchFactor(pb6, 2)
            # # </editor-fold>

            # <editor-fold desc="标签">
            hl_tag = QtWidgets.QHBoxLayout()
            hl_tag.setContentsMargins(0, 0, 0, 0)
            hl_tag.setSpacing(10)
            pb_tag = QtWidgets.QPushButton(text1)  # 标签
            pb_tag.setMinimumWidth(170)
            pb_tag.setStyleSheet("QPushButton{font-size:14px;font-family:MicrosoftYaHei;font-weight:bold;"
                                 "border:none; text-align: right; color:rgba(77,177,77,1);}")
            le_tag = QtWidgets.QLineEdit()
            # le_tag.setMinimumWidth(140)
            le_tag.setStyleSheet("font-size:18px;font-family:MicrosoftYaHei;font-weight:bold;"
                                 "border-color: gray;border-width: 2px;border-radius: 10px;padding: 6px;"
                                 "height : 18px;border-style: outset;"
                                 "color:rgba(177,77,77,1);")
            le_tag.setText(text2)
            le_tag.textChanged.connect(partial(self.slot_changed, pb_tag, le_tag))
            pb7 = QtWidgets.QPushButton()
            hl_tag.addWidget(pb_tag)
            hl_tag.addWidget(le_tag)
            hl_tag.addWidget(pb7)
            hl_tag.setStretchFactor(pb_tag, 1)
            hl_tag.setStretchFactor(le_tag, 2)
            # </editor-fold>

            # <editor-fold desc="备注">
            hl_remarks = QtWidgets.QHBoxLayout()
            hl_remarks.setContentsMargins(0, 0, 0, 10)
            hl_remarks.setSpacing(10)
            pb_remarks = QtWidgets.QPushButton(sensitive)  # sensitive 代表 ‘备注’
            pb_remarks.setMinimumWidth(170)
            pb_remarks.setStyleSheet("QPushButton{font-size:14px;font-family:MicrosoftYaHei;font-weight:bold;"
                                     "border:none; text-align: right; color:rgba(77,177,77,1);}")
            te_remarks = QtWidgets.QTextEdit()
            te_remarks.setStyleSheet("font-size:18px;font-family:MicrosoftYaHei;font-weight:bold;"
                                     "border-color: gray;border-width: 2px;border-radius: 10px;padding: 6px;"
                                     "height : 180px;border-style: outset;"
                                     "color:rgba(177,77,77,1);")
            te_remarks.setText(icon_path)  # icon_path此时就是备注的文字
            te_remarks.textChanged.connect(partial(self.slot_changed, pb_remarks, te_remarks))
            pb8 = QtWidgets.QPushButton()
            hl_remarks.addSpacing(8)
            hl_remarks.addWidget(pb_remarks)
            hl_remarks.addWidget(te_remarks)
            hl_remarks.addWidget(pb8)
            hl_remarks.setStretchFactor(pb_remarks, 1)
            hl_remarks.setStretchFactor(te_remarks, 2)
            # </editor-fold>

            vl.addLayout(hl_field)
            # vl.addLayout(hl_node)
            # vl.addLayout(hl_file)
            vl.addLayout(hl_tag)
            vl.addLayout(hl_remarks)

            item.setSizeHint(QtCore.QSize(0, 380))  # 设置QListWidgetItem大小
        else:
            hl = QtWidgets.QHBoxLayout(wg)
            hl.setAlignment(QtCore.Qt.AlignVCenter)
            hl.setContentsMargins(0, 0, 0, 0)
            hl.setSpacing(0)

            if mold < -1:  # 添加小节
                pb1 = QtWidgets.QPushButton()
                pb1.setText('')
                pb1.setMinimumWidth(170)
                # pb1.setStyleSheet("font-size:14px;font-family:MicrosoftYaHei;font-weight:bold;"
                #                   "border:none; text-align: right;"
                #                   "color:rgba(77,177,77,1);")
                pb2 = QtWidgets.QPushButton(text1)
                # pb2.setMinimumWidth(340)
                pb2.setStyleSheet("QPushButton{border:none; color:rgba(177,177,77,1);text-align: left;"
                                  "font-size:16px; font-family:MicrosoftYaHei; font-weight:bold;}"
                                  "QPushButton:hover{border:none; color:rgb(200, 62, 134);}")
                # pb2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                pb3 = QtWidgets.QPushButton()
                pb3.setStyleSheet("QPushButton{border: none;text-align: right;"
                                  "qproperty-iconSize: 30px 30px; qproperty-icon: url(res/add2.png);}")
                pb3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                pb4 = QtWidgets.QPushButton()
                pb4.setStyleSheet("background-color:transparent; border:none;text-align: left;"
                                  "qproperty-iconSize:30px 30px; qproperty-icon: url(res/move.png);")
                pb4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                pb5 = QtWidgets.QPushButton()

                hl.addWidget(pb1)
                hl.addSpacing(20)
                hl.addWidget(pb2)
                hl.addWidget(pb5)
                hl.addWidget(pb3)
                hl.addWidget(pb4)
                hl.setStretchFactor(pb1, 1)
                hl.setStretchFactor(pb5, 2)
                pb2.clicked.connect(partial(self.slot_btn_click, pb2))  # 连接点击槽
                pb3.clicked.connect(partial(self.slot_tmp))
                pb4.clicked.connect(partial(self.slot_move, pb4))

            elif mold < 0:  # 题头
                # print(mold)
                pb = QtWidgets.QPushButton()
                pb.setObjectName('title')
                # pb1.setStyleSheet("border-image: url(res/cross_1.png)")
                pb.setStyleSheet("border:none; text-align:right;"
                                 "qproperty-iconSize:40px 40px; qproperty-icon: url({});".format(icon_path))
                pb.setMinimumWidth(180)

                le = QtWidgets.QLineEdit()
                le.setMinimumWidth(340)
                le.setStyleSheet("font-size:18px;font-family:MicrosoftYaHei;font-weight:bold;"
                                 "border-color: gray;border-width: 2px;border-radius: 10px;padding: 6px;"
                                 "height : 18px;border-style: outset;"
                                 "color:rgba(177,77,77,1);")
                le.setText(' ' + text2)

                pb.clicked.connect(partial(self.slot_btn_click, pb))  # 连接点击槽
                le.textChanged.connect(partial(self.slot_changed, pb, le))

                # hl_item.addStretch(0)
                hl.addWidget(pb)
                hl.addSpacing(20)
                hl.addWidget(le)
                hl.addSpacing(45)
                hl.setStretchFactor(pb, 1)
                hl.setStretchFactor(le, 2)
                item.setSizeHint(QtCore.QSize(0, 90))  # 设置QListWidgetItem大小
            elif mold < 2:  # 密码和支付密码
                pb1 = QtWidgets.QPushButton()
                pb1.setText(text1)
                pb1.setStyleSheet("QPushButton{font-size:14px;font-family:MicrosoftYaHei;font-weight:bold;"
                                  "border:none; text-align: right; color:rgba(77,177,77,1);}"
                                  "QPushButton:hover{border:none; color:rgb(200, 62, 134);}")
                pb1.setMinimumWidth(170)
                pb1.clicked.connect(partial(self.slot_btn_click, pb1))  # 连接点击槽

                le = QtWidgets.QLineEdit()
                # le.setMinimumWidth(340)
                le.setStyleSheet("font-size:14px;font-family:MicrosoftYaHei;font-weight:bold;"
                                 "border-color: gray;border-width: 2px;border-radius: 10px;padding: 6px;"
                                 "height : 14px;border-style: outset;"
                                 "color:rgba(77,77,177,1);")
                # le.setStyleSheet("QLineEdit {border: 2px solid #EEE;border-radius: 4px;padding-right: 14px;}"
                #                  "QLineEdit:focus {border-color: #bbbec4;}"
                #                  "QLineEdit QPushButton{width:16px; height:16px; qproperty-flat:true; margin-right:4px;"
                #                  "border:none; border-width:0; border-image:url(res/1_horizontal.jpg) 0 0 0 0 stretch stretch;}")
                le.setText(' ' + text2)
                le.textChanged.connect(partial(self.slot_changed, pb1, le))
                # le.setClearButtonEnabled(True)

                # eyeAct = QtWidgets.QAction(QtGui.QIcon("res/eye1.png"), "&New", self)
                # le.addAction(eyeAct, QtWidgets.QLineEdit.TrailingPosition)
                # le.connect(eyeAct, QtCore.SINGAL("triggered()"), self.slot_tmp)
                pb_eye = QtWidgets.QPushButton()
                pb_eye.setStyleSheet("background-color:transparent; border:none;text-align: left;"
                                     "qproperty-iconSize:30px 30px; qproperty-icon: url(res/1.png);")
                pb_eye.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                hl_eye = QtWidgets.QHBoxLayout(le)
                hl_eye.setContentsMargins(0, 0, 0, 0)
                hl_eye.setSpacing(0)
                hl_eye.addStretch()
                hl_eye.addWidget(pb_eye)
                # le.setLayout(hl_eye)

                pb2 = QtWidgets.QPushButton()
                pb2.setStyleSheet("background-color:transparent; border:none;text-align: left;"
                                  "qproperty-iconSize:30px 30px; qproperty-icon: url(res/copy1.png);")
                pb2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                pb3 = QtWidgets.QPushButton()
                pb3.setStyleSheet("background-color:transparent; border:none;text-align: left;"
                                  "qproperty-iconSize:30px 30px; qproperty-icon: url(res/flower.png);")
                pb3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                pb4 = QtWidgets.QPushButton()
                pb4.setStyleSheet("background-color:transparent; border:none;text-align: left;"
                                  "qproperty-iconSize:30px 30px; qproperty-icon: url(res/move.png);")
                pb4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

                hl.addWidget(pb1)
                hl.addSpacing(10)
                hl.addWidget(le)
                hl.addSpacing(5)
                hl.addWidget(pb2)
                hl.addWidget(pb3)
                hl.addWidget(pb4)
                hl.setStretchFactor(pb1, 1)
                hl.setStretchFactor(le, 2)
            else:  # 其他所有类型
                if sensitive:  # 敏感，密文显示
                    pb1 = QtWidgets.QPushButton()
                    pb1.setText(text1)
                    pb1.setStyleSheet("QPushButton{font-size:14px;font-family:MicrosoftYaHei;font-weight:bold;"
                                      "border:none; text-align: right; color:rgba(77,177,77,1);}"
                                      "QPushButton:hover{border:none; color:rgb(200, 62, 134);}")
                    pb1.setMinimumWidth(170)
                    le = QtWidgets.QLineEdit()
                    # le.setMinimumWidth(340)
                    le.setStyleSheet("font-size:14px;font-family:MicrosoftYaHei;font-weight:bold;"
                                     "border-color: gray;border-width: 2px;border-radius: 10px;padding: 6px;"
                                     "height : 14px;border-style: outset;"
                                     "color:rgba(77,77,177,1);")
                    le.setText(' ' + text2)
                    le.textChanged.connect(partial(self.slot_changed, pb1, le))
                    pb2 = QtWidgets.QPushButton()
                    pb2.setStyleSheet("background-color:transparent; border:none;text-align: left;"
                                      "qproperty-iconSize:30px 30px; qproperty-icon: url(res/eye1.png);")
                    pb2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                    pb3 = QtWidgets.QPushButton()
                    pb3.setStyleSheet("background-color:transparent; border:none;text-align: left;"
                                      "qproperty-iconSize:30px 30px; qproperty-icon: url(res/move.png);")
                    pb3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                    hl.addWidget(pb1)
                    hl.addSpacing(10)
                    hl.addWidget(le)
                    # hl.addSpacing(15)
                    hl.addWidget(pb2)
                    hl.addWidget(pb3)
                    hl.setStretchFactor(pb1, 1)
                    hl.setStretchFactor(le, 2)
                else:  # 不敏感，明文显示
                    pb1 = QtWidgets.QPushButton()
                    pb1.setText(text1)
                    pb1.setStyleSheet("QPushButton{font-size:14px;font-family:MicrosoftYaHei;font-weight:bold;"
                                      "border:none; text-align: right; color:rgba(77,177,77,1);}"
                                      "QPushButton:hover{border:none; color:rgb(200, 62, 134);}")
                    pb1.setMinimumWidth(170)
                    le = QtWidgets.QLineEdit()
                    le.setMinimumWidth(340)
                    le.setStyleSheet("font-size:14px;font-family:MicrosoftYaHei;font-weight:bold;"
                                     "border-color: gray;border-width: 2px;border-radius: 10px;padding: 6px;"
                                     "height : 14px;border-style: outset;"
                                     "color:rgba(77,77,177,1);")
                    le.setText(text2)

                    pb2 = QtWidgets.QPushButton()
                    pb2.setObjectName('move')
                    pb2.setStyleSheet("background-color:transparent; border:none;text-align: left;"
                                      "qproperty-iconSize:30px 30px; qproperty-icon: url(res/move.png);")
                    pb2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

                    pb1.clicked.connect(partial(self.slot_btn_click, pb1))  # 连接点击槽
                    pb2.clicked.connect(partial(self.slot_move, pb1, le))

                    hl.addWidget(pb1)
                    hl.addSpacing(10)
                    hl.addWidget(le)
                    hl.addWidget(pb2)
                    hl.setStretchFactor(pb1, 1)
                    hl.setStretchFactor(le, 2)

        self.listWidget.addItem(item)  # 添加item
        self.listWidget.setItemWidget(item, wg)  # 为item设置widget

    def emit_delete(self, style):
        print(f'emit_delete {style}')

    def emit_save(self, text1, text2, sensitive, style):
        if style == 99:  # 无需保存
            print(f'emit_save {style}')
            pass
        elif style == 0:  # 保存三种 标准窗口
            print(text1, text2, sensitive)
        else:  # 保存小节名称
            print(text1)

    def slot_changed(self, control1, control2):
        self.isSaveAble = True
        # control = QtWidgets.QTextEdit()
        # print()
        msg = control2.text() if type(control2) == QtWidgets.QLineEdit else control2.toPlainText()
        print(f'{control1.text()} : {msg}')
        # 获取 控件
        control = self.sender()
        # 获取按钮相对于 listWidget的坐标 —— listWidget 相对于窗体的坐标 减去 control 相对于窗体的坐标
        control_pos = control.mapToGlobal(QtCore.QPoint(0, 0)) - self.listWidget.mapToGlobal(QtCore.QPoint(0, 0))
        # 获取到对象
        item = self.listWidget.indexAt(control_pos)
        # print(item)
        # 获取位置
        print(item.row())

    def slot_btn_click(self, control1):
        name = control1.objectName()
        if name == 'title':
            print(name)
            model = DlgModel(self)
            model.init_ui(1)
            rect = self.rect()
            model.setGeometry(rect.x() + rect.width(), rect.y(), model.width(), rect.height())
            Utils.doAnim(model)
        else:
            # self.isSaveAble = True
            control = self.sender()  # 获取控件
            # 获取按钮相对于 listWidget的坐标 —— listWidget 相对于窗体的坐标 减去 control 相对于窗体的坐标
            control_pos = control.mapToGlobal(QtCore.QPoint(0, 0)) - self.listWidget.mapToGlobal(QtCore.QPoint(0, 0))
            item = self.listWidget.indexAt(control_pos)  # 获取到对象
            row_index = item.row()  # 获取位置
            # print(row_index)

            text = self.parent_data.field_style[self.card_data[row_index][2]]
            self.myWin.update_ui(self.card_data[row_index][0], text,
                                 self.card_data[row_index][2], self.card_data[row_index][3])
            rect = self.myWin.geometry()
            # print(rect)
            pt = QtGui.QCursor.pos()  # 获取鼠标的绝对位置
            pos = QtCore.QPoint(pt.x() - rect.width()-20, pt.y() - int(rect.height() / 2))
            self.myWin.move(pos)
            self.myWin.show()

    def slot_move(self, control1, control2):
        print(control1.text())
        print(control2.text())

    def slot_save(self):
        if self.isSaveAble:
            print('saving')

            self.isSaveAble = False

        self.close()

    def slot_tmp(self):
        pass
        # print("这是一个万金油{}".format(self.windowTitle()))

    def resizeEvent(self, event):
        palette = QtGui.QPalette()
        # pix = QtGui.QPixmap('res/background.jpg')
        # pix = pix.scaled(self.width(), self.height())
        # palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        palette.setColor(palette.Background, QtGui.QColor(13, 71, 161))
        self.setPalette(palette)

    def closeEvent(self, event):
        if self.isSaveAble:
            # AnimWin('保存数据提醒')
            reply = QtWidgets.QMessageBox.question(
                self, '询问', '这是一个询问消息对话框，默认是No',
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel,
                QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                # AnimWin('你选择了Yes！')
                self.slot_save()
            elif reply == QtWidgets.QMessageBox.No:
                # AnimWin('你选择了No！')
                self.isSaveAble = False
                self.slot_save()
                # event.ignore()
                # return
            else:
                # AnimWin('你选择了Cancel！')
                event.ignore()
                return

        if self.animation is None:
            self.animation = QtCore.QPropertyAnimation(self, b'geometry')
            self.animation.setTargetObject(self)
            self.animation.setDuration(300)
            # self.animation.setEasingCurve(QtCore.QEasingCurve.InQuad)  # 设置动画的节奏
            start_point = self.geometry()
            end_point = QtCore.QRect(start_point.x() + start_point.width(), start_point.y(), start_point.width(),
                                     start_point.height())
            self.animation.setStartValue(start_point)
            self.animation.setEndValue(end_point)
            self.animation.finished.connect(self.close)
            self.animation.start()
            event.ignore()


class UiModel(Ui_Model):
    def setupUI(self, Model):
        super().setupUi(Model)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.hl_model.setContentsMargins(0, 0, 0, 0)
        self.hl_model.setSpacing(0)
        # TODO 修改原始控件
        self.toolButton_model.setStyleSheet('background-color:transparent;border:none; qproperty-iconSize:30px 30px;'
                                            'qproperty-icon: url(./res/exit.png) on;')
        self.label_model.setStyleSheet('font-size:16px;font-family:微软雅黑;font-weight:bold;'
                                       'color:rgba(255, 255, 255, 1);background-color: rgb(13, 71, 161);'
                                       'border:none;')
        self.label_model.setText(' 添加项目')
        self.lineEdit_model.setVisible(False)
        self.lineEdit_model.setStyleSheet("font-size:14px;font-family:MicrosoftYaHei;font-weight:bold;"
                                          "border-color: gray;border-width: 2px;border-radius: 10px;padding: 6px;"
                                          "height : 16px;border-style: outset;"
                                          "color:rgba(177,77,77,1);")
        self.toolButton_model.clicked.connect(Model.slot_closed)
        self.lineEdit_model.textChanged['QString'].connect(Model.slot_keyword_changed)
        self.listWidget_model.clicked['QModelIndex'].connect(Model.slot_model_clicked)


class DlgModel(QtWidgets.QDialog, UiModel):
    def __init__(self, parent=None):
        super(DlgModel, self).__init__(parent)
        self.setupUI(self)
        self.parent = parent
        self.family = []  # 类别数据
        self.list_data = []  # 当前选择的模板序号
        self.cur_family = 0  # 当前类别
        self.isModel = False  # 是模板列表还是类别列表
        self.animation = None

        self.setModal(QtCore.Qt.ApplicationModal)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 无边框
        self.setMinimumWidth(400)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 置顶
        # self.setStyleSheet("border-image:url(./res/background.jpg)")

    def init_ui(self, style=0):
        if style == 1:
            self.label_model.setText('选择图标')
            self.lineEdit_model.setVisible(True)
            self.hl_model.addStretch()
            toolButton_open = QtWidgets.QToolButton(self)
            toolButton_open.setStyleSheet('background-color:transparent;border:none;'
                                          'qproperty-iconSize:30px 30px;'
                                          'qproperty-icon: url(./res/add1.png) on;')
            toolButton_open.clicked.connect(self.slot_open)
            self.hl_model.addWidget(toolButton_open)
            self.hl_model.addSpacing(4)
        else:
            self.updateList()
        self.show()

    def updateList(self):
        if not self.isModel:  # 选择类别
            if self.parent is None:
                return

            self.family = self.parent.data.data_family
            if not self.family:
                AnimWin('没有类别项')
                return

            self.list_data.clear()
            for i in range(len(self.family)):
                self.list_data.append(self.family[i][0:2])
        # else:   # 选择模板
        # self.isModel = True

        self.listWidget_model.clear()
        for index in range(len(self.list_data)):
            self.creat_model_item(self.list_data[index][0], self.list_data[index][1])

    def creat_model_item(self, icon_path, text):
        wg = QtWidgets.QWidget()
        wg.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)  # 鼠标穿透 不响应鼠标点击事件
        hl_item = QtWidgets.QHBoxLayout(wg)
        hl_item.setContentsMargins(5, 0, 5, 0)

        pb_left = QtWidgets.QPushButton()
        pb_left.setText(Utils.elideText(text, 250, pb_left.font()))
        pb_left.setStyleSheet("font-size:16px;font-family:MicrosoftYaHei;font-weight:bold;"
                              "color:rgba(0,0,200,1);"
                              "border:none;qproperty-iconSize:30px 30px;"
                              "qproperty-icon: url({});".format(icon_path))
        pb_right = QtWidgets.QPushButton()
        pb_right.setStyleSheet("color:rgba(77,77,77,1);"
                               "border:none; qproperty-iconSize:30px 30px;"
                               "qproperty-icon: url(./res/right.png) off, url(./res/cross_1.png) on;")
        hl_item.addWidget(pb_left)
        hl_item.addStretch()
        hl_item.addWidget(pb_right)
        # font = QtGui.QFont('Microsoft YaHei')
        # font.setPointSize(12)
        # font.setBold(True)
        # pb_right.setFont(font)
        item = QtWidgets.QListWidgetItem()  # 创建QListWidgetItem对象
        item.setSizeHint(QtCore.QSize(220, 40))  # 设置QListWidgetItem大小
        self.listWidget_model.addItem(item)  # 添加item
        self.listWidget_model.setItemWidget(item, wg)  # 为item设置widget

    def card_animation(self, index):
        self.parent.card = DlgCard(self.parent)
        rect = self.geometry()
        self.parent.card.setGeometry(rect.x() + rect.width(), rect.y(), self.parent.card.width(), rect.height())
        Utils.doAnim(self.parent.card)
        self.parent.card.update_card(index)
        self.close()

    def slot_keyword_changed(self):
        print('slot_save')

    def slot_open(self):
        print('open图标文件')

    def slot_closed(self):
        if self.isModel:
            self.isModel = False
            self.toolButton_model.setIcon(QtGui.QIcon('./res/exit.png'))
            self.label_model.setText('添加项目')
            self.updateList()
        else:
            self.close()

    def slot_model_clicked(self, item):
        cur = item.row()
        if not self.isModel:  # 进入选择模板模式
            self.cur_family = cur
            model_list = self.family[cur][2]
            if model_list:
                self.label_model.setText('选择模板')
                self.toolButton_model.setIcon(QtGui.QIcon('res/left.png'))
                self.listWidget_model.clear()
                self.isModel = True
                units = self.parent.data.data_unit
                print(model_list)
                self.list_data.clear()
                for each in model_list:
                    self.list_data.append(units[each][1:3])
                self.updateList()
            else:
                print('无模板，直接调出 card 对话框')
                # self.isModel = False
                self.card_animation(cur)
        else:  # 进入card类
            # self.isModel = False
            self.card_animation(self.family[self.cur_family][2][cur])

    def slot_tmp(self):
        pass
        # print("这是一个万金油{}".format(self.windowTitle()))

    def resizeEvent(self, event):
        palette = QtGui.QPalette()
        # pix = QtGui.QPixmap('res/background.jpg')
        # pix = pix.scaled(self.width(), self.height())
        # palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        palette.setColor(palette.Background, QtGui.QColor(13, 71, 161))
        self.setPalette(palette)

    def closeEvent(self, event):
        print('close')
        if self.animation is None:
            self.animation = QtCore.QPropertyAnimation(self, b'geometry')
            self.animation.setTargetObject(self)
            self.animation.setDuration(300)
            # self.animation.setEasingCurve(QtCore.QEasingCurve.InQuad)  # 设置动画的节奏
            start_point = self.geometry()
            end_point = QtCore.QRect(start_point.x() + start_point.width(), start_point.y(), start_point.width(),
                                     start_point.height())
            self.animation.setStartValue(start_point)
            self.animation.setEndValue(end_point)
            self.animation.finished.connect(self.close)
            self.animation.start()
            event.ignore()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = DlgCard()
    # win = DlgModel()
    # win = DlgTest()
    # win = Thumbnail()
    # win.setupThumbnail('res/cross.png', '好啊这是什么情况啊安抚啊 啊')
    # win.setIconSize(30)
    # win = DlgField()
    win.show()
    sys.exit(app.exec_())
