#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @项目名称: python
# @File    : Utilities.py
# @Time    : 2019/12/30 23:22
# @Author  : big
# @Email   : shdorado@126.com

import os
import sys
import re
import psutil

import ctypes
from ctypes.wintypes import HWND, DWORD

import win32api
import win32com
import win32con
import win32gui

from win32com.client import constants, gencache, Dispatch, DispatchEx
from PyPDF4 import PdfFileReader, PdfFileWriter

import copy
import docx
import json
import random
import array
import string
import time
import uuid

# import cv2
from PIL import Image, ImageStat, ImageEnhance, ImageQt, ImageFilter
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import functools

import cgitb  # 相当管用

cgitb.enable(format='text')  # 解决 pyqt5 异常只要进入事件循环,程序就崩溃,而没有任何提示


class AllData(object):
    def __init__(self, parent=None):
        self.users_name = ['cyh', 'ganmin']
        self.users_pwd = {'cyh': ['pwd1=agcg', 'pwd2=gwtsd'], 'ganmin': ['dddd']}
        '''库数据-类别-网站-账户-细节'''
        self.vault_data = []
        self.data_unit = [[0, 'res/cross.png', '默认/登录'],
                          [1, 'res/flower.png', '默认/信任卡'],
                          [2, 'res/flower.png', '默认/身份'],
                          [3, 'res/flower.png', '默认/备注'],
                          [4, 'res/flower.png', '默认/密码'],
                          [5, 'res/flower.png', '默认/许可证'],
                          [6, 'res/flower.png', '默认/财务'],
                          [7, 'res/flower.png', '默认/旅游'],
                          [8, 'res/flower.png', '默认/电脑'],
                          [9, 'res/flower.png', '默认/杂项'],
                          [10, ['', '百度网盘', -1, False, 'res/cross.png'], ['账户', '', 2, False, ''],
                           ['密码', '', 0, True, ''],
                           ['邮箱', None, 2, False, ''], ['手机', None, 3, False, ''],
                           ['url', 'https://www.baidu.com', 2, False, '']],
                          [11, 'res/cross.png', '网易邮箱'],
                          [12, 'res/cross.png', '微博'],
                          [13, 'res/cross.png', '工行'],
                          [14, 'res/cross.png', 'QQ'],
                          [15, 'res/cross.png', '微信']]  # 模板，常用网站的信息
        """ mold: 0=标题 1=普通3个控件 2=分段 3=密码复合区 4=密码保护复合区 5=底部复合区
        """
        self.data_family = [['res/flower.png', '登录', [0, 10, 14]],  # 模板序号
                            ['res/flower.png', '信任卡', [1, 12]],
                            ['res/flower.png', '身份', [2]],
                            ['res/flower.png', '备注', [3]],
                            ['res/flower.png', '密码', [4]],
                            ['res/flower.png', '许可证', [5]],
                            ['res/flower.png', '财务', [6]],
                            ['res/flower.png', '旅游', [7]],
                            ['res/flower.png', '电脑', [8]],
                            ['res/flower.png', '杂项', [9]]]  # 类别
        self.field_style = ['密码', '支付密码', '文字', '用户名', 'URL', '电话', '电邮', 'PIN码', '数字', '日期', 'TOTP', '多行',
                            '持卡人姓名', '卡号', 'CVC', '卡PIN码', '有效日期', '银行名称', '卡类型', '有效自']
        self.data_cards = [
            [[1, '百度网盘', -1, None, 'res/cross.png'], ['账户', '', 2, False, None], ['密码', '', 0, True, None],
             ['邮箱', None, 6, False, None], ['手机', None, 5, False, None],
             ['其他详细信息', None, -2, None, None], ['标签', '', -3, '备注', '']],
            [[4, '工行', -1, None, 'res/cross.png'], ['账户', '', 2, False, None], ['密码', '', 0, True, None],
             ['邮箱', None, 6, False, None], ['手机', None, 5, False, ''], ['标签', '', -3, '备注', '']],
            [[1, '网易邮箱', -1, None, 'res/cross.png'], ['账户', '', 2, False, None], ['密码', '', 0, True, None],
             ['标签', '', -3, '备注', '']],  # 第一个数字是家庭/类别的代号，最后一项必须是标签和备注的混合体
            [[1, '微信', -1, None, 'res/cross.png'], ['账户', '', 2, False, None], ['密码', '', 0, True, None],
             ['邮箱', None, 6, False, None], ['标签', '', -3, '备注', '']]]  # 详情卡片
        self.cur_card = 0
        self.favorites = []  # 保存收藏夹各项在cards里的序号


# class MyEncoder(json.JSONEncoder):
#     def default(self, obj):
#         """
#         只要检查到了是bytes等特殊类型的数据就把它转为str类型
#         :param obj:
#         :return:
#         """
#         from datetime import date, datetime, time
#         if isinstance(obj, int):
#             return int(obj)
#         elif isinstance(obj, float):
#             return float(obj)
#         elif isinstance(obj, bytes):
#             # return str(obj, encoding='utf-8')
#             return str(obj, encoding='ISO-8859-1')
#         elif isinstance(obj, time):
#             return obj.__str__()
#         elif isinstance(obj, datetime):
#             return obj.strftime('%Y-%m-%d %H:%M:%S')
#         elif isinstance(obj, date):
#             return obj.strftime('%Y-%m-%d')
#         else:
#             return json.JSONEncoder.default(self, obj)
class MyJson(object):
    # data = [{'a': '中国'}, {'c': 'ddd'}, {'e': 'fff'}]

    def __init__(self, *args, **kwargs):
        super(MyJson, self).__init__(*args, **kwargs)

    @staticmethod
    def read(file):
        # json文件的读入
        if not os.path.exists(file):
            print('read error：json文件不存在')
            return None
        with open(file, 'r', errors='ignore')as f:
            data = json.load(f)  # data是字典等原型
            # data = f.read()  # data是字符串
            # print(type(data), data, 'dg')
            # self.data = pickle.load(f)
            # self.data = json.loads(data)  # 把字符串变成字典等原型
            # print(type(self.data), self.data)
            return data

    @staticmethod
    def write(data, file):
        # 以json格式写入文件
        path, _ = os.path.split(file)
        if not os.path.exists(path):
            os.makedirs(path)  # 创建多级目录
        if os.path.exists(file):
            os.remove(file)
        fd = open(file, mode="w", encoding="utf-8")  # 无文件时创建
        fd.close()
        j_data = json.dumps(data, sort_keys=True,  # 先dumps打包成字典,再写入
                            indent=4, separators=(',', ': '),  # 数据格式化输出
                            ensure_ascii=False)  # 默认为True，会将中文编码成ascii
        with open(file, "w", ) as file:
            file.write(j_data)  # json
            # json.dump(j_data, file)  # assic码
            # pickle.dump(data, file, 0) #

    def __str__(self):
        return "json文件读写"

    __repr__ = __str__


# 图片类型的相互转换
class ImageConvert:

    @staticmethod
    def alpha2white_opencv2(imgfile):
        """
        将图片透明背景转换成白色背景-opencv2实现
        :return:
        """
        try:
            img = cv2.imread(imgfile, -1)
            img_copy = img.copy()  # 注意：这里copy()，避免覆盖原img

            sp = img_copy.shape
            width = sp[0]
            height = sp[1]
            for yh in range(height):
                for xw in range(width):
                    color_d = img[xw, yh]
                    if color_d[3] == 0:
                        img[xw, yh] = [229, 229, 229, 255]

            cv2.imwrite("./res/img_match/Mask.png", img)
            # cv2.imshow("after", img)
            # cv2.waitKey(0)
            return img
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def alphabg2white_PIL(imgfile):
        """
        将图片透明背景转换成白色背景-PIL实现
        :param imgfile:
        :return:
        """
        try:
            img = Image.open(imgfile)
            img = img.convert('RGBA')
            sp = img.size
            width = sp[0]
            height = sp[1]
            # print(sp)
            for yh in range(height):
                for xw in range(width):
                    dot = (xw, yh)
                    color_d = img.getpixel(dot)
                    if color_d[3] == 0:
                        color_d = (255, 255, 255, 255)
                        img.putpixel(dot, color_d)
            # img.show()
            return img
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def qtpixmap_to_cvimg(qtpixmap):
        """
        QPixmap转opencv
        :param qtpixmap:
        :return:
        """
        qimg = qtpixmap.toImage()
        temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
        temp_shape += (4,)
        ptr = qimg.bits()
        ptr.setsize(qimg.byteCount())
        result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
        result = result[..., :3]

        return result

    @staticmethod
    def cvimg_to_qtimg(cvimg):
        """
        opencv转QImage
        :param cvimg:
        :return:
        """
        imgDown = np.float32(cvimg)
        height, width, depth = imgDown.shape
        bytesPerLine = 3 * width
        cvimg = cv2.cvtColor(imgDown, cv2.COLOR_BGR2RGB)
        tempImage = QtGui.QImage(cvimg.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        # print(type(tempImage))
        # tempImage = QtGui.QPixmap.toImage()  # QPixmap->QImage
        tempPixmap = QtGui.QPixmap.fromImage(tempImage)  # QImage->QPixmap
        # tempPixmap = QtGui.QPixmap(tempImage)
        # print(type(tempPixmap))

        return tempPixmap

    # Qpixmap -> Qimage
    @staticmethod
    def get_QImage_QPixmap(img: QtGui.QPixmap):
        return img.toImage()
        # painter.drawImage(0, 0, image)

    # Qimage -> Qpixmap
    @staticmethod
    def get_QPixmap_QImage(img: QtGui.QImage):
        return QtGui.QPixmap.fromImage(img)
        # painter.drawPixmap(0, 0, pixtemp)

    # QImage 转 Image
    @staticmethod
    def get_QImage_Image(img: QtGui.QImage):
        return ImageQt.fromqimage(img)

    # Image 转 QImage
    @staticmethod
    def get_QImage_Image(img: Image):
        return ImageQt.ImageQt(img)

    # QPixmap 格式转 PIL 格式
    @staticmethod
    def pixmap2pil(pixmap: QtGui.QPixmap):
        # print("QPixmap格式转PIL格式")
        return ImageQt.fromqpixmap(pixmap)

    # PIL 格式转 QPixmap 格式
    @staticmethod
    def pil2pixmap(pil_img: Image):
        # print("PIL格式转 QPixmap 格式")
        return ImageQt.toqpixmap(pil_img)
        # return QtGui.QPixmap.fromImage(ImageQt(pil_img))

    # jpg格式:是有损图片压缩类型,可用最少的磁盘空间得到较好的图像质量
    # png格式:不是压缩性,能保存透明等图
    @staticmethod
    def png_jpg(file_png, file_jpg, scale=1.0):
        img = Image.open(file_png)
        width = int(img.size[0] * scale)
        height = int(img.size[1] * scale)
        # f_type = img.format
        # print(type(f_type), f_type)
        img = img.resize((width, height), Image.ANTIALIAS)
        # 第二个参数：
        # Image.NEAREST ：低质量
        # Image.BILINEAR：双线性
        # Image.BICUBIC ：三次样条插值
        # Image.ANTIALIAS：高质量

        try:
            if len(img.split()) == 4:
                # prevent IOError: cannot write mode RGBA as BMP
                r, g, b, a = img.split()
                img = Image.merge("RGB", (r, g, b))
                img.convert('RGB').save(file_jpg, quality=100)
                # os.remove(file_png)
            else:
                img.convert('RGB').save(file_jpg, quality=100)
                # os.remove(PngPath)

        except Exception as e:
            print("PNG转换JPG 错误", e)

    def __init__(self):
        pass

    def __str__(self):
        return '图片类型转换类'

    __repr__ = __str__


class BackLabel(QtWidgets.QLabel):
    """
        label作为底图，应该是父窗体win中的第一个控件，否则覆盖前面控件，
        label跟窗口一样大小，且不加入窗口布局。
        在父窗口的 resize event 里调用 update

        :param img_file: 底图文件
        :param flag_show:
            0-默认方式，图片适应窗口，任意伸缩
            1-图片按比例显示全宽或全高，无空白，且显示图片中心
            2-图片按比例全部显示在窗口里，会留空白
            （后面的必须放在主窗体开始调用，窗口应固定大小 不能改变)
            2-保持窗口宽度不变，根据图片调整窗口高度，保证图片全景显示
            3-保持窗口高度不变，根据图片调整窗口宽度，保证图片全景显示
            4-根据图片宽高按比例调整窗体宽高，保证图片全景显示，需系数
        :param scale: 系数
    """

    def __init__(self, parent, img_file, radius=20, margin=0, flag_show=1):
        super(BackLabel, self).__init__(parent)
        self.parent = parent
        self.img_file = img_file
        self.flag_show = flag_show  # 图片显示方式
        self.radius = radius  # 圆角半径
        self.margin = margin  # 边框距离
        self.pix = None

        self.setMouseTracking(True)
        # self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)  # 设置鼠标穿透
        # Utils.set_effect(self, 0, 10, QtWidgets.QGraphicsBlurEffect.QualityHint)
        # Utils.set_effect(self, 2, 0.9)
        # Utils.set_effect(self, 3, QtGui.QColor(0, 229, 0, 100), 5.0)
        Utils.set_effect(self, 1, 20, 5, 5, QtGui.QColor(0, 0, 0, 200))

        # self.setStyleSheet('border-radius:15px;     /*画出圆角*/'
        #                    '/* background-color: skyblue;  */'
        #                    'background-image:url(./res/background/bk5.jpg);  /* */')
        # self.setAlignment(Qt.AlignCenter)

    def update(self, is_max=False):
        # self.setGeometry(0, 0, self.parent.width() - 2 * self.margin, self.parent.height() - 2 * self.margin)
        if is_max:  # 窗口最大化了
            self.resize(self.parent.width(), self.parent.height())
        else:
            self.resize(self.parent.width() - self.margin, self.parent.height() - self.margin)

        if self.flag_show == 0:
            self.setScaledContents(True)
            self.pix = QtGui.QPixmap(self.img_file)
        elif self.flag_show == 1:
            self.pix = Utils.img_center(self.width(), self.height(), self.img_file, None, 1)
        elif self.flag_show == 2:
            self.pix = Utils.img_center(self.width(), self.height(), self.img_file, None, 0)

        super(BackLabel, self).update()

    def paintEvent(self, event):
        # # 主窗体无边框时是加载不了样式的，仅在子控件上实现样式。
        # # 要在主窗体本身实现样式，需要在paintEvent事件中加上如下代码，设置底图也是一样的
        # opt = QStyleOption()
        # opt.initFrom(self)
        # p = QPainter(self)
        # p.setRenderHint(QPainter.Antialiasing)  # 反锯齿
        # self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
        # # super(Canvas, self).paintEvent(event)

        # 不通过样式，直接设置圆角，通用，且不继承于子控件
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)  # 反锯齿

        # 显示全图充满
        if self.pix:
            painter.setBrush(QtGui.QBrush(self.pix))  # 设置底图的方式之一
        # painter.setBrush(QBrush(Qt.blue))
        painter.setPen(QtCore.Qt.transparent)

        rect = self.rect()
        rect.setWidth(rect.width() - 1)
        rect.setHeight(rect.height() - 1)
        painter.drawRoundedRect(rect, self.radius, self.radius)

        # 也可用QPainterPath 绘制代替 painter.drawRoundedRect(rect, 15, 15)
        # painterPath= QPainterPath()
        # painterPath.addRoundedRect(rect, 15, 15)
        # painter.drawPath(painterPath)

        # 直接设置底图，与圆角的画刷设置不能同时
        # pix = QPixmap('./res/images/background11.jpg')
        # painter.drawPixmap(self.rect(), pix)

        super(BackLabel, self).paintEvent(event)

    def __str__(self):
        return '可以作为窗体的背景，可以设置图片、底色、圆角、模糊化等特效'

    __repr__ = __str__


