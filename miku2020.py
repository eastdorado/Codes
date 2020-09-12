#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @项目名称: python
# @File    : miku2020.py
# @Time    : 2019/12/27 23:37
# @Author  : big
# @Email   : shdorado@126.com


import sys
# import pyautogui  # 控制鼠标和键盘的模块，实现自动化任务
# pyautogui.PAUSE = 1.5  # 每执行一个函数后暂停几秒钟
# pyautogui.FAILSAFE = True  # 鼠标移动到屏幕的左上角时触法PyAutoGUI的FailSafeException异常

from utilities import Utils, AnimWin, AllData
from myUi import DlgModel, DlgCard, UiMain

from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtCore import QSize
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtCore import Qt, pyqtSignal, QPoint
# from PyQt5.QtGui import QFont, QEnterEvent, QPainter, QColor, QPen
# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QPushButton
# from PyQt5.QtGui import QIcon
# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit

# 样式
Qss = '''
            QLabel#TitleContent
            {
                color: #FFFFFF;
            }
        
            QPushButton#ButtonMin
            {
                border-image:url(./min.png) 0 81 0 0 ;

            }

            QPushButton#ButtonMin:hover
            {
                border-image:url(./min.png) 0 54 0 27 ;
            }

            QPushButton#ButtonMin:pressed
            
            {
                border-image:url(./min.png) 0 27 0 54 ;
            }

            QPushButton#ButtonMax
            {
                border-image:url(./max.png) 0 81 0 0 ;
            }

            QPushButton#ButtonMax:hover
            {
                border-image:url(./max.png) 0 54 0 27 ;
            }

            QPushButton#ButtonMax:pressed
            {
                border-image:url(./max.png) 0 27 0 54 ;
            }

            QPushButton#ButtonRestore
            {
                border-image:url(./restore.png) 0 81 0 0 ;
            }

            QPushButton#ButtonRestore:hover
            {
                border-image:url(./restore.png) 0 54 0 27 ;
            }

            QPushButton#ButtonRestore:pressed
            {
                border-image:url(./restore.png) 0 27 0 54 ;
            }

            QPushButton#ButtonClose
            {
                border-image:url(./close.png) 0 81 0 0 ;
                border-top-right-radius:3 ;
            }

            QPushButton#ButtonClose:hover
            {
                border-image:url(./close.png) 0 54 0 27 ;
                border-top-right-radius:3 ;
            }

            QPushButton#ButtonClose:pressed
            {
                border-image:url(./close.png) 0 27 0 54 ;
                border-top-right-radius:3 ;
            }
'''
StyleSheet = """
/*标题栏*/
TitleBar {
    background-color: #00AEAE;
}
/*最小化最大化关闭按钮通用默认背景*/
#buttonMinimum,#buttonMaximum,#buttonClose {
    border: none;
    background-color: #00AEAE;
}
/*悬停*/
#buttonMinimum:hover,#buttonMaximum:hover:hover {
    background-color: #00E3E3;
    color: white;
}
#buttonClose:hover {
    color: white;
}
/*鼠标按下不放*/
#buttonMinimum:pressed,#buttonMaximum:pressed {
    background-color: Firebrick;
}
#buttonClose:pressed {
    color: white;
    background-color: Firebrick;
}
"""

# 按钮高度
BUTTON_HEIGHT = 30
# 按钮宽度
BUTTON_WIDTH = 30
# 标题栏高度
TITLE_HEIGHT = 30


