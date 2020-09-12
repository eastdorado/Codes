#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Project: PyCharm
# @File    : imageRecognition.py
# @Author  : tiger
# @Email   : shdorado@126.com
# @Time    : 2020/5/22 17:19

import sys
from cv2 import *
import numpy as np
from numpy import mat
import copy

from PyQt5 import QtCore, QtGui, QtWidgets


class Recognition(QtWidgets.QFrame):
    def __init__(self, parent):
        super(Recognition, self).__init__(parent)
        self.parent = parent
        self.img = parent.img_background
        self.img_canny = './res/images/canny_bird.png'
        self.img_mask = './res/images/mask_bird.png'

        self.img_river = './res/images/river.png'

        self.init_ui()

        # self.get_border()
        # for i in range(2):
        #     self.faltung()
        # self.pickup()
        # self.get_mask_img()
        # self.sobelTest()
        Recognition.myOtsu(self.img_river)

    def init_ui(self):
        # 总体框架
        hl_main = QtWidgets.QHBoxLayout(self)
        self.setLayout(hl_main)

        lb = QtWidgets.QLabel(self)
        hl_main.addWidget(lb)

        lb.setScaledContents(True)  # 让图片自适应label大小
        lb.setPixmap(QtGui.QPixmap(self.img))
        lb.setGeometry(200, 0, 1200, 300)

        # flag = '居中'
        # if bg.isNull():
        #     self.setStyleSheet('background-color:BurlyWood')  # Tan
        # else:
        #     if flag == '居中':
        #         lb.setStyleSheet('background-image:url(./res/images/test1.png); background-color:black')
        #     elif flag == '缩放':
        #         # lb.setStyleSheet("background-color:black")
        #         lb.setAlignment(QtCore.Qt.AlignCenter)
        #         lb.setPixmap(bg.scaled(self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        #     elif flag == '拉伸':
        #         lb.setPixmap(bg.scaled(self.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation))
        #     elif flag == '平铺':
        #         lb.setStyleSheet("background-color:black;background-image:url(./res/images/test1.png);"
        #                          "background-position:top left;background-repeat:repeat-xy;")

    def get_border(self):
        """
        用canny函数得到最佳边缘, 轮廓必须有完整的闭合区域
        :return:
        """
        img = cv2.imread(self.img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度图像
        # gray = cv2.GaussianBlur(gray, (5, 5), 0)  # 高斯模糊
        c_canny_img = cv2.Canny(gray, 50, 150)  # 边缘检测

        cv2.imwrite(self.img_canny, c_canny_img)

        # cv2.imshow('mask', c_canny_img)
        # k = cv2.waitKey(500) & 0xFF
        # if k == 27:
        #     cv2.destroyAllWindows()

    def faltung(self):
        """
        对边缘像素周围的像素用进行迭代像素填充  
         定义一个3X3或者5X5的卷积核，遍历这张边缘图片的每一个像素，当遇到像素点为白色（255，255，255）时，
         对它周围的像素全部置成白色。有可能第一步效果并不理想，不过没关系，多迭代几次就好了
        :return: 
        """
        img = cv2.imread(self.img_canny)
        rows, cols, ch = img.shape
        SIZE = 3  # 卷积核大小
        P = int(SIZE / 2)
        BLACK = [0, 0, 0]
        WHITE = [255, 255, 255]
        BEGIN = False
        BP = []

        for row in range(P, rows - P, 1):
            for col in range(P, cols - P, 1):
                # print(img[row,col])
                if (img[row, col] == WHITE).all():
                    kernal = []
                    for i in range(row - P, row + P + 1, 1):
                        for j in range(col - P, col + P + 1, 1):
                            kernal.append(img[i, j])
                            if (img[i, j] == BLACK).all():
                                # print(i,j)
                                BP.append([i, j])

        # print(len(BP))
        uniqueBP = np.array(list(set([tuple(c) for c in BP])))
        # print(len(uniqueBP))

        for x, y in uniqueBP:
            img[x, y] = WHITE

        cv2.imwrite(self.img_canny, img)
        # cv2.imshow('img', img)
        #
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    @staticmethod
    def pickup(img_source, img_canny):
        """
        用掩膜位运算提取白色区域的内容
        :return: 
        """
        try:
            img1 = imread(img_source)
            img2 = imread(img_canny)
            if not isinstance(img1, np.ndarray) or not isinstance(img2, np.ndarray):
                return

            img_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            # print('图片尺寸', img_gray.shape)

            return cv2.bitwise_and(img1, img1, mask=img_gray)

        except Exception as e:
            print(e)

    @staticmethod
    def sobelTest():
        img = cv2.imread('./res/images/test.jpg', 0)
        # print(type(img.all()))
        if not img.all():
            return

        # sobel_x:发现垂直边缘
        sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0)
        # sobel_y:发现水平边缘
        sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1)

        sobel_x = np.uint8(np.absolute(sobel_x))
        sobel_y = np.uint8(np.absolute(sobel_y))
        np.set_printoptions(threshold=np.inf)
        # print(sobel_x)

        sobelCombined = cv2.bitwise_or(sobel_x, sobel_y)  # 按位或
        sumed = sobel_x + sobel_y

        # x = cv2.Sobel(img, cv2.CV_16S, 1, 0)
        # y = cv2.Sobel(img, cv2.CV_16S, 0, 1)
        #
        # absX = cv2.convertScaleAbs(x)  # 转回uint8
        # absY = cv2.convertScaleAbs(y)
        #
        # dst = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)

        # cv2.imshow('sobel_x',sobel_x)
        # cv2.imshow('sobel_y',sobel_y)
        cv2.imshow('sobel_combined', sobelCombined)
        cv2.imshow('sumed', sumed)

        # cv2.imwrite('./res/images/sobel_x.jpg', sobel_x)
        # cv2.imwrite('./res/images/sobel_y.jpg', sobel_y)
        cv2.imwrite('./res/images/sobel_combined.jpg', sobelCombined)
        cv2.imwrite('./res/images/sum.jpg', sumed)

        Recognition.pickup('./res/images/test.jpg', './res/images/sobel_combined.jpg')

        cv2.waitKey()
        cv2.destroyAllWindows()

    def get_mask_img(self):
        """
        首先对采集的图片进行灰度化处理（方便进行数据处理），
        然后对灰度图像进行中值滤波操作去除湖面上的细小杂质，
        之后通过x方向和y方向上的Sobel梯度算子分别获取梯度图像，并将梯度图像转换成CV_8UC1类型，
        并对转换后的x，y方向上的梯度图像进行OTSU二值化操作获取二值图像，
        并对两幅二值图像按对应像素位置进行与运算，目的是为了去除河道上的波纹干扰。
        （可以继续对与运算之后的结果图进行中值滤波去除湖面上的细小杂质）。
        最后对二值图进行多次迭代的膨胀腐蚀操作以及小区域块的填充操作（
        用到findContours与drawContours接口进行轮廓查找与填充）
        获取河道连通区域，掩码图
        :return: 
        """
        img = cv2.imread(self.img_river)
        srcImage2 = copy.deepcopy(img)
        srcImage3 = copy.deepcopy(img)
        g_nKrenel = 3  # 中值滤波，相当于将9个值进行排序，取中值作为当前值, 5x5、3x3
        img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度化处理
        out_img = medianBlur(img, g_nKrenel)  # 首先对灰度图进行中值滤波操作，去除一些杂质。

        grad_x = cv2.Sobel(out_img, cv2.CV_16S, 1, 0)
        abs_grad_x = convertScaleAbs(grad_x)  # 转回uint8
        grayImage_x = abs_grad_x  # convertTo(abs_grad_x, CV_8U)

        grad_y = Sobel(out_img, CV_16S, 0, 1)
        abs_grad_y = convertScaleAbs(grad_y)
        grayImage_y = abs_grad_y  # convertTo(abs_grad_y, CV_8U)

        n_thresh_x = self.myOtsu(grayImage_x)
        XBin = threshold(grayImage_x, n_thresh_x, 255, THRESH_BINARY)

        n_thresh_y = self.myOtsu(grayImage_y)
        YBin = threshold(grayImage_y, n_thresh_y, 255, THRESH_BINARY)

        Bin = bitwise_and(XBin, YBin)
        outBin = medianBlur(Bin, 3)  # 去除一些杂质点。

        outBin2 = outBin.clone()
        n_iterations = 5
        element = getStructuringElement(MORPH_ELLIPSE, QtCore.QSize(15, 15))  # 膨胀变亮形成连通域。
        element2 = getStructuringElement(MORPH_ELLIPSE, QtCore.QSize(5, 5))  # 腐蚀操作断开一些连通域。
        dilate(outBin2, outBin2, element, QtCore.QPoint(-1, -1), n_iterations)
        erode(outBin2, outBin2, element2, QtCore.QPoint(-1, -1), 3)  # 腐蚀操作，断开河流区域内部的连接区域，方便后续的填充处理。

        # 将河流ROI区域小块连通域填黑。
        outBin3 = outBin2.clone()
        h = findContours(outBin3, RETR_LIST, CHAIN_APPROX_SIMPLE)
        contours = h[0]  # 提取轮廓
        # print(type(h)) #打印返回值，这是一个元组
        # print(type(h[1])) #打印轮廓类型，这是个列表
        # print (len(contours)) #查看轮廓数量

        mask_color = (0, 0, 255)
        f_area = 0.0
        for i in range(len(contours)):
            f_area = contourArea(contours[i])
            if f_area < 250000:
                drawContours(outBin3, contours, i, mask_color, -1)  # 颜色填充

        # 由于final bin2在腐蚀过程中存在部分背景区域为黑色空洞，需要将其填白。
        outBin4_tmp = ~outBin3
        outBin4 = mat()
        contours.clear()
        contours = findContours(outBin4_tmp, RETR_EXTERNAL | CHAIN_APPROX_SIMPLE, None)  # 轮廓逼近方法，使用NONE表示所有轮廓都显示
        for i in range(len(contours)):
            f_area = contourArea(contours[i])
            if f_area < 250000:
                drawContours(outBin4_tmp, contours, i, mask_color, -1)

        outBin4 = ~outBin4_tmp

        # 迭代腐蚀突出河流边界区域。
        erode(outBin4, outBin4, element, QtCore.QPoint(-1, -1), 10)

        # (可以对腐蚀图在进行一次外轮廓填充)。
        outBin5_tmp = ~outBin4.clone()
        contours = findContours(outBin5_tmp, contours, RETR_CCOMP | CHAIN_APPROX_SIMPLE, None)
        for i in range(len(contours)):
            f_area = contourArea(contours[i])
            if f_area < 100000:
                drawContours(outBin5_tmp, contours, i, mask_color, -1)
        outBin5 = ~outBin5_tmp

        # 根据outBin4，对原rgb图取感兴趣区域（即河流区域）
        for i in range(outBin5.rows):
            for j in range(outBin5.cols):
                if outBin5.at(i, j) == 255:
                    srcImage2.at(i, j)[0] = 0
                    srcImage2.at(i, j)[1] = 0
                    srcImage2.at(i, j)[2] = 0

        namedWindow("finalImage", 0)
        imshow("finalImage", srcImage2)  # 这里的srcImage2表示最后所需效果图

        waitKey(30)

    @staticmethod
    def myOtsu(img_file):
        img = cv2.imread('./res/images/test.jpg', 0)
        # img = cv2.imread(img_file, 0)
        if not img.all():
            return

        t, dst = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)  # t表示返回的阈值
        t2, otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        #  第二个参数必须是0， 第四个参数的第一位可以是之前博客说的那五种阈值处理的方式

        athdMEAN = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 3)
        athdGAUS = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 3)
        #  自适应的输入图片必须是单通道图片

        # cv2.imshow('img', img)
        # cv2.imshow('dst', dst)
        cv2.imshow('mean', athdMEAN)
        cv2.imshow('gaus', athdGAUS)
        # cv2.imshow('otsu', otsu)
        cv2.waitKey()
        cv2.destroyAllWindows()

        # return otsu


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.img_background = 'res/images/test1.png'
        self._setup_ui()

        # TODO(tiger) Change this to use relations
        # 总体框架
        # hl_main = QtWidgets.QHBoxLayout(self)
        # self.setLayout(hl_main)

        self.reg = Recognition(self)
        # wg_right = QtWidgets.QWidget()
        # wg_right.setFixedWidth(200)
        # vl_right = QtWidgets.QVBoxLayout(wg_right)
        # hl_main.addWidget(self.reg)

    def _setup_ui(self):
        self.setWindowTitle('窗口')
        self.setGeometry(0, 0, 800, 600)
        self._center()

    def _center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # def resizeEvent(self, event):
    # palette = QtGui.QPalette()
    # pix = QtGui.QPixmap(self.img_background)
    # pix = pix.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
    # palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
    # self.setPalette(palette)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
