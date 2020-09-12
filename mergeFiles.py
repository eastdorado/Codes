#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @项目名称: python
# @File    : mergeFiles.py
# @Time    : 2020/3/7 12:31
# @Author  : big
# @Email   : shdorado@126.com

import os
import sys
import copy
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets, QtWinExtras
from enum import IntEnum, unique
from ui_mergeFiles import Ui_MainWindow
from utilities import Utils, AnimWin, BackLabel, StyleSheet, FileButler, ImageConvert
from ui_watermark import Ui_Dialog

# import cgitb  # 相当管用
# cgitb.enable(format='text')  # 解决 pyqt5 异常只要进入事件循环,程序就崩溃,而没有任何提示

'''
QFileDialog要使用历史记录，有三个需要注意的地方：
1、directory设为空字符串（ ‘’）；
2、要使用参数少的那个函数方法，即不含有selectedFilter；
3、最后一个参数（options）要设为QtGui.QFileDialog.DontUseNativeDialog
'''


class TitleBar(QtWidgets.QWidget):
    StyleSheet = """
    /*标题栏*/
    TitleBar {
        /*background: transparent;     全透明*/
        /*background-color: skyblue;   */
        /*background-color: rgba(0,0,0,50);   半透明*/
        background: rgba(0, 0, 0, 50);  /*半透明*/
        border-top-left-radius:15;
        border-top-right-radius:15;
        /*background-image:url(./res/background/bk5.jpg);*/
        background-repeat: no-repeat;       /*背景不要重复*/
        background-position: center center;      /*图片的位置，居中，靠左对齐*/
    }
    /*最小化最大化关闭按钮通用默认背景*/
    #buttonMinimum,#buttonMaximum,#buttonClose {
        /*background-color: skyblue;*/
        /*background:rgba(0,0,0,0.3)      半透明*/
        border:none;    /*全透明*/
        color:rgb(0, 200, 200)
    }
    /*悬停*/
    #buttonMinimum:hover,#buttonMaximum:hover {
        /*background-color: green;*/
        /*color: red;放在下面的前面才有效果*/
        background:rgba(0,0,0,0.2)     /*半透明*/
    }
    /*鼠标按下不放*/
    #buttonMinimum:pressed,#buttonMaximum:pressed {
        /*background-color: Firebrick;*/
        /*color: blue;放在下面的前面才有效果*/
        background:rgba(0,0,0,0.4)      /*半透明*/
    }
    #buttonClose:hover {
        color: red;
        /*background-color: gray;*/
        /*background:rgba(0,0,0,0.4)      半透明*/
    }
    #buttonClose:pressed {
        color: red;
        /*background-color: Firebrick;*/
        /*background:rgba(0,0,0,0.4)      半透明*/
    }
    """

    # region 信号声明区
    # sign_pb_prev = QtCore.pyqtSignal()  # 前一个
    # sign_pb_next = QtCore.pyqtSignal()  # 后一个
    sign_win_minimize = QtCore.pyqtSignal()  # 窗口最小化信号
    sign_win_maximize = QtCore.pyqtSignal()  # 窗口最大化信号
    sign_win_resume = QtCore.pyqtSignal()  # 窗口恢复信号
    sign_win_close = QtCore.pyqtSignal()  # 窗口关闭信号
    sign_win_move = QtCore.pyqtSignal(QtCore.QPoint)  # 窗口移动

    # endregion

    def __init__(self, *args, **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)

        # region 总体设计
        self.setStyleSheet(TitleBar.StyleSheet)

        self.setMouseTracking(True)
        # 窗体透明，控件不透明
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)  # 支持qss设置背景
        self.mPos = None
        self.iconSize = 20  # 图标的默认大小
        # 设置默认背景颜色,否则由于受到父窗口的影响导致透明
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(palette.Window, QtGui.QColor(240, 240, 240))
        self.setPalette(palette)

        # 布局
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 0, 0)

        # 窗口左图标
        self.lb_icon = QtWidgets.QLabel(self)
        self.lb_icon.setPixmap(QtGui.QPixmap('./res/images/star.png'))
        # self.lb_icon.setScaledContents(True)
        # self.lb_icon.setFixedWidth(100)
        # self.lb_icon.setStyleSheet('background: transparent; ')
        layout.addWidget(self.lb_icon)

        # 窗口标题
        # layout.addStretch()
        self.lb_title = QtWidgets.QLabel(self.tr('运动达人'), self)
        self.lb_title.setMargin(2)
        self.lb_title.setStyleSheet('color: rgb(255, 255, 0);font-size:24px;font-weight:bold;font-family:Roman times;')
        layout.addWidget(self.lb_title)
        # endregion

        # region 自定义按钮
        # layout.addStretch()
        # pb_prev = QtWidgets.QPushButton(QtGui.QIcon('./res/images/src2.gif'), '转换', self)
        # pb_prev.setToolTip('word批量转pdf，并合并pdf')
        # # pb_prev.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.toolButtonStyle)
        # pb_prev.setStyleSheet('color:white;font-size:24px;font-weight:bold;font-family:Roman times;')
        # pb_next = QtWidgets.QPushButton('打开文件')
        # pb_next.setStyleSheet('color:white;font-size:24px;font-weight:bold;font-family:Roman times;')
        # pb_prev.clicked.connect(self.sign_pb_prev.emit)
        # pb_next.clicked.connect(self.sign_pb_next.emit)
        # layout.addWidget(pb_prev)
        # layout.addWidget(pb_next)
        # layout.addStretch()
        # # 中间伸缩条
        # # layout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        # endregion

        # region 标准按钮
        # 利用Webdings字体来显示图标
        font = self.font() or QtGui.QFont()
        font.setFamily('Webdings')

        # 最小化按钮
        self.min_button = QtWidgets.QPushButton(
            '0', self, clicked=self.sign_win_minimize.emit, font=font, objectName='buttonMinimum')
        # self.min_button.setAutoFillBackground(False)
        # self.min_button.setStyleSheet("background-color: rgb(28, 255, 3);")
        # self.min_button.setAutoDefault(False)
        # self.min_button.setDefault(False)
        # self.min_button.setFlat(False)
        layout.addWidget(self.min_button)

        # 最大化/还原按钮
        self.buttonMaximum = QtWidgets.QPushButton(
            '1', self, clicked=self.showMaximized, font=font, objectName='buttonMaximum')
        layout.addWidget(self.buttonMaximum)

        # 关闭按钮
        self.buttonClose = QtWidgets.QPushButton(
            'r', self, clicked=self.sign_win_close.emit, font=font, objectName='buttonClose')
        layout.addWidget(self.buttonClose)

        # 初始高度
        self.setHeight()
        # endregion

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
        self.min_button.setMinimumSize(height, height)
        self.min_button.setMaximumSize(height, height)
        self.buttonMaximum.setMinimumSize(height, height)
        self.buttonMaximum.setMaximumSize(height, height)
        self.buttonClose.setMinimumSize(height, height)
        self.buttonClose.setMaximumSize(height, height)

    def setTitle(self, title):
        """设置标题"""
        self.lb_title.setText(title)

    def setIcon(self, icon):
        """设置图标"""
        self.iconLabel.setPixmap(icon.pixmap(self.iconSize, self.iconSize))

    def setIconSize(self, size):
        """设置图标大小"""
        self.iconSize = size

    def mouseDoubleClickEvent(self, event):
        super(TitleBar, self).mouseDoubleClickEvent(event)
        self.showMaximized()

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == QtCore.Qt.LeftButton:
            self.mPos = event.pos()  # widget窗口左上角相对于电脑屏幕的左上角的（x=0,y=0）偏移位置
            # pos = QtGui.QMouseEvent()
            # self.mPos = event.globalPos()  # 鼠标偏离电脑屏幕左上角（x=0,y=0）的位置
        event.accept()

    def mouseReleaseEvent(self, event):
        """鼠标弹起事件"""
        self.mPos = None
        event.accept()

    def mouseMoveEvent(self, event):
        # 这里要判断靠近边界与否，在移动窗体还是拉伸窗体之间选择
        if event.buttons() == QtCore.Qt.LeftButton and self.mPos:
            # （需要在主窗体隐藏后减去背景窗体的margins）————顶部没有阴影，不需要
            self.sign_win_move.emit(self.mapToGlobal(event.pos() - self.mPos))
            # self.sign_win_move.emit(event.globalPos() - self.mPos)
        event.accept()

    def enterEvent(self, event):
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))  # 更改鼠标图标
        super(TitleBar, self).enterEvent(event)
        event.accept()

    def leaveEvent(self, event):
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        event.accept()

    def wheelEvent(self, event):
        event.accept()


