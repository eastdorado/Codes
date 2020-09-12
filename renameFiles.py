#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @项目名称: python
# @File    : renameFiles.py
# @Time    : 2019/12/23 13:09
# @Author  : big
# @Email   : shdorado@126.com

import sys
import os

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_ChangeFilenName import Ui_Form
import json
import re
from utilities import Utils, AnimWin


class MainWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.data = {}
        self.files = []
        self.matched_files = []
        # self.count = 0

        try:
            with open("./res/data.json", 'r') as load_f:
                self.data = json.load(load_f)
            # print(self.data)
        except IOError as e:
            self.data = {'path_src': '', 'path_dec': '',
                         'text_mask': '', 'text_fake': '',
                         'enabled_cover': 'True'}
            print(e)
        finally:
            self.init_ui()

    def resizeEvent(self, event):
        palette = QtGui.QPalette()
        # pix = QtGui.QPixmap('res/timg4.jpeg')
        # pix = pix.scaled(self.width(), self.height())
        # palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(palette)

    def closeEvent(self, event):
        # 清理一些 自己需要关闭的东西
        try:
            with open('./res/data.json', 'w') as f:
                json.dump(self.data, f)

            event.accept()  # 界面的关闭   但是会有一些时候退出不完全    需要调用 os 的_exit 完全退出
            os._exit(5)
        except Exception as e:
            print(e)

    def init_ui(self):
        font = QtGui.QFont('NSimSun')
        font.setPointSize(15)
        font.setWeight(50)
        self.listWidget_src_files.setFont(font)
        self.listWidget_dec_files.setFont(font)
        self.lineEdit_mask.setPlaceholderText('掩码为空时，可以复制所有文件，但不能覆盖')
        self.lineEdit_fake.setPlaceholderText('选择覆盖时，只在源目录操作')
        self.lineEdit_mask.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_fake.setAlignment(QtCore.Qt.AlignCenter)
        qss1 = 'QListWidget { outline: none; border:1px solid gray; color: black;}' \
               'QListWidget::Item { width: 50px; height: 30px;}' \
               'QListWidget::Item:hover { background: #4CAF50; color: white; }' \
               'QListWidget::item:selected { background: #e7e7e7; color: #f44336; }' \
               'QListWidget::item:selected:!active { background: lightgreen}'
        qss2 = "QListWidget{border:1px solid gray; color:black; }" \
               "QListWidget::Item{padding-top:20px; padding-bottom:4px; }" \
               "QListWidget::Item:hover{background:skyblue; }" \
               "QListWidget::item:selected{background:lightgray; color:red; }" \
               "QListWidget::item:selected:!active{border-width:0px; background:lightgreen; }"
        self.listWidget_src_files.setStyleSheet(qss1)
        self.listWidget_dec_files.setStyleSheet(qss1)
        # self.listWidget_src_files.setViewMode(QtWidgets.QListView.ListMode)     # 设置为列表显示模式
        # self.listWidget_src_files.setFlow(QtWidgets.QListView.LeftToRight)      # 设置列表从左往右排列
        # self.listWidget_src_files.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.listWidget_src_files.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  # 屏蔽水平与垂直的滑动条
        # self.listWidget_src_files.setHorizontalScrollMode(QtWidgets.QListWidget.ScrollPerPixel)   # 像素滚动
        # QtWidgets.QScroller.grabGesture(self.listWidget_src_files, QtWidgets.QScroller.LeftMouseButtonGesture)  #  鼠标左键拖动

        self.label_path_src.setText('%s' % Utils.getSubStr(self.data['path_src']))
        self.label_path_dec.setText('%s' % Utils.getSubStr(self.data['path_dec']))
        self.lineEdit_mask.setText('%s' % self.data['text_mask'])
        self.lineEdit_fake.setText('%s' % self.data['text_fake'])
        self.checkBox.setChecked(self.data['enabled_cover'])

        self.lineEdit_mask.setAcceptDrops(True)
        self.lineEdit_mask.setDragEnabled(True)
        self.lineEdit_fake.setAcceptDrops(True)
        self.lineEdit_fake.setDragEnabled(True)
        # self.listWidget_src_files.setAcceptDrops(True)
        self.listWidget_src_files.setDragEnabled(True)
        # self.listWidget_dec_files.setAcceptDrops(True)
        self.listWidget_dec_files.setDragEnabled(True)

        self.flush()

    def flush(self):
        self.listWidget_src_files.clear()
        self.files.clear()
        self.matched_files.clear()
        count = 0
        cur_dir = self.data['path_src']
        if os.path.isdir(cur_dir):
            list_files = os.listdir(cur_dir)  # 列出文件夹下所有的目录与文件
            for each in list_files:
                path = os.path.join(cur_dir, each)  # 构造完整路径
                # 判断路径是否是一个文件目录或者文件
                # 如果是文件目录，继续递归
                if os.path.isdir(path):
                    # _files.extend(list_all_files(path))
                    continue
                if os.path.isfile(path):
                    self.files.append(each)
                    count += 1
                    item = QtWidgets.QListWidgetItem(each)
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                    if self.data['text_mask'] != '' and re.search(r'.*%s.*' % self.data['text_mask'], each):
                        item.setBackground(QtGui.QColor('lightblue'))
                        self.matched_files.append(each)
                    self.listWidget_src_files.addItem(item)
            path = Utils.getSubStr(self.data['path_src'])
            self.label_path_src.setText(f'{path}    共{count}  匹配{len(self.matched_files)}')

    def go(self):
        if self.data['path_src'] == '' or not self.files:
            spirit = AnimWin("未找到目录或文件", self, 18)
            return
        try:
            self.listWidget_dec_files.clear()
            count = 0
            if self.data['enabled_cover']:  # 覆盖
                if not self.matched_files:
                    AnimWin("未匹配到合适的文件", self, 18)
                    return
                for each in self.matched_files:
                    new_name = each.replace(self.data['text_mask'], self.data['text_fake'])
                    path_src = self.data['path_src'] + '/' + each
                    path_dec = self.data['path_src'] + '/' + new_name
                    path_src = path_src.replace('/', '\\\\')
                    path_dec = path_dec.replace('/', '\\\\')
                    print(path_src)
                    os.rename(path_src, path_dec)
                    self.listWidget_dec_files.addItem(new_name)
                    count += 1
                    self.label_path_dec.setText('%s    %d个' % (Utils.getSubStr(self.data['path_src']), count))
            else:   # 复制
                if self.data['path_dec'] == '':
                    AnimWin("保存目录不能为空", self, 18)
                    # QtWidgets.QSystemTrayIcon.showMessage()
                    return
                if self.data['text_mask'] == '':     # 全部复制
                    for each in self.files:
                        path_src = self.data['path_src'] + '/' + each
                        path_dec = self.data['path_dec'] + '/' + each
                        path_src = path_src.replace('/', '\\\\')
                        path_dec = path_dec.replace('/', '\\\\')
                        '''必须加双引号把路径括起来，才能解决路径里有空格的问题。中文也可'''
                        os.popen('copy "%s" "%s"' % (path_src, path_dec))
                        self.listWidget_dec_files.addItem(each)
                        count += 1
                else:
                    for each in self.matched_files:
                        new_name = each.replace(self.data['text_mask'], self.data['text_fake'])
                        path_src = self.data['path_src'] + '/' + each
                        path_dec = self.data['path_dec'] + '/' + new_name

                        path_src = path_src.replace('/', '\\\\')
                        path_dec = path_dec.replace('/', '\\\\')
                        print(path_src)
                        order = 'copy "%s" "%s"' % (path_src, path_dec)
                        os.system(order)
                        print(order)
                        self.listWidget_dec_files.addItem(new_name)
                        count += 1
                self.label_path_dec.setText('%s    %d个' % (Utils.getSubStr(self.data['path_dec']), count))
        except Exception as e:
            print(e)
        finally:
            pass

    def slot_clicked(self, control):
        if control.objectName() == r'pushButton_src':
            self.data['path_src'] = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                               "选取源文件夹",
                                                                               self.data['path_src'])  # 起始路径
            # print(self.data['path_src'])
            self.flush()

        elif control.objectName() == r'pushButton_dec':
            self.data['path_dec'] = QtWidgets.QFileDialog.getExistingDirectory(self, "选取保存文件夹", self.data['path_dec'])  # 起始路径
            # print(self.data['path_dec'])
            self.label_path_dec.setText('%s    %d个' % (Utils.getSubStr(self.data['path_dec']), 0))
            self.listWidget_dec_files.clear()

        elif control.objectName() == r'pushButton_flush':
            self.flush()
        else:
            reply = QtWidgets.QMessageBox.question(self, '警告', '改名过程不可逆，\n你确认要更改吗？',
                                                   QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.go()
            else:
                pass
        # control = QtWidgets.QPushButton
        # print(control.objectName())

    def slot_text_changed(self, control):
        if control.objectName() == r'lineEdit_mask':
            self.data['text_mask'] = control.text()
            # print(self.data['text_mask'])
            self.flush()
        else:
            self.data['text_fake'] = control.text()
            # print(self.data['text_fake'])

    def slot_covered(self, enabled):
        self.data['enabled_cover'] = enabled
        # print(enabled)

    def dragEnterEvent(self, e):
        print(e)
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        print(e.mimeData().text())
        # self.addItem(e.mimeData().text())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    # print(win.getSubStr("12345678987654321"))
    sys.exit(app.exec_())
