#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Project: PyCharm
# @File    : parsePdf.py
# @Author  : tiger
# @Email   : shdorado@126.com
# @Time    : 2020/4/6 17:40

import sys
import os
from io import StringIO
import io
import re
import time
from PyPDF4 import PdfFileReader, PdfFileWriter
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import TextConverter
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator
import fitz
import zipfile
import shutil
import glob
from PIL import Image, PngImagePlugin
from multiprocessing import cpu_count
from multiprocessing import Pool, Manager
import cv2 as cv
import numpy as np
import random
import psutil
# from wand.image import Image
# from wand.color import Color
from utilities import Utils

"""
目标：从pdf文件中抽取出含有关键字的页面，并将这些页面合并一个新的pdf文件
"""


def PDF_Img(pdfPath, imagePath):
    t0 = time.perf_counter()  # 生成图片初始时间

    if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
        os.makedirs(imagePath)  # 若图片文件夹不存在就创建

    pdfDoc = fitz.open(pdfPath)

    c1, c2 = 120, 50
    page_count = pdfDoc.pageCount
    for pg in range(page_count):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 2.33333333  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 2.33333333
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        # rect = page.rect  # 页面大小
        # mp = rect.tl + (rect.bl - (0, 75 / zoom_x))  # 矩形区域    56=75/1.3333
        # clip = fitz.Rect(mp, rect.br)  # 想要截取的区域
        # pix = page.getPixmap(matrix=mat, alpha=False, clip=clip)  # 将页面转换为图像

        pix = page.getPixmap(matrix=mat, alpha=False)

        # for x in range(pix.w):
        #     for y in range(pix.h):
        #         if pix.pixel(x, y)[0] > c1:
        #             pix.setPixel(x, y, [254, 254, 254])
        #         else:
        #             pix.setPixel(x, y, [c2, c2, c2])

        new_name = os.path.join(imagePath, f'img{pg}.png')  # 生成图片的名称

        if pix.n < 5:  # 如果pix.n<5,可以直接存为PNG
            pix.writePNG(new_name)  # 将图片写入指定的文件夹内
        else:  # 否则先转换CMYK
            pix0 = fitz.Pixmap(fitz.csRGB, pix)
            pix0.writePNG(new_name)
            pix0 = None

        pix = None  # 释放资源
        print("处理了第{}页".format(pg))

    pdfDoc.close()

    t1 = time.perf_counter()  # 图片完成时间
    print("总共处理了{}页".format(page_count))
    print("运行时间:{}s".format(t1 - t0))


# 除掉 pdf里所有杂色，仅留黑色文字
# 使用正则表达式查找PDF中的图片
def pdf2pic(pdf_path, pic_path):
    """
    # 从pdf中提取图片
    :param pdf_path: pdf的路径
    :param pic_path: 图片保存的路径
    :return:
    """
    # pic_path = r'C:\Users\big\Desktop\tt'

    t0 = time.perf_counter()  # 生成图片初始时间

    # 使用正则表达式来查找图片
    checkXO = r"/Type(?= */XObject)"
    checkIM = r"/Subtype(?= */Image)"

    doc = fitz.open(pdf_path)  # 打开pdf文件
    img_count = 0  # 图片计数
    len_XREF = doc._getXrefLength()  # 获取对象数量长度

    # 打印PDF的信息
    print("文件名:{}, 页数: {}, 对象: {}".format(pdf_path, len(doc), len_XREF - 1))

    c1, c2 = 170, 50
    # 遍历每一个对象
    # for i in range(1, 7780):
    # for i in range(len_XREF - 1, 0, -1):
    for i in range(1, len_XREF):
        text = doc._getXrefString(i)  # 定义对象字符串
        isXObject = re.search(checkXO, text)  # 使用正则表达式查看是否是对象
        isImage = re.search(checkIM, text)  # 使用正则表达式查看是否是图片

        if not isXObject or not isImage:  # 如果不是对象也不是图片，则continue
            continue

        img_count += 1
        # print(i, img_count)
        # continue

        pix = fitz.Pixmap(doc, i)  # 根据索引生成图像 生成图像对象
        # print(type(pix), pix.w, pix.pixel(1, 2))
        # return

        for x in range(pix.w):
            for y in range(pix.h):
                if pix.pixel(x, y)[0] > c1:
                    pix.setPixel(x, y, [254, 254, 254])
                else:
                    pix.setPixel(x, y, [c2, c2, c2])

        # print(pix.pixel(1, 2))

        # # 根据pdf的路径生成图片的名称
        # # new_name = pdf_path.replace('\\', '_') + "_img{}.png".format(imgcount)
        # # new_name = new_name.replace(':', '')
        new_name = os.path.join(pic_path, f'{img_count}.png')
        # # print(new_name)
        # # new_name = "图片{}.png".format(imgcount)  # 生成图片的名称
        #
        if pix.n < 5:  # 如果pix.n<5,可以直接存为PNG
            pix.writePNG(new_name)
        else:  # 否则先转换CMYK
            pix0 = fitz.Pixmap(fitz.csRGB, pix)
            pix0.writePNG(new_name)
            pix0 = None

        pix = None  # 释放资源
        print("提取了第{}张图片".format(img_count))

        # t1 = time.perf_counter()  # 图片完成时间
        # print("运行时间:{}s".format(t1 - t0))

        # img = Image.open(os.path.join(pic_path, new_name))
        # # print(type(img))
        # img = img.convert('RGBA')
        # pixdata = img.load()

        # for y in range(img.size[1]):
        #     for x in range(img.size[0]):
        #         if pixdata[x, y][0] > c1 and pixdata[x, y][1] > c1 and pixdata[x, y][2] > c1:
        #             pixdata[x, y] = (255, 255, 255, 255)
        #         else:
        #             pixdata[x, y] = (c2, c2, c2, 255)
        #             # pixdata[x, y] = (pixdata[x, y][0] - c2, pixdata[x, y][1] - c2, pixdata[x, y][2] - c2, 255)
        #
        # img.show()

    doc.close()

    t1 = time.perf_counter()  # 图片完成时间
    print("总共提取了{}张图片".format(img_count))
    print("运行时间:{}s".format(t1 - t0))