@unique  # @unique 装饰器可以帮助我们检查保证value没有重复值
class Const(IntEnum):
    # 继承于Enum的枚举类中的Key不能相同，Value可以相，
    # 要Value也不能相同，那么在导入Enum的同时，需要导入unique函数
    # 枚举项可以用来比较，使用==，或者is。枚举类不能用来实例化对象,在类外部不能修改Value值
    CENTER = '0'
    TOP = 1
    BOTTOM = '2'
    LEFT = 3
    RIGHT = 4
    TL_CORNER = 5  # 左上角
    TR_CORNER = 6  # 右上角
    BL_CORNER = 7
    BR_CORNER = 8

    PADDING = 20  # 鼠标跟踪边框的边距，>=margin
    MARGIN = 15  # 四周边距


class CustomMainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(CustomMainWindow, self).__init__(*args, **kwargs)

        # w = QtWinExtras.QtWin()
        if QtWinExtras.QtWin.isCompositionEnabled():  # 返回DWM组合状态
            QtWinExtras.QtWin.extendFrameIntoClientArea(self, -1, -1, -1, -1)  # 玻璃效果
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)  # 半透明背景
            self.setAttribute(QtCore.Qt.WA_NoSystemBackground, False)  # 禁用无背景
            self.setStyleSheet("background: transparent;")
        else:
            ...
            # QtWin:: resetExtendedFrame(this)
            # setAttribute(Qt::WA_TranslucentBackground, false)
            # setStyleSheet(QString("MusicPlayer { background: %1; }").arg(QtWin::realColorizationColor().name()))