class FileButler(object):
    def __init__(self, *args, **kwargs):
        super(FileButler, self).__init__(*args, **kwargs)

    def __str__(self):
        return '文件大管家'

    __repr__ = __str__

    # 合并同一目录下的所有PDF文件
    @staticmethod
    def merge_pdf(pdf_dir, outfile):
        if not pdf_dir:
            return

        output = PdfFileWriter()
        outputPages = 0
        pdf_files = Utils.files_in_dir(pdf_dir, ['.pdf'], True)

        if pdf_files:
            Utils.sort_nicely(pdf_files)

            for each in pdf_files:
                print("路径：%s" % each)

                # 读取源PDF文件
                input = PdfFileReader(open(each, "rb"))

                # 获得源PDF文件中页面总数
                pageCount = input.getNumPages()
                outputPages += pageCount
                print("页数：%d" % pageCount)

                # 分别将page添加到输出output中
                for iPage in range(pageCount):
                    output.addPage(input.getPage(iPage))

            print("合并后的总页数:%d." % outputPages)
            # 写入到目标PDF文件
            outputStream = open('/'.join([pdf_dir, outfile]), "wb")
            output.write(outputStream)
            outputStream.close()
            print("PDF文件合并完成！")

        else:
            print("没有可以合并的PDF文件！")

    # word 转 pdf
    @staticmethod
    def word2pdf(word_path, pdf_path):
        """
        word转pdf
        :param word_path: word文件路径
        :param pdf_path:  生成pdf文件路径
        """
        # w = Dispatch("Word.Application")
        # try:
        #     # w.Visible = Debug
        #     doc = w.Documents.Open(input, ReadOnly=1)
        #     doc.ExportAsFixedFormat(pdfPath, constants.wdExportFormatPDF,
        #                             Item=constants.wdExportDocumentWithMarkup,
        #                             CreateBookmarks=constants.wdExportCreateHeadingBookmarks)
        #     return 0
        # except:
        #     return 1
        # finally:
        #     w.Quit(constants.wdDoNotSaveChanges)

        # 打开word软件

        # 必须把路径中的 / 换成\\，否则容易出错
        word_path = word_path.replace('/', '\\')
        pdf_path = pdf_path.replace('/', '\\')
        name, ext = os.path.splitext(word_path)

        if ext == '.doc':
            name = f'{word_path}x'
            # print(word_path, '\n', name)

            FileButler.doc_docx(word_path, name)
            word_path = name

        word = gencache.EnsureDispatch('Word.Application')
        # 非可视化运行
        word.Visible = False
        doc = word.Documents.Open(word_path, ReadOnly=1)

        doc.ExportAsFixedFormat(pdf_path,
                                constants.wdExportFormatPDF,
                                Item=constants.wdExportDocumentWithMarkup,
                                CreateBookmarks=constants.wdExportCreateHeadingBookmarks)
        # doc.Close() # 每次都要弹窗保存框
        word.Quit(constants.wdDoNotSaveChanges)

    @staticmethod
    def doc2docx(src_doc, dst_docx):
        # print(src_doc)  # 路径要用\\,不要用/
        word = Dispatch('Word.Application')
        doc = word.Documents.Open(src_doc, ReadOnly=1)  # 目标路径下的文件
        doc.SaveAs(dst_docx, 12, False, "", True, "", False, False, False, False)  # 转化后路径下的文件
        doc.Close()
        word.Quit()

    @staticmethod
    def doc_docx(src_doc, dst_docx):
        # w = client.Dispatch('Word.Application')
        # 或者使用下面的方法，使用启动独立的进程：
        w = DispatchEx('Word.Application')
        doc = w.Documents.Open(src_doc)
        doc.SaveAs(dst_docx, 16)  # 必须有参数16，否则会出错. #参数16，表示将doc转成docx
        doc.Close()
        w.Quit()