# 多进程提取图片并保存
def worker(i, img_count, pdf_path, pic_path):
    # print("进程%d开始执行,进程号为%d" % (img_count, os.getpid()))
    # print(i, img_count, pdf_path, pic_path)
    # t0 = time.perf_counter()  # 生成图片初始时间

    doc = fitz.open(pdf_path)  # 打开pdf文件
    # trans = fitz.Matrix(2, 2).preRotate(0)
    pix = fitz.Pixmap(doc, i)  # 根据索引生成图像 生成图像对象
    # pix.setResolution(pix.w // 2, pix.h // 2)
    # print(type(pix))

    c1, c2 = 140, 50

    # print(type(pix), pix.w, pix.pixel(1, 2))
    for x in range(pix.w):
        for y in range(pix.h):
            if pix.pixel(x, y)[0] > c1:
                pix.setPixel(x, y, [255, 255, 255])
            else:
                pix.setPixel(x, y, [c2, c2, c2])
    # print(pix.pixel(1, 2))

    # # 根据pdf的路径生成图片的名称
    new_name = os.path.join(pic_path, f'{img_count}.png')

    if pix.n < 5:  # 如果pix.n<5,可以直接存为PNG
        pix.writePNG(new_name)
    else:  # 否则先转换CMYK
        pix0 = fitz.Pixmap(fitz.csRGB, pix)
        pix0.writePNG(new_name)
        pix0 = None

    pix = None  # 释放资源
    doc.close()

    # t1 = time.perf_counter()  # 图片完成时间
    # print(f"处理了第{img_count}张图片     运行时间:{t1 - t0}s")


# 进程池处理大文件 pdf， 去颜色
def dealpdf():
    """
    # 从pdf中提取图片
    :param pdf_path: pdf的路径
    :param pic_path: 图片保存的路径
    :return:
    """
    pdf_path = r'C:\Users\big\Desktop\曹经纬 习题集.pdf'
    pic_path = r'C:\Users\big\Desktop\tt'

    for cpu in range(7, 8):
        t0 = time.perf_counter()  # 生成图片初始时间

        pool = Pool(processes=cpu)  # 创建4个进程

        # 使用正则表达式来查找图片
        checkXO = r"/Type(?= */XObject)"
        checkIM = r"/Subtype(?= */Image)"

        doc = fitz.open(pdf_path)  # 打开pdf文件
        img_count = 0  # 图片计数
        len_XREF = doc._getXrefLength()  # 获取对象数量长度

        # 打印PDF的信息
        # print("开始处理文件:{}, 页数: {}, 对象: {}".format(pdf_path, len(doc), len_XREF - 1))

        # 遍历每一个对象
        # for i in range(1, 7780):
        for i in range(len_XREF - 1, 0, -1):
            # for i in range(1, lenXREF):
            text = doc._getXrefString(i)  # 定义对象字符串
            isXObject = re.search(checkXO, text)  # 使用正则表达式查看是否是对象
            isImage = re.search(checkIM, text)  # 使用正则表达式查看是否是图片

            if not isXObject or not isImage:  # 如果不是对象也不是图片，则continue
                continue

            img_count += 1
            # print(i, img_count)

            pool.apply_async(worker, (i, img_count, pdf_path, pic_path))

            # t1 = time.perf_counter()  # 图片完成时间
            # print("运行时间:{}s".format(t1 - t0))

            # img = Image.open(os.path.join(pic_path, new_name))
            # # print(type(img))
            # img = img.convert('RGBA')
            # pixdata = img.load()

            # for y in range(img.size[1]):
            #     for x in range(img.size[0]):
            #         if pixdata[x, y][0] > c1 and pixdata[x, y][1] > c1 and pixdata[x, y][2] > c1:
            #             pixdata[x, y] = (255, 255, 255, 255)
            #         else:
            #             pixdata[x, y] = (c2, c2, c2, 255)
            #             # pixdata[x, y] = (pixdata[x, y][0] - c2, pixdata[x, y][1] - c2, pixdata[x, y][2] - c2, 255)
            #
            # img.show()

        pool.close()  # 关闭进程池，表示不能再往进程池中添加进程，需要在join之前调用
        pool.join()  # 等待进程池中的所有进程执行完毕
        # print("Sub-process(es) done.")
        doc.close()

        t1 = time.perf_counter()  # 图片完成时间
        print(f"共提取{img_count}张图片    进程池:{cpu} 运行时间:{t1 - t0}s")


