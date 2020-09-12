#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @项目名称: python
# @File    : customTableWg.py
# @Time    : 2020/3/10 13:32
# @Author  : big
# @Email   : shdorado@126.com

import sys
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
from utilities import Utils


class CustTableWidget(QtWidgets.QTableWidget):
    """TableWidgetDragDropRows
        支持在各个QTableWidget之间拖放行的QTableWidget自定义扩展类
        Extends:
            QTableWidget
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setDragDropOverwriteMode(False)
        self.last_drop_row = None

        self.parent = parent
        self.margin = 0
        self.item_width = [0, 60, 80, 80, 140, 80, 80]  # table 列宽
        self.flag_sort = True
        # self.stretch_col_width = 0  # 可伸缩列的实际宽度
        self.data = []  # 二维数组

    def initUI(self):
        self.setShowGrid(False)  # 设置不显示格子线
        self.setFrameShape(QtWidgets.QFrame.NoFrame)  # 设置无表格的外框
        # self.tableWidget.sortItems(0, QtGui.Qt.DescendingOrder)  # 设置按照第一列自动降序排序
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)  # 进行多选 设置SingleSelection只可以单选，

        # table.setColumnCount(5)  ##设置表格一共有五列
        # table.setHorizontalHeaderLabels(['id', '姓名', '年龄', '学号', '地址'])  # 设置表头文字
        # self.tableWidget.setColumnWidth(0, 280)  # 设置j列的宽度
        # self.tableWidget.setRowHeight(i, 50)  # 设置i行的高度
        # self.tableWidget.verticalHeader().setVisible(False)  # 隐藏垂直表头
        # table.setColumnHidden(1, True)  # 将第二列隐藏
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 设置表格不可更改
        # self.setSortingEnabled(True)  # 设置表头可以自动排序
        self.setStyleSheet("selection-background-color:skyblue;")  # 设置选中背景色

        h_header = self.horizontalHeader()
        h_header.setStyleSheet('QHeaderView::section{background:lightblue;color:green}')  # 设置表头的背景色为绿色
        # SortIndicator为水平标题栏文字旁边的三角指示器
        # h_header.setSortIndicator(1, QtCore.Qt.AscendingOrder)
        # h_header.setSortIndicatorShown(True)

        font = QtGui.QFont('微软雅黑', 12)
        font.setBold(True)  # 设置字体加粗
        h_header.setFont(font)  # 设置表头字体
        # 为font设置的字体样式

        h_header.setFixedHeight(25)  # 设置表头高度
        # headerGoods.setStretchLastSection(True)  #设置最后一列拉伸至最大
        # headerGoods.resizeSection(0, 200)  # 设置第一列的宽度为200
        # h_header.setSectionsClickable(False)  # 设置表头不可点击（默认点击后进行排序/全选）
        # h_header.setVisible(False)  # 隐藏水平表头
        # sz = headerGoods.width()
        # cut = sum(self.item_width, - self.item_width[0]) + sz + 2 * self.margin + 2
        # self.item_width[0] = self.size().width() - cut  # 第一列宽度
        # # print(cut, self.item_width, self.size(), self.tableWidget.width())

        h_header.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)  # 固定大小
        # h_header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  # 所有列自动拉伸，充满界面
        # h_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)
        # h_header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        h_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)  # 设置第1列宽度自动调整，充满屏幕
        for i in range(1, 7):
            self.setColumnWidth(i, self.item_width[i])

        # self.tableWidget.sectionClicked[int].connect(self.slot_le_edited)
        self.itemClicked.connect(self.parent.parent().handleItemClicked)
        self.horizontalHeader().sectionClicked.connect(self.slot_HorSectionClicked)  # 表头单击信号
        self.itemChanged.connect(self.parent.parent().slot_itemchanged)

    def createWidget(self, flag_other=0):
        '''
        嵌入table的控件
        :param flag_other: 不嵌入 tabel的控件组
        :return:
        '''

        wg_operate = QtWidgets.QWidget(self.parent)
        hl = QtWidgets.QHBoxLayout(wg_operate)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(0)
        # self.wg_operate.setFixedSize(QtCore.QSize(20, 20))
        sz = None
        if flag_other == 1:
            sz = QtCore.QSize(25, 25)
            sz0 = QtCore.QSize(25*3, 25)
        else:
            sz = QtCore.QSize(20, 20)
            sz0 = QtCore.QSize(25*3, 25)

        # 这两行解决了控件不居中显示的问题
        wg_operate.setMinimumSize(sz0)
        wg_operate.setMaximumSize(sz0)

        # qss = Utils.readQss('./res/style/QToolButtonQss.txt')

        tb_open_file = QtWidgets.QPushButton(wg_operate)
        tb_open_file.setStyleSheet("border:none")
        tb_open_file.setIcon(QtGui.QIcon('./res/images/file.gif'))
        tb_open_file.setIconSize(sz)
        tb_open_file.setObjectName('open_file')
        tb_open_file.setToolTip('打开文件')

        tb_open_dir = QtWidgets.QToolButton(wg_operate)
        tb_open_dir.setStyleSheet("border:none")
        tb_open_dir.setIcon(QtGui.QIcon('./res/images/dir.gif'))
        tb_open_dir.setIconSize(sz)
        tb_open_dir.setObjectName('open_dir')
        tb_open_dir.setToolTip('打开目录')

        tb_recycle = QtWidgets.QToolButton(wg_operate)
        tb_recycle.setStyleSheet("border:none")
        tb_recycle.setIcon(QtGui.QIcon('./res/images/recycle.gif'))
        tb_recycle.setIconSize(sz)
        tb_recycle.setObjectName('recycle')
        if flag_other == 1:
            tb_recycle.setToolTip("删除文件")
        else:
            tb_recycle.setToolTip('剔除')

        tb_open_file.clicked.connect(partial(self.parent.parent().slot_tb_clicked, tb_open_file, flag_other))
        tb_open_dir.clicked.connect(partial(self.parent.parent().slot_tb_clicked, tb_open_dir, flag_other))
        tb_recycle.clicked.connect(partial(self.parent.parent().slot_tb_clicked, tb_recycle, flag_other))

        hl.addWidget(tb_open_file)
        hl.addWidget(tb_open_dir)
        hl.addWidget(tb_recycle)

        return wg_operate

    def update_data(self, data, isAppend=True):
        """
        更新行列数据
        :param data: 行列数据二维列表
        :param isAppend: 覆盖或者追加
        :return:
        """
        if data is None:
            self.data.clear()
        if not isinstance(data, list):
            return
        if not isAppend:
            self.data.clear()
        self.data.extend(data)

        CustTableWidget._sort_nicely(self.data)

    def update_table(self):
        for rP in range(0, self.rowCount())[::-1]:
            self.removeRow(rP)
        # self.clearContents()  # 清空内容，不包括表头,不删除行

        count = len(self.data)
        self.setRowCount(count)
        for i in range(count):
            self._write_cols(i, self.data[i])

    def _write_cols(self, row, data_cols=None):
        """
        填充已存在行的各列数据
        :param row: 行序号
        :param data_cols: 列数据的列表
        :return:
        """
        if not data_cols or not 0 <= row < self.rowCount():
            return
        # print(data_cols)
        count = min(self.columnCount() - 1, len(data_cols))  # 取前count个有效数据
        # todo 填充每列数据
        # 第一列实际宽度，像素数，扣除行头宽
        # v_head_w = self.verticalHeader().width()
        # h_head_w = self.horizontalHeader().width()
        # print('kuandu:', h_head_w, v_head_w)
        # stretch_col_width = h_head_w - v_head_w - sum(self.item_width, - self.item_width[0]) -20
        # value = Utils.getSubStr(cols_data_list[0], stretch_col_width, self.font())
        if data_cols[0] is None:  # 列数据不能是 None
            data_cols[0] = ''
        value = data_cols[0]
        item = QtWidgets.QTableWidgetItem(value)
        self.setItem(row, 0, item)  # 设置i行0列的内容为Value
        for i in range(1, count):
            if data_cols[i] is None:
                data_cols[i] = ''
            item = QtWidgets.QTableWidgetItem(data_cols[i])
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.setItem(row, i, item)  # 设置row行i列的内容为 Value
        self.setCellWidget(row, 6, self.createWidget())  # 添加最后的控件组

    def update_row(self, row, data_cols=None, isNew=False):
        """
        更新或插入一行数据
        :param row: 行序号
        :param data_cols: 列数据的列表
        :param isNew: 新建行
        :return:
        """
        if data_cols is None:
            return
        if row > self.rowCount():
            row = self.rowCount()
            isNew = True
        if row < 0:
            row = 0
            isNew = True
        if isNew:
            self.insertRow(row)  # 中间插入一行
            self.data.insert(row, data_cols)

        self._write_cols(row, data_cols)

    def delete_row(self, row):
        if not 0 <= row < self.rowCount():
            return

        self.removeRow(row)  # 删除 row行
        if row < len(self.data):
            del (self.data[row])  # 删除对应数据

    def slot_HorSectionClicked(self, index):
        if index == 0:
            # if not self.flag_sort:
            self.data.reverse()
            # self.flag_sort = bool(1 - self.flag_sort)

            # self.update_data(self.createDate(self.src_files), False)
            self.update_table()

    def dropMimeData(self, row, col, mimeData, action):
        """dropMimeData
        复写此方法以获取要插入的行的索引
        Arguments:
            row {int} -- 所在行的索引
            col {int} -- 所在列的索引
            mimeData {str} -- mimeData
            action {str} -- action
        Returns:
            bool -- 操作成功与否
        """
        self.last_drop_row = row
        return True

    def dropEvent(self, event):
        """dropEvent
        拖放的放事件
        Arguments:
            event {object} -- 事件对象
        """
        # 将从中移动所选行的QTableWidget
        sender = event.source()
        # 默认dropEvent方法触发带有参数的dropMimeData(我们感兴趣的是行索引)。
        super().dropEvent(event)
        # 现在我们直到要在哪里插入所选的行了
        dropRow = self.last_drop_row
        selectedRows = sender.getselectedRowsFast()

        # 分配传送所需的空间
        for _ in selectedRows:
            self.insertRow(dropRow)

        # 如果发送者和接收者是同一个,那么,在创建新的空行之后，所选的行可能会更改它们的位置
        sel_rows_offsets = [0 if self != sender or srow < dropRow else len(
            selectedRows) for srow in selectedRows]
        selectedRows = [row + offset for row,
                                         offset in zip(selectedRows, sel_rows_offsets)]

        # 复制所选的行的内容到空行中
        for i, srow in enumerate(selectedRows):
            for j in range(self.columnCount()):
                item = sender.item(srow, j)
                if item:
                    source = QtWidgets.QTableWidgetItem(item)
                    self.setItem(dropRow + i, j, source)
        # 删除所选的行
        for srow in reversed(selectedRows):
            sender.removeRow(srow)

        event.accept()

    def getselectedRowsFast(self):
        selectedRows = []
        for item in self.selectedItems():
            if item.row() not in selectedRows:
                selectedRows.append(item.row())
        selectedRows.sort()
        return selectedRows

    # region string 中包含数字，根据数字排序
    ''' python list sort中string 中包含数字，根据数字排序 '''
    @staticmethod
    def _alphanum_key(s):
        """ Turn a string into a list of string and number chunks.
            "z23a" -> ["z", 23, "a"]
        """
        return [Utils.tryint(c) for c in re.split('([0-9]+)', s[0])]

    @staticmethod
    def _sort_nicely(l):
        """ Sort the given list in the way that humans expect.
        """
        if isinstance(l, list):
            l.sort(key=CustTableWidget._alphanum_key)
    # endregion


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        # TODO 修改原始控件

    def resizeEvent(self, event):
        palette = QtGui.QPalette()
        pix = QtGui.QPixmap('res/images/background.jpg')
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(palette)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