class Utils(object):
    def __init__(self):
        pass

    @staticmethod
    def call_dll(win):
        # 调用 api
        hWnd = HWND(int(win.winId()))  # 直接HWND(self.winId())会报错
        gradientColor = DWORD(0x50F2F2F2)  # 设置和亚克力效果相叠加的背景颜色

        dll_file = r'E:/Neworld/res/dll/acrylic.dll'
        # ctypes.cdll.LoadLibrary(dll_file)

        dll = ctypes.cdll.LoadLibrary(dll_file)
        # dll = ctypes.windll.LoadLibrary(dll_file)
        dll.setBlur(hWnd, gradientColor)

        # # dll 是 __stdcall 格式的调用时
        # dll = ctypes.windll.LoadLibrary('test.dll')
        # dll = ctypes.WinDLL(dll_file)

        # # dll 是 __cdecl 格式的调用时：
        # dll = ctypes.cdll.LoadLibrary('test.dll')
        # dll = ctypes.CDLL(dll_file)

        print(type(dll))
        # dll.setBlur(hWnd, gradientColor)

    # 显示图片中心或显示全部
    @staticmethod
    def img_center(w_win, h_win, img_file, save_file=None, flag=1) -> QtGui.QPixmap:
        """
        以图片中心充满窗口
        :param w_win:
        :param h_win:
        :param img_file:
        :param save_file: 可以保存到文件中
        :param flag: 0-图片全部显示，有空白；1-图片中心尽量全部显示，无空白
        :return: 文件或 pix， 也可以换其他格式
        """
        if not os.path.isfile(img_file):
            return QtGui.QPixmap()

        img = Image.open(img_file)

        h_img = img.size[1]  # 图片高度
        w_img = img.size[0]  # 图片宽度

        ratio_w = w_img / w_win
        ratio_h = h_img / h_win

        # 开始截取
        region = None
        new_img = None
        if ratio_w < ratio_h:
            if flag == 0:
                img.thumbnail((w_win, h_win))  # 只能缩小自身,且按大值作为长宽统一比例
                new_img = img  # .resize((int(w_img / ratio_h), h_win), Image.BILINEAR)  # 默认缩放NEARESET
            elif flag == 1:
                region = img.resize((w_win, int(h_img / ratio_w)), Image.NEAREST)
                new_img = region.crop([
                    0, (region.size[1] - h_win) // 2,  # 左上角
                    w_win, (region.size[1] - h_win) // 2 + h_win])  # 右下角
        else:
            if flag == 0:
                img.thumbnail((w_win, h_win))  # 只能缩小自身,且按大值作为长宽统一比例
                new_img = img  # .resize((w_win, int(h_img / ratio_w)))  # 缩放
            elif flag == 1:
                region = img.resize((int(w_img / ratio_h), h_win))
                new_img = region.crop([
                    (region.size[0] - w_win) // 2, 0,  # 左上角
                    (region.size[0] - w_win) // 2 + w_win, 0 + h_win])  # 右下角

        # 2. 对图片进行模糊效果
        # for i in range(5):
        #     new_img = new_img.filter(ImageFilter.BLUR)
        # print('heree')

        if save_file:
            new_img.save("test.jpg")  # 保存图片
            return QtGui.QPixmap()
        else:
            return ImageConvert.pil2pixmap(new_img)

    # 为窗体、控件设置背景图片，可伸缩
    @staticmethod
    def setBg(win, label: QtWidgets.QLabel, img_file, flag_show=1, scale=1):
        """
            label作为底图，应该是父窗体win中的第一个控件，否则覆盖前面控件，
            因为label跟窗口一样大小，且不加入窗口布局。
            函数要在 resize event 的最后调用
            :param win: 父窗体
            :param label: 底图载体
            :param img_file: 底图文件
            :param flag_show:
                        0-默认方式，图片适应窗口，任意伸缩
                        1-图片按比例显示全宽或全高，无空白，且显示图片中心
                        2-图片按比例全部显示在窗口里，会留空白
                        （后面的必须放在主窗体开始调用，窗口应固定大小 不能改变)
                        2-保持窗口宽度不变，根据图片调整窗口高度，保证图片全景显示
                        3-保持窗口高度不变，根据图片调整窗口宽度，保证图片全景显示
                        4-根据图片宽高按比例调整窗体宽高，保证图片全景显示，需系数
            :param scale: 系数
            :return:
        """

        # label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)  # 设置鼠标穿透
        label.resize(win.width(), win.height())

        pix = None
        if flag_show == 0:
            label.setScaledContents(True)
            pix = QtGui.QPixmap(img_file)
        elif flag_show == 1:
            pix = Utils.img_center(label.width(), label.height(), img_file, None, 1)
        elif flag_show == 2:
            pix = Utils.img_center(label.width(), label.height(), img_file, None, 0)

        label.setPixmap(pix)

    # 给窗体产生特效
    @staticmethod
    def set_effect(*args):
        """
        使用 QGraphicsEffect 产生三大特效
        :param args: 需要特效的窗体、特效类型、特效参数等
        :return:
        """

        if not args or not isinstance(args[0], object):
            return

        effect = None

        if args[1] == 0:  # 模糊特效
            effect = QtWidgets.QGraphicsBlurEffect()  # 虚化
            # m_pBlurEffect = QGraphicsBlurEffect()
            effect.setBlurRadius(args[2])  # 设置模糊半径，半径越大，模糊效果越明显，默认为5
            effect.setBlurHints(args[3])
            # 设置模糊质量 参数如下：
            # PerformanceHint = 0 表明渲染性能是最重要的因素，但可能会降低渲染质量。（默认参数）
            # QualityHint = 1 表明渲染质量是最重要的因素，但潜在的代价是降低性能。
            # AnimationHint = 2 表示模糊半径将是动画的，暗示实现可以保留一个源的模糊路径缓存。如果源要动态更改，则不要使用此提示。
        elif args[1] == 1:  # 阴影特效
            effect = QtWidgets.QGraphicsDropShadowEffect()  # 阴影
            effect.setBlurRadius(args[2])  # 阴影半径，虚化程度，不能大于圆角半径
            effect.setOffset(args[3], args[4])  # 阴影宽度
            effect.setColor(args[5])  # 阴影颜色
            # widget.setContentsMargins(50, 50, 50, 50) # 父窗口要留显示阴影的边距

        elif args[1] == 2:  # 透明特效,可以部分透明
            effect = QtWidgets.QGraphicsOpacityEffect()  # 透明
            effect.setOpacity(args[2])  # 透明度 0-1.0
            # 你的控件.setGraphicsEffect(op)
            # 你的控件.setAutoFillBackground(True)

        elif args[1] == 3:  # 着色效果
            effect = QtWidgets.QGraphicsColorizeEffect()
            effect.setColor(args[2])  # 设定颜色
            effect.setStrength(args[3])  # 着色强度

        elif args[1] == 4:  # 阴影 + 模糊
            effect1 = QtWidgets.QGraphicsBlurEffect()
            effect2 = QtWidgets.QGraphicsDropShadowEffect()

        else:
            return

        args[0].setGraphicsEffect(effect)

    # 语言国际化
    @staticmethod
    def tr(msg):
        return QtCore.QCoreApplication.translate("@default", msg)

    # 获取大小写字母、数字、特殊字符等可见字符的列表
    @staticmethod
    def get_chars(mold=5):
        """
        # 0～31及127(共33个)是控制字符或通信专用字符（其余为可显示字符）
        # 32～126(共95个)是字符(32是空格），
        # 其中48～57为0到9十个阿拉伯数字。
        # 65～90为26个大写英文字母，
        # 97～122号为26个小写英文字母。
        # 其他为特殊字符，33个 special_
        mold:类型，1：大小字母集 2：小写字母集 3：大小写字母集 4：数字集
                    5：字母+数字 6：特殊字符集 7：所有可见字符集(前6项)
        """

        char_list = []
        if mold == 1:
            char_list = string.ascii_uppercase
        elif mold == 2:
            char_list = string.ascii_lowercase
        elif mold == 3:
            char_list = string.ascii_letters
        elif mold == 4:
            char_list = string.digits
        elif mold == 5:
            char_list = string.ascii_letters + string.digits
        else:
            for i in range(32, 48):
                char_list.append(chr(i))
            for i in range(58, 65):
                char_list.append(chr(i))
            for i in range(91, 97):
                char_list.append(chr(i))
            for i in range(123, 127):
                char_list.append(chr(i))

            if mold != 6:  # not special only
                char_list.extend(string.ascii_letters + string.digits)

        # print(len(char_list), char_list)
        return char_list

    @staticmethod
    def swaps(a, b):
        # a ^= b
        # b ^= a
        # a ^= b
        a, b = b, a
        return a, b

    @staticmethod
    def rand_int(num_min, num_max):
        seed = time.time()
        sr = random.SystemRandom(seed)
        # print(type(sr))

        ret = sr.randint(num_min, num_max)
        # print(ret)

        return ret

    @staticmethod
    # 字符串是否合法的PIN码
    def validate_pin(pin):
        return len(pin) in (4, 6) and pin.isdigit()
        # return len(pin) in (4, 6) and pin.isnumeric()

    @staticmethod
    def get_pin(arr=[1, 2, 3, 5, 4, 6], mold=1):
        if mold == 1:  # 数字
            # 方法baidu1用数学方法计算出结果
            return functools.reduce(lambda x, y: x * 10 + y, arr)
            # 方法2用字符串合并出zhi结果
            # return int(functools.reduce(lambda x, y: str(x) + str(y), arr))
        else:  # 下面是字符串
            return str(arr).replace("[", "").replace("]", "").replace(",", "").replace(" ", "")

    @staticmethod
    def rand_float(num_min, num_max, n=2):
        # 小数位数
        seed = time.time()
        sr = random.SystemRandom(seed)
        # print(type(sr))

        ret = sr.uniform(num_min, num_max)
        # ret = sr.random()

        ret = round(ret, n)  # n位小数，碰到.5，前一位小数是奇数，则直接舍弃，如果偶数则向上取舍
        # print('{:04.2f}'.format(sr.random()))

        return ret

    # 生成随机字符串 密码学意义上更加安全的版本
    @staticmethod
    def rand_str(char_set=string.ascii_letters + string.digits, size=10):
        print(char_set)  # 将大/小写的ASCII字符列表和数字组合起来

        seed = time.time()
        sr = random.SystemRandom(seed)
        # print(type(sr), sr.choice(char_set))
        # print(type(sr.choice(char_set) for _ in range(size)))
        # return
        random_string = ''.join(sr.choice(char_set) for _ in range(size))

        # 首字母不能是数字
        random_string = Utils.rand_str(size) if random_string[0].isdigit() else random_string
        # print(random_string)

        return random_string

    # 使用Python内置的uuid库 生成随机字符串
    @staticmethod
    def rand_str2(size=10):
        random_string = str(uuid.uuid4()).replace("-", "")  # Remove the UUID '-'
        size = len(random_string) if size > len(random_string) else size
        random_string = random_string[0:size]
        print(type(random_string))

        # 首字母不能是数字
        random_string = Utils.rand_str2(size) if random_string[0].isdigit() else random_string
        print(random_string)

        return random_string

    @staticmethod
    def readQss(style_file):
        """读取qss文件"""
        with open(style_file, 'r') as f:
            return f.read()

    @staticmethod
    def elideText(strInfo, width, font):
        """长字符串省略表示法"""
        """font: 显示的字体
           width: 显示的长度限制
           strInfo: 原始的长字符串
           return: 带省略号的字符串
        """
        try:
            fontMetrics = QtGui.QFontMetrics(font)
            # 如果当前字体下，字符串长度大于指定宽度
            if fontMetrics.width(strInfo) > width:
                strInfo = fontMetrics.elidedText(strInfo, QtCore.Qt.ElideRight, width)
        except Exception as e:
            print(e)
        finally:
            return strInfo

    @staticmethod
    def getSubStr(longStr, max_width=15, font=QtGui.QFont('微软雅黑', 12)):
        """截取字符串中间用省略号显示"""
        try:
            assert isinstance(longStr, str)

            fontMetrics = QtGui.QFontMetrics(font)
            char_width = fontMetrics.width('a')
            max_len = int(max_width / char_width)
            # 如果当前字体下，字符串长度大于指定宽度
            # if fontMetrics.width(longStr) > max_width:
            if len(longStr) > max_len:
                # subStr1 = longStr[0:10]
                # subStr2 = longStr[-5:]
                subStr1 = longStr[0:int(max_len / 2) - 3 * char_width]
                subStr2 = longStr[-int(max_len / 2) + 3 * char_width:]
                subStr = subStr1 + "..." + subStr2
                return subStr
            else:
                return longStr
        except Exception as e:
            print(e)
            return longStr

    @staticmethod
    def getSubStr1(longStr):
        """截取字符串中间用省略号显示"""
        assert isinstance(longStr, str)

        if len(longStr) > 15:
            subStr1 = longStr[0:10]
            subStr2 = longStr[-5:]
            subStr = subStr1 + "..." + subStr2
            return subStr
        else:
            return longStr

    @staticmethod
    def doAnim(widget, started=True):
        """窗体移动/缩放动画"""
        if widget:
            animation = QtCore.QPropertyAnimation(widget, b"geometry", widget)
            animation.setDuration(300)
            sp = widget.geometry()
            if started:
                ep = QtCore.QRect(sp.x() - sp.width(), sp.y(), sp.width(), sp.height())
            else:
                ep = QtCore.QRect(sp.x() + sp.width(), sp.y(), sp.width(), sp.height())
            animation.setStartValue(sp)
            animation.setEndValue(ep)
            animation.start()
        # ani = QtCore.QPropertyAnimation(self)  # 创建动画对象
        # ani.setTargetObject(self)     # 设置动画目标对象
        # ani.setPropertyName(b'pos')  # 设置动画属性
        # # 注意：字节类型
        # # pos---位置动画---QPoint
        # # size---大小动画---QSize
        # # geometry----位置+大小动画----QRect
        # # windowOpacity---窗口的透明度(0.0是透明的    1.0是不透明)---好像只适合顶层窗口
        # ani.setStartValue(QtCore.QPoint(self.x(), self.y()))  # 设置开始位置---按钮的左上角位置
        # ani.setEndValue(QtCore.QPoint(300, 300))  # 设置结束位置
        # # ani.setStartValue(QSize(0, 0))  # 设置开始大小
        # # ani.setEndValue(QSize(300, 300))  # 设置结束大小
        # # ani.setStartValue(QRect(0, 0,100,100))  # 设置开始位置和大小
        # # ani.setEndValue(QRect(100,100,300, 300))  # 设置结束位置和大小
        # # ani.setStartValue(1)  # 设置开始不透明
        # # ani.setKeyValueAt(0.5,0.2)#在动画的某时间点插入一个值
        # # 参数1 0.0到1.0  0.0表示开始点，1.0表示结束点
        # # 在动画的中间插入透明度0.2
        # # ani.setKeyValueAt(1, 1)  #在动画的结束点是不透明的
        # # ani.setEndValue(0)  # 设置结束透明
        #
        # ani.setDuration(5000)  # 设置动画单次时长---单位毫秒
        # ani.setEasingCurve(QtCore.QEasingCurve.InQuad)  # 设置动画的节奏
        # # # 取值   https://doc.qt.io/qt-5/qeasingcurve.html#Type-enum
        # #
        # ani.start()  # 动画开始---非阻塞
        # ani.setLoopCount(3)  # 设置动画次数---默认1次
        # ani.setDirection(QAbstractAnimation.Forward)  # 设置动画方向
        # # QAbstractAnimation.Backward=1  动画的当前时间随着时间减少（即，从结束/持续时间向0移动）---倒序
        # # QAbstractAnimation.Forward=0 动画的当前时间随着时间而增加（即，从0移动到结束/持续时间）---顺序
        #
        # # 信号
        # ani.currentLoopChanged.connect(self.FF)  # 循环遍数发生变化时
        # # 会向槽函数传递一个参数---当前循环的遍数
        #
        # # directionChanged(QAbstractAnimation.Direction newDirection)   动画方向发生改变时
        # # 会向槽函数传递一个参数---动画新方向
        #
        # ani.finished.connect(self.HH)  # 动画完成时
        #
        # ani.stateChanged.connect(self.GG)  # 状态发生改变时
        # # 会向槽函数传递两个参数---新状态和老状态
        #
        # ani.start()  # 启动动画
        # # 参数 QAbstractAnimation.KeepWhenStopped  停止时不会删除动画
        # #     QAbstractAnimation.DeleteWhenStopped   停止时动画将自动删除

    @staticmethod
    def clear_layout(layout):
        if layout is None:
            AnimWin('no layout')
            return
        # print(f'begin:count={layout.count()}')
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if isinstance(item, QtWidgets.QLayout):
                Utils.clear_layout(item)
            elif isinstance(item, QtWidgets.QSpacerItem):
                # print(item)
                # item = QtWidgets.QSpacerItem()
                item.changeSize(0, 0)
                # item.setGeometry(QtCore.QRect(0, 0, 0, 0))
                # print(type(item.spacerItem()))
            # elif isinstance(item, object):
            else:
                wg = item.widget()
                if wg:
                    wg.setAttribute(QtCore.Qt.WA_DeleteOnClose)
                    # wg.setParent(None)
                    # layout.removeWidget(wg)
                    wg.deleteLater()
            layout.removeItem(item)
        # print(f'end:count={layout.count()}')

    @staticmethod
    def get_version_via_com(filename):  # error
        parser = win32com.client.Dispatch("Scripting.FileSystemObject")
        version = parser.GetFileVersion(filename)
        size = os.path.getsize(filename)
        return version

    @staticmethod
    def getFileVersion(file_name):  # none
        try:
            info = win32api.GetFileVersionInfo(file_name, os.sep)
            ms = info['FileVersionMS']
            ls = info['FileVersionLS']
            version = '%d.%d.%d.%d' % (
                win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.LOWORD(ls))
            return version
        except Exception as e:
            return "None"

    @staticmethod
    def formatTime(localtime):
        """格式化时间的函数"""
        import time
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(localtime))

    @staticmethod
    def formatByte(f_size):
        """格式化文件大小"""
        f_size = round(f_size, 2)  # 首先四舍五入到2位小数
        for (scale, label) in [(1024 * 1024 * 1024, "GB"), (1024 * 1024, "MB"), (1024, "KB")]:
            if f_size >= scale:
                return "%.2f %s" % (f_size * 1.0 / scale, label)
        # 小于1K字节
        return f'{f_size or 0} B'
        # byte = "%.2f" % (f_size or 0)
        # return (byte[:-3] if byte.endswith(".00") else byte) + "字节"

    @staticmethod
    def getFileInfo(filePath):
        # f_size = os.path.getsize(filePath)
        # f_size = f_size / float(1024 * 1024)
        # return round(f_size, 2)

        if not os.path.isfile(filePath):
            return

        file_info = os.stat(filePath)  # 获取文件的基本信息
        info = dict()
        info['完整路径'] = f'{os.path.abspath(filePath)}'
        info['索引号'] = f'{file_info.st_ino}'
        info['设备名'] = f'{file_info.st_dev}'
        info['最后一次的修改时间'] = Utils.formatTime(file_info.st_mtime)
        info['最后一次的状态变化时间'] = Utils.formatTime(file_info.st_ctime)
        info['最后一次的访问时间'] = Utils.formatTime(file_info.st_atime)
        info['文件大小'] = Utils.formatByte(file_info.st_size)

        return info

    @staticmethod
    def _getCompanyNameAndProductName(file_path):
        """
            Read all properties of the given file return them as a dictionary.
        """
        propNames = ('Comments', 'InternalName', 'ProductName',
                     'CompanyName', 'LegalCopyright', 'ProductVersion',
                     'FileDescription', 'LegalTrademarks', 'PrivateBuild',
                     'FileVersion', 'OriginalFilename', 'SpecialBuild')

        props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}

        try:
            # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
            fixedInfo = win32api.GetFileVersionInfo(file_path, '\\')
            props['FixedFileInfo'] = fixedInfo
            props['FileVersion'] = "%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
                                                    fixedInfo['FileVersionMS'] % 65536,
                                                    fixedInfo['FileVersionLS'] / 65536,
                                                    fixedInfo['FileVersionLS'] % 65536)

            # \VarFileInfo\Translation returns list of available (language, codepage)
            # pairs that can be used to retreive string info. We are using only the first pair.
            lang, codepage = win32api.GetFileVersionInfo(file_path, '\\VarFileInfo\\Translation')[0]

            # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
            # two are language/codepage pair returned from above

            strInfo = {}
            for propName in propNames:
                strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
                ## print str_info
                strInfo[propName] = win32api.GetFileVersionInfo(file_path, strInfoPath)

            props['StringFileInfo'] = strInfo
        except Exception as e:
            print(e)

        if not props["StringFileInfo"]:
            return None, None
        else:
            return props["StringFileInfo"]["CompanyName"], props["StringFileInfo"]["ProductName"]

    @staticmethod
    def _get_company_and_product(file_path):
        import pefile
        """ linux系统
            Read all properties of the given file return them as a dictionary.
            @return: a tumple, (company, product)
            """
        mype = pefile.PE(file_path)
        companyName = ""
        productName = ""

        if hasattr(mype, 'VS_VERSIONINFO'):
            if hasattr(mype, 'FileInfo'):
                for entry in mype.FileInfo:
                    if hasattr(entry, 'StringTable'):
                        for st in entry.StringTable:
                            for k, v in st.entries.items():
                                if k == u"CompanyName":
                                    companyName = v
                                elif k == u"ProductName":
                                    productName = v
        if not companyName:
            companyName = None
        if not productName:
            productName = None
        return companyName, productName

    @staticmethod
    def get_file_extension(filename):
        result = None
        if filename:
            result = re.findall(r'\.[^.\\/:*?"<>|\r\n]+$', filename)[0]
        return result

    @staticmethod
    def file_is_given_type(img_filename, file_extension=('.jpg', '.jpeg', '.gif', '.tiff', '.bmp', '.png', '*.xpm')):
        """
        忽略大小写，忽略list还是tuple，判断文件后缀是否在内，后缀最好带上‘，’，以免误判
        :param img_filename: 文件名
        :param file_extension: 文件后缀列表或元祖或字符串或字符
        :return: True or False
        """
        try:
            suffixes = tuple(each.lower() for each in file_extension if isinstance(each, str))
            return img_filename.lower().endswith(suffixes)
        except Exception as e:
            print(f'is_image_file() : {e}')

    @staticmethod
    def files_in_dir(dir_name, suffix_list: list = None, full_path=False):
        '''
        列出目录下指定类型的所有文件
        :param dir_name: 目录名称
        :param suffix_list: 带.号的文件后缀列表
        :param full_path: 文件名带路径或者不含路径
        :return: 文件名称的列表
        '''
        if not dir_name:
            print('null dir')
            return
        if not isinstance(suffix_list, list):
            print('后缀应该存入列表中')

        if not os.path.isdir(dir_name):
            print("it's not a directory")
            return

        list_files = []
        dir_files = os.listdir(dir_name)  # 列出文件夹下所有的目录与文件
        for each in dir_files:
            # path = os.path.join(dir_name, each)  # 构造完整路径
            path = '/'.join([dir_name, each])
            # 判断路径是否是一个文件目录或者文件
            if os.path.isfile(path):
                if not suffix_list:  # 后缀列表空，默认全部文件列出
                    if full_path:
                        list_files.append(path)
                    else:
                        list_files.append(each)
                else:
                    if Utils.file_is_given_type(each, suffix_list):
                        # portion = os.path.splitext(each)  # 分离文件名与扩展名
                        # if portion[1] in suffix_list:
                        if full_path:
                            list_files.append(path)
                        else:
                            list_files.append(each)
            else:
                # print('it is a dir')
                pass

        return list_files

    @staticmethod
    def getFiles(path, suffixes):
        """ 列出目录及子目录下所有的指定类型的文件 """
        return [os.path.join(root, file) for root, dirs, files in os.walk(path)
                for file in files if Utils.file_is_given_type(file, suffixes)]

    @staticmethod
    def cout_list(the_list, indent=False, level=0, fh=sys.stdout):
        """	　　　　　　	　
        函数：print_list()
        功能：打印列表中的数据项，如果子项是列表，则递归打印
        参数：
        　　the_list:  列表
        　　indent:	　 是否开启嵌套打印时缩进显示，默认False表示不开启，即各级显示在同一列
        　　level:	　　控制缩进，如果level为正值，表示一行要增加多少个空格，如果为0，不缩进
        　　fh:　　	　 输出位置，默认为标准输出，即窗口，可以指定输出到文件中。　　
        """
        for item in the_list:
            if isinstance(item, list):  # 判断当前项是不是列表，如果是列表，递归操作
                Utils.cout_list(item, indent, level + 2, fh)  # 如果用++level会有问题
            else:  # 如果是具体的项
                if indent:  # 如果开启缩进
                    for tab_stop in range(level):  # 输出空格
                        print(" ", end='', file=fh)
                print(item, file=fh)

    # @staticmethod
    # def cout_dict(the_dict, json_file):
    #     # stus = {'xiaojun': '123456', 'xiaohei': '7890', 'lrx': '111111'}
    #     res = json.dumps(the_dict, indent=4, ensure_ascii=False, cls=MyEncoder)  # 使用.dumps()方法是要写入
    #     with open(json_file, 'w', encoding='utf8') as f:
    #         # json.dump(the_dict, f)
    #         f.write(res)

    # region string 中包含数字，根据数字排序
    ''' python list sort中string 中包含数字，根据数字排序 '''

    def tryint(c):
        try:
            return int(c)
        except:
            return c

    def alphanum_key(s):
        """ Turn a string into a list of string and number chunks.
            "z23a" -> ["z", 23, "a"]
        """
        return [Utils.tryint(c) for c in re.split('([0-9]+)', s)]

    def sort_nicely(l):
        """ Sort the given list in the way that humans expect.
        """
        if isinstance(l, list):
            l.sort(key=Utils.alphanum_key)

    # endregion

    @staticmethod
    def getDocPageNum(filePath):
        pageNum = 0
        try:
            # 建立ActiveX部件
            word = gencache.EnsureDispatch('Word.Application')
            word.Visible = False
            wrdDocs = word.getProperty("Documents").toDispatch()

            doc = word.Documents.Open(filePath, ReadOnly=1)
            selection = word.Selection()
            pageNum = selection.information(4)

            word.Close(constants.wdDoNotSaveChanges)
            word.Quit(constants.wdDoNotSaveChanges)
            # ActiveXComponent wordCom = new ActiveXComponent("Word.Application");
            # // word应用程序不可见
            # wordCom.setProperty("Visible", false);
            # // 返回wrdCom.Documents的Dispatch
            # Dispatch wrdDocs = wordCom.getProperty("Documents").toDispatch(); // Documents表示word的所有文档窗口（word是多文档应用程序）
            # // 调用wrdCom.Documents.Open方法打开指定的word文档，返回wordDoc
            # Dispatch wordDoc = Dispatch.call(wrdDocs, "Open", filePath, false, true, false).toDispatch();
            # Dispatch selection = Dispatch.get(wordCom, "Selection").toDispatch();
            # pageNum = Integer.parseInt(Dispatch.call(selection, "information", 4).toString()); // 总页数 // 显示修订内容的最终状态
            # // 关闭文档且不保存
            # Dispatch.call(wordDoc, "Close", new Variant(false));
            # // 退出进程对象
            # wordCom.invoke("Quit", new Variant[] {});
        except Exception as e:
            print(e)
        finally:
            return pageNum

    @staticmethod
    def wordinfo(wordPath):
        try:
            # 打开word软件
            word = gencache.EnsureDispatch('Word.Application')
            # 非可视化运行
            word.Visible = False
            doc = word.Documents.Open(wordPath, ReadOnly=1)

            # 下面是取得打开文件的页数
            pages = doc.ComputeStatistics(constants.wdStatisticPages)
            word.Close(constants.wdDoNotSaveChanges)
            word.Quit(constants.wdDoNotSaveChanges)

            return pages
        except Exception as e:
            return -1
        finally:
            return 0

    @staticmethod
    def mergewords(files_list, outfile, ctl_progress=None):
        '''
        合并多个已经排序的word文档
        :param files_list: 已经排序的文件名列表
        :param outfile: 合成后的文件
        :param ctl_progress:
        :return:
        '''

        if not files_list:
            return
        # 打开word软件
        word = gencache.EnsureDispatch('Word.Application')
        # 非可视化运行
        word.Visible = False
        output = word.Documents.Add()  # 新建合并后空白文档

        # 需要合并的文档路径，这里有个文档1.docx，2.docx，3.docx.
        # files = ['F://work//2.docx', 'F://work//1.docx', 'F://work//3.docx']
        Utils.sort_nicely(files_list)  # 按数字大小排序
        files_list.reverse()  # 从后往前插入

        files_weight = []
        if isinstance(ctl_progress, QtWidgets.QProgressBar):
            for file in files_list:
                files_weight.append(Utils.get_FileSize(file))
        print(sum(files_weight))

        for i in range(len(files_list)):
            output.Application.Selection.Range.InsertFile(files_list[i])  # 拼接文档
            if isinstance(ctl_progress, QtWidgets.QProgressBar):
                value = int(sum(files_weight[:i + 1]) / sum(files_weight) * 100)
                # print(value)
                ctl_progress.setValue(value)

        # # 获取合并后文档的内容
        # doc = output.Range(output.Content.Start, output.Content.End)
        # doc.Font.Name = "黑体"  # 设置字体

        output.SaveAs(outfile)  # 保存
        output.Close()

    # 获取CPU信息
    @staticmethod
    def GetCpuInfo():

        cpu_count = psutil.cpu_count(logical=False)  # 1代表单核CPU，2代表双核CPU
        # 获取cpu物理个数    计算方式：单个cpu核数*cpu个数

        xc_count = psutil.cpu_count()  # 线程数，如双核四线程
        # 获取cpu逻辑个数
        # 计算方式：单个cpu核数*cpu个数*2（cpu cores 这个规格值，如果支持并开启ht）
        # ht：intel的超线程技术(HT), 可以在逻辑上再分一倍数量的cpu core出来

        cpu_slv = round((psutil.cpu_percent(1)), 2)  # cpu使用率

        list_cpu = [cpu_count, xc_count, cpu_slv]
        return list_cpu

    # 获取内存信息
    @staticmethod
    def GetMemoryInfo():
        memory = psutil.virtual_memory()
        total_nc = round((float(memory.total) / 1024 / 1024 / 1024), 2)  # 总内存
        used_nc = round((float(memory.used) / 1024 / 1024 / 1024), 2)  # 已用内存
        free_nc = round((float(memory.free) / 1024 / 1024 / 1024), 2)  # 空闲内存
        syl_nc = round((float(memory.used) / float(memory.total) * 100), 2)  # 内存使用率

        ret_list = [total_nc, used_nc, free_nc, syl_nc]
        return ret_list

    # 获取硬盘信息
    @staticmethod
    def GetDiskInfo():
        list_disk = psutil.disk_partitions()  # 磁盘列表
        ilen = len(list_disk)  # 磁盘分区个数
        i = 0
        retlist1 = []
        retlist2 = []
        while i < ilen:
            diskinfo = psutil.disk_usage(list_disk[i].device)
            total_disk = round((float(diskinfo.total) / 1024 / 1024 / 1024), 2)  # 总大小
            used_disk = round((float(diskinfo.used) / 1024 / 1024 / 1024), 2)  # 已用大小
            free_disk = round((float(diskinfo.free) / 1024 / 1024 / 1024), 2)  # 剩余大小
            syl_disk = diskinfo.percent

            retlist1 = [i, list_disk[i].device, total_disk, used_disk, free_disk, syl_disk]  # 序号，磁盘名称，
            retlist2.append(retlist1)
            i = i + 1

        return retlist2

    @staticmethod
    def addTransparency(img_file, factor=0.7):
        img = Image.open(img_file)
        img = img.convert('RGBA')
        img_blender = Image.new('RGBA', img.size, (0, 0, 0, 0))
        img = Image.blend(img_blender, img, factor)
        return img

    @staticmethod
    def bg_trans(save_file: str = None, width=200, height=100, bk_color=(255, 255, 255, 125)):
        """
        创建某种颜色半透明的图片，用于控件的底图，可创造出半透明效果。
        因为 qss不支持背景半透明
        :param save_file: 保存的图片
        :param width:
        :param height:
        :param bk_color:
        :return: 有文件名则 None，无则返回内存中的 pix
        """
        img = Image.new("RGBA", (width, height), bk_color)
        if save_file:
            # 文件不存在则应该强制创造出文件
            # if not os.path.exists(save_file):

            return img.save(save_file, "PNG")  # None
        else:
            return Utils.pil2pix(img)

    @staticmethod
    # PIL Image -> QPixmap
    def pil2pix(im):
        if im.mode == "RGB":
            r, g, b = im.split()
            im = Image.merge("RGB", (b, g, r))
        elif im.mode == "RGBA":
            r, g, b, a = im.split()
            im = Image.merge("RGBA", (b, g, r, a))
        elif im.mode == "L":
            im = im.convert("RGBA")
        # Bild in RGBA konvertieren, falls nicht bereits passiert
        im2 = im.convert("RGBA")
        data = im2.tobytes("raw", "RGBA")
        qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
        return QtGui.QPixmap.fromImage(qim)

    @staticmethod
    # 窗口置于屏幕中心
    def center_win(win):
        # desktop.width() 多屏幕的累加宽度   desktop.screenGeometry() 单个屏幕的整个屏幕
        # desktop.availableGeometry() 单屏幕的可用区域
        # self.frameGeometry() 包括标题栏和边框的高度,但是要在显示之后调用才有效
        # self.geometry() 不包括标题栏和边框的高度
        # move(int x,int y) 包括标题栏的高度和边框的宽度
        # setGeometry() resize() 不包括题栏的高度和边框

        # self.move(self.width() * (-2), 0)  # 先将窗口放到屏幕外，可避免移动窗口时的闪烁现象。
        # self.show()

        win.show()  # 必须先显示，geo才有效果
        desktop = QtWidgets.QApplication.desktop()

        x = (desktop.availableGeometry().width() - win.frameSize().width()) // 2
        y = (desktop.availableGeometry().height() - win.frameSize().height()) // 2
        win.move(x, y)

        # print(x, y, self.x(), self.y(), self.frameGeometry(), self.frameSize())
        # print(desktop.width(), desktop.height(), desktop.screenGeometry(), desktop.availableGeometry())

        # qr = self.frameGeometry()
        # # print(type(qr), qr)
        # cp = QtWidgets.QDesktopWidget().availableGeometry().center() + QtCore.QPoint(1600, 0)
        # qr.moveCenter(cp)
        # self.move(qr.topLeft())

        # screen = QtWidgets.QDesktopWidget().screenGeometry()
        # size = self.geometry()
        # print(size.height())
        # self.move((screen.width() - size.width()) / 2,
        #           (screen.height() - size.height()) / 2)

    # @staticmethod
    # # 为窗口设置底图   失败的函数
    # def set_background(win, label, img_file, flag_show=0, scale=1):
    #     """
    #     """
    #
    #     img = QtGui.QPixmap(img_file)
    #     w_win, h_win = win.width(), win.height()
    #     w_img, h_img = img.width(), img.height()
    #
    #     ratio_w = w_img / w_win
    #     ratio_h = h_img / h_win
    #
    #     img_new = None
    #     is_w = True if ratio_w > ratio_h else False
    #     if flag_show == 0:
    #         print(is_w)
    #         img_new = img.scaledToWidth(w_win, QtCore.Qt.SmoothTransformation) if is_w else \
    #             img.scaledToHeight(h_win, QtCore.Qt.SmoothTransformation)
    #     elif flag_show == 1:
    #         img_new = img.scaledToHeight(h_win, QtCore.Qt.SmoothTransformation) if is_w else \
    #             img.scaledToWidth(w_win, QtCore.Qt.SmoothTransformation)
    #     elif flag_show == 2:
    #         height = h_img / w_img * w_win  # 窗口要调整的高度
    #         win.resize(w_win, height)
    #         img_new = img.scaled(w_win, height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
    #     elif flag_show == 3:
    #         width = w_img / h_img * h_win
    #         win.resize(width, h_win)
    #         img_new = img.scaled(width, h_win)
    #     elif flag_show == 4:
    #         width, height = w_img * scale, h_img * scale
    #         win.resize(width, height)
    #         img_new = img.scaled(width, height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
    #
    #     else:
    #         print('类型不对')
    #         pass
    #     print('adf', win.width(), img_new.width())
    #     label.setPixmap(img_new)
    #     label.resize(win.width(), win.height())
    #
    #     # bg.setAlignment(QtCore.Qt.AlignCenter)

    # # 读取图片原有的亮度值
    # @staticmethod
    # def brightness(path):
    #     im = Image.open(path)
    #     stat = ImageStat.Stat(im)
    #     r, g, b = stat.mean
    #     return math.sqrt(0.241 * (r ** 2) + 0.691 * (g ** 2) + 0.068 * (b ** 2))
    # # 获取文件亮度平均值
    # @staticmethod
    # def brightness_avg(path):
    #     os.chdir(path)
    #     sum = 0.0
    #     img_len = len(os.listdir())
    #     for name_list_image in os.listdir():
    #         if name_list_image.endswith(".jpg"):
    #             image_url = os.getcwd() + '/' + name_list_image
    #             b = Utils.brightness(image_url)
    #             sum += b
    #             print('%s=%s' % (image_url, b))
    #     avg = sum / img_len
    #     return avg
    # 设置图片亮度
    # @staticmethod
    # def set_brightness(b_avg, path):
    #     for name_list_image in os.listdir():
    #         if name_list_image.endswith(".jpg"):
    #             image_url = os.getcwd() + '/' + name_list_image
    #             im = Image.open(image_url)
    #             im = ImageEnhance.Brightness(im).enhance(b_avg / Utils.brightness(image_url))
    #             # path = r'C:\Users\Smart\Desktop\image\new'
    #             flag = os.path.exists(path)
    #             if not flag:
    #                 os.mkdir(path)
    #             im.save(path + '/' + name_list_image)


class AnimWin(QtWidgets.QWidget):
    """ 自动消失的提示框 """

    def __init__(self, msg='', parent=None, font_size=16):
        super(AnimWin, self).__init__(parent)

        # self.parent = parent
        self.animation = None

        # 一定要先设置鼠标床头，否则无法穿透，应该是属性中间有值影响
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)  # 无边框，最前端
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)   # 透明

        label = QtWidgets.QLabel(self)
        label.setText(msg)

        font = QtGui.QFont("Microsoft YaHei")
        font.setPointSize(font_size)
        font.setBold(True)
        fm = QtGui.QFontMetrics(font)
        rect = QtCore.QRect(fm.boundingRect(msg))  # 字符串所占的像素宽度, 高度
        margin = 5
        rect.setWidth(rect.width() + 5 * margin)
        rect.setHeight(rect.height() + 2 * margin)
        # rect = QtCore.QRect(0, 0, 1820, 980)
        self.resize(rect.size())
        # self.resize(500, 100)

        label.setFont(font)
        label.setAutoFillBackground(True)
        palette = QtGui.QPalette()  # 新建一个调色板
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor('#4682B4'))  # 设置颜色
        palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.darkRed)  # 设置颜色
        label.setPalette(palette)
        label.setAlignment(QtCore.Qt.AlignCenter)

        vl = QtWidgets.QVBoxLayout()  # 设置垂直布局
        # vl.setContentsMargins(margin*3, margin, margin*3, margin)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.addWidget(label)  # 添加控件
        self.setLayout(vl)

        # if parent:
        #     print(parent.frameGeometry(), parent.geometry())
        #     self.move(parent.x() + int((parent.width() - rect.width()) / 2),
        #               parent.y() + int((parent.height() - rect.height()) / 2))
        self.win_center(parent)

        self.close()
        self.show()

    '''无边框移动'''

    # def mousePressEvent(self, QMouseEvent):
    #     if QMouseEvent.button() == Qt.LeftButton:
    #         self.flag = True
    #         self.m_Position = QMouseEvent.globalPos() - self.pos()
    #         QMouseEvent.accept()
    #         self.setCursor(Qt.QCursor(Qt.OpenHandCursor))
    #
    # def mouseMoveEvent(self, QMouseEvent):
    #     if Qt.LeftButton and self.flag:
    #         self.move(QMouseEvent.globalPos() - self.m_Position)
    #         QMouseEvent.accept()
    #
    # def mouseReleaseEvent(self, QMouseEvent):
    #     self.flag = False
    #     self.setCursor(Qt.QCursor(Qt.Qt.ArrowCursor))
    def closeEvent(self, event):
        if self.animation is None:
            self.animation = QtCore.QPropertyAnimation(self, b'windowOpacity')
            self.animation.setDuration(3000)
            self.animation.setStartValue(1)
            self.animation.setEndValue(0)
            self.animation.finished.connect(self.close)
            self.animation.start()
            event.ignore()

    def win_center(self, parent=None):
        if parent:
            rect = self.rect()
            self.move(int((parent.width() - rect.width()) / 2),
                      int((parent.height() - rect.height()) / 2))
        else:
            # availableGeometry()返回屏幕可用区域的位置和尺寸的QRect对象，即扣除任务栏的区域
            # screenGeomtry():返回整个屏幕的位置和尺寸的QRect对象
            center = QtWidgets.QDesktopWidget().availableGeometry().center()
            window = self.geometry()
            # window = self.frameGeometry()  # 包括标题栏的高度和边框的宽度且要在显示之后调用才有效
            window.moveCenter(center)
            self.move(window.topLeft())


