#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @项目名称: python
# @File    : docManager.py
# @Time    : 2020/3/25 13:42
# @Author  : big
# @Email   : shdorado@126.com

import os
import sys
import random
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QAxContainer import QAxWidget
from uiBridge import UiDocManager
import win32com
from win32com.client import Dispatch
from PyPDF4 import PdfFileReader
from PyPDF4 import PdfFileWriter


class PdfManager(object):

    # region 解密加密的PDF
    @staticmethod
    def get_reader(filename, password):
        try:
            old_file = open(filename, 'rb')
            print('run  jiemi1')
        except Exception as err:
            print('文件打开失败！' + str(err))
            return None

        # 创建读实例
        pdf_reader = PdfFileReader(old_file, strict=False)

        # 解密操作
        if pdf_reader.isEncrypted:
            if password is None:
                print('%s文件被加密，需要密码！' % filename)
                return None
            else:
                if pdf_reader.decrypt(password) != 1:
                    print('%s密码不正确！' % filename)
                    return None
        if old_file in locals():
            old_file.close()
        return pdf_reader

    @staticmethod
    def decrypt_pdf(filename, password, decrypted_filename=None):
        """
        将加密的文件及逆行解密，并生成一个无需密码pdf文件
        :param filename: 原先加密的pdf文件
        :param password: 对应的密码
        :param decrypted_filename: 解密之后的文件名
        :return:
        """
        # 生成一个Reader和Writer
        print('run  jiemi')
        pdf_reader = PdfManager.get_reader(filename, password)
        if pdf_reader is None:
            return
        if not pdf_reader.isEncrypted:
            print('文件没有被加密，无需操作！')
            return
        pdf_writer = PdfFileWriter()

        pdf_writer.appendPagesFromReader(pdf_reader)

        if decrypted_filename is None:
            decrypted_filename = "".join(filename[:-4]) + '_' + 'decrypted' + '.pdf'

        # 写入新文件
        pdf_writer.write(open(decrypted_filename, 'wb'))

    @staticmethod
    def add_encryption(input_pdf, output_pdf, password):
        """
        PDF加密
        :param input_pdf:
        :param output_pdf:
        :param password:
        :return:
        """

        pdf_writer = PdfFileWriter()
        pdf_reader = PdfFileReader(input_pdf)

        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))

        pdf_writer.encrypt(user_pwd=password, owner_pwd=None,
                           use_128bit=True)

        with open(output_pdf, 'wb') as fh:
            pdf_writer.write(fh)

    # decrypt_pdf(r'test.pdf', '')  # 密码不知道，就设置为空
    # endregion

    # region 读写pdf
    @staticmethod
    def getPdfContent(filename):
        """
        粗略读取PDF内容
        :param filename:
        :return:
        """
        pdf = PdfFileReader(open(filename, "rb"))
        content = ""
        for i in range(0, pdf.getNumPages()):
            pageObj = pdf.getPage(i)

            extractedText = pageObj.extractText()
            content += extractedText + "\n"
            # return content.encode("ascii", "ignore")
        return content

    @staticmethod
    def readPdf(readFile='./input.pdf'):
        # 获取 PdfFileReader 对象
        pdfFileReader = PdfFileReader(readFile)
        # 或者这个方式：pdfFileReader = PdfFileReader(open(readFile, 'rb'))
        # 获取 PDF 文件的文档信息
        documentInfo = pdfFileReader.getDocumentInfo()
        print('documentInfo = %s' % documentInfo)
        # 获取页面布局
        pageLayout = pdfFileReader.getPageLayout()
        print('pageLayout = %s ' % pageLayout)

        # 获取页模式
        pageMode = pdfFileReader.getPageMode()
        print('pageMode = %s' % pageMode)

        xmpMetadata = pdfFileReader.getXmpMetadata()
        print('xmpMetadata  = %s ' % xmpMetadata)

        # 获取 pdf 文件页数
        pageCount = pdfFileReader.getNumPages()

        print('pageCount = %s' % pageCount)
        for index in range(0, pageCount):
            # 返回指定页编号的 pageObject
            pageObj = pdfFileReader.getPage(index)
            print('index = %d , pageObj = %s' % (index, type(pageObj)))
            # <class 'PyPDF2.pdf.PageObject'>
            # 获取 pageObject 在 PDF 文档中处于的页码
            pageNumber = pdfFileReader.getPageNumber(pageObj)
            print('pageNumber = %s ' % pageNumber)

    @staticmethod
    def addBlankpage():
        # PDF写入操作
        readFile = './01.pdf'
        outFile = './01_new.pdf'
        pdfFileWriter = PdfFileWriter()

        # 获取 PdfFileReader 对象
        pdfFileReader = PdfFileReader(readFile)  # 或者这个方式：pdfFileReader = PdfFileReader(open(readFile, 'rb'))
        numPages = pdfFileReader.getNumPages()

        for index in range(0, numPages):
            pageObj = pdfFileReader.getPage(index)
            pdfFileWriter.addPage(pageObj)  # 根据每页返回的 PageObject,写入到文件
            pdfFileWriter.write(open(outFile, 'wb'))

        pdfFileWriter.addBlankPage()  # 在文件的最后一页写入一个空白页,保存至文件中
        pdfFileWriter.write(open(outFile, 'wb'))

    @staticmethod
    def create_watermark(input_pdf, output, watermark):
        """
        添加水印
        :param input_pdf: 要加水印的PDF文件路径
        :param output: 要保存PDF的水印版本的路径
        :param watermark: 包含水印图像或文本的PDF
        :return: 
        """

        watermark_obj = PdfFileReader(watermark)
        watermark_page = watermark_obj.getPage(0)
        pdf_reader = PdfFileReader(input_pdf)
        pdf_writer = PdfFileWriter()
        # 给所有页面添加水印
        for page in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page)
            page.mergePage(watermark_page)
            pdf_writer.addPage(page)
        with open(output, 'wb') as out:
            pdf_writer.write(out)

    # endregion

    # region 分隔与合并
    @staticmethod
    def splitPdf(path='./input.pdf', N=5):
        if not os.path.isfile(path):
            return

        pdfFileWriter = PdfFileWriter()
        pdfFileReader = PdfFileReader(path)  # 获取 PdfFileReader 对象
        # 或者这个方式：pdfFileReader = PdfFileReader(open(readFile, 'rb'))

        numPages = pdfFileReader.getNumPages()  # 文档总页数
        print(numPages)

        # fname = os.path.splitext(os.path.basename(path))[0]
        fname = os.path.splitext(path)[0]
        outFile1 = '{}p1_{}.pdf'.format(fname, N)
        outFile2 = '{}p{}_{}.pdf'.format(fname, N + 1, numPages)
        print(outFile1, outFile2)

        if numPages > N:
            # 第N页之前的页面，输出到一个新的文件中，即分割文档
            for index in range(N - 1):
                pageObj = pdfFileReader.getPage(index)
                pdfFileWriter.addPage(pageObj)
            # 添加完每页，再一起保存至文件中
            pdfFileWriter.write(open(outFile1, 'wb'))

            # 从第N页之后的页面，输出到一个新的文件中，即分割文档
            for index in range(N, numPages):
                pageObj = pdfFileReader.getPage(index)
                pdfFileWriter.addPage(pageObj)
            # 添加完每页，再一起保存至文件中
            pdfFileWriter.write(open(outFile2, 'wb'))

    @staticmethod
    def mergePdf(inFileList, outFile):
        '''
        合并文档
        :param inFileList: 要合并的文档的 list
        :param outFile:    合并后的输出文件
        :return:
        '''
        pdfFileWriter = PdfFileWriter()
        for inFile in inFileList:
            # 依次循环打开要合并文件
            pdfReader = PdfFileReader(open(inFile, 'rb'))
            numPages = pdfReader.getNumPages()
            for index in range(0, numPages):
                pageObj = pdfReader.getPage(index)
                pdfFileWriter.addPage(pageObj)

            # 最后,统一写入到输出文件中
            pdfFileWriter.write(open(outFile, 'wb'))
    # endregion


