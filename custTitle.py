#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @Product: PyCharm
#  @Project: python
#  @File    : custTitle.py
#  @Author  : big
#  @Email   : shdorado@126.com
#  @Time    : 2020/6/25 21:23
#  功能：

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets  # pip install PyQtWebEngine

# region 可拉伸的无边框
qss = """/**********Title**********/
    QTitleLabel{
            background-color: Gainsboro;
            font: 100 10pt;
    }

    /**********Button**********/
    QTitleButton{
            background-color: rgba(255, 255, 255, 0);
            color: black;
            border: 0px;
            font: 100 10pt;
    }
    QTitleButton#MinMaxButton:hover{
            background-color: #D0D0D1;
            border: 0px;
            font: 100 10pt;
    }
    QTitleButton#CloseButton:hover{
            background-color: #D32424;
            color: white;
            border: 0px;
            font: 100 10pt;
    }

    """


class QTitleLabel(QLabel):
    """
    新建标题栏标签类
    """

    def __init__(self, *args):
        super(QTitleLabel, self).__init__(*args)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setFixedHeight(30)


class QTitleButton(QPushButton):
    """
    新建标题栏按钮类
    """

    def __init__(self, *args):
        super(QTitleButton, self).__init__(*args)
        self.setFont(QFont("Webdings"))  # 特殊字体以不借助图片实现最小化最大化和关闭按钮
        self.setFixedWidth(40)