class BitSet(object):
    # from low to high "00000001 00000010 00000011", the array is [1, 2, 3]
    def __init__(self, capacity):
        # "B"类型相当于 C 语言的 unsigned char， 即占用1byte（8位），所以size大小设置为8
        self.unit_size = 8
        self.unit_count = (capacity + self.unit_size - 1) // self.unit_size
        self.capacity = capacity
        self.arr = array.array("B", [0] * self.unit_count)

    def any(self):
        # 是否存在置为 1 的位
        for a in self.arr:
            if a != 0:
                return True
        return False

    def all(self):
        # 是否所有位都为 1， 即是否存在置为 0 的位
        t = (1 << self.unit_size) - 1
        for a in self.arr:
            if (a & t) != t:
                return False
        return True

    def none(self):
        # 是否所有位都为 0，即是否不存在置为 1 的位
        for a in self.arr:
            if a != 0:
                return False
        return True

    def count(self):
        # 置为 1 的位的个数
        c = 0
        for a in self.arr:
            while a > 0:
                if a & 1:
                    c += 1
                a = a >> 1
        return c

    def size(self, flag='bits'):
        # 所有位的个数 or 所有字节数
        return self.unit_count * self.unit_size if flag == 'bits' else self.unit_count

    def get(self, pos):
        # 获取第 pos 位的值
        index = int(pos / self.unit_size)
        offset = (self.unit_size - (pos - index * self.unit_size) - 1) % self.unit_size
        return (self.arr[index] >> offset) & 1

    def test(self, pos):
        # 判断第 pos 位的值是否为 1
        if self.get(pos):
            return True
        return False

    def set(self, pos=-1):
        # 设置第 pos 位的值为 1，若 pos 为 -1， 则所有位都置为 1
        if pos >= 0:
            index = int(pos / self.unit_size)
            offset = (self.unit_size - (pos - index * self.unit_size) - 1) % self.unit_size
            self.arr[index] = (self.arr[index]) | (1 << offset)
        else:
            t = (1 << self.unit_size) - 1
            for i in range(self.unit_count):
                self.arr[i] = self.arr[i] | t

    def reset(self, pos=-1):
        # 设置第 pos 位的值为 0，若 pos 为 -1， 则所有位都置为 0
        if pos >= 0:
            index = int(pos / self.unit_size)
            offset = (self.unit_size - (pos - index * self.unit_size) - 1) % self.unit_size
            x = (1 << offset)
            self.arr[index] = (self.arr[index]) & (~x)
        else:
            for i in range(self.unit_count):
                self.arr[i] = 0

    def flip(self, pos=-1):
        # 把第 pos 位的值取反，若 pos 为 -1， 则所有位都取反
        if pos >= 0:
            if self.get(pos):
                self.reset(pos)
            else:
                self.set(pos)
        else:
            for i in range(self.unit_count):
                self.arr[i] = ~self.arr[i] + (1 << self.unit_size)

    def bin_str(self):
        b = ""
        for a in self.arr:
            t = bin(a)
            b += "0" * (self.unit_size - len(t) + 2) + t + ","
        return "[" + b.replace("0b", "").strip(",") + "]"

    def show(self):
        return self.arr

    def __repr__(self):
        return self.bin_str()