class TitleBar(QtWidgets.QWidget):
    # 窗口最小化信号
    windowMinimumed = QtCore.pyqtSignal()
    # 窗口最大化信号
    windowMaximumed = QtCore.pyqtSignal()
    # 窗口还原信号
    windowNormaled = QtCore.pyqtSignal()
    # 窗口关闭信号
    windowClosed = QtCore.pyqtSignal()
    # 窗口移动
    windowMoved = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, *args, **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)
        # 支持qss设置背景
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet(StyleSheet)
        self.mPos = None
        self.iconSize = 20  # 图标的默认大小
        # 设置默认背景颜色,否则由于受到父窗口的影响导致透明
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(palette.Window, QtGui.QColor(240, 240, 240))
        self.setPalette(palette)
        # 布局
        layout = QtWidgets.QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        # 窗口图标
        self.iconLabel = QtWidgets.QLabel(self)
        #         self.iconLabel.setScaledContents(True)
        layout.addWidget(self.iconLabel)
        # 窗口标题
        self.titleLabel = QtWidgets.QLabel(self)
        self.titleLabel.setMargin(2)
        layout.addWidget(self.titleLabel)
        # 中间伸缩条
        layout.addSpacerItem(QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        # 利用Webdings字体来显示图标
        font = self.font() or QtGui.QFont()
        font.setFamily('Webdings')

        self.buttonmy = QtWidgets.QPushButton('dd')
        layout.addWidget(self.buttonmy)

        # 最小化按钮
        self.buttonMinimum = QtWidgets.QPushButton(
            '0', self, clicked=self.windowMinimumed.emit, font=font, objectName='buttonMinimum')
        layout.addWidget(self.buttonMinimum)
        # 最大化/还原按钮
        self.buttonMaximum = QtWidgets.QPushButton(
            '1', self, clicked=self.showMaximized, font=font, objectName='buttonMaximum')
        layout.addWidget(self.buttonMaximum)
        # 关闭按钮
        self.buttonClose = QtWidgets.QPushButton(
            'r', self, clicked=self.windowClosed.emit, font=font, objectName='buttonClose')
        layout.addWidget(self.buttonClose)
        # 初始高度
        self.setHeight()

    def showMaximized(self):
        if self.buttonMaximum.text() == '1':
            # 最大化
            self.buttonMaximum.setText('2')
            self.windowMaximumed.emit()
        else:  # 还原
            self.buttonMaximum.setText('1')
            self.windowNormaled.emit()

    def setHeight(self, height=38):
        """设置标题栏高度"""
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        # 设置右边按钮的大小
        self.buttonMinimum.setMinimumSize(height, height)
        self.buttonMinimum.setMaximumSize(height, height)
        self.buttonMaximum.setMinimumSize(height, height)
        self.buttonMaximum.setMaximumSize(height, height)
        self.buttonClose.setMinimumSize(height, height)
        self.buttonClose.setMaximumSize(height, height)

    def setTitle(self, title):
        """设置标题"""
        self.titleLabel.setText(title)

    def setIcon(self, icon):
        """设置图标"""
        self.iconLabel.setPixmap(icon.pixmap(self.iconSize, self.iconSize))

    def setIconSize(self, size):
        """设置图标大小"""
        self.iconSize = size

    def enterEvent(self, event):
        self.setCursor(QtCore.Qt.ArrowCursor)
        super(TitleBar, self).enterEvent(event)

    def mouseDoubleClickEvent(self, event):
        super(TitleBar, self).mouseDoubleClickEvent(event)
        self.showMaximized()

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == QtCore.Qt.LeftButton:
            self.mPos = event.pos()
        event.accept()

    def mouseReleaseEvent(self, event):
        '''鼠标弹起事件'''
        self.mPos = None
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and self.mPos:
            self.windowMoved.emit(self.mapToGlobal(event.pos() - self.mPos))
        event.accept()


# 枚举左上右下以及四个定点
Left, Top, Right, Bottom, LeftTop, RightTop, LeftBottom, RightBottom = range(8)


class FramelessWindow(QtWidgets.QWidget):
    # 四周边距
    Margins = 5

    def __init__(self, *args, **kwargs):
        super(FramelessWindow, self).__init__(*args, **kwargs)
        # self.setStyleSheet('#FramelessWindow{border-image:url(./res/background.jpg);}')
        # self.setStyleSheet('background-image:url(res/background.jpg)')
        self.setMinimumHeight(550)
        self.resize(1100, 600)

        self._pressed = False
        self.Direction = None
        # 背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        # 无边框
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        # 鼠标跟踪
        self.setMouseTracking(True)
        # 布局
        layout = QtWidgets.QVBoxLayout(self, spacing=0)
        # 预留边界用于实现无边框窗口调整大小
        layout.setContentsMargins(
            self.Margins, self.Margins, self.Margins, self.Margins)
        # 标题栏
        self.titleBar = TitleBar(self)
        layout.addWidget(self.titleBar)
        # 信号槽
        self.titleBar.windowMinimumed.connect(self.showMinimized)
        self.titleBar.windowMaximumed.connect(self.showMaximized)
        self.titleBar.windowNormaled.connect(self.showNormal)
        self.titleBar.windowClosed.connect(self.close)
        self.titleBar.windowMoved.connect(self.move)
        self.windowTitleChanged.connect(self.titleBar.setTitle)
        self.windowIconChanged.connect(self.titleBar.setIcon)

    def setTitleBarHeight(self, height=38):
        """设置标题栏高度"""
        self.titleBar.setHeight(height)

    def setIconSize(self, size):
        """设置图标的大小"""
        self.titleBar.setIconSize(size)

    def setWidget(self, widget):
        """设置自己的控件"""
        if hasattr(self, '_widget'):
            return
        self._widget = widget
        # 设置默认背景颜色,否则由于受到父窗口的影响导致透明
        self._widget.setAutoFillBackground(True)
        palette = self._widget.palette()
        palette.setColor(palette.Window, QtGui.QColor(240, 240, 240))
        self._widget.setPalette(palette)
        self._widget.installEventFilter(self)
        self.layout().addWidget(self._widget)

    def move(self, pos):
        if self.windowState() == QtCore.Qt.WindowMaximized or self.windowState() == QtCore.Qt.WindowFullScreen:
            # 最大化或者全屏则不允许移动
            return
        super(FramelessWindow, self).move(pos)

    def showMaximized(self):
        """最大化,要去除上下左右边界,如果不去除则边框地方会有空隙"""
        super(FramelessWindow, self).showMaximized()
        self.layout().setContentsMargins(0, 0, 0, 0)

    def showNormal(self):
        """还原,要保留上下左右边界,否则没有边框无法调整"""
        super(FramelessWindow, self).showNormal()
        self.layout().setContentsMargins(
            self.Margins, self.Margins, self.Margins, self.Margins)

    def eventFilter(self, obj, event):
        """事件过滤器,用于解决鼠标进入其它控件后还原为标准鼠标样式"""
        if isinstance(event, QtGui.QEnterEvent):
            self.setCursor(QtCore.Qt.ArrowCursor)
        return super(FramelessWindow, self).eventFilter(obj, event)

    def paintEvent(self, event):
        """由于是全透明背景窗口,重绘事件中绘制透明度为1的难以发现的边框,用于调整窗口大小"""
        super(FramelessWindow, self).paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 1), 2 * self.Margins))
        painter.drawRect(self.rect())

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        super(FramelessWindow, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self._mpos = event.pos()
            self._pressed = True

    def mouseReleaseEvent(self, event):
        '''鼠标弹起事件'''
        super(FramelessWindow, self).mouseReleaseEvent(event)
        self._pressed = False
        self.Direction = None

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        super(FramelessWindow, self).mouseMoveEvent(event)
        pos = event.pos()
        xPos, yPos = pos.x(), pos.y()
        wm, hm = self.width() - self.Margins, self.height() - self.Margins
        if self.isMaximized() or self.isFullScreen():
            self.Direction = None
            self.setCursor(QtCore.Qt.ArrowCursor)
            return
        if event.buttons() == QtCore.Qt.LeftButton and self._pressed:
            self._resizeWidget(pos)
            return
        if xPos <= self.Margins and yPos <= self.Margins:
            # 左上角
            self.Direction = LeftTop
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif wm <= xPos <= self.width() and hm <= yPos <= self.height():
            # 右下角
            self.Direction = RightBottom
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif wm <= xPos and yPos <= self.Margins:
            # 右上角
            self.Direction = RightTop
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
        elif xPos <= self.Margins and hm <= yPos:
            # 左下角
            self.Direction = LeftBottom
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
        elif 0 <= xPos <= self.Margins and self.Margins <= yPos <= hm:
            # 左边
            self.Direction = Left
            self.setCursor(QtCore.Qt.SizeHorCursor)
        elif wm <= xPos <= self.width() and self.Margins <= yPos <= hm:
            # 右边
            self.Direction = Right
            self.setCursor(QtCore.Qt.SizeHorCursor)
        elif self.Margins <= xPos <= wm and 0 <= yPos <= self.Margins:
            # 上面
            self.Direction = Top
            self.setCursor(QtCore.Qt.SizeVerCursor)
        elif self.Margins <= xPos <= wm and hm <= yPos <= self.height():
            # 下面
            self.Direction = Bottom
            self.setCursor(QtCore.Qt.SizeVerCursor)

    def _resizeWidget(self, pos):
        """调整窗口大小"""
        if self.Direction == None:
            return
        mpos = pos - self._mpos
        xPos, yPos = mpos.x(), mpos.y()
        geometry = self.geometry()
        x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()
        if self.Direction == LeftTop:  # 左上角
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
        elif self.Direction == RightBottom:  # 右下角
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos = pos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos = pos
        elif self.Direction == RightTop:  # 右上角
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos.setX(pos.x())
        elif self.Direction == LeftBottom:  # 左下角
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos.setY(pos.y())
        elif self.Direction == Left:  # 左边
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            else:
                return
        elif self.Direction == Right:  # 右边
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos = pos
            else:
                return
        elif self.Direction == Top:  # 上面
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            else:
                return
        elif self.Direction == Bottom:  # 下面
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos = pos
            else:
                return
        self.setGeometry(x, y, w, h)


class MyMain(QtWidgets.QWidget, UiMain):
    def __init__(self, *args, **kwargs):
        super(MyMain, self).__init__(*args, **kwargs)
        self.parent = kwargs
        self.data = AllData()  # 数据接口
        self.wg_list_left = []  # 左列表项的widget
        self.hided_family = True  # 做列表项的展开或收起
        self.data_list_mid = []  # 保存检索结果在数据区的序号

        self.card = None
        self.model = None

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 窗体无边框
        # self.setWindowOpacity(0.1)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 透明
        # self.resize(1100, 560)

        self.setupUI(self)
        self.init_ui()

    def init_ui(self):

        self.update_left()
        self.update_mid()

    def update_left(self):
        # TODO 创建所有控件
        self.wg_list_left.clear()
        self.wg_list_left.append(self.creat_left_item('res/house.png', '所有项目', 2000))
        self.wg_list_left.append(self.creat_left_item('res/star.png', '收藏夹', 8))
        self.wg_list_left.append(self.creat_left_item('res/points.png', '类别', -1))
        for i in range(len(self.data.data_family)):
            self.wg_list_left.append(self.creat_left_item(self.data.data_family[i][0], self.data.data_family[i][1], 8))
        self.wg_list_left.append(self.creat_left_item('res/add.png', '标签', -1))
        self.wg_list_left.append(self.creat_left_item('', '瞭望塔', -2))
        self.wg_list_left.append(self.creat_left_item('', '其他', -2))

        # TODO 创建所有列表项
        for each in self.wg_list_left:
            item = QtWidgets.QListWidgetItem()  # 创建QListWidgetItem对象
            item.setSizeHint(QtCore.QSize(210, 40))  # 设置QListWidgetItem大小
            self.listWidget_left.addItem(item)  # 添加item
            self.listWidget_left.setItemWidget(item, each)  # 为item设置widget

        # TODO 收缩列表项
        for i in range(len(self.data.data_family)):
            self.listWidget_left.setRowHidden(i + 3, self.hided_family)

        # pyautogui.click(38, 500, clicks=1, interval=0.0, button='left')
        self.listWidget_left.setCurrentRow(0)

        # brush_red = QtGui.QBrush(Qt.red)
        # root.setBackground(0, brush_red)
        # brush_blue = QtGui.QBrush(Qt.blue)
        # root.setBackground(1, brush_blue)
        # QtWidgets.QToolTip.setFont(QFont('OldEnglish', 30))

    def update_mid(self):
        self.listWidget_mid.clear()
        if not self.data_list_mid:
            return

        for each in self.data_list_mid:
            card = self.data.data_cards[each]
            self.creat_mid_item(card[1], card[2], card[3][1])

    def creat_left_item(self, icon_path, text, num=0):
        wg = QtWidgets.QWidget()
        wg.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)  # 鼠标穿透 不响应鼠标点击事件
        # wg.setFixedWidth(80)
        hl_item = QtWidgets.QHBoxLayout(wg)
        hl_item.setContentsMargins(5, 0, 5, 0)

        pb_left = QtWidgets.QPushButton()
        # pb_left.clicked.connect(lambda: self.slot_left_clicked(text))
        if num == -2:
            qss = "font-size:16px;font-family:MicrosoftYaHei;font-weight:bold;" \
                  "color:rgba(0,0,200,1);" \
                  "border:none;"
            pb_left.setStyleSheet(qss)
            text = Utils.elideText(text, 180, pb_left.font())
            hl_item.addWidget(pb_left)
            hl_item.addStretch()
        elif num == -1:
            pb_left.setStyleSheet("font-size:16px;font-family:MicrosoftYaHei;font-weight:bold;"
                                  "color:rgba(0,0,200,1);"
                                  "border:none;")
            pb_right = QtWidgets.QPushButton()
            pb_right.setStyleSheet("color:rgba(77,77,77,1);"
                                   "border:none; qproperty-iconSize:30px 30px;"
                                   "qproperty-icon: url({}) off, url(./res/cross_1.png) on;".format(icon_path))
            text = Utils.elideText(text, 150, pb_left.font())
            hl_item.addWidget(pb_left)
            hl_item.addStretch()
            hl_item.addWidget(pb_right)
        elif num >= 0:
            pb_left.setStyleSheet("font-size:16px;font-family:MicrosoftYaHei;font-weight:bold;"
                                  "color:rgba(77,77,77,1);"
                                  "border:none;"
                                  "qproperty-iconSize:30px 30px;"
                                  "qproperty-icon: url({});".format(icon_path))
            pb_right = QtWidgets.QPushButton(str(num))
            pb_right.setStyleSheet("border:1px groove gray;border-radius:10px;padding:2px 4px;"
                                   "color:rgba(77,77,77,1);")  # 圆角
            font = QtGui.QFont('Microsoft YaHei')
            font.setPointSize(12)
            font.setBold(True)
            pb_right.setFont(font)

            text = Utils.elideText(text, 120, pb_left.font())

            hl_item.addWidget(QtWidgets.QLabel(' '))
            hl_item.addWidget(pb_left)
            hl_item.addStretch()
            hl_item.addWidget(pb_right)
        else:
            AnimWin('list item 序号超出范围')
            return
            # pb_left.setStyleSheet("text-align: right;")
        pb_left.setText(text)
        return wg

    def creat_mid_item(self, icon_path, text1, text2):
        wg = QtWidgets.QWidget()
        wg.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)  # 鼠标穿透 不响应鼠标点击事件
        # wg.setObjectName(text2)
        hl_item = QtWidgets.QHBoxLayout(wg)
        hl_item.setContentsMargins(5, 0, 0, 0)

        msg = text1 + '\n' + text2
        pb = QtWidgets.QPushButton(msg)
        pb.setStyleSheet("font-size:16px;font-family:MicrosoftYaHei;font-weight:bold;"
                         "color:rgba(77,77,77,1);"
                         "border:none;"
                         "qproperty-iconSize:40px 40px;"
                         "qproperty-icon: url({});".format(icon_path))
        # pb.setStyleSheet("text-align: right;")
        hl_item.addWidget(pb)
        hl_item.addStretch()

        item = QtWidgets.QListWidgetItem()  # 创建QListWidgetItem对象
        item.setSizeHint(QtCore.QSize(220, 60))  # 设置QListWidgetItem大小
        self.listWidget_mid.addItem(item)  # 添加item
        self.listWidget_mid.setItemWidget(item, wg)  # 为item设置widget

    def show_card(self, index):
        print('show_card')
        rect = self.rect()
        dlg = DlgCard(index, self)
        dlg.setGeometry(rect.x() + rect.width(), rect.y(), dlg.width(), rect.height())
        Utils.doAnim(dlg, self)

    # <editor-fold desc="创建右键菜单">
    def creat_menu(self):
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # 创建QMenu
        self.contextMenu = QtWidgets.QMenu(self)
        self.actionA = self.contextMenu.addAction(QtWidgets.QIcon("images/0.png"), u'|  删除')
        # 显示菜单
        self.customContextMenuRequested.connect(self.showContextMenu)
        # 点击删除menu
        self.contextMenu.triggered[QtWidgets.QAction].connect(self.remove)

    def showContextMenu(self):
        # 如果有选中项，则显示显示菜单
        items = self.view.selectedIndexes()
        if items:
            self.contextMenu.show()
            self.contextMenu.exec_(QtGui.QCursor.pos())  # 在鼠标位置显示

    def remove(self, qAction):
        print(self.f)
        # self.view.takeItem(self.f)#删除行(实际上是断开了与list的联系)

        # 注意：removeItemWidget(self, QListWidgetItem)  # 移除一个Item，无返回值
        # 注意：takeItem(self, int)  # 切断一个Item与List的联系，返回该Item
        self.view.removeItemWidget(self.view.takeItem(self.f))  # 删除

    # </editor-fold>
    def slot_model_clicked(self):
        print('slot_model_clicked')

    def slot_mid_clicked(self, item):
        cur = item.row()
        print(cur)
        print('mid data:{}'.format(self.data_list_mid[cur]))
        print('card data:{}'.format(self.data.data_cards[cur]))
        # print('haoa {}'.format(index))
        # wg = index.getItemWidget()

    def slot_left_clicked(self, item):
        # index = QtWidgets.QListWidgetItem
        cur = item.row()
        if cur == 0:  # 所有项目
            self.data_list_mid.clear()
            for i in range(len(self.data.data_cards)):
                self.data_list_mid.append(i)
            self.update_mid()
        elif cur == 1:  # 收藏夹
            self.data_list_mid.clear()
            self.data_list_mid = self.data.favorites
            self.update_mid()
        elif cur == 2:  # 类别
            self.hided_family = not self.hided_family
            for i in range(len(self.data.data_family)):
                self.listWidget_left.setRowHidden(i + 3, self.hided_family)
        elif 3 <= cur < 3 + len(self.data.data_family):
            self.data_list_mid.clear()
            for i in range(len(self.data.data_cards)):
                if self.data.data_cards[i][0] == (cur - 3) * 3 + 1:
                    self.data_list_mid.append(i)
            self.update_mid()

        print(cur)

    def slot_select(self, item):
        cur = item.row()
        print(cur)

    def slot_animation(self, control):
        # print('56')
        if control.objectName() == 'toolButton_add':
            # self.model = DlgModel(self)
            # rect = self.rect()
            # self.model.setGeometry(rect.x() + rect.width(), rect.y(), self.model.width(), rect.height())
            # Utils.doAnim(self.model)

            model = DlgModel(self)
            model.init_ui()
            rect = self.rect()
            model.setGeometry(rect.x() + rect.width(), rect.y(), model.width(), rect.height())
            Utils.doAnim(model)
        elif control.objectName() == 'toolButton_edit':
            # if self.card:
            #     return
            print('toolButton_edit')

            self.card = DlgCard(self)
            rect = self.rect()
            self.card.setGeometry(rect.x() + rect.width(), rect.y(), self.card.width(), rect.height())
            Utils.doAnim(self.card)
            self.card.update_card(0, False)

    def slot_vaults(self):
        print('slot_vaults')

    def slot_keyword_changed(self, text):
        print(text)

    def slot_tools_clicked(self, control):
        # print(control.objectName())
        # sender = self.sender()
        # AnimationWin(sender.text() + ' 被按下')
        print('tools')

    def slot_tmp(self):
        pass

        # print("这是一个万金油{}".format(self.windowTitle()))

    def resizeEvent(self, event):
        palette = QtGui.QPalette()
        pix = QtGui.QPixmap('res/images/background.jpg')
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(palette)

        rect = self.rect()
        if self.card:
            self.card.setGeometry(rect.x() + rect.width()-self.card.width(), rect.y(), self.card.width(), rect.height())
        if self.model:
            self.model.setGeometry(rect.x() + rect.width()-self.model.width(), rect.y(), self.model.width(), rect.height())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # qssStyle = CommonHelper.readQss("./res/styleSheet.qss")
    # app.setStyleSheet(qssStyle)
    mainWnd = FramelessWindow()
    mainWnd.setWindowTitle('测试标题栏')
    mainWnd.setWindowIcon(QtGui.QIcon('res/1.gif'))
    # mainWnd.resize(QSize(1250, 780))
    mainWnd.setWidget(MyMain(mainWnd))
    mainWnd.show()
    sys.exit(app.exec_())
