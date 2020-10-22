#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Project    : Codes
@File       : miko.py
@Time       : 2020/10/19 13:13
@Author     : big QQ: 260125177
@Contact    : shdorado@126.com  
@License    : Copyright (C) 2018-2020 BIG
@Version    : 1.0 
@Desciption :
"""

import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from utilities import Utils, MyLog, ImageConvert, AnimWin
from PIL import Image, ImageFilter
from functools import partial

log = MyLog()


# 自定义高斯模糊图片
class MyGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=2, bounds=None):
        self.radius = radius
        self.bounds = bounds

    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)


class PopForm(QtWidgets.QWidget):
    """ 框架类，提供子窗体，自动隐藏或关闭，弱交互 """

    def __init__(self, parent, wg=None):
        super(PopForm, self).__init__(parent)
        self.father = parent

        vl = QtWidgets.QVBoxLayout(self)
        if wg:
            self.resize(wg.width(), wg.height())
            vl.addWidget(wg)
        else:
            self.resize(100, 100)
        self.show()
        self.setFocus()

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.close()


class PopWin(QtWidgets.QWidget):
    """ 框架类，提供弹出的顶层窗体，强交互 """

    def __init__(self, parent=None, wg=None, callback=None):
        super(PopWin, self).__init__(parent)
        self.father = parent
        self.wg = wg
        self.callback = callback

        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)  # 设置窗体无边框
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 置顶
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.resize(400, 200)

        self.vl_main = QtWidgets.QVBoxLayout(self)
        self.vl_main.setContentsMargins(10, 20, 10, 10)
        if wg:
            self.vl_main.addWidget(wg)

        # self.init_ui_custom()
        self.init_ui_sys()
        self.show()

    def init_ui_custom(self):
        cb_theme = QtWidgets.QComboBox()
        cb_theme.addItems(['现代主题', '经典主题'])

        cb_count = QtWidgets.QCheckBox('在侧栏显示项目计数')
        cb_src = QtWidgets.QCheckBox('使用网站图标')

        rb_genus = QtWidgets.QRadioButton('类别')
        rb_temp = QtWidgets.QRadioButton('模板')
        rb_new = QtWidgets.QRadioButton('新建')
        rb_copy = QtWidgets.QRadioButton('复制')
        rb_genus.setChecked(True)
        rb_new.setChecked(True)

        gb1 = QtWidgets.QGroupBox()
        vl1 = QtWidgets.QVBoxLayout(gb1)
        vl1.addWidget(rb_genus)
        vl1.addWidget(rb_temp)

        gb2 = QtWidgets.QGroupBox()
        vl2 = QtWidgets.QVBoxLayout(gb2)
        vl2.addWidget(rb_new)
        vl2.addWidget(rb_copy)

        hl_gb = QtWidgets.QHBoxLayout()
        hl_gb.addWidget(gb1)
        hl_gb.addWidget(gb2)

        wg_new_genus = QtWidgets.QWidget()
        hl_new_genus = QtWidgets.QHBoxLayout(wg_new_genus)
        tb_genus = QtWidgets.QToolButton()
        le_genus = QtWidgets.QLineEdit()
        le_genus.setPlaceholderText('输入类别的名称')
        hl_new_genus.addWidget(tb_genus)
        hl_new_genus.addWidget(le_genus)

        self.vl_main.addWidget(cb_theme)
        self.vl_main.addWidget(cb_count)
        self.vl_main.addWidget(cb_src)
        self.vl_main.addLayout(hl_gb)
        self.vl_main.addWidget(wg_new_genus)

    def init_ui_sys(self):
        wg_order = QtWidgets.QWidget()
        wg_order.setStyleSheet('font-size:16px;font-weight:bold;'
                               'font-family:Microsoft YaHei;KaiTi; ')
        hl_order = QtWidgets.QHBoxLayout(wg_order)
        hl_order.setSpacing(20)

        pb_save = QtWidgets.QPushButton('保存')
        pb_cancel = QtWidgets.QPushButton('取消')
        pb_exit = QtWidgets.QPushButton('退出')
        hl_order.addWidget(pb_save)
        hl_order.addWidget(pb_cancel)
        hl_order.addWidget(pb_exit)

        pb_save.clicked.connect(lambda: self.slot_button_clicked(pb_save))
        pb_cancel.clicked.connect(lambda: self.slot_button_clicked(pb_cancel))
        pb_exit.clicked.connect(lambda: self.slot_button_clicked(pb_exit))

        self.vl_main.addWidget(wg_order)

    def slot_button_clicked(self, ctl):
        name = ctl.text()
        print(name)

        if name == '退出':
            self.close()
        elif name == '保存':
            if self.wg and self.callback:  # 调用回调函数，专门保存数据
                self.callback()
        else:
            ...

    # def closeEvent(self, event):
    #     """重写该方法主要是解决打开子窗口时，如果关闭了主窗口但子窗口仍显示的问题，
    #     使用sys.exit(0) 时就会只要关闭了主窗口，所有关联的子窗口也会全部关闭"""
    #     # super().closeEvent(event)  # 先添加父类的方法，以免导致覆盖父类方法（这是重点！！！）
    #     sys.exit(0)