# 多进程 提取 pdf文件的图片并保存
def worker2(page_ID):
    pdf_file = r'C:\Users\big\Desktop\曹经纬 习题集.pdf'
    pic_path = r'C:\Users\big\Desktop\tt'
    # pdffile = glob.glob(pdf_file)[0]

    # print("进程%d开始执行,进程号为%d" % (img_count, os.getpid()))
    t0 = time.perf_counter()  # 生成图片初始时间

    # doc = fitz.open(pdffile)
    doc = fitz.open(pdf_file)

    # for pg in range(0, doc.pageCount):
    page = doc[page_ID]
    # zoom = int(100)  # 原来的分辨率
    zoom = 4
    rotate = int(0)
    trans = fitz.Matrix(zoom, zoom).preRotate(rotate)
    # pm = page.getPixmap(matrix=trans, alpha=True)
    pix = page.getPixmap(matrix=trans, alpha=0)  # alpha=0 白色背景  不透明

    c1, c2 = 140, 50
    # print(type(pix), pix.w, pix.pixel(1, 2))
    for x in range(pix.w):
        for y in range(pix.h):
            if pix.pixel(x, y)[0] > c1:
                pix.setPixel(x, y, [255, 255, 255])
            else:
                pix.setPixel(x, y, [c2, c2, c2])

    # 根据pdf的路径生成图片的名称
    new_name = os.path.join(pic_path, f'{page_ID + 1}.png')

    if pix.n < 5:  # 如果pix.n<5,可以直接存为PNG
        pix.writePNG(new_name)
    else:  # 否则先转换CMYK
        pix0 = fitz.Pixmap(fitz.csRGB, pix)
        pix0.writePNG(new_name)
        pix0 = None

    pix = None  # 释放资源
    page = None
    doc.close()

    t1 = time.perf_counter()  # 图片完成时间
    print(f"处理了第{page_ID + 1}张图片     运行时间:{t1 - t0}s")


# 进程池处理大文件 pdf， 去颜色
def dealpdf2():
    """
    # 从pdf中提取图片
    :param pdf_path: pdf的路径
    :param pic_path: 图片保存的路径
    :return:
    """
    pdf_path = r'C:\Users\big\Desktop\曹经纬 习题集.pdf'
    pic_path = r'C:\Users\big\Desktop\tt'

    for cpu in range(7, 8):
        t0 = time.perf_counter()  # 生成图片初始时间

        pool = Pool(processes=cpu)  # 创建4个进程

        doc = fitz.open(pdf_path)  # 打开pdf文件
        count = doc.pageCount
        count = 5
        doc.close()
        # 打印PDF的信息
        # print("开始处理文件:{}, 页数: {}, 对象: {}".format(pdf_path, len(doc), len_XREF - 1))

        # 遍历每一页面
        for i in range(count):
            pool.apply_async(worker2, (i,))

            # t1 = time.perf_counter()  # 图片完成时间
            # print("运行时间:{}s".format(t1 - t0))

            # img = Image.open(os.path.join(pic_path, new_name))
            # # print(type(img))
            # img = img.convert('RGBA')
            # pixdata = img.load()

            # for y in range(img.size[1]):
            #     for x in range(img.size[0]):
            #         if pixdata[x, y][0] > c1 and pixdata[x, y][1] > c1 and pixdata[x, y][2] > c1:
            #             pixdata[x, y] = (255, 255, 255, 255)
            #         else:
            #             pixdata[x, y] = (c2, c2, c2, 255)
            #             # pixdata[x, y] = (pixdata[x, y][0] - c2, pixdata[x, y][1] - c2, pixdata[x, y][2] - c2, 255)
            #
            # img.show()

        pool.close()  # 关闭进程池，表示不能再往进程池中添加进程，需要在join之前调用
        pool.join()  # 等待进程池中的所有进程执行完毕
        # print("Sub-process(es) done.")

        t1 = time.perf_counter()  # 图片完成时间
        print(f"共提取{count}张图片    进程池:{cpu} 运行时间:{t1 - t0}s")


# 把处理好的图片变回 pdf
def pic2pdf(pdf_file, pic_path):
    """
    把图片插入 pdf
    :param pdf_file:要保存的pdf文件
    :param pic_path:图片目录
    :return:
    """

    t0 = time.perf_counter()  # 生成图片初始时间

    ll = sorted(glob.glob(f"{pic_path}/*"))
    Utils.sort_nicely(ll)
    # ll = ll[0:4]

    doc = fitz.open()
    for img in ll:  # 读取图片，确保按文件名排序
        print(img)
        imgdoc = fitz.open(img)  # 打开图片
        pdfbytes = imgdoc.convertToPDF()  # 使用图片创建单页的 PDF
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)  # 将当前页插入文档

    if os.path.exists(pdf_file):
        os.remove(pdf_file)
    doc.save(pdf_file)  # 保存pdf文件
    doc.close()

    t1 = time.perf_counter()  # 图片完成时间
    print("总共合并了{}张图片".format(len(ll)))
    print("运行时间:{}s".format(t1 - t0))