class ImgWatermark(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(ImgWatermark, self).__init__(parent)
        self.parent = parent

        self.file_open = None
        self.file_save = None
        self.watermark = ''

        self.lb_water = QtWidgets.QLabel()
        self.cd = QtWidgets.QColorDialog(QtGui.QColor(100, 100, 200), self)
        self.fd = QtWidgets.QFontDialog()

        self._init_ui()
        # self.show()
        self._init_colorDialog()

    def _init_ui(self):
        self.setupUi(self)

        self.lb_img.setScaledContents(True)
        self.lb_water.setParent(self.lb_img)
        self.lb_water.setMouseTracking(True)
        self.lb_water.setAcceptDrops(True)
        self.lb_water.setAutoFillBackground(False)
        self.lb_water.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
        self.lb_water.setLineWidth(2)
        self.lb_water.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_water.setObjectName("lb_water")
        _translate = QtCore.QCoreApplication.translate
        self.lb_water.setText(_translate("Dialog", "水印 水印 水印"))

        Dialog = self
        self.le_file_src.textChanged['QString'].connect(partial(Dialog.slot_text_changed, self.le_file_src))
        self.le_file_dst.textChanged['QString'].connect(partial(Dialog.slot_text_changed, self.le_file_dst))
        self.le_watermark.textChanged['QString'].connect(partial(Dialog.slot_text_changed, self.le_watermark))
        self.tb_open_file.clicked.connect(partial(Dialog.slot_btn_clicked, self.tb_open_file))
        self.tb_save_file.clicked.connect(partial(Dialog.slot_btn_clicked, self.tb_save_file))
        self.pb_color_dlg.clicked.connect(partial(Dialog.slot_btn_clicked, self.pb_color_dlg))
        self.pb_font_dlg.clicked.connect(partial(Dialog.slot_btn_clicked, self.pb_font_dlg))
        self.pb_add_watermark.clicked.connect(partial(Dialog.slot_btn_clicked, self.pb_add_watermark))

    def _init_colorDialog(self):
        def func(col):
            # QPalette.Highlight # 被选中后文字的背景色.
            # QPalette.HighlightText # 被选中后文字的前景色.
            # QPalette.Text # 文字的前景色 QPalette.WindowText
            # QPalette.Base # QTextEdit的背景色, 默认是白色的
            if col.isValid():
                # palette = QtGui.QPalette()
                # palette.setColor(QtGui.QPalette.ButtonText, col)
                # palette.setColor(QtGui.QPalette.Text, col)
                # self.pb_add_watermard.setPalette(palette)
                self.set_label_color(self.lb_water, col)
                # self.lb_water.setStyleSheet(
                #     f'background: transparent; color:{col.name()};')

        # 颜色选择对话框的两个信号
        #       一个是 颜色最终被选中 colorSelected
        #       一个是 当前颜色的改变 currentColorChanged
        # self.cd.colorSelected.connect(func)  # 颜色被选择
        # 捕获当前颜色变化的信号，连接槽函数。用于实时展示颜色变化
        self.cd.currentColorChanged.connect(func)

        # 选择对话框的选项设置：隐藏确认取消按钮，允许用户选择颜色的Alpha分量
        self.cd.setOptions(QtWidgets.QColorDialog.ShowAlphaChannel |
                           QtWidgets.QColorDialog.NoButtons)

    @staticmethod
    def set_label_color(lb, color):
        # print(type(color), color)

        # 第一种，使用setPalette()方法
        pe = QtGui.QPalette()
        pe.setColor(QtGui.QPalette.WindowText, color)
        lb.setPalette(pe)

        # # 第二种，使用样式表
        # lb.setStyleSheet(f"color:{color.name()};font-size:25px;")

        # 第三种，使用QStyle

        # # 第四种，使用一些简单的HTML格式
        # self.lb_water.setText("Hello Qt!")
        # self.lb_water = QtWidgets.QLabel("<h2><i>Hello</i><font color=red>Qt!</font></h2>")

    def slot_text_changed(self, obj, text):
        name = obj.objectName()
        print(name, text)
        if name == 'le_file_src':
            self.file_open = text
            if text and os.path.exists(text) and os.path.isfile(text):
                self.lb_img.setPixmap(Utils.img_center(self.lb_img.width(),
                                                       self.lb_img.height(),
                                                       text))

        elif name == 'le_file_dst':
            self.file_save = text
        elif name == 'le_watermark':
            self.lb_water.setText(text)

    def slot_btn_clicked(self, obj):
        # obj = QtWidgets.QPushButton().text
        # print(obj.text())
        name = obj.objectName()
        # print(name)

        if name == 'pb_font_dlg':
            # self.fd.move(self.x()+self.width() - self.cd.width(),
            #              self.y() + self.height() - self.cd.height())
            font, ok = self.fd.getFont()
            if ok:
                self.lb_water.setFont(font)
        elif name == 'pb_color_dlg':
            self.getColorByShow()  # 颜色对话框弹出方式
            # # p1 = self.mapToParent(tl)
            # p2 = self.mapToGlobal(tl)
            self.cd.move(self.x() - self.cd.width(),
                         self.y() + self.height() - self.cd.height())
            # col = QtWidgets.QColorDialog.getColor()
            # print(col.rgba(), col.name())
            # if col.isValid():
            #     # p = self.lb_water.palette()  # QtGui.QPalette()
            #     # p.setColor(QtGui.QPalette.Text, col)
            #     # self.lb_water.setPalette(p)  # 修改了调色板.
            #     self.lb_water.setStyleSheet(f'background: transparent; color:{col.name()};')
        elif name == 'pb_add_watermark':
            print('打水印，待完善')
        else:
            file, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, '单文件选取', '',
                'img Files(*.png *.jpg *.jpeg *.gif *.bmp *.tiff);;All Files(*.*)',
                '', QtWidgets.QFileDialog.DontUseNativeDialog)
            # print(file, _)

            if file and os.path.exists(file) and os.path.isfile(file):
                if name == 'tb_open_file':
                    self.le_file_src.setText(file)
                elif name == 'tb_save_file':
                    self.le_file_dst.setText(file)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super(ImgWatermark, self).resizeEvent(a0)

    # region 获取所设置的颜色对象，三种不同的对话框弹出方式，一个常用颜色表
    # 使用 cd.show() 弹出颜色对话框并获取颜色
    def getColorByShow(self):
        def func(col):
            print('getColorByShow')
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Text, col)
            self.lb_water.setPalette(palette)

        # self.connect(self.cd, QtCore.pyqtSignal('colorSelected()'), func)
        self.cd.colorSelected.connect(func)  # 发射的信号cd.colorSelected
        self.cd.show()

    # 使用 cd.open(func)弹出颜色对话框并获取颜色
    def getColorByOpen(self):
        def func():
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Background, self.cd.selectedColor())  # 最终选中的颜色cd.selectedColor()
            self.lb_water.setPalette(palette)

        self.cd.open(func)

    # 使用cd.exec() 的值0或1确定是否调用函数
    def getColorByExec(self):
        def func():
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Background, self.cd.selectedColor())
            self.lb_water.setPalette(palette)

        if self.cd.exec():
            func()

    # 颜色选择对话框的常用调色板色块的添加与获取
    #           以下均为静态方法，类名调用
    #           QColorDialog.setCustomColor( index, QColor() )
    #           QColorDialog.setStandardColor( index, QColor() )
    #           QColorDialog.getColor( QColor() )
    def get_Custom_Color(self):
        def func():
            QtWidgets.QColorDialog.setCustomColor(3, QtGui.QColor(10, 60, 200))  # 设置自定义色块区的第三个色块颜色
            color = QtWidgets.QColorDialog.getColor(QtWidgets.QColorDialog.customColor(3), self, '选择颜色')
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Background, color)
            self.setPalette(palette)
            self.cd.show()

        self.btn.clicked.connect(func)
    # endregion