class DataMiko:
    dir_icons = 'E:/Codes/res/images/'
    mold_watch = [('1.ico', '已泄露的网站'), ('goB1.png', '易受攻击的密码'),
                  ('1067868.gif', '重复使用的密码'), ('1190300.gif', '弱密码'),
                  ('3.ico', '不安全的网站'), ('watermark.jpg', '双重验证'),
                  ('watermark.gif', '到期')]  # 内定的瞭望塔分类
    mold_genre = [('open.gif', '登录信息'), ('open.gif', '信用卡'), ('open.gif', '密码'),
                  ('open.gif', '身份标识'), ('open.gif', '邮件账户'), ('open.gif', '财务'),
                  ('open.gif', '许可证'), ('open.gif', '数据库'), ('open.gif', '会员信息'),
                  ('open.gif', '驾照'), ('open.gif', '护照'), ('open.gif', '无线路由器')]  # 内定的项目分类

    def __init__(self):
        self.__pri_pwd__ = None
        self.__vault_path = None
        self.__vault_file = None
        self.__vault_pwd = None

    def load_vault(self):
        ...

    def save_vault(self, data):
        file = f'{self.__vault_path}/{self.__vault_file}'
        log.debug(file)
        with open(file, 'wb') as fp:
            data = fp.write(data)  # type(data) === bytes
            # text = int.from_bytes(data, byteorder='big')

    def create_vault(self, parent):
        lb_title = QtWidgets.QLabel('在此电脑上创建新的保险库')
        lb_title.setStyleSheet('color:rgba(5,120,243,255);font-size:22px;'
                               'font-weight:bold;font-family:Microsoft YaHei;')
        lb_title.setAlignment(QtCore.Qt.AlignHCenter)

        le_name = QtWidgets.QLineEdit()
        le_name.setPlaceholderText('输入新保险库名称：')
        le_name.textChanged.connect(partial(self.slot_text_changed, 'name'))
        hl_name = QtWidgets.QHBoxLayout()
        hl_name.addWidget(le_name)

        self.le_pwd = QtWidgets.QLineEdit()
        self.le_pwd.setPlaceholderText('输入密码：可自动产生或复制主密码')
        self.le_pwd.textChanged.connect(partial(self.slot_text_changed, 'pwd'))
        tb_pwd = QtWidgets.QToolButton()
        tb_pwd.setObjectName('copy')
        tb_pwd.setToolTip('复制您的主密码')
        tb_pwd.setIcon(QtGui.QIcon(f'{self.dir_icons}copy1.png'))
        tb_pwd.setIconSize(QtCore.QSize(25, 25))
        tb_pwd.clicked.connect(lambda: self.slot_button_clicked(tb_pwd))
        hl_pwd = QtWidgets.QHBoxLayout()
        hl_pwd.addWidget(self.le_pwd)
        hl_pwd.addWidget(tb_pwd)

        self.le_pwd_re = QtWidgets.QLineEdit()
        self.le_pwd_re.setPlaceholderText('再次输入新保险库密码：')
        self.le_pwd_re.textChanged.connect(partial(self.slot_text_changed, 'pwd_re'))
        hl_pwd_re = QtWidgets.QHBoxLayout()
        hl_pwd_re.addWidget(self.le_pwd_re)

        note = '       您在上方输入的密码将用于对此保险库中的数据进行加密。您仍将使用您的主密码来解锁米库程序。' \
               '如果您无意与他人共享此保险库，我们推荐您使用您的主密码，而非使用新密码，以免增加记忆负担。'
        lb_note = QtWidgets.QLabel(note)
        lb_note.setStyleSheet('font:18px;')
        lb_note.setAlignment(QtCore.Qt.AlignLeft)
        lb_note.setWordWrap(True)

        self.le_path = QtWidgets.QLineEdit()
        self.le_path.setPlaceholderText('同步保险库的文件路径')
        self.le_path.textChanged.connect(partial(self.slot_text_changed, 'path'))
        pb_path = QtWidgets.QPushButton(QtGui.QIcon(f'{self.dir_icons}copy1.png'), '')
        pb_path.setObjectName('path')
        pb_path.setToolTip('点击打开文件对话框')
        pb_path.setIconSize(QtCore.QSize(25, 25))
        pb_path.clicked.connect(lambda: self.slot_button_clicked(pb_path))
        hl_path = QtWidgets.QHBoxLayout()
        hl_path.addWidget(self.le_path)
        hl_path.addWidget(pb_path)

        wg = QtWidgets.QWidget()
        # wg.setFixedSize(400, 400)
        wg.setStyleSheet('color:rgba(25,22,173,255);'
                         'font-size:20px; font-weight:normal;font-family:STKaiti;')
        vl = QtWidgets.QVBoxLayout(wg)
        vl.addWidget(lb_title)
        vl.addSpacing(10)
        vl.addLayout(hl_name)
        vl.addLayout(hl_pwd)
        vl.addLayout(hl_pwd_re)
        vl.addWidget(lb_note)
        vl.addLayout(hl_path)
        vl.setAlignment(QtCore.Qt.AlignCenter)

        PopWin(parent, wg, self._save_new_vault)

    def slot_text_changed(self, name: str, text):
        log.debug(text, name)
        if name == 'name':
            self.__vault_file = f'{text}.movault'
        elif name == 'pwd':
            self.__vault_pwd = text
        elif name == 'pwd_re':
            if text != self.__vault_pwd:
                AnimWin('两次密码输入不一致，\n请重新输入！')
        elif name == 'path':
            self.__vault_path = text

    def slot_button_clicked(self, ctl):
        log.debug(ctl.objectName())
        if ctl.objectName() == 'path':
            path = QtWidgets.QFileDialog.getExistingDirectory(
                ctl, "选取文件夹", './')  # 起始路径 当前程序文件位置
            log.debug(path)
            self.le_path.setText(path)
        else:  # copy
            self.le_pwd.setText(self.__pri_pwd__)
            self.le_pwd_re.setText(self.__pri_pwd__)

    def _save_new_vault(self):
        ...

    def delete_vault(self):
        ...


