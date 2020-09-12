#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @项目名称: python
# @File    : smartGo.py
# @Time    : 2020/1/9 18:06
# @Author  : big
# @Email   : shdorado@126.com

import sys
import os
from PySide2 import QtCore, QtGui, QtWidgets
import math
from functools import partial
import win32api, win32gui, win32con, win32com.client, win32
# import pefile

from myUi import UiSmartGo
from utilities import AnimWin, Utils


class Demo(QtWidgets.QToolBox):
    def __init__(self):
        super(Demo, self).__init__()
        self.resize(400, 600)
        # self.
        self.groupbox_1 = QtWidgets.QGroupBox(self)  # 2
        self.groupbox_2 = QtWidgets.QGroupBox(self)
        self.groupbox_3 = QtWidgets.QGroupBox(self)

        self.toolbtn_f1 = QtWidgets.QToolButton(self)  # 3
        self.toolbtn_f2 = QtWidgets.QToolButton(self)
        self.toolbtn_f3 = QtWidgets.QToolButton(self)
        self.toolbtn_m1 = QtWidgets.QToolButton(self)
        self.toolbtn_m2 = QtWidgets.QToolButton(self)
        self.toolbtn_m3 = QtWidgets.QToolButton(self)

        self.v1_layout = QtWidgets.QVBoxLayout()
        self.v2_layout = QtWidgets.QVBoxLayout()
        self.v3_layout = QtWidgets.QVBoxLayout()

        self.addItem(self.groupbox_1, 'Couple One')  # 4
        self.addItem(self.groupbox_2, 'Couple Two')
        self.addItem(self.groupbox_3, 'Couple Three')
        self.currentChanged.connect(self.print_index_func)  # 5

        self.layout_init()
        self.groupbox_init()
        self.toolbtn_init()

    def layout_init(self):
        self.v1_layout.addWidget(self.toolbtn_f1)
        self.v1_layout.addWidget(self.toolbtn_m1)
        self.v2_layout.addWidget(self.toolbtn_f2)
        self.v2_layout.addWidget(self.toolbtn_m2)
        self.v3_layout.addWidget(self.toolbtn_f3)
        self.v3_layout.addWidget(self.toolbtn_m3)

    def groupbox_init(self):  # 6
        # self.groupbox_1.setFlat(True)
        # self.groupbox_2.setFlat(True)
        # self.groupbox_3.setFlat(True)
        self.groupbox_1.setLayout(self.v1_layout)
        self.groupbox_2.setLayout(self.v2_layout)
        self.groupbox_3.setLayout(self.v3_layout)

    def toolbtn_init(self):  # 7
        self.toolbtn_f1.setIcon(QtGui.QIcon('res/1.png'))
        self.toolbtn_f2.setIcon(QtGui.QIcon('res/exit.png'))
        self.toolbtn_f3.setIcon(QtGui.QIcon('res/copy.png'))
        self.toolbtn_m1.setIcon(QtGui.QIcon('res/1.gif'))
        self.toolbtn_m2.setIcon(QtGui.QIcon('res/lines.png'))
        self.toolbtn_m3.setIcon(QtGui.QIcon('res/pionts.png'))

    def print_index_func(self):
        couple_dict = {
            0: 'Couple One',
            1: 'Couple Two',
            2: 'Couple Three'
        }
        sentence = 'You are looking at {}.'.format(couple_dict.get(self.currentIndex()))
        print(sentence)


class MyTabWidget(QtWidgets.QTabWidget):
    def __init__(self, centralwidget):
        # centralwidget 窗体参数
        super().__init__(centralwidget)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rightMenuShow)  # 开放右键策略

    def rightMenuShow(self, point):
        # 添加右键菜单
        self.popMenu = QtWidgets.QMenu()
        tj = QtWidgets.QAction(u'添加', self)
        sc = QtWidgets.QAction(u'删除', self)
        xg = QtWidgets.QAction(u'修改', self)
        self.popMenu.addAction(tj)
        self.popMenu.addAction(sc)
        self.popMenu.addAction(xg)
        # 绑定事件
        tj.triggered.connect(self.test)
        sc.triggered.connect(self.test)
        xg.triggered.connect(self.test)
        self.showContextMenu(QtGui.QCursor.pos())

    def test(self):
        print('test')

    def showContextMenu(self, pos):
        # 调整位置
        '''''
        右键点击时调用的函数
        '''
        # 菜单显示前，将它移动到鼠标点击的位置
        self.popMenu.move(pos)
        self.popMenu.show()


