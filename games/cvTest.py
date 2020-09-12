#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Project: PyCharm
# @File    : cvTest.py
# @Author  : tiger
# @Email   : shdorado@126.com
# @Time    : 2020/5/22 22:34

import sys
import cv2
# import numpy as np
from PIL import Image
# from pylab import *
import os
# from scipy.ndimage import filters
from numpy import *
from ctypes import *

from PyQt5 import QtCore, QtGui, QtWidgets


class Test(object):
    def __init__(self, parent):
        super(Test, self).__init__()
        self.parent = parent
        self.img = './res/img_match/majsss.png'
        # self.img = './res/img_match/TeTRUNC.png'
        # self.img = './res/img_match/TeMEAN.png'

        self.deal_img(self.img)
        # self.filtering()
        # self.sobel()
        # self.testit()

        # stdcall调用
        # Objdll = windll.LoadLibrary(r"./vl.dll")
        # # Objdll = WinDLL(r"./vl.dll")
        # print(type(Objdll))
        # # cdecl调用约定
        # Objdll = cdll.LoadLibrary(r"./vl.dll")
        # Objdll = CDLL(r"./vl.dll")  # 其实windll和cdll分别是WinDLL类和CDll类的对象
        # print(type(Objdll))
        # img = imread(self.img, cv2.IMREAD_GRAYSCALE)
        # color_img = imread(self.img)
        # # float_img = img.convertTo(img, cv2.CV_32F)
        # rows = img.rows
        # cols = img.cols
        # vl_sift = Objdll.vl_sift_new(cols, rows, 4, 3, 0)
        # Objdll.vl_sift_set_peak_thresh(vl_sift, 0.04);
        # Objdll.vl_sift_set_edge_thresh(vl_sift, 10);
        #
        # vl_sift_pix = img.data
        # print(type(vl_sift_pix))

    def test(self):
        imname = self.img
        im = array(Image.open(imname).convert('L'))
        self.process_image(imname, './building.sift')
        l1, d1 = self.read_features_from_file('./building.sift')
        figure()
        gray()

        """Figure1:SIFT特征"""
        self.plot_features(im, l1, circle=False)
        title('SIFT-Features')

        """Figure2:使用圆圈表示特征尺度的SIFT特征"""
        figure()
        gray()
        self.plot_features(im, l1, circle=True)
        title('Detect-SIFT-Features')

        """Figure3:Harris角点检测的结果"""
        harrisim = self.compute_harris_response(im)
        filtered_coords = self.get_harris_points(harrisim, 6, 0.05)
        self.plot_harris_points(im, filtered_coords)

    @staticmethod
    def process_image(imagename, resultname, params="--edge-thresh 10 --peak-thresh 5"):
        """ Process an image and save the results in a file. """
        if imagename[-3:] != 'pgm':
            # create a pgm file
            im = Image.open(imagename).convert('L')
            im.save('tmp.pgm')
            imagename = 'tmp.pgm'

        ll = ["E:/python/games/vlfeat-0.9.21/bin/win64/sift.exe ", imagename, " --output=", resultname, " ", params]
        cmmd = ''.join(ll)
        print(cmmd)
        try:
            ret = os.system(cmmd)
        except Exception as e:
            print(e)
        print('processed', imagename, 'to', resultname)

    @staticmethod
    def read_features_from_file(filename):
        """ Read feature properties and return in matrix form. """
        # if not filename:
        #     return None
        file = loadtxt(filename)
        print(file.shape, filename)
        return file[:, :4], file[:, 4:]  # feature locations, descriptors

    @staticmethod
    def write_features_to_file(filename, locs, desc):
        """ Save feature location and descriptor to file. """
        savetxt(filename, hstack((locs, desc)))

    @staticmethod
    def plot_features(im, locs, circle=False):
        """ Show image with features. input: im (image as array),
            locs (row, col, scale, orientation of each feature). """

        def draw_circle(c, r):
            t = arange(0, 1.01, .01) * 2 * pi
            x = r * cos(t) + c[0]
            y = r * sin(t) + c[1]
            plot(x, y, 'b', linewidth=2)

        imshow(im)
        if circle:
            for p in locs:
                draw_circle(p[:2], p[2])
        else:
            plot(locs[:, 0], locs[:, 1], 'ob')
        axis('off')

    @staticmethod
    def compute_harris_response(im, sigma=3):
        """ Compute the Harris corner detector response function
            for each pixel in a graylevel image. """

        # derivatives
        imx = zeros(im.shape)
        filters.gaussian_filter(im, (sigma, sigma), (0, 1), imx)
        imy = zeros(im.shape)
        filters.gaussian_filter(im, (sigma, sigma), (1, 0), imy)

        # compute components of the Harris matrix
        Wxx = filters.gaussian_filter(imx * imx, sigma)
        Wxy = filters.gaussian_filter(imx * imy, sigma)
        Wyy = filters.gaussian_filter(imy * imy, sigma)

        # determinant and trace
        Wdet = Wxx * Wyy - Wxy ** 2
        Wtr = Wxx + Wyy

        return Wdet / Wtr

    @staticmethod
    def get_harris_points(harrisim, min_dist=10, threshold=0.1):
        """ Return corners from a Harris response image
            min_dist is the minimum number of pixels separating
            corners and image boundary. """

        # find top corner candidates above a threshold
        corner_threshold = harrisim.max() * threshold
        harrisim_t = (harrisim > corner_threshold) * 1

        # get coordinates of candidates
        coords = array(harrisim_t.nonzero()).T

        # ...and their values
        candidate_values = [harrisim[c[0], c[1]] for c in coords]

        # sort candidates (reverse to get descending order)
        index = argsort(candidate_values)[::-1]

        # store allowed point locations in array
        allowed_locations = zeros(harrisim.shape)
        allowed_locations[min_dist:-min_dist, min_dist:-min_dist] = 1

        # select the best points taking min_distance into account
        filtered_coords = []
        for i in index:
            if allowed_locations[coords[i, 0], coords[i, 1]] == 1:
                filtered_coords.append(coords[i])
                allowed_locations[(coords[i, 0] - min_dist):(coords[i, 0] + min_dist),
                (coords[i, 1] - min_dist):(coords[i, 1] + min_dist)] = 0

        return filtered_coords

    @staticmethod
    def plot_harris_points(image, filtered_coords):
        """ Plots corners found in image. """

        figure()
        gray()
        imshow(image)
        plot([p[1] for p in filtered_coords], [p[0] for p in filtered_coords], '*')
        axis('off')
        title('Harris-Features')
        show()

    def filtering(self):
        srcImage = cv2.imread(self.img, 0)
        outImage = cv2.medianBlur(srcImage, 5)  # 首先对灰度图进行中值滤波操作，去除一些杂质。

        cv2.imshow('mid', outImage)
        cv2.imshow('grep', srcImage)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def sobel(self):
        img = cv2.imread(self.img, 0)
        if not img.all():
            return

        sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0)  # sobel_x:发现垂直边缘
        sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1)  # sobel_y:发现水平边缘

        sobel_x = np.uint8(np.absolute(sobel_x))
        sobel_y = np.uint8(np.absolute(sobel_y))
        np.set_printoptions(threshold=np.inf)
        # print(sobel_x)

        sobelCombined = cv2.bitwise_or(sobel_x, sobel_y)  # 按位或
        sumed = sobel_x + sobel_y

        # cv2.imshow('sobel_x',sobel_x)
        # cv2.imshow('sobel_y',sobel_y)
        cv2.imshow('sobel_combined', sobelCombined)
        cv2.imshow('sumed', sumed)

        cv2.waitKey()
        cv2.destroyAllWindows()

        # cv2.imwrite('./res/images/sobel_x.jpg', sobel_x)
        # cv2.imwrite('./res/images/sobel_y.jpg', sobel_y)
        cv2.imwrite('./res/images/sobel_combined.jpg', sobelCombined)
        cv2.imwrite('./res/images/sum.jpg', sumed)

        # Recognition.pickup('./res/images/test.jpg', './res/images/sobel_combined.jpg')

    def deal_img(self, file):
        img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)  # 0:单通道灰度 -1:原色 1:3通道彩色

        ret, BINARY = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)  # 简单滤波 （黑白二值）
        ret, BINARY_INV = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)  # （黑白二值反转）
        ret, TRUNC = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC)  # 得到的图像为多像素值
        ret, THRESH_TOZERO = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)  # 高于阈值时像素设置为255，低于阈值时不作处理
        ret, TOZERO_INV = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO_INV)  # 低于阈值时设置为255，高于阈值时不作处理
        ret, Otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Otsu 滤波
        print(ret)

        # 第一个参数为原始图像矩阵，第二个参数为像素值上限，第三个是自适应方法（adaptive method）：
        #                                              -----cv2.ADAPTIVE_THRESH_MEAN_C:领域内均值
        #                                              -----cv2.ADAPTIVE_THRESH_GAUSSIAN_C:领域内像素点加权和，权重为一个高斯窗口
        # 第四个值的赋值方法：只有cv2.THRESH_BINARY和cv2.THRESH_BINARY_INV
        # 第五个Block size：设定领域大小（一个正方形的领域）
        # 第六个参数C，阈值等于均值或者加权值减去这个常数（为0相当于阈值，就是求得领域内均值或者加权值）
        # 这种方法理论上得到的效果更好，相当于在动态自适应的调整属于自己像素点的阈值，而不是整幅图都用一个阈值
        th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)
        MEAN = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        GAUSSIAN = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # cv2.imshow('BINARY', BINARY)
        # cv2.imshow('BINARY_INV', BINARY_INV)
        cv2.imshow('TRUNC', TRUNC)
        cv2.imwrite('./res/img_match/TeTRUNC.png', TRUNC)
        # cv2.imshow('THRESH_TOZERO', THRESH_TOZERO)
        # cv2.imshow('TOZERO_INV', TOZERO_INV)
        # cv2.imshow('Otsu', Otsu)
        cv2.imshow('MEAN', MEAN)
        cv2.imwrite('./res/img_match/TeMEAN.png', MEAN)
        # cv2.imshow('GAUSSIAN', GAUSSIAN)
        # cv2.imshow('grey-map', img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def order_points(self, pts):
        img = self.img
        # 四个点按照左上、右上、右下、左下
        # pts 是四个点的列表
        rect = np.zeros((4, 2), dtype="float32")

        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect

    def four_point_transform(self, image, pts):
        """
        通过转递图像和边缘矩形的四个点，就可以通过透视转换将不是正视投影的文本图片转化为正视角投影

        :param image: 为需要透视变换的图像
        :param pts: 为四个点
        :return:
        """
        rect = self.order_points(pts)  # 四点排序
        (tl, tr, br, bl) = rect  # 方便计算

        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

        return warped

    def filter_matches(self, kp1, kp2, matches, ratio=0.75):
        mkp1, mkp2 = [], []
        for m in matches:
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                m = m[0]
                mkp1.append(kp1[m.queryIdx])
                mkp2.append(kp2[m.trainIdx])
        p1 = np.float32([kp.pt for kp in mkp1])
        p2 = np.float32([kp.pt for kp in mkp2])
        kp_pairs = zip(mkp1, mkp2)
        return p1, p2, kp_pairs

    def explore_match(self, win, img1, img2, kp_pairs, status=None, H=None):
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        vis = np.zeros((max(h1, h2), w1 + w2), np.uint8)
        vis[:h1, :w1] = img1
        vis[:h2, w1:w1 + w2] = img2
        vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)

        if H is not None:
            corners = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
            corners = np.int32(cv2.perspectiveTransform(corners.reshape(1, -1, 2), H).reshape(-1, 2) + (w1, 0))
            cv2.polylines(vis, [corners], True, (255, 255, 255))

        if status is None:
            status = np.ones(len(kp_pairs), np.bool)
        p1 = np.int32([kpp[0].pt for kpp in kp_pairs])
        p2 = np.int32([kpp[1].pt for kpp in kp_pairs]) + (w1, 0)

        green = (0, 255, 0)
        red = (0, 0, 255)
        white = (255, 255, 255)
        kp_color = (51, 103, 236)
        for (x1, y1), (x2, y2), inlier in zip(p1, p2, status):
            if inlier:
                col = green
                cv2.circle(vis, (x1, y1), 2, col, -1)
                cv2.circle(vis, (x2, y2), 2, col, -1)
            else:
                col = red
                r = 2
                thickness = 3
                cv2.line(vis, (x1 - r, y1 - r), (x1 + r, y1 + r), col, thickness)
                cv2.line(vis, (x1 - r, y1 + r), (x1 + r, y1 - r), col, thickness)
                cv2.line(vis, (x2 - r, y2 - r), (x2 + r, y2 + r), col, thickness)
                cv2.line(vis, (x2 - r, y2 + r), (x2 + r, y2 - r), col, thickness)
        vis0 = vis.copy()
        for (x1, y1), (x2, y2), inlier in zip(p1, p2, status):
            if inlier:
                cv2.line(vis, (x1, y1), (x2, y2), green)

        cv2.imshow(win, vis)

    def TestSIFT(self):
        """
        进行SIFT特征进行匹配
        :return: 
        """
        img1 = cv2.imread("E:\python\Python Project\opencv_showimage\images\multi_view_big.jpg")
        img2 = cv2.imread("E:\python\Python Project\opencv_showimage\images\multi_view_small.jpg")

        img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        sift = cv2.SIFT()

        kp1, des1 = sift.detectAndCompute(img1_gray, None)
        kp2, des2 = sift.detectAndCompute(img2_gray, None)

        # BFmatcher with default parms
        bf = cv2.BFMatcher(cv2.NORM_L2)
        matches = bf.knnMatch(des1, des2, k=2)

        p1, p2, kp_pairs = self.filter_matches(kp1, kp2, matches, ratio=0.5)
        self.explore_match('matches', img1_gray, img2_gray, kp_pairs)
        # img3 = cv2.drawMatchesKnn(img1_gray,kp1,img2_gray,kp2,good[:10],flag=2)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def testit(self):
        imgname1 = './res/images/timg.jpg'
        imgname2 = './res/images/maj1.jpg'

        sift = cv2.xfeatures2d.SIFT_create()

        img1 = cv2.imread(imgname1)
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)  # 灰度处理图像
        kp1, des1 = sift.detectAndCompute(img1, None)  # des是描述子

        img2 = cv2.imread(imgname2)

        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)  # 灰度处理图像
        kp2, des2 = sift.detectAndCompute(img2, None)  # des是描述子

        # hmerge = np.hstack((gray1, gray2)) #水平拼接
        # cv2.imshow("gray", hmerge) #拼接显示为gray
        # cv2.waitKey(0)

        # img3 = cv2.drawKeypoints(img1,kp1,img1,color=(255,0,255)) #画出特征点，并显示为红色圆圈
        # img4 = cv2.drawKeypoints(img2,kp2,img2,color=(255,0,255)) #画出特征点，并显示为红色圆圈

        # hmerge = np.hstack((img3, img4)) #水平拼接
        # cv2.imshow("point", hmerge) #拼接显示为gray
        # cv2.waitKey(0)

        # BFMatcher解决匹配
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)
        # 调整ratio
        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append([m])

        img5 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)

        cv2.imshow("BFmatch", img5)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._setup_ui()

        # TODO(tiger) Change this to use relations
        self.img_background = 'res/images/background.jpg'

    def _setup_ui(self):
        self.setWindowTitle('窗口')
        self.setGeometry(0, 0, 800, 600)
        self._center()

    def _center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resizeEvent(self, event):
        palette = QtGui.QPalette()
        pix = QtGui.QPixmap(self.img_background)
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(palette)


if __name__ == '__main__':
    # app = QtWidgets.QApplication(sys.argv)
    # win = MainWindow()
    # win.show()
    # sys.exit(app.exec_())
    test = Test(None)