class MainWindow(QtWidgets.QMainWindow, UiDocManager):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.axWidget = QAxWidget(self)
        self.doc = r'E:\考证\岩土\党工\党工 工程地质.pdf'

        self.setupUI(self)
        # self.verticalLayout.addWidget(self.axWidget)

        # pdf = PdfManager()
        # pdf.splitPdf(self.doc, 62)
        # pdf.readPdf(self.doc)

    def flushMap(self):
        self.wg.clicked()

    def openOffice(self, path, App=None):
        if not os.path.isfile(path):
            return
        self.doc = path

        self.axWidget.clear()
        if not self.axWidget.setControl(App):
            return QtWidgets.QMessageBox.critical(self, '错误', '没有安装  %s' % App)
        self.axWidget.dynamicCall(
            'SetVisible (bool Visible)', 'false')  # 不显示窗体
        self.axWidget.setProperty('DisplayAlerts', False)
        self.axWidget.setControl(path)
        self.axWidget.show()

    def openPdf(self, path):
        if not os.path.isfile(path):
            return
        self.doc = path

        self.axWidget.clear()
        if not self.axWidget.setControl('Adobe PDF Reader'):
            return QtWidgets.QMessageBox.critical(self, '错误', '没有安装 Adobe PDF Reader')
        # self.axWidget.setControl("{233C1507-6A77-46A4-9443-F871F945D258}")
        self.axWidget.dynamicCall(
            'SetVisible (bool Visible)', 'false')  # 不显示窗体
        self.axWidget.dynamicCall('LoadFile(const QString&)')

    def closeEvent(self, event):
        self.axWidget.close()
        self.axWidget.clear()
        self.layout().removeWidget(self.axWidget)
        del self.axWidget
        super(MainWindow, self).closeEvent(event)

    def resizeEvent(self, event):
        palette = QtGui.QPalette()
        pix = QtGui.QPixmap('res/images/background9.jpg')
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(palette)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    # win = D2Pane()
    sys.exit(app.exec_())