class Button(QtWidgets.QPushButton):
    def __init__(self, title, parent):
        super().__init__(title, parent)

    def mouseMoveEvent(self, e):
        if e.buttons() != QtCore.Qt.RightButton:
            print('')

        mimeData = QtCore.QMimeData()

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAcion = drag.exec_(QtCore.Qt.MoveAction)


class MainWindow(QtWidgets.QWidget, UiSmartGo):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.layout_w = False  # 水平布局
        self.layout = None
        self.list_groups = [['res/1.png', '常用'], ['', '娱乐'], ['', '工具']]
        self.cur_group = 0
        self.list_apps = [[[None, 'res/cross.png', '闹猴屏幕取色精灵', r'E:\tools\闹猴屏幕取色精灵1.4.6.128/IdealGetcolor.exe'],
                           [None, '', '', '']],
                          [[None, '', '', ''], [None, '', '', '']]]
        self.cur_pb = 0

        self.miniWidth = 80  # 按钮最小宽度
        self.setupUI(self)
        self.init_ui()

    def init_ui(self):
        if self.layout_w:
            self.layout = self.hl_main
        else:
            self.layout = self.vl_main
        self.setLayout(self.layout)

        self.layout.setContentsMargins(0, 5, 0, 5)
        self.layout.setSpacing(5)
        self.layout.addLayout(self.gl_groups)
        # self.layout.addLayout(self.hl_apps)
        self.layout.addWidget(self.gb_apps)

        self.updateUI()
        '''
        Qt.DefaultContextMenu	默认菜单，重写 contextMenuEvent() 实现自定义
        Qt.NoContextMenu	    无菜单，事件响应传递给部件父级
        Qt.PreventContextMenu	无菜单，事件响应不继续传递
        Qt.ActionsContextMenu	事件菜单，只响应部件事件，部件子件的事件不响应
        Qt.CustomContextMenu	用户自定义菜单，需绑定事件 customContextMenuRequested，并实现 槽函数
        '''
        # self.bar.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # # self.tabWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        # self.bar.customContextMenuRequested.connect(self.custom_right_menu)

    def updateUI(self):
        Utils.clear_layout(self.gl_groups)

        if self.list_groups:
            count = len(self.list_groups)
            row = int(self.rect().width() / self.miniWidth)
            # print(f'row= {row}')
            col = math.ceil(count / row)
            # print(f'col= {col}')
            # 2创建按钮的标签列表
            names = [each[1] for each in self.list_groups]
            # 3 在网格中创建一个位置列表
            positions = [(i, j) for i in range(col) for j in range(row)]
            # 4 创建按钮并通过addWIdget（）方法添加到布局中
            for position, name in zip(positions, names):
                button = QtWidgets.QPushButton(name)
                button.setMinimumWidth(self.miniWidth)
                button.setStyleSheet('border:none;font-size:18px;font-family:MicrosoftYaHei;font-weight:bold;')
                button.clicked.connect(partial(self.slot1, position))
                self.gl_groups.addWidget(button, *position)

        Utils.clear_layout(self.hl_apps)
        if self.list_apps:
            # qss = Utils.readQss('res/styleSheet.qss')
            qss = '''QToolButton{
               min-width:80px;
               min-height:32px;
            }
            QToolButton{
            color:rgb(255, 255, 255);
            min-height:20;
            border-style:solid;
            border-top-left-radius:2px;
            border-top-right-radius:2px;
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop:0 rgb(226,236,241), 
                                        stop: 0.3 rgb(160,160,160),
                                          stop: 1 rgb(140,140,140));
            border:1px;
            border-radius:5px;padding:2px 4px;/*border-radius控制圆角大小*/
            }
            QToolButton:hover{  /*鼠标放上后*/
            color:rgb(255, 255, 255);
            min-height:20;
            border-style:solid;
            border-top-left-radius:2px;
            border-top-right-radius:2px;
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop:0 rgb(226,236,241), 
                                        stop: 0.3 rgb(160,160,160),
                                          stop: 1 rgb(120,120,120));
            border:1px;
            border-radius:5px;padding:2px 4px;
            }
            QToolButton:pressed{ /*按下按钮后*/
            color:rgb(255, 255, 255);
            min-height:20;
            border-style:solid;
            border-top-left-radius:2px;
            border-top-right-radius:2px;
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop:0 rgb(226,236,241), 
                                        stop: 0.3 rgb(190,190,190),
                                          stop: 1 rgb(160,160,160));
            border:1px;
            border-radius:5px;padding:2px 4px;
            }
            QToolButton:checked{    /*选中后*/
            color:rgb(255, 255, 255);
            min-height:20;
            border-style:solid;
            border-top-left-radius:2px;
            border-top-right-radius:2px;
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop:0 rgb(226,236,241), 
                                        stop: 0.3 rgb(190,190,190),
                                          stop: 1 rgb(160,160,160));
            border:1px;
            border-radius:5px;padding:2px 4px;
            }'''

            for each in self.list_apps[self.cur_group]:
                pb = QtWidgets.QToolButton()
                # pb = QtWidgets.QPushButton()
                pb.setText(each[1])
                pb.setIcon(QtGui.QIcon(each[0]))
                # pb.setIconSize(QtCore.QSize(30, 30))
                pb.setToolTip(each[3])
                pb.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
                # pb.setStyleSheet(qss)
                # print(each[0])
                pb.clicked.connect(partial(self.slot2, each[2]))
                # pb.clicked.connect(lambda: self.slot2(each[2]))
                self.hl_apps.addWidget(pb)

    def custom_right_menu(self, pos):
        menu = QtWidgets.QMenu()
        opt1 = menu.addAction("menu1")
        opt2 = menu.addAction("menu2")
        action = menu.exec_(self.bar.mapToGlobal(pos))
        if action == opt1:
            # do something
            print("menu1")
            return
        elif action == opt2:
            # do something
            print("menu2")
            return
        else:
            print("other")
            return

    def slot1(self, index):
        print(f'slot1 {index}')

    def slot2(self, order):
        # print(f'order= {order}')
        # path = os.path.dirname(order)
        # file = os.path.basename(order)
        (filepath, tempfilename) = os.path.split(order)
        # (filename, extension) = os.path.splitext(tempfilename)
        print(f'dir={filepath}  exe={tempfilename}')
        win32api.ShellExecute(0, 'open', tempfilename, '', filepath, 1)  # 前台打开

    def resizeEvent(self, event):
        palette = QtGui.QPalette()
        pix = QtGui.QPixmap('res/background.jpg')
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(palette)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        position = e.pos()
        for each in self.list_apps[self.cur_group]:
            if each[0].isDown():
                each[0].move(position)
        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()


