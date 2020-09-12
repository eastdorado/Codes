#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @项目名称: python
# @File    : dealPdf.py
# @Time    : 2019/12/25 20:27
# @Author  : big
# @Email   : shdorado@126.com
import sys
import datetime
import glob
import os
import time
import gevent, threading
from gevent import monkey  # 猴子补丁

monkey.patch_all()  # 给所有的耗时操作打上补丁，协程自动切换

# from reportlab.lib.pagesizes import portrait
# from reportlab.pdfgen import canvas
# from wand.image import Image
# from PyPDF2 import PdfFileReader, PdfFileWriter
import shutil
import fitz
from PIL import Image, ImageQt
from PyQt5 import QtGui, QtWidgets, QtCore

from ui_dealPdf import Ui_Form
from utilities import Utils, AnimWin



class DealPdf(object):
    def __init__(self):
        self.pdfDoc = None
        self.pdf_total_pages = 0
        self.tmp = './tmp'  # 临时目录

        self.coroutine_count = 40  # 协程数量
        self.coroutine_index = 0
        # self.image_suffix = ".png"  # 图片后缀

    def read_Pdf(self, pdf_file):
        if not os.path.isfile(pdf_file):
            AnimWin('请输入正确的pdf文件')
            return
        try:
            # self.old_pdf_name = pdf_file

            if os.path.exists(self.tmp):  # 判断存放图片的文件夹是否存在
                shutil.rmtree(self.tmp)  # 递归删除文件夹
                # os.removedirs(self.tmp)   # 删除空文件夹
            os.makedirs(self.tmp)  # 图片文件夹不存在就创建

            if self.pdfDoc:
                self.pdfDoc.close()
            self.pdfDoc = fitz.open(pdf_file)  # 打开PDF文件，生成一个对象
            self.pdf_total_pages = self.pdfDoc.pageCount  # pdf总页数
            return self.pdf_total_pages
        except Exception as e:
            print("read_Pdf: %s " % e)

    def get_page_image(self, index):
        if index < 0 or index > self.pdf_total_pages:
            AnimWin('请输入正确的pdf页码')
            return None
        try:
            page = self.pdfDoc[index]
            ro = page.rect.height / page.rect.width
            rotate = int(0)
            # 此处若是不做设置，默认图片大小为：516X729, dpi=96
            # (1.33333333-->1056x816)   (2-->1584x1224)
            # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高四倍的图像。
            zoom_x = 3.0
            zoom_y = 3.0
            mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
            pix = page.getPixmap(matrix=mat, alpha=False)
            # pix = page.getPixmap(alpha=False)
            # pix = page.getPixmap(matrix=mat, alpha=0)  # alpha = 0 白色背景 不透明

            # # set the mode depending on alpha
            # mode = "RGBA" if pix.alpha else "RGB"
            # img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
            # return img
            # qt_img = ImageQt.ImageQt(img)
            # set the correct QImage format depending on alpha,不用pil
            fmt = QtGui.QImage.Format_RGBA8888 if pix.alpha else QtGui.QImage.Format_RGB888
            qt_img = QtGui.QImage(pix.samples, pix.width, pix.height, pix.stride, fmt)
            return qt_img
        except Exception as e:
            print("get_page_image: %s " % e)
            return None

    def save_page_image(self, img, index):
        if img:
            test = True
            if test:
                # rect:   350-480  596-738, 130,142     12,64
                startx = int(img.width() / 2 - 65)
                endx = int(img.width() / 2 + 65)
                starty = int(img.height() - 142)
                endy = img.height()
                for y in range(starty, endy):
                    for x in range(startx, endx):
                        img.setPixelColor(x, y, QtGui.QColor(255, 255, 255, 255))
                if index > 1 and index % 2 == 0:
                    startx = 0
                    endx = 120
                    starty = 0
                    endy = img.height()
                    for y in range(starty, endy):
                        for x in range(startx, endx):
                            img.setPixelColor(x, y, QtGui.QColor(255, 255, 255, 255))
                        # c = img.pixel(x, y)
                        # colors = QtGui.QColor(c).getRgb()
                        # # colors_ = (204, 255, 204)
                        # colors_ = (80, 80, 80)
                        # if colors[0]<colors_[0] and colors[1]<colors_[1] and colors[2]<colors_[2]:
                        # if abs(colors[0] - colors_[0]) < 10 \
                        #         and abs(colors[1] - colors_[1]) < 10 \
                        #         and abs(colors[2] - colors_[2]) < 10:
                        # print(colors)
                        # img.setPixelColor(x, y, QtGui.QColor(0, 0, 0, 255))
                        # else:
                        #     img.setPixelColor(x, y, QtGui.QColor(255, 255, 255, 255))
            img.save('{}/img{:0>6d}.png'.format(self.tmp, index))

    def png_to_pdf(self, new_pdf_name):
        """图片合并为 PDF 文件"""
        try:
            doc = fitz.open()
            for img in sorted(glob.glob("{}/*.png".format(self.tmp))):  # 读取所有图片文件，确保按文件名排序
                # print(img)
                img_doc = fitz.open(img)  # 打开图片文件
                pdf_bytes = img_doc.convertToPDF()  # 使用图片创建单页的 PDF 数据流
                # print(type(pdf_bytes))
                img_pdf = fitz.open("pdf", pdf_bytes)  # 形成 pdf 文档(页)
                # print(type(img_pdf))
                doc.insertPDF(img_pdf)  # 将当前页插入总文档
                # os.remove(img)  # 删除文件

            if os.path.exists(new_pdf_name):
                os.remove(new_pdf_name)
            doc.save(new_pdf_name)  # 保存总文档到pdf文件
            doc.close()
            # os.removedirs(self.tmp)
            shutil.rmtree(self.tmp)  # 递归删除文件夹

        except Exception as e:
            print(e)

    def creat_new_pdf(self, save_pdf_name):
        if not save_pdf_name:
            AnimWin('请输入正确的pdf文件名称')
            return
        if not self.pdfDoc:
            AnimWin('请打开pdf文件')
            return

        # for index in range(11):
        for index in range(self.pdf_total_pages):
            self.save_page_image(self.get_page_image(index), index)

        self.png_to_pdf(save_pdf_name)

    def run(self):
        # self.thread_go()
        # self.coroutine_go()
        # self.deal_pdf(self.old_pdf_name)
        # self.pdf_to_png(self.new_pdf_name)
        self.deal_pdf()
        # self.png_to_pdf(self.new_pdf_name)

    def thread_go(self):
        startTime_pdf2img = datetime.datetime.now()  # 开始时间

        for i in range(self.coroutine_count):
            t = threading.Thread(target=self.work, args=(i,))
            t.start()

        endTime_pdf2img = datetime.datetime.now()  # 结束时间
        print('多线程 时间=', (endTime_pdf2img - startTime_pdf2img).seconds)

    def coroutine_go(self):
        startTime_pdf2img = datetime.datetime.now()  # 开始时间
        # 创建多协程与    创建多进程\多线程    的过程差不多
        gevent.joinall([gevent.spawn(self.work, i) for i in range(self.coroutine_count)])
        endTime_pdf2img = datetime.datetime.now()  # 结束时间
        print('多协程 时间=', (endTime_pdf2img - startTime_pdf2img).seconds)

    def work(self, cor_index=0):
        for index in range(cor_index, self.pdf_total_pages, self.coroutine_count):
            page = self.pdfDoc[index]
            rotate = int(0)
            zoom_x = 3.0
            zoom_y = 3.0
            mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
            pix = page.getPixmap(matrix=mat, alpha=False)
            pix.writePNG('%s/images_%s.png' % (self.tmp, index))

    def deal_pdf(self):
        startTime = datetime.datetime.now()  # 开始时间
        try:
            # pdfDoc = fitz.open(pdf_file_name)  # 打开PDF文件，生成一个对象
            self.pdf_total_pages = 1
            for index in range(self.pdf_total_pages):
                page = self.pdfDoc[1]
                # page = self.pdfDoc[index]
                rotate = int(0)
                # 此处若是不做设置，默认图片大小为：792X612, dpi=96
                # (1.33333333-->1056x816)   (2-->1584x1224)
                # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高四倍的图像。
                zoom_x = 3.0
                zoom_y = 3.0
                mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
                # pm = page.getPixmap(matrix=trans, alpha=False)
                pix = page.getPixmap(matrix=mat, alpha=0)  # alpha = 0 白色背景 不透明

                # # set the mode depending on alpha
                # mode = "RGBA" if pix.alpha else "RGB"
                # img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
                # qt_img = ImageQt.ImageQt(img)

                # set the correct QImage format depending on alpha,不用pil
                fmt = QtGui.QImage.Format_RGBA8888 if pix.alpha else QtGui.QImage.Format_RGB888
                qt_img = QtGui.QImage(pix.samples, pix.width, pix.height, pix.stride, fmt)

                # pm = fitz.fitz.Pixmap()
                # print("x=%d y=%d w=%d h=%d" % (pix.x, pix.y, pix.w, pix.h))
                # pd.writeImage()
                # pix.writePNG('%s/images_%s.png' % (self.tmp, str(index + 1)))
                # areas = page.searchFor("市政", hit_max=16)
                # page = fitz.Page()
                # print(type(areas))
                # print(areas)

        except Exception as e:
            print(e)
        endTime = datetime.datetime.now()  # 结束时间
        print('deal_pdf 时间=', (endTime - startTime).seconds)

    def deal_png(self):
        for each in sorted(glob.glob("%s/*.png" % self.tmp)):  # 读取所有图片文件，确保按文件名排序
            # print(each)
            im = Image.open(each)
            # 图片的宽度和高度
            img_size = im.size
            print("图片" + each + " 图片宽度和高度分别是{}".format(img_size))
            '''
            裁剪：传入一个元组作为参数
            元组里的元素分别是：（距离图片左边界距离x， 距离图片上边界距离y，裁剪框宽度w，裁剪框高度h）
            '''
            #   设置抠图区域
            box1 = (80, 29, 120, 90)
            #   从图片上抠下此区域
            region1 = im.crop(box1)
            box2 = (180, 29, 220, 90)
            region2 = im.crop(box2)
            #   将此区域旋转180度
            # region = region.transpose(Image.ROTATE_180)
            #   查看抠出来的区域
            # region.show()
            #   将此区域粘回去
            im.paste(region2, box1)
            im.paste(region2, box2)

            name = each.replace('.png', 'new.png')
            im.save(name)
            os.remove(each)

            # region = im.crop((x, y, x + w, y + h))
            # region.save(newImageName)
            #
            # # ==== 图片背景色设为白色
            # im = pilImage.open(newImageName)
            # x, y = im.size
            # p = pilImage.new('RGBA', im.size, (255, 255, 255))
            # print(type(im))
            # p.paste(im, (0, 0, x, y), p)
            # p.save(newImageName)

    def pdf_to_png(self, pdf_file_name):
        """PDF 转为图片"""
        try:
            startTime_pdf2img = datetime.datetime.now()  # 开始时间
            # pdfDoc = fitz.open(pdf_file_name)  # 打开PDF文件，生成一个对象
            # print(type(doc))
            # self.pdf_total_pages = pdfDoc.pageCount
            for pg in range(self.pdf_total_pages):
                page = self.pdfDoc[pg]
                rotate = int(0)
                # 此处若是不做设置，默认图片大小为：792X612, dpi=96
                # (1.33333333-->1056x816)   (2-->1584x1224)
                # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高四倍的图像。
                zoom_x = 3.0
                zoom_y = 3.0
                mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
                # pm = page.getPixmap(matrix=trans, alpha=False)
                pix = page.getPixmap(matrix=mat, alpha=0)  # alpha = 0 白色背景 不透明
                # pm = fitz.fitz.Pixmap()
                # print("x=%d y=%d w=%d h=%d" % (pix.x, pix.y, pix.w, pix.h))
                # pd.writeImage()
                pix.writePNG('{}/img_{:0>4d}.png'.format(self.tmp, pg))

                # # 下面的这段代码就是想要从一页PDF的中心点为起点截取到右下角的区域，截取整张图的1/4.
                # mat = fitz.Matrix(2, 2)  # 在每个方向缩放因子2
                # rect = page.rect  # 页面的矩形
                # mp = rect.tl + (rect.br - rect.tl) * 0.5  # 矩形的中心
                # clip = fitz.Rect(mp, rect.br)  # 我们想要的剪切区域
                # pix = page.getPixmap(matrix=mat, alpha=False, clip=clip)
            endTime_pdf2img = datetime.datetime.now()  # 结束时间
            print('pdf_to_png 时间=', (endTime_pdf2img - startTime_pdf2img).seconds)

        except Exception as e:
            print(e)
        finally:
            pass


class MainWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.resize(1024, 768)  # 设置窗体大小
        self.label.setMouseTracking(True)  # 设置鼠标跟踪

        self.cwd = os.getcwd()  # 获取当前程序文件位置
        self.file_pdf = 'E:/考证/2019版一建《市政》电子教材.pdf'  # 原pdf文件名
        self.new_pdf_name = "./2019版一建《市政》电子教材new.pdf"  # 新pdf文件名

        self.dealer = DealPdf()
        self.cur_page = 0
        self.total_page = 0

        self.horizontalScrollBar.setMaximum(10)
        self.horizontalScrollBar.setToolTipDuration(1000)
        self.horizontalScrollBar.setToolTip('第 1 页')

        # self.label.setAlignment(QtCore.Qt.AlignCenter)
        # self.label.setMinimumSize(250, 20000)   #设置滚动条的尺寸
        # self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)
        # self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)

        # img = QtGui.QImage(r"E:\python\res\copy.jpg")
        # for y in range(img.height()):
        #     for x in range(img.width()):
        #         c = img.pixel(x, y)
        #         colors = QtGui.QColor(c).getRgb()
        #         if abs(colors[0] - 221) < 10 \
        #                 and abs(colors[1] - 215) < 10 \
        #                 and abs(colors[2] - 65) < 10:
        #             print(colors)
        #             img.setPixelColor(x, y, QtGui.QColor(255, 255, 255, 255))

        # pixmap = QtGui.QPixmap.fromImage(img)
        # self.label.setPixmap(pixmap)

    def mousePressEvent(self, mE):
        print('x=%d y=%d' % (mE.x(), mE.y()))
        area_rect = self.scrollArea.rect()
        print(area_rect)
        # print('area  x=%d y=%d width=%d height=%d' %
        #       (area_rect.x(), area_rect.y(), areaself.scrollArea.height()))
        # t = QMouseEvent.localPos()
        # t = QMouseEvent.windowPos()
        # self.label.setMouseTracking(True)
        # print(f'move to: {t.x()}, {t.y()} ')
        # mE = QtGui.QMouseEvent()

    @staticmethod
    def slot_open_color():
        col = QtWidgets.QColorDialog.getColor()
        if col.isValid():
            print(col.name())

    def resizeEvent(self, event):
        palette = QtGui.QPalette()
        pix = QtGui.QPixmap('res/images/background.jpg')
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(palette)
        # sz = self.scrollArea.size()
        # self.scrollAreaWidgetContents.resize(sz.width()-2, sz.height()-2)
        # self.label.resize(sz.width()-2, sz.height()-2)
        # print(self.label.size())
        # print(self.scrollAreaWidgetContents.size())
        # self.show_page(self.cur_page)

    def show_page(self, index):
        try:
            # self.dealer.read_Pdf("./2012  岩土基础考试1500题（含历年真题）.pdf")
            img = self.dealer.get_page_image(index)
            # print('img  width=%d height=%d ' % (img.width(), img.height()))
            # print(self.label.size())

            test = True
            if img:
                # self.dealer.save_page_image(img, index)  # 保存图片到临时文件夹
                self.label.resize(img.width(), img.height())
                # print('%d  %d' % (self.label.x(), self.label.y()))
                # print('%d  %d' % (self.scrollArea.x(), self.scrollArea.y()))

                # rw = img.width() / self.label.width()
                # rh = img.height() / self.label.height()
                # if rw >= rh:
                #     ratio = rw
                # else:
                #     ratio = rh
                # new_img = img.scaled(img.width() / ratio, img.height() / ratio, QtCore.Qt.KeepAspectRatio)
                # pixmap = QtGui.QPixmap.fromImage(new_img)
                # data = img.tobytes("raw", "RGB")
                # qim = QtGui.QImage.fromData(data)
                # qim = QtGui.QImage(data, img.size[0], img.size[1], QtGui.QImage.Format_ARGB32)
                # qim = ImageQt(img)
                pixmap = QtGui.QPixmap.fromImage(img)
                self.label.setPixmap(pixmap)
                # self.label.resize(pixmap.size())
                # self.label.setScaledContents(True)  # 图片自适应
                # self.label.setPixmap(pixmap1)
        except Exception as e:
            print("show_page: %s " % e)

    def slot_creat_pdf(self):
        self.dealer.creat_new_pdf(self.new_pdf_name)

    def slot_open(self):
        try:
            # fileName_choose, filetype = QtWidgets.QFileDialog.getOpenFileName(
            #     self, "选取文件", self.cwd,  # 起始路径
            #     "Pdf Files (*.pdf, *.pdf)")  # 设置文件扩展名过滤,用双分号间隔
            # if fileName_choose == "":
            #     AnimationWin("\n取消了选择")
            #     return
            # self.file_pdf = fileName_choose
            # print("\n你选择的文件为: %s" % fileName_choose)
            # print("文件筛选器类型: ", filetype)

            # self.total_page = self.dealer.read_Pdf(self.file_pdf)
            # self.total_page = self.dealer.read_Pdf("2019版一建《市政》电子教材.pdf")
            self.total_page = self.dealer.read_Pdf("./2019版一建《市政》电子教材.pdf")
            self.horizontalScrollBar.setMaximum(self.total_page-1)
            # self.horizontalScrollBar.setMinimum(1)
            self.slot_page_changed(0)

        except Exception as e:
            print("slot_open: %s " % e)

    def slot_page_changed(self, value):
        self.cur_page = value
        self.horizontalScrollBar.setToolTip('第 %d 页' % (value+1))
        # print(value)
        self.show_page(self.cur_page)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

    # localtime = time.asctime(time.localtime(time.time()))
    # print("开始时间为 :", localtime)
    # delLogo_pdf = DealPdf()
    # delLogo_pdf.run()
    # localtime = time.asctime(time.localtime(time.time()))
    # print("结束时间为 :", localtime)