class Bits:
    # This Is Base Class Of All Bits Operator Achieve
    # Use Numpy DArray#
    #
    # Achieve Port Of Bit set In C++ Standard
    # e.g. flip,set,reset,....
    #
    # Achieve L/Rshift Local
    # And Xor Between Different Size Of Bits
    TYPE_BITS_NUM = 8
    TYPE_IN_USE = 'uint8'

    def __init__(self, start=None, n_vail=None):

        if start is None:
            start = np.zeros(0, self.TYPE_IN_USE)

        # Ini The start If It's Str Which Include only '0' And '1'
        elif type(start) is str:
            idx = len(start) - self.TYPE_BITS_NUM
            n_vail = len(start)
            idx2 = 0
            tmp_start = np.zeros((len(start) + self.TYPE_BITS_NUM - 1) / self.TYPE_BITS_NUM, self.TYPE_IN_USE)

            while idx > 0:
                tmp_start[idx2] = int(start[idx:idx + self.TYPE_BITS_NUM], 2)
                idx -= self.TYPE_BITS_NUM
                idx2 += 1
            tmp_start[idx2] = int(start[:idx + self.TYPE_BITS_NUM], 2)
            start = tmp_start
        self._status = copy.deepcopy(start)
        # Ini The Valid Bits Num
        # Set The High Mask
        if n_vail is None:
            self._len = start.size * self.TYPE_BITS_NUM
        else:
            self._len = n_vail
            self._status.resize((n_vail + self.TYPE_BITS_NUM - 1) / self.TYPE_BITS_NUM)
        self._mask = self._set_mask()

    def _set_mask(self):
        ret_mask = np.array(0xFF, self.TYPE_IN_USE)
        per_mask = 1 << int(self._len % self.TYPE_BITS_NUM)
        tmp_mask = np.array(per_mask - 1, self.TYPE_IN_USE)
        if tmp_mask != 0:
            ret_mask = tmp_mask
        return ret_mask

    def _get_block_num(self, n):
        return n / self.TYPE_BITS_NUM

    def _get_block_offset(self, n):
        return n & (self.TYPE_BITS_NUM - 1)

    def get_status(self):
        return self._status

    def any(self):
        return self._status.any()

    def none(self):
        return ~(self.any())

    def flip(self, pos=None):
        if pos is None:
            self._status = ~self._status
        elif pos < self._len:
            self._status[self._get_block_num(pos)] ^= (1 << (self._get_block_offset(pos)))

    def set(self, pos=None):
        setted_block = (1 << self.TYPE_BITS_NUM) - 1
        if pos is None:
            for idx in range(0, self._status.size):
                self._status[idx] = setted_block
        elif pos < self._len:
            tmp_mask = (1 << (self._get_block_offset(pos)))
            self._status[self._get_block_num(pos)] &= (~tmp_mask)
            self._status[self._get_block_num(pos)] ^= tmp_mask

    def reset(self, pos=None):
        if pos is None:
            self._status = np.zeros(self._status.size, self.TYPE_IN_USE)
        elif pos < self._len:
            tmp_mask = (1 << (self._get_block_offset(pos)))
            self._status[self._get_block_num(pos)] &= (~tmp_mask)

    def test(self, pos=0):
        if self[pos] == 1:
            return True
        else:
            return False

    def resize(self, new_len):
        if len <= 0:
            self.__init__()
        else:
            sz = ((new_len + self.TYPE_BITS_NUM - 1) / self.TYPE_BITS_NUM)
            self._len = new_len
            self._status.resize(sz)
            self._mask = self._set_mask()

    def store_size(self):
        return self._status.size

    def __len__(self):
        return self._len

    def __getitem__(self, item):
        return (self._status[self._get_block_num(item)] >> (self._get_block_offset(item))) & 1

    def __setitem__(self, key, value):
        assert (value == 0 or value == 1)
        if value == 0:
            self.reset(key)
        else:
            self.set(key)

    def __rshift__(self, mov):
        ret_bits = Bits()
        ret_bits.resize(self._len)
        mov = int(mov)

        if mov >= self._len:
            ret_bits.reset()
        else:
            sta = mov / self.TYPE_BITS_NUM
            offset = mov % self.TYPE_BITS_NUM
            j = 0

            for idx in range(sta, (len(self._status) - 1)):
                ret_bits._status[j] = ((self._status[idx]) >> offset) \
                                      ^ (self._status[idx + 1] << (self.TYPE_BITS_NUM - offset))
                j += 1
            ret_bits._status[j] = (self._status[-1] & self._mask) >> offset

        return ret_bits

    def __lshift__(self, mov):
        ret_bits = Bits()
        ret_bits.resize(self._len)
        mov = int(mov)

        if mov >= self._len:
            ret_bits.reset()
        else:
            sta = len(self._status) - 1 \
                  - mov / self.TYPE_BITS_NUM

            offset = mov % self.TYPE_BITS_NUM

            j = len(self._status) - 1

            for idx in reversed(range(sta, 0, -1)):
                ret_bits._status[j] = ((self._status[idx]) << offset) \
                                      ^ (self._status[idx - 1] >> (self.TYPE_BITS_NUM - offset))
                j -= 1

            ret_bits._status[j] = (self._status[0]) << offset

        return ret_bits

    def __xor__(self, other_bits):

        if self._len >= len(other_bits):
            ret_bits = Bits(self.get_status(), len(self))
            oppo = other_bits
        else:
            ret_bits = Bits(other_bits.get_status(), len(other_bits))
            oppo = self

        for idx in range(oppo._status.size - 1):
            ret_bits._status[idx] ^= oppo.get_status()[idx]

        idx = oppo._status.size - 1
        print(idx)
        ret_bits._status[idx] ^= (oppo._status[idx] & oppo._mask)
        return ret_bits