class QUnFrameWindow(QWidget):
    """
    无边框窗口类
    """

    def __init__(self, *args, **kwargs):
        super(QUnFrameWindow, self).__init__(None, Qt.FramelessWindowHint)  # 设置为顶级窗口，无边框
        # super(QUnFrameWindow, self).__init__(*args, **kwargs)
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏边框

        self._padding = 5  # 设置边界宽度为5
        self.initTitleLabel()  # 安放标题栏标签
        self.setWindowTitle = self._setTitleText(self.setWindowTitle)  # 用装饰器将设置WindowTitle名字函数共享到标题栏标签上
        self.setWindowTitle("自定义")
        self.initLayout()  # 设置框架布局
        self.setMinimumWidth(250)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.initDrag()  # 设置鼠标跟踪判断默认值
        self.resize(800, 600)
        self.setStyleSheet(qss)

    def initDrag(self):
        # 设置鼠标跟踪判断扳机默认值
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False

    def initTitleLabel(self):
        # 安放标题栏标签
        self._TitleLabel = QTitleLabel(self)
        self._TitleLabel.setMouseTracking(True)  # 设置标题栏标签鼠标跟踪（如不设，则标题栏内在widget上层，无法实现跟踪）
        self._TitleLabel.setIndent(10)  # 设置标题栏文本缩进
        self._TitleLabel.move(0, 0)  # 标题栏安放到左上角

    def initLayout(self):
        # 设置框架布局
        self._MainLayout = QHBoxLayout()
        self._MainLayout.setSpacing(0)
        self._MainLayout.addWidget(QLabel(), Qt.AlignLeft)  # 顶一个QLabel在竖放框架第一行，以免正常内容挤占到标题范围里
        self._MainLayout.addStretch()
        self.setLayout(self._MainLayout)

    def addLayout(self, QLayout):
        # 给widget定义一个addLayout函数，以实现往竖放框架的正确内容区内嵌套Layout框架
        self._MainLayout.addLayout(QLayout)

    def _setTitleText(self, func):
        # 设置标题栏标签的装饰器函数
        def wrapper(*args):
            self._TitleLabel.setText(*args)
            return func(*args)

        return wrapper

    def setTitleAlignment(self, alignment):
        # 给widget定义一个setTitleAlignment函数，以实现标题栏标签的对齐方式设定
        self._TitleLabel.setAlignment(alignment | Qt.AlignVCenter)

    def setCloseButton(self, bool):
        # 给widget定义一个setCloseButton函数，为True时设置一个关闭按钮
        if bool == True:
            self._CloseButton = QTitleButton(b'\xef\x81\xb2'.decode("utf-8"), self)
            self._CloseButton.setObjectName("CloseButton")  # 设置按钮的ObjectName以在qss样式表内定义不同的按钮样式
            self._CloseButton.setToolTip("关闭窗口")
            self._CloseButton.setMouseTracking(True)  # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self._CloseButton.setFixedHeight(self._TitleLabel.height())  # 设置按钮高度为标题栏高度
            self._CloseButton.clicked.connect(self.close)  # 按钮信号连接到关闭窗口的槽函数

    def setMinMaxButtons(self, bool):
        # 给widget定义一个setMinMaxButtons函数，为True时设置一组最小化最大化按钮
        if bool == True:
            self._MinimumButton = QTitleButton(b'\xef\x80\xb0'.decode("utf-8"), self)
            self._MinimumButton.setObjectName("MinMaxButton")  # 设置按钮的ObjectName以在qss样式表内定义不同的按钮样式
            self._MinimumButton.setToolTip("最小化")
            self._MinimumButton.setMouseTracking(True)  # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self._MinimumButton.setFixedHeight(self._TitleLabel.height())  # 设置按钮高度为标题栏高度
            self._MinimumButton.clicked.connect(self.showMinimized)  # 按钮信号连接到最小化窗口的槽函数
            self._MaximumButton = QTitleButton(b'\xef\x80\xb1'.decode("utf-8"), self)
            self._MaximumButton.setObjectName("MinMaxButton")  # 设置按钮的ObjectName以在qss样式表内定义不同的按钮样式
            self._MaximumButton.setToolTip("最大化")
            self._MaximumButton.setMouseTracking(True)  # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self._MaximumButton.setFixedHeight(self._TitleLabel.height())  # 设置按钮高度为标题栏高度
            self._MaximumButton.clicked.connect(self._changeNormalButton)  # 按钮信号连接切换到恢复窗口大小按钮函数

    def _changeNormalButton(self):
        # 切换到恢复窗口大小按钮
        try:
            self.showMaximized()  # 先实现窗口最大化
            self._MaximumButton.setText(b'\xef\x80\xb2'.decode("utf-8"))  # 更改按钮文本
            self._MaximumButton.setToolTip("恢复")  # 更改按钮提示
            self._MaximumButton.disconnect()  # 断开原本的信号槽连接
            self._MaximumButton.clicked.connect(self._changeMaxButton)  # 重新连接信号和槽
        except:
            pass

    def _changeMaxButton(self):
        # 切换到最大化按钮
        try:
            self.showNormal()
            self._MaximumButton.setText(b'\xef\x80\xb1'.decode("utf-8"))
            self._MaximumButton.setToolTip("最大化")
            self._MaximumButton.disconnect()
            self._MaximumButton.clicked.connect(self._changeNormalButton)
        except:
            pass

    def resizeEvent(self, QResizeEvent):
        # 自定义窗口调整大小事件
        self._TitleLabel.setFixedWidth(self.width())  # 将标题标签始终设为窗口宽度
        # 分别移动三个按钮到正确的位置
        try:
            self._CloseButton.move(self.width() - self._CloseButton.width(), 0)
        except:
            pass
        try:
            self._MinimumButton.move(self.width() - (self._CloseButton.width() + 1) * 3 + 1, 0)
        except:
            pass
        try:
            self._MaximumButton.move(self.width() - (self._CloseButton.width() + 1) * 2 + 1, 0)
        except:
            pass
        # 重新调整边界范围以备实现鼠标拖放缩放窗口大小，采用三个列表生成式生成三个列表
        self._right_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                            for y in range(1, self.height() - self._padding)]
        self._bottom_rect = [QPoint(x, y) for x in range(1, self.width() - self._padding)
                             for y in range(self.height() - self._padding, self.height() + 1)]
        self._corner_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                             for y in range(self.height() - self._padding, self.height() + 1)]

    def mousePressEvent(self, event):
        # 重写鼠标点击的事件
        if (event.button() == Qt.LeftButton) and (event.pos() in self._corner_rect):
            # 鼠标左键点击右下角边界区域
            self._corner_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._right_rect):
            # 鼠标左键点击右侧边界区域
            self._right_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._bottom_rect):
            # 鼠标左键点击下侧边界区域
            self._bottom_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.y() < self._TitleLabel.height()):
            # 鼠标左键点击标题栏区域
            self._move_drag = True
            self.move_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        # 判断鼠标位置切换鼠标手势
        if QMouseEvent.pos() in self._corner_rect:
            self.setCursor(Qt.SizeFDiagCursor)
        elif QMouseEvent.pos() in self._bottom_rect:
            self.setCursor(Qt.SizeVerCursor)
        elif QMouseEvent.pos() in self._right_rect:
            self.setCursor(Qt.SizeHorCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        # 当鼠标左键点击不放及满足点击区域的要求后，分别实现不同的窗口调整
        # 没有定义左方和上方相关的5个方向，主要是因为实现起来不难，但是效果很差，拖放的时候窗口闪烁，再研究研究是否有更好的实现
        if Qt.LeftButton and self._right_drag:
            # 右侧调整窗口宽度
            self.resize(QMouseEvent.pos().x(), self.height())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._bottom_drag:
            # 下侧调整窗口高度
            self.resize(self.width(), QMouseEvent.pos().y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._corner_drag:
            # 右下角同时调整高度和宽度
            self.resize(QMouseEvent.pos().x(), QMouseEvent.pos().y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._move_drag:
            # 标题栏拖放窗口位置
            self.move(QMouseEvent.globalPos() - self.move_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        # 鼠标释放后，各扳机复位
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False


# endregion


# 样式


style_list = """
QListWidget, QListView, QTreeWidget, QTreeView {
    outline: 0px;
}

QListWidget {
    min-width: 120px;
    max-width: 120px;
    color: Black;
    background: #F5F5F5;
}

QListWidget::Item:selected {
    background: lightGray;
    border-left: 5px solid red;
}
HistoryPanel:hover {
    background: rgb(52, 52, 52);
}
"""


class LeftTabWidget(QWidget):
    """左侧选项栏"""

    def __init__(self):
        super(LeftTabWidget, self).__init__()

        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 设置无边框窗口
        self.resize(800, 600)
        self.setObjectName('LeftTabWidget')

        """ 
                设置窗口边框圆角时有两种方式，一种是设置样式，另一种是在paintEvent事件中绘制窗口
                    border-radius 属性，关于这个属性，可选的样式有
                    border-top-left-radius 设置左上角圆角;
                    border-top-right-radius 设置右上角圆角;
                    border-bottom-left-radius 设置左下角圆角;
                    border-bottom-right-radius 设置右下角圆角;
                    border-radius 设置四个角圆角;
                        border-radius:15px 一个参数
                        border-radius: 15px 50px  两个参数 第一个参数设置X轴方向的半径 第二个参数设置Y轴方向的半径 

                    设置无边框或者背景透明可以去掉按钮的白色方框
                    给按钮设置如下样式即可。
                    {background-color:transparent;}
                    或者
                    {border:none;}
                """
        # self.setStyleSheet('background-image:url(./res/images/background1.jpg);border-radius:20px;')

        self.setWindowTitle('LeftTabWidget')
        self.list_style = style_list

        self.main_layout = QHBoxLayout(self, spacing=0)  # 窗口的整体布局
        self.main_layout.setContentsMargins(10, 0, 0, 0)

        self.left_widget = QtWidgets.QListWidget()  # 左侧选项列表
        self.left_widget.setStyleSheet(self.list_style)
        self.main_layout.addWidget(self.left_widget)
        #
        self.right_widget = QtWidgets.QStackedWidget()
        # self.right_widget =QLabel('dgsagaga')
        self.right_widget.setStyleSheet('background-color: blue')
        self.right_widget.setFixedSize(80, 50)
        self.main_layout.addWidget(self.right_widget)

        self._setup_ui()

    def _setup_ui(self):
        """加载界面ui"""
        # self.left_widget.currentRowChanged.connect(self.right_widget.setCurrentIndex)  # list和右侧窗口的index对应绑定

        self.left_widget.setFrameShape(QtWidgets.QListWidget.NoFrame)  # 去掉边框

        self.left_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏滚动条
        self.left_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        list_str = ['岗位需求', '专业要求', '薪水分布', '城市分布']
        url_list = ['1.html',
                    'edu_need.html', 'salary_bar.html', 'edu_salary_bar.mhtml']

        for i in range(4):
            self.item = QtWidgets.QListWidgetItem(list_str[i], self.left_widget)  # 左侧选项的添加
            self.item.setSizeHint(QSize(30, 60))
            self.item.setTextAlignment(Qt.AlignCenter)  # 居中显示

            self.browser = QtWebEngineWidgets.QWebEngineView()  # 右侧用QWebView来显示html网页
            self.browser.setUrl(QtCore.QUrl.fromLocalFile('C:/Users/big/Desktop/tt/%s' % url_list[i]))
            # self.right_widget.addWidget(self.browser)
            # self.right_widget.addWidget(QtWidgets.QLabel(f'tu pian a {i}'))

    def paintEvent(self, event):
        # # 主窗体无边框时是加载不了样式的，仅在子控件上实现样式。
        # # 要在主窗体本身实现样式，需要在paintEvent事件中加上如下代码，设置底图也是一样的
        # opt = QStyleOption()
        # opt.initFrom(self)
        # p = QPainter(self)
        # p.setRenderHint(QPainter.Antialiasing)  # 反锯齿
        # self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
        # super(LeftTabWidget, self).paintEvent(event)

        # 不通过样式，直接设置圆角，通用，且不继承于子控件
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.Antialiasing)  # 反锯齿
        # painter.setBrush(QBrush(QPixmap('./res/images/background10.jpg')))#底图
        # painter.setBrush(QBrush(Qt.red))#颜色
        # painter.setPen(Qt.transparent)
        #
        # rect = self.rect()
        # rect.setWidth(rect.width() - 1)
        # rect.setHeight(rect.height() - 1)
        # painter.drawRoundedRect(rect, 15, 15)
        # 也可用QPainterPath 绘制代替 painter.drawRoundedRect(rect, 15, 15)
        # painterPath= QPainterPath()
        # painterPath.addRoundedRect(rect, 15, 15)
        # painter.drawPath(painterPath)

        # 底图
        pixmap = QPixmap('./res/images/background10.jpg')
        painter.drawPixmap(self.rect(), pixmap)

        super(LeftTabWidget, self).paintEvent(event)


class TitleBar(QWidget):
    StyleSheet = """
    /*标题栏*/
    TitleBar {
        background-color: skyblue;
    }
    /*最小化最大化关闭按钮通用默认背景*/
    #buttonMinimum,#buttonMaximum,#buttonClose {
        border: none;
        background-color: white;
    }
    /*悬停*/
    #buttonMinimum:hover,#buttonMaximum:hover {
        background-color: green;
        color: white;
    }
    /*鼠标按下不放*/
    #buttonMinimum:pressed,#buttonMaximum:pressed {
        background-color: Firebrick;
    }
    #buttonClose:hover {
        color: white;
        background-color: gray;
    }
    #buttonClose:pressed {
        color: white;
        background-color: Firebrick;
    }
    """

    # 信号声明区
    sign_win_minimize = pyqtSignal()  # 窗口最小化信号
    sign_win_maximize = pyqtSignal()  # 窗口最大化信号
    sign_win_resume = pyqtSignal()  # 窗口恢复信号
    sign_win_close = pyqtSignal()  # 窗口关闭信号
    sign_win_move = pyqtSignal(QPoint)  # 窗口移动

    def __init__(self, *args, **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)

        self.setStyleSheet(TitleBar.StyleSheet)
        # 支持qss设置背景
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.mPos = None
        self.iconSize = 20  # 图标的默认大小
        # 设置默认背景颜色,否则由于受到父窗口的影响导致透明
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(palette.Window, QColor(240, 240, 240))
        self.setPalette(palette)
        # 布局
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        # 窗口图标
        self.iconLabel = QLabel(self)
        #         self.iconLabel.setScaledContents(True)
        layout.addWidget(self.iconLabel)
        # 窗口标题
        self.titleLabel = QLabel(self)
        self.titleLabel.setMargin(2)
        layout.addWidget(self.titleLabel)
        # 中间伸缩条
        layout.addSpacerItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        # 利用Webdings字体来显示图标
        font = self.font() or QFont()
        font.setFamily('Webdings')
        # 最小化按钮
        self.buttonMinimum = QPushButton(
            '0', self, clicked=self.sign_win_minimize.emit, font=font, objectName='buttonMinimum')
        layout.addWidget(self.buttonMinimum)
        # 最大化/还原按钮
        self.buttonMaximum = QPushButton(
            '1', self, clicked=self.showMaximized, font=font, objectName='buttonMaximum')
        layout.addWidget(self.buttonMaximum)
        # 关闭按钮
        self.buttonClose = QPushButton(
            'r', self, clicked=self.sign_win_close.emit, font=font, objectName='buttonClose')
        layout.addWidget(self.buttonClose)
        # 初始高度
        self.setHeight()

    def showMaximized(self):
        if self.buttonMaximum.text() == '1':
            # 最大化
            self.buttonMaximum.setText('2')
            self.sign_win_maximize.emit()
        else:  # 还原
            self.buttonMaximum.setText('1')
            self.sign_win_resume.emit()

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
        self.setCursor(Qt.ArrowCursor)
        super(TitleBar, self).enterEvent(event)

    def mouseDoubleClickEvent(self, event):
        super(TitleBar, self).mouseDoubleClickEvent(event)
        self.showMaximized()

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()
        event.accept()

    def mouseReleaseEvent(self, event):
        '''鼠标弹起事件'''
        self.mPos = None
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.mPos:
            self.sign_win_move.emit(self.mapToGlobal(event.pos() - self.mPos))
        event.accept()


# 枚举左上右下以及四个定点
Left, Top, Right, Bottom, LeftTop, RightTop, LeftBottom, RightBottom = range(8)


class FrameLessWindow(QWidget):
    # 四周边距
    Margins = 0

    def __init__(self, *args, **kwargs):
        super(FrameLessWindow, self).__init__(*args, **kwargs)

        self._widget = None
        # self.setStyleSheet(StyleSheet)
        self._mpos = None
        self._pressed = False
        self.Direction = None
        # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 无边框
        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏边框
        # 鼠标跟踪
        self.setMouseTracking(True)
        # 布局
        layout = QVBoxLayout(self, spacing=0)
        # 预留边界用于实现无边框窗口调整大小
        layout.setContentsMargins(self.Margins, self.Margins, self.Margins, self.Margins)
        # 标题栏
        self.titleBar = TitleBar(self)
        layout.addWidget(self.titleBar)
        # 信号槽
        self.titleBar.sign_win_minimize.connect(self.showMinimized)
        self.titleBar.sign_win_maximize.connect(self.showMaximized)
        self.titleBar.sign_win_resume.connect(self.showNormal)
        self.titleBar.sign_win_close.connect(self.close)
        self.titleBar.sign_win_move.connect(self.move)
        # self.windowTitleChanged.connect(self.titleBar.setTitle)
        # self.windowIconChanged.connect(self.titleBar.setIcon)

    def setTitleBarHeight(self, height=38):
        """设置标题栏高度"""
        self.titleBar.setHeight(height)

    def setIconSize(self, size):
        """设置图标的大小"""
        self.titleBar.setIconSize(size)

    def setWidget(self, widget):
        """设置自己的控件"""
        # if hasattr(self, '_widget'):
        #     return

        self._widget = widget
        # 设置默认背景颜色,否则由于受到父窗口的影响导致透明
        widget.setAutoFillBackground(True)
        palette = widget.palette()
        palette.setColor(palette.Window, QColor(240, 240, 240))
        widget.setPalette(palette)
        widget.installEventFilter(self)
        self.layout().addWidget(widget)

    def move(self, pos):
        if self.windowState() == Qt.WindowMaximized or self.windowState() == Qt.WindowFullScreen:
            # 最大化或者全屏则不允许移动
            return
        if self._widget is None:
            return

        super(FrameLessWindow, self).move(pos)

    def showMaximized(self):
        """最大化,要去除上下左右边界,如果不去除则边框地方会有空隙"""
        super(FrameLessWindow, self).showMaximized()
        self.layout().setContentsMargins(0, 0, 0, 0)

    def showNormal(self):
        """还原,要保留上下左右边界,否则没有边框无法调整"""
        super(FrameLessWindow, self).showNormal()
        self.layout().setContentsMargins(
            self.Margins, self.Margins, self.Margins, self.Margins)

    def eventFilter(self, obj, event):
        """事件过滤器,用于解决鼠标进入其它控件后还原为标准鼠标样式"""
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
        return super(FrameLessWindow, self).eventFilter(obj, event)

    def paintEvent(self, event):
        """由于是全透明背景窗口,重绘事件中绘制透明度为1的难以发现的边框,用于调整窗口大小"""
        super(FrameLessWindow, self).paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 255, 255, 1), 2 * self.Margins))
        painter.drawRect(self.rect())

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        super(FrameLessWindow, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._mpos = event.pos()
            self._pressed = True

    def mouseReleaseEvent(self, event):
        """鼠标弹起事件"""
        super(FrameLessWindow, self).mouseReleaseEvent(event)
        self._pressed = False
        self.Direction = None

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""

        super(FrameLessWindow, self).mouseMoveEvent(event)

        pos = event.pos()
        xPos, yPos = pos.x(), pos.y()
        wm, hm = self.width() - self.Margins, self.height() - self.Margins
        if self.isMaximized() or self.isFullScreen():
            self.Direction = None
            self.setCursor(Qt.ArrowCursor)
            return
        if event.buttons() == Qt.LeftButton and self._pressed:
            self._resizeWidget(pos)
            return
        if xPos <= self.Margins and yPos <= self.Margins:
            # 左上角
            self.Direction = LeftTop
            self.setCursor(Qt.SizeFDiagCursor)
        elif wm <= xPos <= self.width() and hm <= yPos <= self.height():
            # 右下角
            self.Direction = RightBottom
            self.setCursor(Qt.SizeFDiagCursor)
        elif wm <= xPos and yPos <= self.Margins:
            # 右上角
            self.Direction = RightTop
            self.setCursor(Qt.SizeBDiagCursor)
        elif xPos <= self.Margins and hm <= yPos:
            # 左下角
            self.Direction = LeftBottom
            self.setCursor(Qt.SizeBDiagCursor)
        elif 0 <= xPos <= self.Margins <= yPos <= hm:
            # 左边
            self.Direction = Left
            self.setCursor(Qt.SizeHorCursor)
        elif wm <= xPos <= self.width() and self.Margins <= yPos <= hm:
            # 右边
            self.Direction = Right
            self.setCursor(Qt.SizeHorCursor)
        elif wm >= xPos >= self.Margins >= yPos >= 0:
            # 上面
            self.Direction = Top
            self.setCursor(Qt.SizeVerCursor)
        elif self.Margins <= xPos <= wm and hm <= yPos <= self.height():
            # 下面
            self.Direction = Bottom
            self.setCursor(Qt.SizeVerCursor)

    def _resizeWidget(self, pos):
        """调整窗口大小"""
        if self.Direction is None:
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

    def center(self):
        qr = self.frameGeometry()
        # print(type(qr), qr)
        cp = QtWidgets.QDesktopWidget().availableGeometry().center() + QtCore.QPoint(1600, 0)
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # screen = QtWidgets.QDesktopWidget().screenGeometry()
        # size = self.geometry()
        # print(size.height())
        # self.move((screen.width() - size.width()) / 2,
        #           (screen.height() - size.height()) / 2)


class YourWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(YourWidget, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.left_tag = LeftTabWidget()
        layout.addWidget(self.left_tag)

        # the same QGraphicsEffect can not be shared by other widgets
        # 无法共享相同的QGraphicsEffect
        for children in self.findChildren(QWidget):
            shadow = QGraphicsDropShadowEffect(blurRadius=15, xOffset=5, yOffset=5, color=QColor(0, 0, 0, 255))
            children.setGraphicsEffect(shadow)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # mainWnd = FrameLessWindow()
    mainWnd = LeftTabWidget()
    # mainWnd.setWindowTitle('测试标题栏')
    # mainWnd.setWindowIcon(QIcon('./res/images/tu.png'))
    # mainWnd.resize(QSize(1250, 780))
    # mainWnd.setWidget(YourWidget())  # 把自己的窗口添加进来
    mainWnd.show()
    sys.exit(app.exec_())