class BackForm(QtWidgets.QWidget):
    """
    背景窗体，提供圆角、底图、鼠标移动、最大最小化及退出按钮 等功能
    """

    def __init__(self, *args, **kwargs):
        super(BackForm, self).__init__()

        self.h_title = 40  # 标题栏高度
        self.h_vault = 50  # 保险库标题高度
        self.h_bar = 30  # 工具栏高度
        self.radius = 10  # 窗体的圆角半径
        self.deep = 0  # 窗体的阴影宽度
        self.mPos = None  # 鼠标位置
        self.vaults_is_show = True  # 两个列表的切换标志
        self.pop_form = None  # 弹出窗口
        self.pop_win = None  # 弹出窗口

        self._init_data()
        self._init_ui_main()
        self._init_ui_title()
        self._init_ui_bench()

    def _init_data(self):
        self.data = DataMiko()

    def _init_ui_main(self):
        self.setGeometry(2200, 200, 1200, 740)  # 黄金分割

        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)  # 设置窗体无边框
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置背景透明
        # Utils.set_effect(self, 1, self.deep, 5, 5, QtGui.QColor(0, 0, 0, 180))
        # self.setMouseTracking(True)

        self.vl_main = QtWidgets.QVBoxLayout(self)
        self.vl_main.setContentsMargins(0, 0, 0, 0)
        self.vl_main.setSpacing(0)

        # self.setFont(QtGui.QFont('Microsoft YaHei', 20))

    # region 标题栏
    def _init_ui_title(self):

        self.wg_title = QtWidgets.QWidget(self)
        # self.wg_title.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        # Utils.set_effect(self.wg_title, 2, 0.4)
        # self.wg_title.setWindowOpacity(0.4)
        self.wg_title.setStyleSheet('color:yellow;')

        h = self.h_bar
        qss = '/*border-top-right-radius:10 px;*/' \
              'border:0px; min-width: {:d}px;max-width: {:d}px;' \
              'min-height: {:d}px;max-height: {:d}px;' \
              'background: rgba(25,225,25, 150);'.format(h, h, h, h)

        self.pb_menu = QtWidgets.QPushButton(QtGui.QIcon('E:/Codes/res/images/lines.png'), '', self.wg_title)
        self.pb_menu.setStyleSheet(qss)
        self.pb_menu.setIconSize(QtCore.QSize(self.h_bar, self.h_bar))
        self.pb_menu.clicked.connect(self.on_pb_menu_clicked)

        self.tb_logo = QtWidgets.QToolButton()
        self.tb_logo.setIcon(QtGui.QIcon('E:/Codes/res/images/dst11.gif'))
        self.tb_logo.setIconSize(QtCore.QSize(30, 30))
        self.tb_logo.setStyleSheet(qss)

        self.lb_title = QtWidgets.QLabel('米库')
        self.lb_title.setStyleSheet('font-size:25px;font-weight:bold;font-family:STKaiti;')
        self.lb_note = QtWidgets.QLabel(' 密码保存专家系统')
        self.lb_note.setStyleSheet('font-size:18px;font-weight:nomal;font-family:Microsoft YaHei;')

        hl_title = QtWidgets.QHBoxLayout(self.wg_title)
        hl_title.addWidget(self.tb_logo)
        hl_title.addWidget(self.lb_title)
        hl_title.addWidget(self.lb_note)
        hl_title.addStretch()

    def _flush_title(self):
        # 绝对定位，用布局会有偏差
        self.wg_title.setGeometry(0, 0, self.width(), self.h_title)

        self.pb_menu.move(self.wg_title.width() - self.deep - 35, 5)
        # self.pb_min.move(self.wg_title.width() - self.deep - 75, 5)
        # self.pb_exit.move(self.wg_title.width() - self.deep - 35, 5)

    def on_pb_menu_clicked(self):
        log.debug('menu')

        def menuSlot(act):
            name = act.text()
            log.debug(name)
            if name == '数据定制':
                self.on_menu_data_custom()
            elif name == '在此电脑上新建保险库...':
                self.data.create_vault(self)

        sys_menu = QtWidgets.QMenu(self)

        # region 米库——保险库
        miko_menu = QtWidgets.QMenu('米库...', sys_menu)  # 一级菜单命令属性设置

        # 二级菜单命令属性设置
        new_vault = QtWidgets.QAction('在此电脑上新建保险库...', sys_menu)
        open_vault = QtWidgets.QAction('打开在此电脑上的保险库...', sys_menu)
        import_data = QtWidgets.QAction('导入', sys_menu)

        miko_menu.addActions([new_vault, open_vault, import_data])  # 新增二级菜单

        # endregion

        # region 账户
        login_menu = QtWidgets.QMenu('账户', sys_menu)  # 一级菜单命令属性设置
        cur_act = QtWidgets.QAction('当前账户...', sys_menu)
        other_act = QtWidgets.QAction('登录其他账户', sys_menu)
        other_act.setShortcut('Ctrl+O')
        login_menu.addActions([cur_act, other_act])
        # endregion

        # region 查看菜单
        look_menu = QtWidgets.QMenu('查看', sys_menu)  # 一级菜单命令属性设置
        # endregion

        # region 项目菜单
        genre_menu = QtWidgets.QMenu('项目', sys_menu)  # 一级菜单命令属性设置
        share_menu = QtWidgets.QMenu('分享', genre_menu)  # 二级菜单命令属性设置

        genre_menu.addMenu(share_menu)
        # endregion

        # region 设置
        setting_menu = QtWidgets.QMenu('设置', sys_menu)  # 一级菜单命令属性设置

        setting_ui = QtWidgets.QAction('界面设置', setting_menu)
        setting_menu.addSeparator()
        custom_data = QtWidgets.QAction('数据定制', setting_menu)
        setting_menu.addActions([setting_ui, custom_data])
        # endregion

        # region 帮助
        help_menu = QtWidgets.QMenu('帮助', sys_menu)  # 一级菜单命令属性设置
        get_act = QtWidgets.QAction('获取帮助', sys_menu)
        about_act = QtWidgets.QAction('关于米库...', sys_menu)

        help_menu.addAction(get_act)
        help_menu.addSeparator()
        help_menu.addAction(about_act)
        # endregion

        # region 传统三按钮
        min_act = QtWidgets.QAction(QtGui.QIcon('exit.png'), '最小化', sys_menu)
        min_act.setShortcut('Ctrl+M')
        # exit_act.setStatusTip('退出应用')
        min_act.triggered.connect(self.showMinimized)  # 触发行为

        exit_act = QtWidgets.QAction(QtGui.QIcon('exit.png'), '退出', sys_menu)
        exit_act.setShortcut('Ctrl+Q')
        # exit_act.setStatusTip('退出应用')
        exit_act.triggered.connect(self.close)  # 触发行为
        # endregion

        # region 菜单总布局
        sys_menu.addMenu(miko_menu)
        sys_menu.addMenu(login_menu)  # 子菜单使用了addMenu()
        sys_menu.addSeparator()
        sys_menu.addMenu(look_menu)
        sys_menu.addMenu(genre_menu)
        sys_menu.addSeparator()
        sys_menu.addMenu(setting_menu)
        sys_menu.addMenu(help_menu)
        sys_menu.addSeparator()
        sys_menu.addAction(min_act)
        sys_menu.addAction(exit_act)

        sys_menu.triggered.connect(menuSlot)
        # sys_menu.exec_(QtGui.QCursor.pos())
        ps = QtCore.QPoint(self.pb_menu.x(), self.pb_menu.height() + 10)
        sys_menu.exec_(self.mapToGlobal(ps))
        # endregion

    def on_menu_data_custom(self):
        log.debug(self.pop_win)
        if not self.pop_win:
            self.pop_win = PopWin(self)
        else:
            self.pop_win.show()

    # endregion

    def _init_ui_bench(self):
        self.wg_bench = QtWidgets.QWidget(self)
        # self.wg_bench.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.wg_bench.setObjectName("bench")
        self.wg_bench.setStyleSheet('#bench{border-bottom-left-radius:10px;'
                                    'border-bottom-right-radius:10px;'
                                    'min-height: 500px;max-height: 1000px;}')

        self.panel = QtWidgets.QWidget()  # 命令面板
        self._init_ui_panel()
        self.folder = QtWidgets.QWidget()  # 项目卡片
        self._init_ui_folder()
        self.detail = QtWidgets.QWidget()  # 详情
        self._init_ui_detail()

        # 动态布局(可拖动控件大小)，实例化QSplitter控件并设置初始为水平方向布局
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.setStyleSheet('QSplitter::handle {image:url(:/res/images/wenli41.jpg);}'
                               'QSplitter::handle:horizontal {width:5px;}'
                               'QSplitter::handle:vertical {width:15px;}'
                               'QSplitter::handle:pressed {background-color:red;}')

        splitter.addWidget(self.panel)  # 向Splitter内添加控件。并设置游戏的初始大小
        splitter.addWidget(self.folder)
        splitter.addWidget(self.detail)
        splitter.setSizes([100, 200, 300])  # 设置控件的初始大小

        hl_bench = QtWidgets.QHBoxLayout(self.wg_bench)
        hl_bench.setContentsMargins(0, 0, 0, 0)
        # hl_bench.setSpacing(50)
        hl_bench.addWidget(splitter)

    # region 控制面板区
    def _init_ui_panel(self):
        # 一个按钮、一个搜索框和两个树视图
        # 后一列表用绝对布局，以便于动画

        self.panel.setObjectName('panel')
        self.panel.setStyleSheet('#panel{background: rgba(57,70,88, 0);/**/'
                                 'border-bottom-left-radius:10px;'
                                 'min-width: 220px;max-width: 320px;}')
        # self.panel.resize(240, 0)
        # rgba(77, 115, 153, 200)
        # rgba(77, 115, 153, 200) rgba(71,84,100, 200) rgba(67,93,121, 200)

        # 顶部按钮，显示保险库标题等
        self.pb_vault = QtWidgets.QPushButton('保险库', self.panel)  # 保险库按钮
        self.pb_vault.setFixedHeight(self.h_vault)
        self.pb_vault.setStyleSheet("QPushButton{color:white;background:rgba(57,70,88, 200);"  # 按键前景色背景色
                                    "border-radius:6px;font : 16px;}"  # 圆角半径
                                    "QPushButton:hover{background:rgba(67,93,121, 200)}"  # 光标移动到上面后的前景色
                                    "/*QPushButton:pressed{background:rgba(57,70,88, 200);border: None;}*/")  # 按下时的样式
        self.pb_vault.setToolTip('保险库菜单 (Ctrl+D)')
        # self.pb_vault.setText('在这台电脑上')
        self.pb_vault.clicked.connect(self.slot_vault_clicked)

        # 搜索框
        self.le_search = QtWidgets.QLineEdit()
        self.le_search.setPlaceholderText('筛选保险库')  # 占位符文本
        self.le_search.isClearButtonEnabled()  # 设置清除内容的按钮
        self.le_search.setStyleSheet('height:25px;')
        # le_search.textEdited.conect(self.slot_search_vault)

        # 所有保险库的列表组
        self.tw_vaults = QtWidgets.QTreeWidget()
        self._init_ui_vaults()

        vl_low = QtWidgets.QVBoxLayout()
        vl_low.setContentsMargins(10, 10, 10, 0)
        vl_low.setSpacing(10)
        vl_low.addWidget(self.le_search)
        vl_low.addWidget(self.tw_vaults)

        vl_panel = QtWidgets.QVBoxLayout(self.panel)
        vl_panel.setContentsMargins(0, 0, 0, 0)
        vl_panel.setSpacing(0)
        vl_panel.addWidget(self.pb_vault)
        vl_panel.addLayout(vl_low)

        # 当前保险库的所有分类项目，绝对布局
        self.tw_genres = QtWidgets.QTreeWidget(self.panel)
        self._init_ui_genres()

    def _flush_panel(self):
        # 面板绝对布局的刷新
        self.pb_vault.setGeometry(0, 0, self.panel.width(), self.h_vault)
        # self.tw_genres.setColumnWidth(1, self.panel.width() - 60)  # 设置树形控件的列的宽度

    # region 库按钮相关
    def _init_ui_vaults(self):
        # 多个保险库的列表
        qss_tree = '''/**********QTreeView**********/
                    QHeaderView::section {
                        height:25px;
                        color:white;
                        background:#505050;
                        border-left:0px solid gray;
                        border-right:1px solid gray;
                        border-top:0px solid gray;
                        border-bottom:0px solid gray;
                    }

                    QTreeView {
                        border:none;
                        background: transparent; /*#404040;*/
                        show-decoration-selected: 1;
                    }
                    QTreeView::item {
                        height: 25px;
                        border: none;
                        color: white;
                        background: transparent;
                    }
                    QTreeView::item:hover {
                        background: transparent;
                    }
                    QTreeView::item:selected{
                        background: #1E90FF;
                    }
                    QTreeView::branch {
                        background: transparent;
                    }
                    QTreeView::branch:hover {
                        background: transparent;
                    }
                    QTreeView::branch:selected {
                        background: #1E90FF;
                    }
                    QTreeView::branch:closed:has-children{
                        image: url(:/image/treeclose.png);
                    }
                    QTreeView::branch:open:has-children{
                        image: url(:/image/treeopen.png);
                    }'''
        self.tw_vaults.setStyleSheet(qss_tree)

        # pb_all = QtWidgets.QPushButton(QtGui.QIcon('E:/Codes/res/images/1.gif'), '所有保险库', self.wg_vaults)
        #
        # vl_vaults = QtWidgets.QVBoxLayout(self.wg_vaults)
        # # vl_vaults.setContentsMargins(0, 0, 0, 0)
        # vl_vaults.setSpacing(0)
        # vl_vaults.addWidget(le_search)
        # vl_vaults.addWidget(pb_all)

    def deal(self):
        all_data = ['所有项目', '收藏夹']

        # def get_item_wight(data):
        #     # 读取属性
        #     ship_name = data['ship_name']
        #     ship_photo = data['ship_photo']
        #     ship_index = data['ship_index']
        #     ship_type = data['ship_type']
        #     ship_country = data['ship_country']
        #     ship_star = data['ship_star']
        #     # 总Widget
        #     wight = QWidget()
        #
        #     # 总体横向布局
        #     layout_main = QHBoxLayout()
        #     map_l = QLabel()  # 头像显示
        #     map_l.setFixedSize(40, 25)
        #     maps = QPixmap(ship_photo).scaled(40, 25)
        #     map_l.setPixmap(maps)
        #
        #     # 右边的纵向布局
        #     layout_right = QVBoxLayout()
        #
        #     # 右下的的横向布局
        #     layout_right_down = QHBoxLayout()  # 右下的横向布局
        #     layout_right_down.addWidget(QLabel(ship_type))
        #     layout_right_down.addWidget(QLabel(ship_country))
        #     layout_right_down.addWidget(QLabel(str(ship_star) + "星"))
        #     layout_right_down.addWidget(QLabel(ship_index))
        #
        #     # 按照从左到右, 从上到下布局添加
        #     layout_main.addWidget(map_l)  # 最左边的头像
        #
        #     layout_right.addWidget(QLabel(ship_name))  # 右边的纵向布局
        #     layout_right.addLayout(layout_right_down)  # 右下角横向布局
        #
        #     layout_main.addLayout(layout_right)  # 右边的布局
        #
        #     wight.setLayout(layout_main)  # 布局给wight
        #     return wight  # 返回wight

        for ship_data in all_data:
            item = QtWidgets.QListWidgetItem(self.lw_genres)  # 创建QListWidgetItem对象
            item.setSizeHint(QtCore.QSize(200, 50))  # 设置QListWidgetItem大小
            item.setText(ship_data)
            item.setIcon(QtGui.QIcon("E:/Codes/res/images/watermark.gif"))
            # self.lw_genres.addItem(item)  # 添加item
            # widget = get_item_wight(ship_data)  # 调用上面的函数获取对应
            # self.lw_genres.setItemWidget(item, widget)  # 为item设置widget

    def slot_vault_clicked(self):
        self.anti(self.vaults_is_show)
        self.vaults_is_show = 1 - self.vaults_is_show

    def anti(self, is_up=True):
        st, ed = None, None
        if is_up:
            st = QtCore.QPoint(0, self.height())
            ed = QtCore.QPoint(0, self.h_vault + 10)
            self.tw_genres.resize(self.panel.width(), self.panel.height() - self.h_vault - 10)
        else:
            st = QtCore.QPoint(0, self.h_vault + 10)
            ed = QtCore.QPoint(0, self.height())

        # 基本动画设置
        anim = QtCore.QPropertyAnimation(self.tw_genres, b"pos", self)
        anim.setStartValue(st)
        anim.setEndValue(ed)
        anim.setDuration(250)
        # animation.setEasingCurve(css)
        anim.start()
        # animation.finished.connect(kj.deleteLater)

    def slot_search_vault(self):
        self.log.debug('slot_search_vault')

    # endregion

    # region 项目列表相关
    def _init_ui_genres(self):
        # 某保险库下的各类别的列表
        size_item = QtCore.QSize(30, 30)
        self.tw_genres.setIconSize(QtCore.QSize(20, 20))
        self.tw_genres.setGeometry(0, self.height(), 100, 100)  # 相当于隐藏了

        qss_tree = """QTreeView {
                    outline: 0px;
                    background:rgba(57,70,88, 255);/*background: rgb(47, 64, 78);*/
                    border:0px;
                    font:16px;
                    alternate-background-color: yellow;
                    show-decoration-selected: 1;/*整行颜色一致  选中整项还是仅仅只是项的文本*/
                    }
                    QTreeView::item {
                        min-height: 30px;
                        color:skyblue;
                        /*background: transparent;
                        border: 1px solid #d9d9d9;
                        border-top-color: transparent;
                        border-bottom-color: transparent;*/
                    }
                    QTreeView::item:hover {
                        background: rgba(77, 115, 153, 255);/*rgb(41, 56, 71);
                        background: transparent;*/
                    }
                    QTreeView::item:selected {
                        background: rgb(41, 56, 71);
                    }
                    QTreeView::item:selected:active{
                        background: rgb(41, 56, 71);
                    }
                    QTreeView::item:selected:!active{
                        background: rgb(41, 56, 71);
                    }
                    QTreeView::branch:open:has-children {
                        background: rgb(41, 56, 71);
                    }
                    QTreeView::branch:has-siblings:!adjoins-item {
                        background: green;
                    }
                    QTreeView::branch:closed:has-children:has-siblings {
                        background: rgb(47, 64, 78);
                    }
                    QTreeView::branch:has-children:!has-siblings:closed {
                        background: rgb(47, 64, 78);
                    }
                    QTreeView::branch:open:has-children:has-siblings {
                        background: rgb(41, 56, 71);
                    }
                    QTreeView::branch:open:has-children:!has-siblings {
                        background: rgb(41, 56, 71);
                    }
                    QTreeView:branch:hover {
                        background: rgba(77, 115, 153, 255);
                    }
                    QTreeView:branch:selected {
                        background: rgb(41, 56, 71);
                    }
                    """
        self.tw_genres.setStyleSheet(qss_tree)
        # self.tw_genres.setFrameShape(QtWidgets.QListWidget.NoFrame)  # 边框透明
        # self.tw_genres.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)  # 去边框
        # self.tw_genres.setStyleSheet("/*background:rgba(57,70,88, 255);*/"  # 背景色为透明
        #                              "QTreeWidget{border:0px solid rgba(57,70,88, 255); color:black;"
        #                              "background: rgba(57,70,88, 250);/**/"
        #                              "border-bottom-left-radius:10px;}"
        #                              "QTreeWidget::Item{padding-top:20px; padding-bottom:4px; }"
        #                              "QTreeWidget::Item:hover{background:skyblue; }"
        #                              "QTreeWidget::item:selected{background:lightgray; color:red; }"
        #                              "QTreeWidget::item:selected:!active{border-width:0px; background:lightgreen; }")
        # self.tw_genres.setStyleSheet('background:rgba(57,70,88, 255);border:0px;'
        #                              'QTreeWidget::item{height:30px;'
        #                              'QTreeWidget::item:selected{border:1px solid transparent;'
        #                              'font: 15px "ubuntu";color:#51637e;}'
        #                              'QTreeWidget::branch {background: white;}'
        #                              'QTreeWidget::item:hover{background-color:rgb(0,255,0,50);}'
        #                              'QTreeWidget::item:selected{background-color:rgb(255,0,0,100)}}')
        # self.tw_genres.setStyleSheet('QTreeView::branch:has-children:!has-siblings:closed,'
        #                              'QTreeView::branch:closed:has-children:has-siblings{border-image: none; image: '
        #                              'none;} '
        #                              'QTreeView::branch:open:has-children:!has-siblings,'
        #                              'QTreeView::branch:open:has-children:has-siblings{border-image: none; image: '
        #                              'none;}')  # 隐藏了可展开节点前的折叠图标（三角图标）
        # self.tw_genres.setStyleSheet("QTreeView::branch:has-children:!has-siblings:closed,"
        #                              "QTreeView::branch:closed:has-children:has-siblings{"
        #                              "border-image: none; image: "
        #                              "url(e:/Codes/res/images/watermark.jpg);} "
        #
        #                              "QTreeView::branch:open:has-children:!has-siblings,"
        #                              "QTreeView::branch:open:has-children:has-siblings{"
        #                              "border-image: none; image: "
        #                              "url(e:/Codes/res/images/watermark.jpg);}")  # 把折叠图标（三角图标）换成自己的图标
        # TODO 优化3 给节点添加响应事件
        self.tw_genres.itemClicked['QTreeWidgetItem*', 'int'].connect(self.slot_tree_clicked)
        # self.tw_genres.clicked.connect(self.slot_tree_clicked)

        # 初始化列表数据
        self.tw_genres.setColumnCount(2)  # 设置列数
        # self.tw_genres.setHeaderLabels(['Key', 'Value'])  # 设置树形控件头部的标题
        self.tw_genres.header().setDefaultSectionSize(20)  # 设置行间距
        self.tw_genres.header().setMinimumSectionSize(20)  # 设置行间距
        # self.tw_genres.setColumnWidth(0, 30)  # 设置树形控件的列的宽度
        self.tw_genres.setColumnWidth(0, 260)  # 设置树形控件的列的宽度
        self.tw_genres.setColumnWidth(1, 30)  # 设置树形控件的列的宽度
        self.tw_genres.header().setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)  # 第一列不能拉伸
        self.tw_genres.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)  # 仅第二列可以拉伸
        self.tw_genres.header().setStretchLastSection(False)  # 关键是去掉默认的拉伸最后列属性
        # self.tw_genres.resizeColumnToContents(0)
        # self.tw_genres.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)  # 根据内容自适应宽度

        self.tw_genres.header().hide()
        # self.tw_genres.setLayoutDirection(QtCore.Qt.RightToLeft)  # 设置右到左排列
        # self.tw_genres.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.tw_genres.setFrameStyle(QtWidgets.QFrame.NoFrame)  # 去掉边框
        # self.tw_genres.setRootIsDecorated(False)  # 隐藏根节点项前的图标（展开折叠图标）
        # self.tw_genres.setExpandsOnDoubleClick(False)  # 屏蔽双击展开折叠树节点

        # 设置一级节点
        # self.create_tree_item_genre('E:/Codes/res/images/569972.gif', '所有项目')

        all_genre = QtWidgets.QTreeWidgetItem(self.tw_genres)
        all_genre.setText(0, '所有项目')
        all_genre.setIcon(0, QtGui.QIcon('E:/Codes/res/images/569972.gif'))
        all_genre.setSizeHint(0, size_item)
        all_genre.setText(1, str(1))
        # # root.setSizeHint(0, QtCore.QSize(0, 0))  # 隐藏了root，免得鼠标露出轨迹
        # # root.setSizeHint(1, QtCore.QSize(10, 0))
        # # todo 优化2 设置根节点的背景颜色
        # # brush_red = QtGui.QBrush(QtCore.Qt.red)
        # # all_genre.setBackground(0, brush_red)
        # # brush_blue = QtGui.QBrush(QtCore.Qt.blue)
        # # root.setBackground(1, brush_blue)
        # brush_back = QtGui.QBrush(QtGui.QColor(57, 70, 88, 255))
        # all_genre.setBackground(0, brush_back)

        # 设置一级节点
        love_genre = QtWidgets.QTreeWidgetItem(self.tw_genres)
        love_genre.setIcon(0, QtGui.QIcon('E:/Codes/res/images/star.png'))
        love_genre.setText(0, '收藏夹')
        love_genre.setSizeHint(0, size_item)
        # love_genre.setText(1, '0')
        # # child1.setCheckState(0, QtCore.Qt.Checked)
        # # root.addChild(child1)

        # 设置子节点3
        watchtower = QtWidgets.QTreeWidgetItem(self.tw_genres)
        watchtower.setText(0, '瞭望塔')
        watchtower.setSizeHint(0, size_item)
        # 设置孙子节点
        for i in range(len(self.data.mold_watch)):
            grandchild = QtWidgets.QTreeWidgetItem(watchtower)
            grandchild.setText(0, self.data.mold_watch[i][1])
            grandchild.setIcon(0, QtGui.QIcon(f'{self.data.dir_icons}{self.data.mold_watch[i][0]}'))
            grandchild.setSizeHint(0, size_item)

        # 设置子节点4
        child4 = QtWidgets.QTreeWidgetItem(self.tw_genres)
        child4.setText(0, '类别')
        child4.setSizeHint(0, size_item)
        child4.setExpanded(True)
        # 设置孙子节点
        for i in range(len(self.data.mold_genre)):
            grand = QtWidgets.QTreeWidgetItem(child4)
            grand.setText(0, self.data.mold_genre[i][1])
            grand.setIcon(0, QtGui.QIcon(f'{self.data.dir_icons}{self.data.mold_genre[i][0]}'))
            grand.setSizeHint(0, size_item)

        # 设置子节点5
        child5 = QtWidgets.QTreeWidgetItem(self.tw_genres)
        child5.setText(0, '标签')
        child5.setSizeHint(0, size_item)

        # 设置子节点6
        child6 = QtWidgets.QTreeWidgetItem(self.tw_genres)
        child6.setText(0, '回收站')
        child6.setIcon(0, QtGui.QIcon('E:/Codes/res/images/recycle.gif'))
        child6.setSizeHint(0, size_item)
        # child6.setText(1, 'android')

        # 加载根节点的所有属性与子控件
        # self.tw_genres.addTopLevelItem(root)

        # 节点全部展开
        # self.tw_genres.expandAll()

    # 创建 tree 项目
    # def create_tree_item_genre(self, icon, text, num=-1, parent=None):
    #     """
    #     num == -1，则是顶级节点
    #     """
    #
    #     father = parent if num >= 0 else self.tw_genres
    #     item = QtWidgets.QTreeWidgetItem(father)
    #     item.setTextAlignment(1, QtCore.Qt.AlignRight)
    #     # item.setText(0, str(num))
    #     # item.setText(1, text)
    #     # item.setIcon(2, QtGui.QIcon(icon))
    #     item.setSizeHint(0, QtCore.QSize(10, 30))
    #     # item.setSizeHint(1, QtCore.QSize(10, 30))
    #     # item.setSizeHint(1, QtCore.QSize(10, 30))
    #
    #     wg_item = QtWidgets.QPushButton()
    #     hl_item = QtWidgets.QHBoxLayout(wg_item)
    #
    #     logo = QtWidgets.QPushButton(QtGui.QIcon(icon), text)
    #     tail = QtWidgets.QPushButton()
    #     if num < 0:
    #         tail.setIcon(QtGui.QIcon('E:/Codes/res/images/right.png'))
    #     else:
    #         tail.setText(str(num))
    #
    #     logo.setFixedSize(QtCore.QSize(250, 25))
    #     tail.setFixedSize(QtCore.QSize(30, 30))
    #     hl_item.addWidget(logo)
    #     hl_item.addStretch()
    #     hl_item.addWidget(tail)
    #
    #     # son1.autoFillBackground = False
    #     self.tw_genres.addTopLevelItem(item)
    #     self.tw_genres.setItemWidget(item, 0, wg_item)
    #     # self.tw_genres.setItemWidget(self.tw_genres.topLevelItem(0).child(1), 0, son1)
    #     # setItemWidget(tree_item, FIRST_COLUMN, my_check_box)
    #
    #     # child1.setTextAlignment(2, QtCore.Qt.AlignRight)
    #     # item.setTextAlignment(1, QtCore.Qt.AlignRight)
    #     # item.setTextAlignment(0, QtCore.Qt.AlignLeft)

    def slot_tree_clicked(self, item, col):
        # item = QtWidgets.QTreeWidgetItem()
        # item
        log.debug(item.text(col), col)

    # endregion

    # endregion

    # region 类别展示区
    def _init_ui_folder(self):
        # 某类的所有项目列表
        self.folder.setObjectName('folder')
        self.folder.setStyleSheet('#folder{background: rgba(57,170,88, 200);/**/'
                                  'min-width: 200px;max-width: 600px;}')
        self.folder.resize(290, 0)

        # region 快捷命令区
        le = QtWidgets.QLineEdit()  # 搜索框
        le.setFixedHeight(self.h_bar)
        le.setToolTip('搜索')

        tb_add = QtWidgets.QToolButton()  # 添加类别
        tb_add.setIcon(QtGui.QIcon('E:/Codes/res/images/add2.png'))
        tb_add.setToolTip('新项目')
        tb_add.setFixedSize(QtCore.QSize(self.h_bar, self.h_bar))
        tb_add.setIconSize(QtCore.QSize(self.h_bar, self.h_bar))
        tb_add.clicked.connect(self.slot_add_genre_clicked)

        self.wg_card = QtWidgets.QWidget()  # 搜索或新增类别的项目
        hl_card = QtWidgets.QHBoxLayout(self.wg_card)
        hl_card.addWidget(le)
        hl_card.addWidget(tb_add)
        # endregion

        # region 排序区
        pb = QtWidgets.QPushButton("按照 标题 排序的5个项目")
        pb.setIcon(QtGui.QIcon("sure.png"))
        pb.setStyleSheet("QPushButton{color:black;background:lightgreen;"
                         "border:2px;border-radius:10px;padding:2px 4px;}"
                         "QPushButton:hover{color:red}")
        # endregion

        # region 罗列区
        lw = QtWidgets.QListWidget()
        # endregion

        vl_folder = QtWidgets.QVBoxLayout(self.folder)
        vl_folder.setContentsMargins(0, 0, 0, 0)
        vl_folder.addWidget(self.wg_card)
        vl_folder.addWidget(pb)
        vl_folder.addWidget(lw)

    def slot_add_genre_clicked(self):
        log.debug('slot_add_genre_clicked')
        if self.pop_form is None:
            lw = QtWidgets.QListWidget()

            for each in self.data.mold_genre:
                item = QtWidgets.QListWidgetItem(lw)  # 创建QListWidgetItem对象
                item.setSizeHint(QtCore.QSize(50, 30))  # 设置QListWidgetItem大小
                item.setText(each[1])
                item.setIcon(QtGui.QIcon(f'{self.data.dir_icons}{each[0]}'))
                lw.addItem(item)  # 添加item
            lw.setCurrentRow(0)
            lw.resize(200, 30 * (len(self.data.mold_genre) + 1))
            lw.itemClicked.connect(self.slot_genre_item_clicked)

            self.pop_form = PopForm(self.folder, lw)
            ps = QtCore.QPoint(self.wg_card.width() - self.pop_form.width(),
                               self.wg_card.y() + self.wg_card.height() - 18)
            self.pop_form.move(ps)
            log.debug(ps)
        else:
            self.pop_form.show()
            log.debug('no')

    def slot_genre_item_clicked(self, item):
        print(str(item.text()))
        self.pop_form.close()
        # self.detail

    # endregion

    # region 详情展示区
    def _init_ui_detail(self):
        # 详情
        self.detail.setObjectName('detail')
        self.detail.setStyleSheet('#detail{background: rgba(57,70,88, 100);/**/'
                                  'border-bottom-right-radius:10px;'
                                  'min-width: 200px;max-width: 600px;}'
                                  'QPushButton{min-height:30px;max-height: 30px;}')

        wg_tools = QtWidgets.QWidget()  # 工具集合
        hl_tools = QtWidgets.QHBoxLayout(wg_tools)
        wg_tools.setObjectName('tools')
        wg_tools.setStyleSheet('#tools{min-height:30px;max-height: 30px;}')

        pb_edit = QtWidgets.QPushButton('编辑')
        pb_edit.setToolTip('编辑')
        pb_change = QtWidgets.QPushButton('转换为登录信息')
        pb_change.setToolTip('转换为登录信息')
        pb_favorite = QtWidgets.QPushButton(QtGui.QIcon('E:/Codes/res/images/star.png'), '', None)
        pb_favorite.setToolTip('喜好')

        hl_tools.addWidget(pb_edit)
        hl_tools.addWidget(pb_change)
        hl_tools.addWidget(pb_favorite)

        lw = QtWidgets.QListWidget()
        lw.setStyleSheet('background: rgba(57,170,88, 100);/**/'
                         'border-bottom-right-radius:10px;')

        vl_detail = QtWidgets.QVBoxLayout(self.detail)
        vl_detail.setContentsMargins(0, 0, 0, 0)
        vl_detail.addWidget(wg_tools)
        vl_detail.addWidget(lw)

    # endregion

    # region 系统消息区
    def mousePressEvent(self, e: QtGui.QMouseEvent):
        if e.button() == QtCore.Qt.LeftButton:
            if e.pos().y() <= self.h_title:  # 工具栏高度范围内可以移动窗体
                self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标
                self.mPos = e.pos()
                # self.mPos = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            else:
                self.mPos = None

            e.accept()

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):
        # self.log.debug(e.pos())
        if QtCore.Qt.LeftButton and self.mPos:
            self.move(self.mapToGlobal(e.pos() - self.mPos))  # 更改窗口位置
            e.accept()

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent):
        self.mPos = None
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        e.accept()

    def closeEvent(self, event):
        """重写该方法主要是解决打开子窗口时，如果关闭了主窗口但子窗口仍显示的问题，
        使用sys.exit(0) 时就会只要关闭了主窗口，所有关联的子窗口也会全部关闭"""
        log.debug(event)
        # e = QtGui.QCloseEvent()

        # event.accept()
        # event.ignore()
        super().closeEvent(event)  # 先添加父类的方法，以免导致覆盖父类方法（这是重点！！！）
        sys.exit(0)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self._flush_title()
        self.wg_bench.setGeometry(0, self.h_title, self.width() - self.deep,
                                  self.height() - self.h_title - self.deep)
        self._flush_panel()

    def paintEvent(self, event):
        # opt = QStyleOption()
        # opt.initFrom(self)
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)  # 抗锯齿
        # self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
        # super(Canvas, self).paintEvent(event)

        # image = Image.open(r'E:\Codes\res\background\bk2.jpg')
        # image = image.filter(MyGaussianBlur(radius=6))
        # image.save('./tmp.jpg')
        img_new = Utils.img_center(self.rect().width() - self.deep,
                                   self.rect().height() - self.deep,
                                   r'E:\Codes\res\background\bk2.jpg')
        p.setBrush(QtGui.QBrush(img_new))  # 图片刷子
        # p.setBrush(QtGui.QBrush(QtGui.QPixmap(r'E:\Codes\res\background\bk3.jpg')))  # 图片刷子
        # painter.setBrush(QBrush(Qt.blue))
        p.setPen(QtCore.Qt.transparent)

        rect = self.rect()
        rect.setWidth(rect.width() - self.deep)
        rect.setHeight(rect.height() - self.deep)
        p.drawRoundedRect(rect, self.radius, self.radius)
        # painterPath= QPainterPath()
        # painterPath.addRoundedRect(rect, 15, 15)
        # painter.drawPath(painterPath)

        # 直接填充图片
        # pix = QPixmap('./res/images/background11.jpg')
        # painter.drawPixmap(self.rect(), pix)

        super(BackForm, self).paintEvent(event)
    # endregion


if __name__ == '__main__':
    import cgitb  # 相当管用

    # cgitb.enable(format='text')  # 解决 pyqt5 异常只要进入事件循环,程序就崩溃,而没有任何提示
    sys.excepthook = cgitb.enable(1, None, 5, '')
    app = QtWidgets.QApplication(sys.argv)
    w = BackForm()
    # w = PopWin()
    w.show()
    sys.exit(app.exec_())