# 定制窗体，自定义工具栏
class CustomFrame(QtWidgets.QFrame):
    def __init__(self, *args, **kwargs):
        super(CustomFrame, self).__init__(*args, **kwargs)
        self.is_max = False  # 窗口最大化标志
        self.LOCATION = Const.CENTER
        # self.dragPosition = 0  # 拖动时坐标
        self.src_path = None
        self.src_files = None
        self.butler = FileButler()
        self.lb_bg = BackLabel(self, 'res/background/bk2.jpg', Const.MARGIN, Const.MARGIN)
        self.titleBar = TitleBar(self)
        self.toolbar = QtWidgets.QToolBar()  # QtWidgets.QToolBar('gjlfd ')
        self.canvas = QtWidgets.QStackedWidget()
        self.child_win = ImgWatermark()

        self._init_main()

    def slot_toolbar_clicked(self, name):
        if name == 'doc转换':
            wg = self.canvas.currentWidget()

            # path = QtWidgets.QFileDialog.getExistingDirectory(
            #     self, "选取源文件夹", r'F:\重要\法律与工程经济讲义',
            #     QtWidgets.QFileDialog.ShowDirsOnly)  # 起始路径
            path = r'F:\重要\法律与工程经济讲义'
            print(path)
            # return
            if path:
                self.src_path = path
                self.src_files = Utils.files_in_dir(path, ['.doc', '.docx'])

                Utils.sort_nicely(self.src_files)
                print(self.src_files)
                if not self.src_files:
                    return
                for each in self.src_files:
                    item = QtWidgets.QListWidgetItem(QtGui.QIcon(), each, wg)
                    #     item.setToolTip(self.data[i])
                    item.setSizeHint(QtCore.QSize(16777215, 50))  # 设置item的默认宽高(这里只有高度比较有用)
                    item.setTextAlignment(QtCore.Qt.AlignCenter)  # 文字居中

                    name, _ = os.path.splitext(each)
                    doc = f'{path}\\{each}'
                    pdf = f'{path}\\{name}.pdf'
                    print(doc, pdf)

                    self.butler.word2pdf(doc, pdf)
                #
                # # print(path)
                self.butler.merge_pdf(path, '合并.pdf')

        elif name == '缩图':
            file_list, _ = QtWidgets.QFileDialog.getOpenFileNames(
                self, '多文件选取', '',
                'img Files(*.png *.jpg *.jpeg *.gif *.bmp *.tiff);;All Files(*.*)',
                None,
                QtWidgets.QFileDialog.DontUseNativeDialog)
            print(file_list)

            scale = 1.0
            for each in file_list:
                file_in, ext = os.path.splitext(each)
                file_jpg = f'{file_in}.jpg'
                print(file_in, file_jpg, ext)
                ImageConvert.png_jpg(each, file_jpg, scale)

        elif name == '水印':
            # self.child_win.show()  # -----  modeless dialog
            self.child_win.exec()  # ------ modal  dialog

    def _init_canvas(self):
        ...
        # self.canvas.setStyleSheet('background-color: skyblue;  /* */')
        # region 文件列表
        lw_files = QtWidgets.QListWidget()
        # lw_files.setViewMode(QtWidgets.QListView.IconMode)  # 显示模式,Icon模式(一般文本配合图标,setViewMode)
        lw_files.setFrameShape(QtWidgets.QListView.NoFrame)  # 无边框
        # lw_files.setFlow(QtWidgets.QListWidget.LeftToRight)  # 从左到右
        # lw_files.setWrapping(True)  # 这三个组合可以达到和FlowLayout一样的效果
        # lw_files.setResizeMode(QtWidgets.QListWidget.Adjust)  # 设置自动适应布局调整（Adjust适应，Fixed不适应），默认不适应
        # lw_files.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  # 隐藏滚动条
        lw_files.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # lw_files.setIconSize(QtCore.QSize(100, 100))  # 设置QListWidget中单元项的图片大小
        # lw_files.setSpacing(10)  # 设置QListWidget中单元项的间距

        # lw_videos.setViewportMargins(0, 0, 0, 0)
        # lw_files.setMovement(QtWidgets.QListWidget.Static)  # 设置不能移动
        lw_files.setStyleSheet(
            'background: transparent;     /*全透明*/'
            'color: rgb(255, 0, 0);   /**/'
            'font-size:24px;font-weight:bold;font-family:Roman times;')
        lw_files.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

        # 连接竖着的滚动条滚动事件
        # lw_videos.verticalScrollBar().actionTriggered.connect(self.onActionTriggered)
        # lw_files.clicked.connect(self.submenu_resource)
        # item_height = 40
        # item_count = 11 if len(self.data_video) > 11 else len(self.data_video)
        # lw_videos.setFixedHeight(item_height * item_count)
        # print(lw_videos.height(), self.menu_height * item_count)

        self.canvas.addWidget(lw_files)
        # endregion

        # 多子窗体的窗体
        # self.mdi = QMdiArea()QMdiSubWindow()
        # # 为子窗口计数
        # self.count = self.count + 1
        # # 创建一个子窗口
        # sub = QMdiSubWindow()
        # # 为子窗口添加一个TextEdit控件
        # sub.setWidget(QTextEdit())
        # self.mdi.addSubWindow(sub)
        # sub.show()
        # self.mdi.cascadeSubWindows()  # 当点击菜单栏中的Cascade时，堆叠子窗口
        # self.mdi.tileSubWindows()  # 当点击菜单栏中的Tiled时，平铺子窗口

    def _init_toolbar(self):
        self.setToolTip('toolbar')
        self.toolbar.setStyleSheet('QToolBar#toolbar{background: transparent;     /*全透明*/'
                                   '/*background-color: skyblue;   */'
                                   '/*background-color: rgba(0,0,0,50);   半透明*/'
                                   '/*background: rgba(255, 0, 0, 150);  半透明*/'
                                   'height: 25px;}'
                                   'QToolButton{background: rgba(0, 200, 200, 50);'
                                   'color: black;'
                                   'font-size:22px;'
                                   'font-weight:bold;'
                                   'font-family:verdana,arial,Roman times;}')

        tb = QtWidgets.QToolButton()
        tb.setText('转换')
        tb.setToolTip('把多个doc批量转入一个pdf')
        tb.clicked.connect(partial(self.slot_toolbar_clicked, 'doc转换'))
        self.toolbar.addWidget(tb)

        tb = QtWidgets.QToolButton()
        tb.setText('缩图')
        tb.setToolTip('把图片的分辨率缩小')
        tb.clicked.connect(partial(self.slot_toolbar_clicked, '缩图'))
        self.toolbar.addWidget(tb)

        tb = QtWidgets.QToolButton()
        tb.setText('水印')
        tb.setToolTip('给图片设置水印')
        tb.clicked.connect(partial(self.slot_toolbar_clicked, '水印'))
        self.toolbar.addWidget(tb)

    def _init_main(self):
        self.resize(1200, 800)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)  # 设置无边框窗口
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # self.setAttribute(Qt.WA_StyledBackground, True)  # 子QWdiget背景透明
        self.setMouseTracking(True)  # 跟踪鼠标移动事件的必备

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, Const.MARGIN, Const.MARGIN)  # 给阴影留下位置，不过左边和上边就没有拉伸的功能，被遮蔽了
        # layout.setContentsMargins(0, 0, 0, 0)  # 给阴影留下位置
        layout.setSpacing(0)
        layout.addWidget(self.titleBar)
        # self.titleBar.setVisible(False)
        layout.addWidget(self.toolbar)
        # layout.addStretch()
        layout.addWidget(self.canvas)
        # pb = QtWidgets.QPushButton('dgskgls')
        # pb.setToolTip('测试一下')
        # layout.addWidget(pb)

        Utils.center_win(self)
        self.titleBar.setTitle('文件管家')
        self._init_toolbar()
        self._init_canvas()

        # 信号槽
        # self.titleBar.sign_pb_prev.connect(partial(self.sign_title_clicked, '打开文件夹'))
        # self.titleBar.sign_pb_next.connect(partial(self.sign_title_clicked, '打开文件'))
        self.titleBar.sign_win_minimize.connect(self.sign_showMinimized)
        self.titleBar.sign_win_maximize.connect(self.sign_showMaximized)
        self.titleBar.sign_win_resume.connect(self.sign_showNormal)
        self.titleBar.sign_win_close.connect(self.close)
        self.titleBar.sign_win_move.connect(partial(self.sign_move, 0))
        # self.windowTitleChanged.connect(self.titleBar.setTitle)
        # self.windowIconChanged.connect(self.titleBar.setIcon)

    # region 通用主窗口事件，不用再改
    def sign_showMinimized(self):
        self.showMinimized()

    def sign_showMaximized(self):
        self.is_max = True
        """最大化,要先去除上下左右边界,如果不去除则边框地方会有空隙"""
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.showMaximized()

    def sign_showNormal(self):
        self.is_max = False
        """还原,要先保留上下左右边界,否则没有边框无法调整"""
        self.layout().setContentsMargins(0, 0, Const.MARGIN, Const.MARGIN)
        super(CustomFrame, self).showNormal()

    # def nativeEvent(self):
    #     pass

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        # if event.button() == Qt.LeftButton:#也可以
        if event.buttons() == QtCore.Qt.LeftButton:
            if self.LOCATION != Const.CENTER:
                self.mouseGrabber()  # 得到正在捕获键盘事件的窗口
            else:
                pass
                # self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        # if event.buttons() == Qt.LeftButton:#就不行
        if event.button() == QtCore.Qt.LeftButton:
            if self.LOCATION is not Const.CENTER:  # 非边线附近一律恢复鼠标形状
                self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.unsetCursor()

    def cursor_location(self, pos_current):
        """
                给光标标定位
                :param pos_current:相对位置
                :return:
                """
        x, y = pos_current.x(), pos_current.y()  # 相对于无边框窗口左上角的位置
        # print(f'x={x}  y={y}')
        width = self.width() - Const.PADDING  # 无边框窗口的宽减去边距
        height = self.height() - Const.PADDING  # 无边框窗口的长减去边距

        if x < Const.PADDING and y < Const.PADDING:  # 左上角内侧
            self.LOCATION = Const.TL_CORNER
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))  # 设置鼠标形状
        elif x > width and y > height:  # 右下角内侧
            self.LOCATION = Const.BR_CORNER
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))
        elif x < Const.PADDING and y > height:  # 左下角内侧
            self.LOCATION = Const.BL_CORNER
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeBDiagCursor))
        elif x > width and y < Const.PADDING:  # 右上角内侧
            self.LOCATION = Const.TR_CORNER
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeBDiagCursor))

        elif x < Const.PADDING:  # 左边内侧
            self.LOCATION = Const.LEFT
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        elif x > width:  # 右边内侧
            self.LOCATION = Const.RIGHT
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        elif y < Const.PADDING:  # 上边
            self.LOCATION = Const.TOP
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        elif y > height:  # 下边
            self.LOCATION = Const.BOTTOM
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))

        else:  # 中间 默认
            self.LOCATION = Const.CENTER
            self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

        # print(self.LOCATION)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        mouse_pos = event.globalPos()
        top_left = self.mapToGlobal(self.rect().topLeft())
        # top_left = self.pos
        bottom_right = self.mapToGlobal(self.rect().bottomRight())

        # print(self.LOCATION)

        # if event.buttons() and event.button() != Qt.LeftButton:  # 也不行
        if not event.buttons():
            self.cursor_location(event.pos())
        else:
            if event.buttons() == QtCore.Qt.LeftButton:
                # print('left press')
                if self.LOCATION is Const.CENTER:
                    pass
                    # print('center')
                    # self.move(event.globalPos() - self.dragPosition)  # 将窗口移动到指定位置
                else:
                    geo = QtCore.QRect(top_left, bottom_right)

                    if self.LOCATION == Const.LEFT:
                        # if bottom_right.x() - mouse_pos.x() > self.minimumWidth():#不需要，有setmin、max、fix决定
                        # geo.setWidth(bottom_right.x() - mouse_pos.x())  # 自动计算的
                        geo.setX(mouse_pos.x())
                    elif self.LOCATION is Const.RIGHT:
                        geo.setWidth(mouse_pos.x() - top_left.x())
                    elif self.LOCATION is Const.TOP:
                        geo.setY(mouse_pos.y())
                    elif self.LOCATION == Const.BOTTOM:
                        geo.setHeight(mouse_pos.y() - top_left.y())
                    elif self.LOCATION == Const.TL_CORNER:
                        geo.setX(mouse_pos.x())
                        geo.setY(mouse_pos.y())
                    elif self.LOCATION == Const.TR_CORNER:
                        geo.setWidth(mouse_pos.x() - top_left.x())
                        geo.setY(mouse_pos.y())
                    elif self.LOCATION == Const.BL_CORNER:
                        geo.setX(mouse_pos.x())
                        geo.setHeight(mouse_pos.y() - top_left.y())
                    elif self.LOCATION == Const.BR_CORNER:
                        geo.setWidth(mouse_pos.x() - top_left.x())
                        geo.setHeight(mouse_pos.y() - top_left.y())
                    # else:  # is Const.CENTER
                    #     pass
                    self.setGeometry(geo)  # 设置影子的父窗口的位置

            # else:
            #     print('other press')
        # QEvent的accept（）和ignore（）一般不会用到，因为不如直接调用QWidget类的事件处理函数直接，而且作用是一样的
        # 唯有在closeEvent（）中必须调用accept（）或ignore（）。
        event.ignore()

    def close(self):
        super(CustomFrame, self).close()

    def sign_move(self, x_offset, pos):
        if self.windowState() == QtCore.Qt.WindowMaximized or \
                self.windowState() == QtCore.Qt.WindowFullScreen:
            # 最大化或者全屏则不允许移动
            return

        # if self._widget is None:
        #     return

        pos_new = copy.copy(pos)
        pos_new.setX(pos.x() - x_offset)  # 减去左侧列表框占用的
        # print('this', pos_new.x(), pos.x())

        super(CustomFrame, self).move(pos_new)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super(CustomFrame, self).resizeEvent(a0)
        self.lb_bg.update(self.is_max)

    def __str__(self):
        return '文件大管家'

    __repr__ = __str__
    # endregion


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.src_path = None
        self.save_path = None
        self.src_files = []
        self.merge_files = []
        # self.files_weight = []  # 文件大小
        self.ext_filter = "WORD Files(*.doc *.docx);;All Files(*.*)"
        # self.ext_filter = "Word Files(*.doc)\0*.doc\0All Files(*.*)\0*.*\0\0"

        self.margin = 10
        self.item_width = [0, 60, 80, 80, 140, 80, 80]  # table 列宽
        self.flag_sort = True

        # TODO 修改原始控件
        self.customUI()
        self.resize(1000, 600)

    def customUI(self):
        # self.verticalLayout.setMargin(self.margin)
        self.setupUi(self)
        self.tableWidget.initUI()

        pss = Utils.readQss('res/style/QProgressBarQss.txt')
        self.progressBar.setStyleSheet(pss)

        self.statusbar.showMessage('我昔钓白龙，放龙溪水傍。', 0)  # 状态栏本身显示的信息 第二个参数是信息停留的时间，单位是毫秒，默认是0（0表示在下一个操作来临前一直显示）
        self.allNum = QtWidgets.QLabel('总数:')
        self.selectNum = QtWidgets.QLabel('选中:')

        self.statusbar.addPermanentWidget(self.allNum, stretch=0)
        self.statusbar.addPermanentWidget(self.selectNum, stretch=0)

        font = QtGui.QFont('楷体', 14)
        # font.setBold(True)  # 设置字体加粗
        self.setFont(font)  # 设置字体
        qss = Utils.readQss('./res/style/radio_checkQss.txt')
        self.setStyleSheet(qss)

        self.cb_exit.setChecked(True)
        self.rb_digit_little.setChecked(True)
        # self.cb_select_all.setStyleSheet(qss)

        wg = self.tableWidget.createWidget(1)
        self.horizontalLayout_3.addWidget(wg)

        self.pb_save_path.clicked.connect(partial(self.slot_pb_clicked, self.pb_save_path))
        self.pb_merge.clicked.connect(lambda: self.slot_pb_clicked(self.pb_merge))
        self.pb_add_files.pressed.connect(lambda: self.slot_pb_clicked(self.pb_add_files))
        self.pb_open_dir.pressed.connect(lambda: self.slot_pb_clicked(self.pb_open_dir))
        self.pb_clear.pressed.connect(lambda: self.slot_pb_clicked(self.pb_clear))
        self.cb_select_all.pressed.connect(lambda: self.slot_cb_clicked(self.cb_select_all))
        self.comboBox.currentIndexChanged['int'].connect(self.slot_comboBox_clicked)
        self.cb_eyebrow.clicked.connect(partial(self.slot_cb_clicked, self.cb_eyebrow))
        self.cb_watermark.clicked.connect(partial(self.slot_cb_clicked, self.cb_watermark))
        self.lineEdit_src_dir.editingFinished.connect(partial(self.slot_le_edited, self.lineEdit_src_dir))
        self.lineEdit_save_path.editingFinished.connect(partial(self.slot_le_edited, self.lineEdit_save_path))

    def _createDate(self, files):
        if not files:
            return

        data = []
        for i in range(len(files)):
            file = files[i]
            size = Utils.getFileInfo(file)['文件大小']
            ct = Utils.getFileInfo(file)['最后一次的修改时间']
            data.append([files[i], '', '', size, ct])
        return data

    def slot_pb_clicked(self, controls):
        name = controls.objectName()
        # print(name)
        if name == 'pb_add_files':
            file_list, _ = QtWidgets.QFileDialog.getOpenFileNames(
                self, '多文件选取', '', self.ext_filter, None,
                QtWidgets.QFileDialog.DontUseNativeDialog)
            # print(file_list)
            data = self.createDate(file_list)
            self.tableWidget.update_data(data)
            self.tableWidget.update_table()
        elif name == 'pb_open_dir':
            path = QtWidgets.QFileDialog.getExistingDirectory(
                self, "选取源文件夹", '',
                QtWidgets.QFileDialog.ShowDirsOnly)  # 起始路径
            if path:
                self.src_path = path
                self.lineEdit_src_dir.setText(path)
                self.src_files = Utils.files_in_dir(path, ['.doc', '.docx'], True)

                data = self._createDate(self.src_files)
                self.tableWidget.update_data(data)
                self.tableWidget.update_table()
        elif name == 'pb_clear':
            self.tableWidget.update_data(None)
            self.tableWidget.update_table()
        elif name == 'pb_save_path':
            path = QtWidgets.QFileDialog.getSaveFileName(
                self, "选取保存文件夹", '.', self.ext_filter)  # 起始路径
            if path:
                # self.save_path, self.save_file = os.path.splitdrive(path[0])
                # self.save_path, self.save_file = os.path.splitext(path[0])
                self.save_path, self.save_file = os.path.split(path[0])
                self.save_path = path[0]
                # print(path)
                self.lineEdit_save_path.setText(self.save_path)
        elif name == 'pb_merge':
            rows = self.tableWidget.selectedItems()
            self.merge_files.clear()
            # self.files_weight.clear()
            for each in rows:
                file_name = each.text()
                file_path = os.path.join(self.src_path, file_name)  # 构造完整路径
                if os.path.isfile(file_path):
                    self.merge_files.append(file_path)
                    # self.files_weight.append(Utils.get_FileSize(file_path))

            # print(self.files_weight)
            # print(self.save_path)

            if self.save_path:
                # path = os.path.join(self.save_path, self.save_file)  # 构造完整路径
                if self.merge_files:
                    Utils.mergewords(self.merge_files, self.save_path, self.progressBar)
                else:
                    AnimWin('请指定保存路径')
        else:
            pass

    def slot_tb_clicked(self, controls, flag_other=0):
        name = controls.objectName()
        # 获取点击所在的行列号
        parent = controls.parent()
        x = parent.frameGeometry().x()
        y = parent.mapToParent(QtCore.QPoint(0, 0)).y()
        index = self.tableWidget.indexAt(QtCore.QPoint(x, y))
        row = index.row()
        col = index.column()
        # print('row', row, col)

        if name == 'open_file':
            file = None
            if flag_other == 1:
                file = self.save_path
            else:
                file = self.tableWidget.item(row, 0).text()
            # print(file)
            if file and os.path.isfile(file):
                os.startfile(file)
        elif name == 'open_dir':
            if flag_other == 1:
                file = self.save_path
            else:
                file = self.tableWidget.item(row, 0).text()
            if file and os.path.isfile(file):
                path, file = os.path.split(file)
                QtWidgets.QFileDialog.getOpenFileName(
                    self, '打开文件', path, self.ext_filter)
        elif name == 'recycle':
            if self.save_path and os.path.isfile(self.save_path):
                reply = QtWidgets.QMessageBox.question(
                    self, '提醒', '删除输出文件吗？',
                    QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    os.remove(self.save_path)
            else:
                self.tableWidget.delete_row(row)  # 删除指定行
        else:
            pass

    def slot_comboBox_clicked(self, value):
        print(value)

    def slot_cb_clicked(self, controls):
        name = controls.objectName()
        unchecked = controls.isChecked()  #
        # print(name, unchecked)
        if name == 'cb_select_all':
            if unchecked:
                self.tableWidget.clearSelection()
                self.tableWidget.setCurrentItem(None)
            else:
                self.tableWidget.selectAll()

    def slot_le_edited(self, controls):
        name = controls.objectName()
        # print(name)
        if name == 'lineEdit_save_path':
            self.save_path = self.lineEdit_save_path.text()
        elif name == 'lineEdit_src_dir':
            self.src_path = self.lineEdit_src_dir.text()
            # print(self.src_path)
        else:
            pass

    def handleItemClicked(self, row):
        # row = QtWidgets.QTableWidgetItem()
        print('row', row.row(), row.column())
        table_column = row.column()
        # table_row = row.row()
        # current_item = self.tableWidget.item(table_row, table_column)
        # current_widget = self.tableWidget.cellWidget(table_row, table_column)
        # print(table_column, table_row)
        # print(type(current_item), type(current_widget))

    def slot_itemchanged(self, value):
        # print(type(value))
        self.allNum.setText(f'总数:{self.tableWidget.rowCount()}')
        self.selectNum.setText(f'选中:{len(self.tableWidget.selectedItems())}')

    def resizeEvent(self, event):
        palette = QtGui.QPalette()
        pix = QtGui.QPixmap('res/background/background6.jpg')
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(palette)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    g_style = StyleSheet()  # 包围窗体，定义在前
    # win = MainWindow()
    win = CustomFrame()
    # win = CustomMainWindow()
    # win = ImgWatermark()

    g_style.set(app)  # 包围窗体，设置在后
    sys.exit(app.exec_())

    # f = FileButler()
    # f.doc2docx(r'C:\Users\chw\Desktop\8月英语作业\2018 中考词组汇总\8A/8A Unit 1  词组.doc',
    #            r'C:\Users\chw\Desktop\8月英语作业\2018 中考词组汇总\8A/8A Unit 1  词组.docx')