def test(exePath):
    import win32ui
    import win32gui
    import win32con
    import win32api

    # ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
    # ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)
    ico_x = 32
    ico_y = 32

    # exePath = "c:/windows/system32/shell32.dll"
    large, small = win32gui.ExtractIconEx(exePath, 0)
    useIcon = large[0]
    destroyIcon = small[0]
    win32gui.DestroyIcon(destroyIcon)
    print('dd', (useIcon))

    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_x)
    hdc = hdc.CreateCompatibleDC()

    hdc.SelectObject(hbmp)
    hdc.DrawIcon((0, 0), useIcon)
    savePath = "d:/test.bmp"
    hbmp.SaveBitmapFile(hdc, savePath)

# def test2(file):
#     info = SHFILEINFO(0)
#     SHGetFileInfo("D:\\book", 0, & info, sizeof(info), SHGFI_TYPENAME | SHGFI_DISPLAYNAME | SHGFI_ICON)
#     pidl = _shell.SHParseDisplayName(file, 0)[0]
#     assert isinstance(pidl, list)
#
#     flags = (shellcon.SHGFI_PIDL | shellcon.SHGFI_ICON |
#              shellcon.SHGFI_DISPLAYNAME | shellcon.SHGFI_TYPENAME |
#              shellcon.SHGFI_ATTRIBUTES | shellcon.SHGFI_SYSICONINDEX)
#
#     hImageList, finfo = win32.shell.SHGetFileInfo(pidl, 0, flags)
#
#     print('hImageList:', hImageList)
#     for name, typ in finfo._fields_:
#         print(name, ': ', ascii(getattr(finfo, name)), sep='')
#
#     if finfo.hIcon:
#         win32gui.DestroyIcon(finfo.hIcon)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    # win = Demo()
    win.show()
    sys.exit(app.exec_())
    # filename = r'E:\vs code\Microsoft VS Code\Code.exe'
    # filename = r"C:\Program Files (x86)\Enpass\Enpass.exe"
    # st = os.stat(filename)
    # test(filename)
    # print(get_version_via_com(filename))
    # print(getFileVersion(filename))
    # print(_getCompanyNameAndProductName(filename))
    # print(_get_company_and_product(filename))
    # szTitle = folderItem.ExtendedProperty("Title")
    # szAuthor = folderItem.ExtendedProperty("Author")

    # fattrs = win32api.GetFileAttributes(filename)
    # print((st))
    # shell = win32com.client.Dispatch("WScript.Shell")
    # shortcut = shell.CreateShortCut(r"C:\Program Files (x86)\Enpass\Enpass.exe")
    # print(shortcut.Targetpath)