# 位标志列表，简洁方便的
class BitMark(object):
    def __init__(self, length):
        self.size = length // 8 + (1 if length % 8 else 0)  # 字节数
        self.values = bytearray(b"\x00" * self.size)
        self.length = length  # 要求的总位数

    def __setitem__(self, index, value):
        if self.length < 1:
            return None

        off = 7 - index % 8
        value = int(bool(value)) << off  # 0000X0000
        mask = (1 << off)  # 000010000

        self.values[index // 8] &= (~mask)  # ----0----
        self.values[index // 8] |= value

        # value = int(bool(value)) << (7 - index % 8)
        # mask = 0xff ^ (7 - index % 8)

        # self.values[index // 8] &= mask
        # self.values[index // 8] |= value

    def __getitem__(self, index):
        if self.length < 1:
            return None

        # 序号小于0，从尾倒数。大于总位数则异常
        mask = 1 << (7 - index % 8)
        # print(index, 7 - index % 8)
        return bool(self.values[index // 8] & mask)

    def __len__(self):
        # 返回位长度，有效位数与总位数
        return self.length

    def __repr__(self):
        if self.length < 1:
            return '空'

        # MyLog().debug(len(self), type(self))
        return "<{}>".format(",".join("{:d}".format(value) for value in self))

    def __str__(self):
        if self.length < 1:
            return '空'

        res = []
        for each in self.values:
            value = "{:08b}".format(each)
            res.append(f'{value[:4]} {value[4:]}')

        return "< {} >".format(", ".join(res))

    def set(self, value=0):
        # 清零或全1
        for i in range(self.size * 8):
            self[i] = bool(value)

    def flip(self, index=None):
        # 把第 index 位的值取反，若 index 为 None， 则所有位都取反
        if index is None:
            for i in range(self.length):
                self.flip(i)
        else:
            self.values[index // 8] ^= (1 << (7 - index % 8))


class MyLog(object):
    log_path = "E:/Codes/Logs"

    # 设置输出的等级
    # LEVELS = {'NOTSET': logging.NOTSET,
    #           'DEBUG': logging.DEBUG,
    #           'INFO': logging.INFO,
    #           'WARNING': logging.WARNING,
    #           'ERROR': logging.ERROR,
    #           'CRITICAL': logging.CRITICAL}

    # 用字典保存日志输出格式
    # format_dict = {0: logging.Formatter('%(message)s'),
    #                1: logging.Formatter('%(name)s - %(message)s'),
    #                2: logging.Formatter('%(filename)s - %(module)s - %(lineno)d - %(levelname)s - %(message)s'),
    #                3: logging.Formatter('%(thread)d - %(threadName)s - %(process)d - %(message)s'),
    #                4: logging.Formatter('%(funcName)s - %(created)f - %(levelname)s - %(message)s'),
    #                5: logging.Formatter('%(pathname)s - %(levelno)s - %(levelname)s - %(message)s'),
    #                6: logging.Formatter('%(asctime)s - %(msecs)d - %(relativeCreated)d - %(levelname)s - %(message)s')}

    def __init__(self, log_file=None, flag=2, log_tags='', log_format=0):
        self.log_file = log_file if log_file else 'log.txt'
        self.flag = flag  # 0仅写入日志文件， 1二者同时输出 2仅屏幕输出
        self.log_tags = log_tags
        self.log_format = log_format
        self.msg = []

        # self.file_name = os.path.split(__file__)[-1].split(".")[0]  # 当前文件名称

        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)

        # print(self.get_cur_info())
        # print(self.get_cur())
        # self.debug(f'{self.flag} ddd {self.file_name}', '好啊')

    def debug(self, *args):
        # self.msg.clear()
        #
        # def list2str(list_arg: list):
        #     for i, element in enumerate(list_arg):
        #         if isinstance(element, list):
        #             self.list2str(element)
        #         else:
        #             self.msg.append(str(element))

        sf = sys._getframe()
        # sf.f_back.f_code.co_name  # 父级调用函数名称
        # sf.f_back.f_lineno  # 父级调用处的行号
        # sf.f_code.co_name  # 调用函数名称
        # sf.f_lineno  # 调用处行号

        # msg = f'【 {sf.f_back.f_code.co_name} {sf.f_back.f_lineno} 】{self.log_tags} {args}'
        # arg = ' '.join(args)
        msg = '【 {:s} {} 】{} {}'.format(sf.f_back.f_code.co_name, sf.f_back.f_lineno, self.log_tags, args)

        if self.flag < 2:
            with open(f'{self.log_path}/{self.log_file}', 'a') as f:
                f.write(msg)

        if self.flag:
            print(f'【 {sf.f_back.f_code.co_name} {sf.f_back.f_lineno} 】', *args)
            # print(msg)

    @staticmethod
    def get_cur():
        return sys._getframe().f_code.co_name, sys._getframe().f_back.f_code.co_name
        # return sys._getframe().f_code.co_name, sys._getframe().f_back.f_code.co_name

    @staticmethod
    def get_cur_info():
        """
            Return the frame object for the caller's stack frame.
            返回调用时的函数和行号
        """
        try:
            raise Exception
        except:
            f = sys.exc_info()[2].tb_frame.f_back
        return f.f_code.co_name, f.f_lineno


# 样式管理类
class StyleSheet(object):
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

            图片是白色半透明，作为子窗体的底图，则子窗体半透明，上面控件不透明。
            实现底图半透明化
            # Tool_Widget{
            border - radius: 10px;
            border - image: url(img / toolbg.png)
            }
        """
    # 美化样式表
    Stylesheets = [
        """     /*******************主窗体***********************/
                #Canvas{
                    /*background-image: url(./res/background/bk5.jpg);*/
                    border-radius:15px;     /*画出圆角*/
                    /*background-repeat: no-repeat;       背景不要重复*/
                    background-position: center center;      /*图片的位置，居中，靠左对齐*/

                                  /*  min-width: 1000px;      屏幕宽度在1000px以内时，图片大小保持不变*/
                                  /*  position:absolute;      固定在屏幕的最上方和最左方*/
                                  /*  top: 0;             固定在屏幕的最上方和最左方*/
                                  /*  left: 0;            固定在屏幕的最上方和最左方*/
                                  /*  width:100%;     屏幕一样的大小，从而达到全屏效果
                                    height:100%;   */

                                    /* 下面都不识别*/
                                    /*z-index:-10;            最下层级, 背景图片
                                    zoom: 1;*/
                                    /*background-size: cover;
                                    -webkit-background-size: cover;
                                    -o-background-size: cover;          让图片随屏幕大小同步缩放*/
                }
        """,
        """     /*******************列表控件***********************/
                /*去掉item虚线边框*/
                QListWidget, QListView, QTreeWidget, QTreeView {
                    outline: 0px;
                }
                /*设置左侧选项的最小最大宽度,文字颜色和背景颜色*/
                QListWidget {
                    /*border-bottom-left-radius:15;
                    min-width: 120px;
                    max-width: 120px;*/
                    color: white;
                    background: rgba(25,25,25, 150);
                    font-size:24px;font-weight:bold;font-family:Roman times;
                }
                /*被选中时的背景颜色和左边框颜色*/
                QListWidget::item:selected {
                    /*background: rgb(52, 52, 52);*/
                    border-left: 2px solid rgb(9, 187, 7);
                }
                /*鼠标悬停颜色*/
                QListWidget::item:hover {
                    color: rgb(94, 172, 230);
                    /*background: black;*/
                }

                /*右侧的层叠窗口的背景颜色*/
                QStackedWidget {
                    background: transparent;     /*全透明*/
                    /*background: rgb(30, 30, 30);
                    background: white;*/
                    margin: 0px;
                    border-bottom-right-radius: 15
                }

                /*模拟的页面
                QLabel {
                    color: white;
                }*/

                QWidget {
                    border: 1px
                }
        """
    ]

    # 初始化并可添加多个样式，字符串型
    def __init__(self, *args, **kwargs):
        super(StyleSheet, self).__init__()

        # print(type(args), args)
        # print(type(kwargs), kwargs)
        if args:
            for each in args:
                if isinstance(each, str):
                    self.Stylesheets.append(each)

    # 输出样式库
    def __str__(self):
        return '\n'.join(self.Stylesheets)

    # 运行时也能输出样式库
    __repr__ = __str__

    # 添加多个样式，字符串型
    def add(self, *args):
        if args:
            for each in args:
                if isinstance(each, str):
                    self.Stylesheets.append(each)

    # 用下标指定的样式列表库中的样式设置的控件/窗体
    def set(self, widget, *args):
        # print(type(args), args)
        style = []
        length = len(self.Stylesheets)
        if args:
            for each in args:
                if isinstance(each, int) and each < length:
                    style.append(self.Stylesheets[each])
        else:
            style = self.Stylesheets

        widget.setStyleSheet(''.join(style))
        # print('\n'.join(style))


# 访问Windows API
# 访问Windows API
class WinInfo(object):
    hwnd_title_class = dict()

    def __init__(self, *args, **kwargs):
        super(WinInfo, self).__init__(*args, **kwargs)

    @staticmethod
    def get_hwnd_pos(class_name="MozillaWindowClass", title_name="百度一下，你就知道"):
        # 通过类名和标题查找窗口句柄，并获得窗口位置和大小
        hwnd = win32gui.FindWindow(class_name, title_name)  # 获取句柄
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)  # 获取窗口左上角和右下角坐标

        return hwnd, left, top, right, bottom

    @staticmethod
    def get_title_class(hwnd, mouse):
        # 获取某个句柄的类名和标题

        if win32gui.IsWindow(hwnd):
            # 去掉条件就输出所有
            if win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                class_name = win32gui.GetClassName(hwnd)

                WinInfo.hwnd_title_class.update({hwnd: (title, class_name)})

    @staticmethod
    def get_child_by_name(hwnd, class_name):
        # 获取父句柄hwnd类名为class_name的子句柄
        return win32gui.FindWindowEx(hwnd, None, class_name, None)

    @staticmethod
    def get_child_wins(hwnd):
        """
        获得 hwnd的所有子窗口句柄
         返回子窗口句柄列表
         """
        if not hwnd:
            return
        hwndChildList = []
        win32gui.EnumChildWindows(hwnd, lambda hwnd, param: param.append(hwnd), hwndChildList)
        return hwndChildList

        # 实现遍历windows所有窗口并输出窗口标题的方法

    @staticmethod
    def get_all_win():
        # 输出所有窗口
        win32gui.EnumWindows(WinInfo.get_title_class, 0)

        for h, t in WinInfo.hwnd_title_class.items():
            if t:
                print(h, t)

    @staticmethod
    def set_mouse_pos(x, y):
        # 鼠标定位到(30,50)
        win32api.SetCursorPos([x, y])

    @staticmethod
    def mouse_clicked(flag=1):
        if flag == 1:  # 执行左单键击，若需要双击则延时几毫秒再点击一次即可
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        else:  # 右键单击
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP | win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)

    @staticmethod
    def key_enter():
        # 发送回车键
        win32api.keybd_event(13, 0, 0, 0)
        win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def close_win(classname, titlename):
        # 关闭窗口
        win32gui.PostMessage(win32gui.findWindow(classname, titlename), win32con.WM_CLOSE, 0, 0)


# 圆形按钮
class EllipseButton(QtWidgets.QPushButton):
    def __init__(self, parent=None, width=100, height=100):
        super(EllipseButton, self).__init__(parent)
        self.parent = parent
        self.setFixedSize(width, height)

    def set(self, img, text='', border=0, padding=0, color=None, background_color=None, border_color=None):

        self.setText(text)

        width, height = self.width(), self.height()
        wide = min(width, height)

        radius = wide // 2 + padding + border

        color = 'blue' if color is None else color
        background_color = 'green' if background_color is None else background_color
        border_color = 'black' if border_color is None else border_color

        qss = None
        if img:
            pix = QtGui.QImage(img)

            ratio_w = pix.width() / width
            ratio_h = pix.height() / height

            is_w = True if ratio_w > ratio_h else False
            # print(sw, sh, is_w)

            img_new = pix.scaledToWidth(height) if is_w else pix.scaledToHeight(width)
            new_img = './tmp.jpg'
            img_new.save(new_img)
            # self.setAutoFillBackground(True)  # /Widget增加背景图片时，这句一定要。
            # wide = min(width, height)
            # pix = QtGui.QPixmap(img).scaled(wide, wide, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
            # self.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(img_new)))
            # self.setIconSize(QtCore.QSize(wide, wide))
            # self.setFlat(True)  # 就是这句能够实现按钮透明，用png图片时很有用
            # border = 0  # 消除边框，取消点击效果

            qss = '''
                color: %s;
                background-color: %s;
                background: transparent;     /*全透明*/
                background-image:url(%s);
                background-position: center center;      /*图片的位置，居中，靠左对齐*/
                background-repeat: no-repeat;       /*背景不要重复*/

                border-style:none;
                border:%dpx solid %s; 
                padding:%dpx;
                min-width:%dpx;max-width:%dpx;
                min-height:%dpx;max-height:%dpx;            
                border-radius:%dpx;
                ''' % (color, background_color, new_img, border, border_color, padding,
                       width, width, height, height, radius)
        else:
            qss = '''
                color: %s;
                background-color: %s;

                border-style:none;
                border:%dpx solid %s; 
                padding:%dpx;
                min-width:%dpx;max-width:%dpx;
                min-height:%dpx;max-height:%dpx;            
                border-radius:%dpx;
                ''' % (color, background_color, border, border_color, padding,
                       width, width, height, height, radius)
        # print(qss)
        self.setStyleSheet(qss)

        # radius = width // 2 + padding + border if width < height else height // 2 + padding + border
        # color = 'blue' if color is None else color
        # background_color = 'green' if background_color is None else background_color
        # border_color = 'gray' if border_color is None else border_color
        #
        # qss = None
        # if img:
        #     qss = '''
        #         color: %s;
        #         background-color: %s;
        #         background-image:url(%s);
        #
        #         border-style:none;
        #         border:%dpx solid %s;
        #         padding:%dpx;
        #         min-width:%dpx;max-width:%dpx;
        #         min-height:%dpx;max-height:%dpx;
        #         border-radius:%dpx;
        #         ''' % (color, background_color, img, border, border_color, padding, width, width,
        #                height, height, self.radius)
        # else:
        #     qss = '''
        #         color: %s;
        #         background-color: %s;
        #
        #         border-style:none;
        #         border:%dpx solid %s;
        #         padding:%dpx;
        #         min-width:%dpx;max-width:%dpx;
        #         min-height:%dpx;max-height:%dpx;
        #         border-radius:%dpx;
        #         ''' % (color, background_color, border, border_color, padding,
        #                width, width, height, height, radius)
        # # print(qss)
        # self.setStyleSheet(qss)

    # def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
    #     painter = QtGui.QPainter(self)
    #     painter.setRenderHint(QtGui.QPainter.Antialiasing)  # 反锯齿
    #     painter.setBrush(QtGui.QBrush(QtGui.QPixmap(self.img)))  # 设置底图的方式之一
    #     # painter.setBrush(QBrush(Qt.blue))
    #     painter.setPen(QtCore.Qt.transparent)
    #
    #     rect = self.rect()
    #     rect.setWidth(rect.width() - 1)
    #     rect.setHeight(rect.height() - 1)
    #     painter.drawEllipse(rect)
    #     # 也可用QPainterPath 绘制代替 painter.drawRoundedRect(rect, 15, 15)
    #     # painterPath= QPainterPath()
    #     # painterPath.addRoundedRect(rect, 15, 15)
    #     # painter.drawPath(painterPath)


class CircleImage(QtWidgets.QWidget):
    """绘制圆形图片"""

    def __init__(self, parent=None):
        super(CircleImage, self).__init__(parent)

        self.parent = parent
        self.img = None
        self.size = None
        self.mold = 0  # 类型
        self.border_color = None
        self.border_width = None

        # self.resize(100, 100)
        # 去除背景
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

    def set_me(self, image, size=QtCore.QSize(100, 100), mold=0x00,
               border_color=QtGui.QColor('#ff0000'), border_width=2):
        """
        设置绘制的图片
        :param image:
        :param size:
        :param mold:类型 &0x0f= 0-显示图片中心 1-显示全图 2-无图
                        &0xf0= 0-无边框 1-有边框 (有框无图:圆环)
        :param border_color:
        :param border_width:
        :return:
        """
        self.img = image
        self.size = size
        self.mold = mold
        self.border_width = border_width
        self.border_color = border_color

        self.resize(size)
        # self.update()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """重写绘制事件"""
        super(CircleImage, self).paintEvent(event)

        # 不通过样式，直接设置圆角，通用，且不继承于子控件
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)  # 设置抗锯齿
        rect = None

        if self.mold & 0xf0 == 0:  # 无边框
            rect = self.rect()
            # print('dsf', rect, self.size)
            painter.setPen(QtCore.Qt.transparent)
            # pen = Qt.NoPen
            # painter.setPen(pen)  # 设置取消描边边框
        else:  # 1-有边框 (有框无图:圆环)
            rect = QtCore.QRect(self.border_width, self.border_width,
                                self.width() - 2 * self.border_width,
                                self.height() - 2 * self.border_width)

            pen = QtGui.QPen(self.border_color)  # 设置边框颜色
            pen.setWidth(self.border_width)  # 设置边框宽度
            painter.setPen(pen)  # 添加描边边框

        flag = self.mold & 0x0f
        if flag == 0:  # 0-显示图片中心
            img_new = Utils.img_center(self.width(), self.height(), self.img)
            print(img_new.size().width(), img_new.size().height())
            painter.setBrush(QtGui.QBrush(img_new))  # 设置底图的方式之一
        elif flag == 1:  # 1-显示全图
            # painter.setBrush(QBrush(QPixmap.fromImage()))  # 设置底图的方式之一
            img_new = Utils.img_center(self.width(), self.height(), self.img, 0)
            painter.setBrush(QtGui.QBrush(QtGui.QPixmap(self.img)))  # 设置绘制内容

        else:  # 2-无图
            painter.setBrush(QtGui.QBrush(QtCore.Qt.NoBrush))  # qt.blue

        # print(rect)
        painter.drawRoundedRect(rect, self.width() // 2, self.height() // 2)

        # # 主窗体无边框时是加载不了样式的，仅在子控件上实现样式。
        # # 要在主窗体本身实现样式，需要在paintEvent事件中加上如下代码，设置底图也是一样的
        # opt = QStyleOption()
        # opt.initFrom(self)
        # p = QPainter(self)
        # p.setRenderHint(QPainter.Antialiasing)  # 反锯齿
        # self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
        # # super(Canvas, self).paintEvent(event)

        # 也可用QPainterPath 绘制代替 painter.drawRoundedRect(rect, 15, 15)
        # painterPath= QPainterPath()
        # painterPath.addRoundedRect(rect, 15, 15)
        # painter.drawPath(painterPath)

        # 直接设置底图，与圆角的画刷设置不能同时
        # pix = QtGui.QPixmap('./res/images/white go-1.png')
        # painter.drawPixmap(rect, pix)
    # def enterEvent(self, a0: QtCore.QEvent):
    #     print('enter', a0.pos())
    #     return super().enterEvent(a0)
    #
    # def leaveEvent(self, a0: QtCore.QEvent):
    #     print('leave', a0)
    #     return super().enterEvent(a0)
    #
    # def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
    #     print('press', a0.pos())
    #     return super(CircleImage, self).mousePressEvent(a0)


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        # self.resize(800, 600)
        # self.setGeometry(800, 100, 800, 600)
        # self.win_center()
        AnimWin('好事多磨', self)

        # self.setupUi(self)

    def resizeEvent(self, event):
        palette = QtGui.QPalette()
        pix = QtGui.QPixmap('res/background.jpg')
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(palette)


if __name__ == '__main__':
    # app = QtWidgets.QApplication(sys.argv)
    # win = MainWindow()
    # win.show()
    # sys.exit(app.exec_())
    # ll = Utils.GetCpuInfo()
    # print(f'cpu物理个数:{ll[0]}    cpu逻辑个数:{ll[1]}    cpu使用率:{ll[2]}')
    # ll = Utils.formatByte(0)
    # print(ll)
    # print(type(Utils.get_file_extension('ddsg.ext')))
    # print('ddd.ext'.endswith(''))
    # print(Utils.rand_str())
    # print(Utils.get_pin())
    print(Utils.files_in_dir(r'F:\重要', '.mp4'))