# 把处理好的图片变回 pdf
def pic_pdf(pdf_name, pic_path):
    file_list = os.listdir(pic_path)
    pic_name = []
    im_list = []
    for x in file_list:
        if "jpg" in x or 'png' in x or 'jpeg' in x:
            pic_name.append(x)

    pic_name.sort()
    new_pic = []

    for x in pic_name:
        if "jpg" in x:
            new_pic.append(x)

    for x in pic_name:
        if "png" in x:
            new_pic.append(x)

    Utils.sort_nicely(new_pic)
    # new_pic = new_pic[0:4]
    print("hec", len(new_pic), new_pic)

    im1 = Image.open(os.path.join(pic_path, new_pic[0]))  # 第一幅图像文件
    w, h = im1.size
    scale = 4
    im1 = im1.resize((w // scale, h // scale), Image.ANTIALIAS)
    print(w, h, im1.size)
    new_pic.pop(0)
    for i in new_pic:
        img = Image.open(os.path.join(pic_path, i))
        w, h = img.size
        img = img.resize((w // scale, h // scale), Image.ANTIALIAS)
        # print(type(img))

        # im_list.append(Image.open(i))
        if img.mode == "RGBA":
            img = img.convert('RGB')
            im_list.append(img)
        else:
            im_list.append(img)
    # out = im1.resize((w_new, h_new), Image.ANTIALIAS)
    im1.save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=im_list)

    print("输出文件名称：", pdf_name)


def parse(pdf_file):
    """解析PDF文本，并保存到TXT文件中"""
    fp = open(pdf_file, 'rb')
    # 来创建一个pdf文档分析器
    parser = PDFParser(fp)
    # 创建一个PDF文档对象存储文档结构
    document = PDFDocument(parser)
    # 检查文件是否允许文本提取
    if not document.is_extractable:
        print('nono')
        raise PDFTextExtractionNotAllowed
    else:
        # 创建一个PDF资源管理器对象来存储共赏资源
        rsrcmgr = PDFResourceManager()
        # 设定参数进行分析
        laparams = LAParams()
        # 创建一个PDF设备对象
        # device=PDFDevice(rsrcmgr)
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # 处理每一页
        pageindex = []
        i = 0
        pattern = re.compile("微信")
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            # # 接受该页面的LTPage对象
            layout = device.get_result()  # return text image line curve
            for x in layout:
                if isinstance(x, LTText):
                    if pattern.search(x.get_text()):
                        pageindex.append(i)
            i += 1

    pdf_output = PdfFileWriter()
    pdf_input = PdfFileReader(fp)
    # 获取 pdf 共用多少页
    for j in pageindex:
        pdf_output.addPage(pdf_input.getPage(j))
    final_path = os.path.join(r"C:\Users\big\Desktop\final.pdf")
    with open(final_path, "wb") as f:
        pdf_output.write(f)
    fp.close()


# 解析pdf文件，获取文件中包含的各种对象
def parse1(pdf_path):
    # print(pdf_path)
    fp = open(pdf_path, 'rb')  # 以二进制读模式打开
    # print(type(fp))
    # 用文件对象来创建一个pdf文档分析器
    parser = PDFParser(fp)
    # 创建一个PDF文档存储文档结构,提供密码初始化，没有就不用传该参数
    doc = PDFDocument(parser, password='')
    # 连接分析器 与文档对象
    # parser.set_document(doc)
    # doc.set_parser(parser)
    # print(type(doc))

    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    # doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源 #caching = False不缓存
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()  # PDF页面聚合对象
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)  # 创建一个PDF设备对象
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 用来计数页面，图片，曲线，figure，水平文本框等对象的数量
        num_page, num_image, num_curve, num_figure, num_TextBoxHorizontal = 0, 0, 0, 0, 0
        num_line, num_rect, num_textbox, num_textline = 0, 0, 0, 0

        # 循环遍历列表，每次处理一个page的内容
        # for page in doc.get_pages():  # doc.get_pages() 获取page列表
        # for page in PDFPage.get_pages(fp, pagenos=set(), maxpages=0,
        # password='', caching=True, check_extractable=True)
        for page in PDFPage.create_pages(doc):
            num_page += 1  # 页面增一
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            # print(type(layout))
            for x in layout:
                # if hasattr(x, "get_text"):
                #     fileNames = os.path.splitext(pdf_path)
                #     with open(fileNames[0] + '.txt', 'a', encoding="utf-8") as f:
                #         results = x.get_text()
                #         # print(results)
                #         f.write(results + '\n')

                if isinstance(x, LTImage):  # 图像对象
                    num_image += 1
                if isinstance(x, LTCurve):  # 通用的Bezier曲线对象
                    num_curve += 1
                if isinstance(x, LTLine):  # 直线对象。可用于分离文本或附图
                    num_line += 1
                if isinstance(x, LTRect):  # 矩形对象。可用于框架的另一图片或数字。
                    num_rect += 1
                # if isinstance(x, LTTextBox):  # 表示一组文本块可能包含在一个矩形区域,
                #     # 包含LTTextLine对象的列表。使用 get_text（）方法返回文本内容
                #     print(type(x))
                #     num_textbox += 1
                if isinstance(x, LTTextLine):  # 单个文本行LTChar对象的列表
                    num_textline += 1
                if isinstance(x, LTFigure):  # figure对象 数字、符号
                    # x = LTFigure
                    print(x.name)
                    num_figure += 1
                if isinstance(x, LTTextBoxHorizontal):  # 如果x是水平文本对象的话, 获取文本内容
                    num_TextBoxHorizontal += 1  # 水平文本框对象增一
                    # 保存文本内容
                    with open(r'C:\Users\big\Desktop\test.txt', 'a', encoding='utf-8') as f:
                        results = x.get_text()
                        f.write(results + '\n')
        print('对象数量：\n',
              f'页面数：{num_page}\n',
              '图片数：%s\n' % num_image,
              'Bezier曲线数：%s\n' % num_curve,
              '直线数：%s\n' % num_line,
              '矩形框数：%s\n' % num_rect,
              '文本块数：%s\n' % num_textbox,
              '文本行数：%s\n' % num_textline,
              '数字、符号数：%s\n' % num_figure,
              '水平文本框：%s\n' % num_TextBoxHorizontal)


def tripimg(pdf_file):
    # trip backgroud images
    doc = fitz.open(pdf_file)
    for i in range(len(doc)):
        imglist = doc.getPageImageList(i)
        for img in imglist:
            xref = img[0]
            if xref == 51:
                doc._deleteObject(xref)
            print(img)
    doc.save(r'C:\Users\big\Desktop\new.pdf')


def convert_pdf_to_txt(path, save_name):
    debug = False
    if debug:
        # 加载内存的方式
        retstr = StringIO()
        fp = StringIO(path)
    else:
        # 读取文件的方式
        retstr = open(path, 'rb')
        fp = open(path, 'rb')
    # 创建一个PDF资源管理器对象来存储共享资源,caching = False不缓存
    rsrcmgr = PDFResourceManager(caching=False)
    # 创建一个PDF设备对象
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    # 创建一个PDF解析器对象
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, pagenos=set(), maxpages=0, password='', caching=True, check_extractable=True):
        interpreter.process_page(page)
    fp.close()  # 关闭输入流
    device.close()  # 关闭输出流
    str = retstr.getvalue()
    retstr.close()
    try:
        with open("%s" % save_name, "w") as f:
            for i in str:
                f.write(i)
        print("%s Writing Succeed!" % save_name)
    except:
        print("Writing Failed!")


def word2pic(path, zip_path, tmp_path, store_path):
    """
    Python提取PDF中的图片
    :param path:源文件
    :param zip_path:docx重命名为zip
    :param tmp_path:中转图片文件夹
    :param store_path:最后保存结果的文件夹（需要手动创建）
    :return:
    """

    # 将docx文件重命名为zip文件
    os.rename(path, zip_path)
    # 进行解压
    f = zipfile.ZipFile(zip_path, 'r')
    # 将图片提取并保存
    for file in f.namelist():
        f.extract(file, tmp_path)
    # 释放该zip文件
    f.close()

    # 将docx文件从zip还原为docx
    os.rename(zip_path, path)
    # 得到缓存文件夹中图片列表
    pic = os.listdir(os.path.join(tmp_path, 'word/media'))

    # 将图片复制到最终的文件夹中
    for i in pic:
        # 根据word的路径生成图片的名称
        new_name = path.replace('\\', '_')
        new_name = new_name.replace(':', '') + '_' + i
        shutil.copy(os.path.join(tmp_path + '/word/media', i), os.path.join(store_path, new_name))

    # 删除缓冲文件夹中的文件，用以存储下一次的文件
    for i in os.listdir(tmp_path):
        # 如果是文件夹则删除
        if os.path.isdir(os.path.join(tmp_path, i)):
            shutil.rmtree(os.path.join(tmp_path, i))


def doc2docx(doc_name, docx_name):
    '''
    # doc转docx
    :param doc_name: doc文档路径
    :param docx_name: docx文档路径
    :return:
    '''
    try:
        # 首先将doc转换成docx
        word = client.Dispatch("Word.Application")
        doc = word.Documents.Open(doc_name)
        # 使用参数16表示将doc转换成docx
        doc.SaveAs(docx_name, 16)
        doc.Close()
        word.Quit()
    except:
        pass


# 删除有水印标志的部分
def removeWatermark(wm_text, inputFile, outputFile):
    from PyPDF4 import PdfFileReader, PdfFileWriter
    from PyPDF4.pdf import ContentStream
    from PyPDF4.generic import TextStringObject, NameObject
    from PyPDF4.utils import b_

    with open(inputFile, "rb") as f:
        source = PdfFileReader(f, "rb")
        output = PdfFileWriter()

        for page in range(source.getNumPages()):
            page = source.getPage(page)
            content_object = page["/Contents"].getObject()
            content = ContentStream(content_object, source)

            for operands, operator in content.operations:
                if operator == b_("Tj"):
                    text = operands[0]
                    # import io
                    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码
                    # print(text)
                    if isinstance(text, str) and text.startswith(wm_text):
                        operands[0] = TextStringObject('')

            page.__setitem__(NameObject('/Contents'), content)
            output.addPage(page)

        with open(outputFile, "wb") as outputStream:
            output.write(outputStream)


# 删除水印图片，水印是图片且长宽固定的情况
# 找到所有这些长宽的图片，然后隐藏
def delete_watermark(src, dst, wwidth=963, wheight=215):
    doc = fitz.open(src)
    for page in range(doc.pageCount):
        images = doc.getPageImageList(page)
        print(doc.pageCount, len(images))

        for content in doc[page]._getContents():
            c = doc._getXrefStream(content)
            for _, _, width, height, _, _, _, img, _ in images:
                # print(width, height)
                c = c.replace("/{} Do".format(img).encode(), b"")
                # if wwidth == width and wheight == height:
                #     c = c.replace("/{} Do".format(img).encode(), b"")
            doc._updateStream(content, c)

    dir = os.path.dirname(dst)
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(dir)
    doc.save(dst)


# import hwloc
# topology = hwloc.Topology()
# topology.load()
# print topology.get_nbobjs_by_type(hwloc.OBJ_CORE)


def pdf_delete_water_mark(pdf_file_src, pdf_file_dst):
    try:
        t0 = time.perf_counter()  # 生成图片初始时间

        if not os.path.isfile(pdf_file_src):
            LINE = str(sys._getframe().f_lineno)
            ex = Exception(LINE + ": pdf源文件不存在")  # 1> 创建异常对象
            raise ex  # 2> raise 主动抛出异常

        if os.path.isfile(pdf_file_dst):
            os.remove(pdf_file_dst)  # 删除目标文件

        # if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
        #     os.makedirs(imagePath)  # 若图片文件夹不存在就创建

        doc_src = fitz.open(pdf_file_src)
        doc_dst = fitz.open()

        # tmp_png = os.path.join(os.environ["TMP"], 'tmp.png')  # 临时图片文件的名称
        tmp_png = './tmp.png'  # 临时图片文件的名称
        print(tmp_png)

        c1, c2 = 120, 50
        page_count = doc_src.pageCount
        # print(page_count)

        for pg in range(1):
            page = doc_src[pg]
            rotate = int(0)
            # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
            # 此处若是不做设置，默认图片大小为：792X612, dpi=96
            zoom_x = 2.5  # (1.33333333-->1056x816)   (2-->1584x1224)
            zoom_y = 2.5
            mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
            # rect = page.rect  # 页面大小
            # mp = rect.tl + (rect.bl - (0, 75 / zoom_x))  # 矩形区域    56=75/1.3333
            # clip = fitz.Rect(mp, rect.br)  # 想要截取的区域
            # pix = page.getPixmap(matrix=mat, alpha=False, clip=clip)  # 将页面转换为图像
            pix = page.getPixmap(matrix=mat, alpha=False)
            # print('0:', type(pix))

            for x in range(pix.w):
                for y in range(pix.h):
                    if 180 < pix.pixel(x, y)[0] or \
                            (120 < pix.pixel(x, y)[0] < 125 and
                             120 < pix.pixel(x, y)[1] < 125 and
                             190 < pix.pixel(x, y)[2] < 195) or \
                            (150 < pix.pixel(x, y)[0] < 155 and
                             220 < pix.pixel(x, y)[1] < 235 and
                             185 < pix.pixel(x, y)[2] < 195):
                        # if 180 < pix.pixel(x, y)[0] and \
                        #         220 < pix.pixel(x, y)[1] and \
                        #         220 < pix.pixel(x, y)[2]:
                        pix.setPixel(x, y, [254, 254, 254])
                    # else:
                    #     pix.setPixel(x, y, [c2, c2, c2])

            # new_name = os.path.join(imagePath, f'img{pg}.png')  # 生成图片的名称

            if pix.n < 5:  # 如果pix.n<5,可以直接存为PNG
                pix.writePNG(tmp_png)  # 将图片写入指定的文件夹内
            else:  # 否则先转换CMYK
                pix0 = fitz.Pixmap(fitz.csRGB, pix)
                pix0.writePNG(tmp_png)
                pix0 = None

            img_doc = fitz.open(tmp_png)  # 打开图片
            pdf_bytes = img_doc.convertToPDF()  # 使用图片创建单页的 PDF
            pdf_img = fitz.open("pdf", pdf_bytes)
            doc_dst.insertPDF(pdf_img)  # 将当前页插入文档

            pix = None  # 释放资源
            print("处理了第{}页".format(pg))

        doc_src.close()
        doc_dst.save(pdf_file_dst)  # 保存pdf文件
        doc_dst.close()
        # os.remove(tmp_png)  # 删除临时文件
        # os.unlink(tmp_png)

        t1 = time.perf_counter()  # 图片完成时间
        print("总共处理了{}页".format(page_count))
        print("运行时间:{}s".format(t1 - t0))

    except Exception as result:
        print(result)


def get_x_ave(pix, x_start, x_end):
    try:
        wide = 100  # 宽竖条的宽度
        x_offset = 5  # 窄竖条的宽度
        y_div = 5  # 竖向分成几段，处理直线倾斜
        data = [0] * y_div
        color = [[0, 254, 0], [254, 254, 0], [0, 0, 254], [0, 254, 254]]
        y_offset = pix.h // y_div

        c = 230

        # for x in range(x_start, x_end):
        #     for y in range(pix.h//2):
        #         pix.setPixel(x, y, [254, 0, 0])

        for k in range(y_div):
            tmp = []
            for x in range(x_start, x_end, x_offset):
                count = 0
                for x1 in range(x, x + x_offset):
                    for y in range(y_offset * k, y_offset * (k + 1)):
                        if pix.pixel(x1, y)[0] < c:
                            count += 1
                tmp.append((count, x))
            tmp.sort(key=lambda t: t[0], reverse=True)
            # print(tmp)
            data[k] = tmp[0]

            # for x in range(data[k][1], data[k][1] + x_offset):
            #     for y in range(y_offset * k, y_offset * (k + 1)):
            #         pix.setPixel(x, y, color[k % 4])

        # print(data)
        xs = [data[i][1] for i in range(len(data))]
        xs.sort()
        mid_i = len(xs) // 2
        mid = xs[mid_i]
        cha = mid - xs[mid_i - 1]

        for i in range(len(xs)):
            if abs(abs(xs[i] - mid) - cha) > x_offset * y_div:
                xs[i] = mid  # 偏差太大的值回归平均值
        ave = sum(xs) // len(data) + x_offset // 2
        # 求均值
        # a_mean = np.mean(data, axis=0)

        # if ave < 130:
        #     print(ave)
        #     ave = 130

        # for x in range(ave - 20, ave + 20):
        #     for y in range(pix.h):
        #         pix.setPixel(x, y, [254, 254, 254])

        # for x in range(ave - x_offset // 2, ave + x_offset // 2):
        #     for y in range(pix.h):
        #         pix.setPixel(x, y, [254, 0, 0])

        # for x in range(pix.w//2):
        #     for y in range(pix.h-160, pix.h):
        #         pix.setPixel(x, y, [254, 0, 0])

        return ave

    except Exception as e:
        print(e)
        return 0


def pdf_halve_pages(pdf_file_src, pdf_file_dst):
    try:
        t0 = time.perf_counter()  # 生成图片初始时间

        if not os.path.isfile(pdf_file_src):
            LINE = str(sys._getframe().f_lineno)
            ex = Exception(LINE + ": pdf源文件不存在")  # 1> 创建异常对象
            raise ex  # 2> raise 主动抛出异常

        if os.path.isfile(pdf_file_dst):
            os.remove(pdf_file_dst)  # 删除目标文件

        # if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
        #     os.makedirs(imagePath)  # 若图片文件夹不存在就创建

        doc_src = fitz.open(pdf_file_src)
        doc_dst = fitz.open()

        # tmp_png = os.path.join(os.environ["TMP"], 'tmp.png')  # 临时图片文件的名称
        tmp_png = './tmp.png'  # 临时图片文件的名称
        # print(tmp_png)

        zoom_x = 2.5  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 2.5
        wide = 150

        page_count = doc_src.pageCount
        # print(page_count)
        # nn = Utils.rand_int(0, page_count)
        # nn = 9
        # print(nn)
        for pg in range(page_count):
            page = doc_src[pg]
            rotate = int(0)
            # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
            # 此处若是不做设置，默认图片大小为：792X612, dpi=96

            mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
            # rect = page.rect  # 页面大小
            # mp = rect.tl + (rect.bl - (0, 75 / zoom_x))  # 矩形区域    56=75/1.3333
            # clip = fitz.Rect(mp, rect.br)  # 想要截取的区域
            # pix = page.getPixmap(matrix=mat, alpha=False, clip=clip)  # 将页面转换为图像
            pix = page.getPixmap(matrix=mat, alpha=False)
            # print('0:', type(pix))
            # pix = fitz.fitz.Pixmap()

            # print(pix.w, pix.h)
            mid = pix.w // 2
            x_start = mid - wide
            x_end = mid + wide

            # if pg == 0 or pg == 20:  # 特殊页面的处理
            #     for x in range(50):
            #         for y in range(pix.h):
            #             pix.setPixel(x, y, [254, 254, 254])

            ave = get_x_ave(pix, x_start, x_end)
            # ave0 = get_x_ave(pix, 0, 120)
            ave0 = ave * 2 - pix.w
            ave0 = ave0 if ave0 > -1 else 0
            # print(ave0)

            # new_name = os.path.join(imagePath, f'img{pg}.png')  # 生成图片的名称

            if pix.n < 5:  # 如果pix.n<5,可以直接存为PNG
                pix.writePNG(tmp_png)  # 将图片写入指定的文件夹内
            else:  # 否则先转换CMYK
                pix0 = fitz.Pixmap(fitz.csRGB, pix)
                pix0.writePNG(tmp_png)
                pix0 = None

            img = cv.imread(tmp_png)
            # [h, w] = img.shape[:2]
            # print(tmp_png, (h, w))
            png1, png2 = r'./tmp1.png', r'./tmp2.png'
            cv.imwrite(png1, img[:pix.h - 160, ave0:ave, :])
            cv.imwrite(png2, img[:pix.h - 160, ave + 1:, :])

            img_doc = fitz.open(png1)  # 打开图片
            pdf_bytes = img_doc.convertToPDF()  # 使用图片创建单页的 PDF
            pdf_img = fitz.open("pdf", pdf_bytes)
            doc_dst.insertPDF(pdf_img)  # 将当前页插入文档
            img_doc.close()

            img_doc = fitz.open(png2)  # 打开图片
            pdf_bytes = img_doc.convertToPDF()  # 使用图片创建单页的 PDF
            pdf_img = fitz.open("pdf", pdf_bytes)
            doc_dst.insertPDF(pdf_img)  # 将当前页插入文档
            img_doc.close()

            pix = None  # 释放资源
            print("处理了第{}页".format(pg))

        doc_src.close()
        doc_dst.save(pdf_file_dst)  # 保存pdf文件
        doc_dst.close()
        os.remove(tmp_png)  # 删除临时文件
        os.remove(png1)  # 删除临时文件
        os.remove(png2)  # 删除临时文件
        # os.unlink(tmp_png)

        t1 = time.perf_counter()  # 图片完成时间
        print("总共处理了{}页".format(page_count))
        print("运行时间:{}s".format(t1 - t0))

    except Exception as result:
        print(result)


# 定义图像拼接函数
def add_img(f1, f2, task_img):
    img1 = Image.open(f1)
    img2 = Image.open(f2)

    # width, height = max(img1.size[0], img2.size[0]), img1.size[1]+img2.size[1]
    width, height = img1.size[0]+img2.size[0]+10, max(img1.size[1], img2.size[1])
    print(img1.size, img2.size, width, height)

    # 创建空白图片
    target = Image.new('RGB', (width, height), (255, 255, 255))

    # 创建header Image对象，paste拼接到空白图片指定位置target.paste(img_h, (0, 0))
    # img_h = img_header(os.path.join(tasktheme_img_path, task_img))
    # 图片合成paste 参数中img_h表示Image对象，(0, 0)表示x,y轴位置 单位像素 target的左上角为原点 y轴向下
    target.paste(img1, (0, 0))
    # target.paste(img2, (0, img1.size[1]))
    target.paste(img2, (img1.size[0]+10, 0))

    target.save(task_img)
    # for each in files:
    #     # img = PngImagePlugin.PngImageFile()
    #     print(img.size)
    # to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE))  # 创建一个新图
    # # 循环遍历，把每张图片按顺序粘贴到对应位置上
    # for y in range(1, IMAGE_ROW + 1):
    #     for x in range(1, IMAGE_COLUMN + 1):
    #         from_image = Image.open(IMAGES_PATH + image_names[IMAGE_COLUMN * (y - 1) + x - 1]).resize(
    #             (IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
    #         to_image.paste(from_image, ((x - 1) * IMAGE_SIZE, (y - 1) * IMAGE_SIZE))
    # return to_image.save(IMAGE_SAVE_PATH)  # 保存新图


# 清洗图片，去灰底
def clean_img(img_file):
    img_array = np.array(Image.open(img_file))
    arr1 = img_array[:]
    print(arr1.shape)
    print(img_array[2, 2])
    for x in range(1, arr1.shape[0]):
        for y in range(1, arr1.shape[1]):
            a = img_array[x, y][0] if img_array[x, y][0] < 150 else 255
            # b = img_array[x, y][1] if img_array[x, y][1] < 150 else 255
            # c = img_array[x, y][2] if img_array[x, y][2] < 150 else 255
            arr1[x, y] = (a, a, a)
            # arr1[x, y] = (b, b, b)
            # arr1[x, y] = (c, c, c)

    image_arr = Image.fromarray(arr1)
    image_arr.save(r'C:\Users\big\Desktop\tt.jpg')


def main():
    # print('cpu逻辑个数：', cpu_count())
    # print('cpu物理个数：', psutil.cpu_count(logical=False))
    # print('cpu逻辑个数：', psutil.cpu_count())
    # print('cpu逻辑个数：', os.cpu_count())
    pic_path = r'C:\Users\big\Desktop\tt'
    pdf_f = r'E:\考证\岩土\岩土 基础 历年真题\公共基础真题\2009-2013年注册岩土公共基础考试真题空白卷.pdf'
    pdf_f1 = r'C:\Users\big\Desktop\t.pdf'
    txt_f = r'C:\Users\big\Desktop\final.txt'

    # pdf_delete_water_mark(r'E:\考证\岩土\岩土 基础 历年真题\18 19年真题.pdf',
    #                       r'E:\考证\岩土\岩土 基础 历年真题\new.pdf')
    # pdf_delete_water_mark(r'E:\考证\岩土\岩土 基础 历年真题\09-17 基础 真题.pdf',
    #                       r'E:\考证\岩土\岩土 基础 历年真题\new.pdf')
    # pdf_halve_pages(r'C:\Users\big\Desktop\机器学习实战.pdf', r'C:\Users\big\Desktop\new.pdf')
    # clean_img(r'C:\Users\big\Desktop\仲裁.jpg')
    add_img(r'C:\Users\big\Desktop\建造师工资水平1.png',
            r'C:\Users\big\Desktop\建造师工资水平2.png',
            r'C:\Users\big\Desktop\last.png')
    # add_img(r'C:\Users\big\Desktop\last.png', r'C:\Users\big\Desktop\证据2.png'
    #         , r'C:\Users\big\Desktop\last.png')
    # 创建保存图片的文件夹
    # if os.path.exists(pic_path):
    #     print("文件夹已存在，不必重新创建！")
    #     pass
    # else:
    #     os.mkdir(pic_path)
    # pdf2pic(pdf_f, pic_path)
    # PDF_Img(pdf_f, pic_path)
    # tripimg(pdf_f)
    # parse1(pdf_f)
    # convert_pdf_to_txt(pdf_f, txt_f)
    # time2 = time.time()
    # print("总共消耗时间为:", time2 - time1)
    # removeWatermark(u'微信搜一搜', pdf_f, r'C:\Users\big\Desktop\t.pdf')
    # delete_watermark(pdf_f, r'C:\Users\big\Desktop\t.pdf')
    # pdf2pic(r'C:\Users\big\Desktop\曹经纬 习题集.pdf', r'C:\Users\big\Desktop\tt')

    # dealpdf()
    # dealpdf2()
    # pic2pdf(r'C:\Users\big\Desktop\t.pdf', r'C:\Users\big\Desktop\tt')
    # pic_pdf(r'C:\Users\big\Desktop\t.pdf', r'C:\Users\big\Desktop\tt')
    # _run_convert(pdf_f, 0)


if __name__ == '__main__':
    sys.exit(main())
