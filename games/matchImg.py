#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Project: PyCharm
# @File    : matchImg.py
# @Author  : tiger
# @Email   : shdorado@126.com
# @Time    : 2020/5/23 12:28

import sys
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
from PIL import Image
import imutils
from skimage import data, draw, color, transform, feature
import random
import time


class MahjongData(object):
    g_pic_path = 'E:/python/games/res/img_match'

    g_tiles_pic = ('character1.png', 'character2.png', 'character3.png', 'character4.png', 'character5.png',
                   'character6.png', 'character7.png', 'character8.png', 'character9.png',
                   'dot1.png', 'dot2.png', 'dot3.png', 'dot4.png', 'dot5.png',
                   'dot6.png', 'dot7.png', 'dot8.png', 'dot9.png',
                   'bamboo1.png', 'bamboo2.png', 'bamboo3.png', 'bamboo4.png', 'bamboo5.png',
                   'bamboo6.png', 'bamboo7.png', 'bamboo8.png', 'bamboo9.png',
                   'windEast.png', 'windSouth.png', 'windWest.png', 'windNorth.png',
                   'dragonRed.png', 'dragonGreen.png', 'dragonWhite.png', 'none', 'none',
                   'flower1', 'flower2', 'flower3', 'flower4', 'flower5', 'flower6', 'flower7', 'flower8')
    g_tiles_name = ("一万", "二万", "三万", "四万", "五万", "六万", "七万", "八万", "九万",
                    "一饼", "二饼", "三饼", "四饼", "五饼", "六饼", "七饼", "八饼", "九饼",
                    "一条", "二条", "三条", "四条", "五条", "六条", "七条", "八条", "九条",
                    "东风", "南风", "西风", "北风", "红中", "发财", "白板", None, None,
                    "春", "夏", "秋", "冬", "梅", "兰", "菊", "竹")

    @staticmethod
    def get_pic_file(index):
        """
        根据序号获得麻将牌的名称与图片文件名称
        :param index:
        :return: [名称，文件名]
        """

        ret = None
        if 0 <= index < 44:
            if index == 34 or index == 35:  # 补位的不算
                return ret, ret

            name = MahjongData.g_tiles_name[index]
            file = None
            style = (index // 9)
            value = (index % 9) + 1
            if style == 0:
                file = ''.join(['character', str(value), '.png'])
            elif style == 1:
                file = ''.join(['dot', str(value), '.png'])
            elif style == 2:
                file = ''.join(['bamboo', str(value), '.png'])
            elif style == 3:
                tmp = ('windEast.png', 'windSouth.png', 'windWest.png', 'windNorth.png',
                       'dragonRed.png', 'dragonGreen.png', 'dragonWhite.png')
                file = tmp[value - 1]
            else:  # 春、夏、秋、冬、梅、兰、竹、菊
                file = ''.join(['flower', str(value), '.png'])

            file = os.path.join(MahjongData.g_pic_path, file)
            file = file.replace('\\', '/')

            return name, file

        else:
            return ret, ret


class AlikeImages(object):
    def __init__(self, parent=None):
        super(AlikeImages, self).__init__()
        self.parent = parent

        f1 = 'E:/python/games/res/img_match/img.jpg'
        f2 = 'E:/python/games/res/img_match/bamboo8.png'
        self.runAllImageSimilaryFun(f1, f2)

        # for i in range(50):
        #     print(self.get_pic_file(i))

    """
    均值哈希算法、差值哈希算法和感知哈希算法都是值越小，相似度越高，取值为0-64，即汉明距离中，64位的hash值有多少不同。 
    三直方图和单通道直方图的值为0-1，值越大，相似度越高。
    汉明距离:两个等长字符串之间的汉明距离是两个字符串对应位置的不同字符的个数。
    换句话说，它就是将一个字符串变换成另外一个字符串所需要替换的字符个数
    """

    @staticmethod
    def aHash(img):
        # 均值哈希算法
        # 缩放为8*8
        img = cv2.resize(img, (8, 8))
        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # s为像素和初值为0，hash_str为hash值初值为''
        s = 0
        hash_str = ''
        # 遍历累加求像素和
        for i in range(8):
            for j in range(8):
                s = s + gray[i, j]
        # 求平均灰度
        avg = s / 64
        # 灰度大于平均值为1相反为0生成图片的hash值
        for i in range(8):
            for j in range(8):
                if gray[i, j] > avg:
                    hash_str = hash_str + '1'
                else:
                    hash_str = hash_str + '0'

        return hash_str

    @staticmethod
    def dHash(img):
        # 差值哈希算法
        # 缩放8*8
        img = cv2.resize(img, (9, 8))
        # 转换灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hash_str = ''
        # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
        for i in range(8):
            for j in range(8):
                if gray[i, j] > gray[i, j + 1]:
                    hash_str = hash_str + '1'
                else:
                    hash_str = hash_str + '0'

        return hash_str

    @staticmethod
    def pHash(img):
        # 感知哈希算法
        # 缩放32*32
        img = cv2.resize(img, (32, 32))  # , interpolation=cv2.INTER_CUBIC

        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 将灰度图转为浮点型，再进行dct变换
        dct = cv2.dct(np.float32(gray))
        # opencv实现的掩码操作
        dct_roi = dct[0:8, 0:8]

        hash_list = []
        avreage = np.mean(dct_roi)
        for i in range(dct_roi.shape[0]):
            for j in range(dct_roi.shape[1]):
                if dct_roi[i, j] > avreage:
                    hash_list.append(1)
                else:
                    hash_list.append(0)

        return hash_list

    @staticmethod
    def GLH(image1, image2):
        # 灰度直方图算法
        # 计算单通道的直方图的相似值
        hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
        hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
        # 计算直方图的重合度
        degree = 0
        for i in range(len(hist1)):
            if hist1[i] != hist2[i]:
                degree = degree + \
                         (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
            else:
                degree = degree + 1
        degree = degree / len(hist1)

        return degree

    @staticmethod
    def classify_hist_with_split(image1, image2, size=(256, 256)):
        # 三直方图算法 : RGB每个通道的直方图相似度
        # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
        image1 = cv2.resize(image1, size)
        image2 = cv2.resize(image2, size)
        sub_image1 = cv2.split(image1)
        sub_image2 = cv2.split(image2)
        sub_data = 0
        for im1, im2 in zip(sub_image1, sub_image2):
            sub_data += AlikeImages.GLH(im1, im2)
        sub_data = sub_data / 3
        return sub_data

    @staticmethod
    def cmpHash(hash1, hash2):
        # 计算汉明距离 Hash值对比
        # 算法中1和0顺序组合起来的即是图片的指纹hash。顺序不固定，但是比较的时候必须是相同的顺序。
        # 对比两幅图的指纹，计算汉明距离，即两个64位的hash值有多少是不一样的，不同的位数越小，图片越相似
        # 汉明距离：一组二进制数据变成另一组数据所需要的步骤，可以衡量两图的差异，汉明距离越小，则相似度越高。汉明距离为0，即两张图片完全一样
        n = 0
        # hash长度不同则返回-1代表传参出错
        if len(hash1) != len(hash2):
            return -1
        # 遍历判断
        for i in range(len(hash1)):
            # 不相等则n计数+1，n最终为相似度
            if hash1[i] != hash2[i]:
                n = n + 1

        return n

    # @staticmethod
    # def getImageByUrl(url):
    #     # 根据图片url 获取图片对象
    #     html = requests.get(url, verify=False)
    #     image = Image.open(BytesIO(html.content))
    #     return image

    @staticmethod
    def PILImageToCV(file):
        # PIL Image转换成OpenCV格式
        img = Image.open(file)
        plt.subplot(121)
        plt.imshow(img)
        print(isinstance(img, np.ndarray))
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        print(isinstance(img, np.ndarray))
        plt.subplot(122)
        plt.imshow(img)
        plt.show()

    @staticmethod
    def CVImageToPIL(file):
        # OpenCV图片转换为PIL image
        img = cv2.imread(file)
        # cv2.imshow("OpenCV",img)
        plt.subplot(121)
        plt.imshow(img)

        img2 = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.subplot(122)
        plt.imshow(img2)
        plt.show()

    @staticmethod
    def bytes_to_cvimage(filebytes):
        # 图片字节流转换为cv image
        image = Image.open(filebytes)
        img = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)

        return img

    @staticmethod
    def runAllImageSimilaryFun(para1, para2):
        # 均值、差值、感知哈希算法三种算法值越小，则越相似,相同图片值为0
        # 三直方图算法和单通道的直方图 0-1之间，值越大，越相似。 相同图片为1

        # t1,t2   14;19;10;  0.70;0.75
        # t1,t3   39 33 18   0.58 0.49
        # s1,s2  7 23 11     0.83 0.86  挺相似的图片
        # c1,c2  11 29 17    0.30 0.31

        img1 = cv2.imread(para1)
        img2 = cv2.imread(para2)

        hash1 = AlikeImages.aHash(img1)
        hash2 = AlikeImages.aHash(img2)
        n1 = AlikeImages.cmpHash(hash1, hash2)
        print('均值哈希算法相似度aHash：', n1)

        hash1 = AlikeImages.dHash(img1)
        hash2 = AlikeImages.dHash(img2)
        n2 = AlikeImages.cmpHash(hash1, hash2)
        print('差值哈希算法相似度dHash：', n2)

        hash1 = AlikeImages.pHash(img1)
        hash2 = AlikeImages.pHash(img2)
        n3 = AlikeImages.cmpHash(hash1, hash2)
        print('感知哈希算法相似度pHash：', n3)

        n4 = AlikeImages.classify_hist_with_split(img1, img2)
        print('三直方图算法相似度：', n4)

        n5 = AlikeImages.GLH(img1, img2)
        print("单通道的直方图", n5)
        print("%d %d %d %.2f %.2f " % (n1, n2, n3, round(n4[0], 2), n5[0]))
        print("%.2f %.2f %.2f %.2f %.2f " % (1 - float(n1 / 64), 1 - float(n2 / 64),
                                             1 - float(n3 / 64), round(n4[0], 2), n5[0]))

        plt.subplot(121)
        plt.imshow(Image.fromarray(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)))
        plt.subplot(122)
        plt.imshow(Image.fromarray(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)))
        plt.show()

    @staticmethod
    def showit(title, img):
        if isinstance(img, np.ndarray):
            # cv2.imshow(title, img)  # 展示图片
            cv2.imshow(MatchImages.zh_ch(title), img)  # 展示图片
            cv2.waitKey(0)  # 等待按键按下
            cv2.destroyAllWindows()  # 清除所有窗口

    @staticmethod
    def zh_ch(title):
        """
        显示中文时乱码的转换
        :param title:
        :return:
        """
        if isinstance(title, str):
            return title.encode("gbk").decode(errors="ignore")


class MatchImages(object):
    def __init__(self, parent=None):
        super(MatchImages, self).__init__()
        self.parent = parent

        self.f1 = 'E:/python/games/res/img_match/img.jpg'

        for i in range(27, 36):
            index = 13  # random.randint(0, 36)
            name, self.f2 = RawData.get_pic_file(i)
            if name is None:
                return
            print(name, index)
            self.cv_SIFT_FLANN_Homography(self.f1, self.f2)

        # self.f2 = 'E:/python/games/res/img_match/bamboo8.png'
        # self.f2 = 'E:/python/games/res/img_match/bamboo7.png'
        # self.f1 = 'E:/python/games/res/img_match/t9.jpg'
        # self.f2 = 'E:/python/games/res/img_match/dot9.png'
        # self.f1 = 'E:/python/games/res/images/1.png'
        # self.f2 = 'E:/python/games/res/images/2.png'

        # path = './res/img_match'
        # create_descriptors(path)
        # matching(path, file1)

        # self.cv_SIFT(self.f1)
        # self.cv_SURF(self.f2)
        # self.cv_ORB_BFMatcher(self.f1, self.f2)
        # cv_SURF_BFMatcher()
        # cv_cv_ORB_BFMatcher_one()
        # cv_KNN_BFMatcher()
        # self.cv_SURF_FLANN(self.f1, self.f2)
        # self.cv_SIFT_FLANN_Homography(self.f1, self.f2)
        # cv_SIFT_FLANN_Homography_matix()
        # self.newtest()

    def newtest(self):
        psd_img_1 = cv2.imread(self.f1, cv2.IMREAD_GRAYSCALE)
        psd_img_2 = cv2.imread(self.f2, cv2.IMREAD_GRAYSCALE)

        # 3) SIFT特征计算
        sift = cv2.xfeatures2d.SIFT_create()

        psd_kp1, psd_des1 = sift.detectAndCompute(psd_img_1, None)
        psd_kp2, psd_des2 = sift.detectAndCompute(psd_img_2, None)

        # 4) Flann特征匹配
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(psd_des1, psd_des2, k=2)

        goodMatch = []
        for m, n in matches:
            # goodMatch是经过筛选的优质配对，如果2个配对中第一匹配的距离小于第二匹配的距离的1/2，
            # 基本可以说明这个第一配对是两幅图像中独特的，不重复的特征点,可以保留。
            if m.distance < 0.50 * n.distance:
                goodMatch.append(m)
        # 增加一个维度
        goodMatch = np.expand_dims(goodMatch, 1)
        # print(goodMatch[:20])

        # 把img_out中的参数goodMatch[:15]改为goodMatch，即展示所有匹配的特征
        # img_out = cv2.drawMatchesKnn(psd_img_1, psd_kp1, psd_img_2, psd_kp2, goodMatch[:15], None, flags=2)
        img_out = cv2.drawMatchesKnn(psd_img_1, psd_kp1, psd_img_2, psd_kp2, goodMatch, None, flags=2)

        self.showit('效果很好的方法', img_out)

    @staticmethod
    def cv_SIFT(imgpath):
        # 读取图片并灰度处理
        img = cv2.imread(imgpath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 创建SIFT对象
        sift = cv2.xfeatures2d.SIFT_create()

        # 将图片进行SURF计算，并找出角点keypoints，keypoints是检测关键点
        # descriptor是描述符，这是图像一种表示方式，可以比较两个图像的关键点描述符，可作为特征匹配的一种方法。
        keypoints, descriptor = sift.detectAndCompute(gray, None)

        # cv2.drawKeypoints() 函数主要包含五个参数：
        # image: 原始图片
        # keypoints：从原图中获得的关键点，这也是画图时所用到的数据
        # outputimage：输出
        # color：颜色设置，通过修改（b,g,r）的值,更改画笔的颜色，b=蓝色，g=绿色，r=红色。
        # flags：绘图功能的标识设置，标识如下：
        # cv2.DRAW_MATCHES_FLAGS_DEFAULT  默认值
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
        # cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG
        # cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS
        img = cv2.drawKeypoints(image=img, outImage=img, keypoints=keypoints, flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT,
                                color=(0, 222, 0))

        # 显示图片
        cv2.imshow('sift_keypoints', img)
        while True:
            if cv2.waitKey(120) & 0xff == ord("q"):
                break
        cv2.destroyAllWindows()

    @staticmethod
    def cv_SURF(imgpath):
        # 读取图片并灰度处理
        img = cv2.imread(imgpath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 创建SURF对象，对象参数float(4000)为阈值，阈值越高，识别的特征越小。
        sift = cv2.xfeatures2d.SURF_create(float(4000))
        # 将图片进行SURF计算，并找出角点keypoints，keypoints是检测关键点
        # descriptor是描述符，这是图像一种表示方式，可以比较两个图像的关键点描述符，可作为特征匹配的一种方法。
        keypoints, descriptor = sift.detectAndCompute(gray, None)

        img = cv2.drawKeypoints(image=img, outImage=img, keypoints=keypoints, flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT,
                                color=(0, 0, 222))

        # 显示图片
        cv2.imshow('sift_keypoints', img)
        while True:
            if cv2.waitKey(120) & 0xff == ord("q"):
                break
        cv2.destroyAllWindows()

    @staticmethod
    def cv_ORB_BFMatcher(file1, file2):
        """
        ORB算法（基于FAST关键点检测和BRIEF的描述符技术） + 暴力匹配
        :return:
        """
        # 读取图片内容
        img1 = cv2.imread(file1, 0)
        img2 = cv2.imread(file2, 0)

        # 使用ORB特征检测器和描述符，计算关键点和描述符
        orb = cv2.ORB_create()

        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        # 暴力匹配BFMatcher，遍历描述符，确定描述符是否匹配，然后计算匹配距离并排序
        # BFMatcher函数参数：
        # normType：NORM_L1, NORM_L2, NORM_HAMMING, NORM_HAMMING2。
        # NORM_L1和NORM_L2是SIFT和SURF描述符的优先选择，NORM_HAMMING和NORM_HAMMING2是用于ORB算法
        bf = cv2.BFMatcher(normType=cv2.NORM_HAMMING, crossCheck=True)  # 暴力匹配
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)
        # matches是DMatch对象，具有以下属性：
        # DMatch.distance - 描述符之间的距离。 越低越好。
        # DMatch.trainIdx - 训练描述符中描述符的索引
        # DMatch.queryIdx - 查询描述符中描述符的索引
        # DMatch.imgIdx - 训练图像的索引。

        # 使用plt将两个图像的匹配结果显示出来
        img3 = cv2.drawMatches(img1=img1, keypoints1=kp1, img2=img2, keypoints2=kp2,
                               matches1to2=matches, outImg=img2, flags=2)
        # plt.imshow(img3), plt.show()
        cv2.imshow('ORB_BFMatcher', img3)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def cv_SURF_BFMatcher(file1='./res/images/tieta1.jpg', file2='./res/images/tieta2.jpg'):
        """
        SURF或者SIFT算法 +暴力匹配
        :return:
        """
        # 读取图片内容
        img1 = cv2.imread(file1, 0)
        img2 = cv2.imread(file2, 0)

        # 使用ORB特征检测器和描述符，计算关键点和描述符
        # orb = cv2.ORB_create()
        orb = cv2.xfeatures2d.SURF_create(float(4000))  # SURF或 SIFT算法

        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        # 暴力匹配BFMatcher，遍历描述符，确定描述符是否匹配，然后计算匹配距离并排序
        # BFMatcher函数参数：
        # normType：NORM_L1, NORM_L2, NORM_HAMMING, NORM_HAMMING2。
        # NORM_L1和NORM_L2是SIFT和SURF描述符的优先选择，NORM_HAMMING和NORM_HAMMING2是用于ORB算法
        # bf = cv2.BFMatcher(normType=cv2.NORM_HAMMING, crossCheck=True)    # 暴力匹配
        bf = cv2.BFMatcher(normType=cv2.NORM_L1, crossCheck=True)  # SURF或 SIFT算法
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)
        # matches是DMatch对象，具有以下属性：
        # DMatch.distance - 描述符之间的距离。 越低越好。
        # DMatch.trainIdx - 训练描述符中描述符的索引
        # DMatch.queryIdx - 查询描述符中描述符的索引
        # DMatch.imgIdx - 训练图像的索引。

        # 使用plt将两个图像的匹配结果显示出来
        img3 = cv2.drawMatches(img1=img1, keypoints1=kp1, img2=img2, keypoints2=kp2,
                               matches1to2=matches, outImg=img2, flags=2)
        # plt.imshow(img3), plt.show()
        cv2.imshow('SURF_BFMatcher', img3)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def cv_ORB_BFMatcher_one(file1='./res/images/tieta1.jpg', file2='./res/images/tieta2.jpg'):
        # 读取图片内容
        img1 = cv2.imread(file1, 0)
        img2 = cv2.imread(file2, 0)

        # 使用ORB特征检测器和描述符，计算关键点和描述符
        orb = cv2.ORB_create()

        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        # 暴力匹配BFMatcher，遍历描述符，确定描述符是否匹配，然后计算匹配距离并排序
        # BFMatcher函数参数：
        # normType：NORM_L1, NORM_L2, NORM_HAMMING, NORM_HAMMING2。
        # NORM_L1和NORM_L2是SIFT和SURF描述符的优先选择，NORM_HAMMING和NORM_HAMMING2是用于ORB算法
        bf = cv2.BFMatcher(normType=cv2.NORM_HAMMING, crossCheck=True)  # 暴力匹配
        matches = bf.match(des1, des2)
        # matches = sorted(matches, key=lambda x: x.distance)

        # 由于匹配顺序是：matches = bf.match(des1,des2)，先des1后des2。
        # 因此，kp1的索引由DMatch对象属性为queryIdx决定，kp2的索引由DMatch对象属性为trainIdx决定

        # 获取aa.jpg的关键点位置
        x, y = kp1[matches[0].queryIdx].pt
        cv2.rectangle(img1, (int(x), int(y)), (int(x) + 5, int(y) + 5), (0, 255, 0), 2)
        cv2.imshow('a', img1)

        # 获取bb.png的关键点位置
        x1, y1 = kp2[matches[0].trainIdx].pt
        cv2.rectangle(img2, (int(x1), int(y1)), (int(x1) + 5, int(y1) + 5), (0, 255, 0), 2)
        cv2.imshow('b', img2)

        # 使用plt将两个图像的第一个匹配结果显示出来
        img3 = cv2.drawMatches(img1=img1, keypoints1=kp1, img2=img2, keypoints2=kp2, matches1to2=matches[:1],
                               outImg=img2,
                               flags=2)
        # plt.imshow(img3), plt.show()
        cv2.imshow('ORB_BFMatcher_one', img3)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def cv_KNN_BFMatcher(file1='./res/images/tieta1.jpg', file2='./res/images/tieta2.jpg'):
        # 读取图片内容
        img1 = cv2.imread(file1, 0)
        img2 = cv2.imread(file2, 0)

        # 使用ORB特征检测器和描述符，计算关键点和描述符
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        # 暴力匹配BFMatcher，遍历描述符，确定描述符是否匹配，然后计算匹配距离并排序
        # BFMatcher函数参数：
        # normType：NORM_L1, NORM_L2, NORM_HAMMING, NORM_HAMMING2。
        # NORM_L1和NORM_L2是SIFT和SURF描述符的优先选择，NORM_HAMMING和NORM_HAMMING2是用于ORB算法
        bf = cv2.BFMatcher(normType=cv2.NORM_HAMMING, crossCheck=True)  # 暴力匹配
        # knnMatch 函数参数k是返回符合匹配的个数，暴力匹配match只返回最佳匹配结果。
        matches = bf.knnMatch(des1, des2, k=1)  # K-最近邻匹配（KNN）

        # 使用plt将两个图像的第一个匹配结果显示出来
        # 若使用knnMatch进行匹配，则需要使用drawMatchesKnn函数将结果显示
        img3 = cv2.drawMatchesKnn(img1=img1, keypoints1=kp1, img2=img2, keypoints2=kp2, matches1to2=matches,
                                  outImg=img2,
                                  flags=2)
        # plt.imshow(img3), plt.show()
        cv2.imshow('KNN_BFMatcher', img3)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def cv_SURF_FLANN(file1='./res/images/tieta1.jpg', file2='./res/images/tieta2.jpg'):
        """
        相对暴力匹配BFMatcher来讲，这匹配算法比较准确、快速和使用方便。
        FLANN具有一种内部机制，可以根据数据本身选择最合适的算法来处理数据集。
        值得注意的是，FLANN匹配器只能使用SURF和SIFT算法。
        :return:
        """
        queryImage = cv2.imread(file1, 0)
        trainingImage = cv2.imread(file2, 0)

        # 只使用SIFT 或 SURF 检测角点
        sift = cv2.xfeatures2d.SIFT_create()
        # sift = cv2.xfeatures2d.SURF_create(float(4000))
        kp1, des1 = sift.detectAndCompute(queryImage, None)
        kp2, des2 = sift.detectAndCompute(trainingImage, None)

        # 设置FLANN匹配器参数
        # algorithm设置可参考https://docs.opencv.org/3.1.0/dc/d8c/namespacecvflann.html
        indexParams = dict(algorithm=0, trees=5)
        searchParams = dict(checks=50)
        # 定义FLANN匹配器
        flann = cv2.FlannBasedMatcher(indexParams, searchParams)
        # 使用 KNN 算法实现匹配
        matches = flann.knnMatch(des1, des2, k=2)

        # 根据matches生成相同长度的matchesMask列表，列表元素为[0,0]
        matchesMask = [[0, 0] for i in range(len(matches))]

        # 去除错误匹配
        for i, (m, n) in enumerate(matches):
            if m.distance < 0.7 * n.distance:
                matchesMask[i] = [1, 0]

        # 将图像显示
        # matchColor是两图的匹配连接线，连接线与matchesMask相关
        # singlePointColor是勾画关键点
        drawParams = dict(matchColor=(0, 255, 0),
                          singlePointColor=(255, 0, 0),
                          matchesMask=matchesMask,
                          flags=0)
        resultImage = cv2.drawMatchesKnn(queryImage, kp1, trainingImage, kp2, matches, None, **drawParams)
        # plt.imshow(resultImage, ), plt.show()
        MatchImages.showit('resultImage', resultImage)

    @staticmethod
    def cv_SIFT_FLANN_Homography(file1='./res/img_match/t9.jpg', file2='./res/img_match/dot9.png'):
        """
        FLANN的单应性匹配，单应性是一个条件，该条件表面当两幅图像中的一副出像投影畸变时
        :return:
        """
        MIN_MATCH_COUNT = 10
        img1 = cv2.imread(file1, 0)
        img2 = cv2.imread(file2, 0)

        # 使用SIFT检测角点
        sift = cv2.xfeatures2d.SIFT_create()
        # 获取关键点和描述符
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)

        # 定义FLANN匹配器
        index_params = dict(algorithm=1, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        # 使用KNN算法匹配
        matches = flann.knnMatch(des1, des2, k=2)
        matches = sorted(matches, key=lambda x: x[0].distance / x[1].distance)
        # 去除错误匹配
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        # 单应性
        if len(good) > MIN_MATCH_COUNT:
            # 改变数组的表现形式，不改变数据内容，数据内容是每个关键点的坐标位置
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            # findHomography 函数是计算变换矩阵
            # 参数cv2.RANSAC是使用RANSAC算法寻找一个最佳单应性矩阵H，即返回值M
            # 返回值：M 为变换矩阵，mask是掩模
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            # ravel方法将数据降维处理，最后并转换成列表格式
            matchesMask = mask.ravel().tolist()
            # 获取img1的图像尺寸
            h, w = img1.shape
            # pts是图像img1的四个顶点
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            # 计算变换后的四个顶点坐标位置
            dst = cv2.perspectiveTransform(pts, M)

            # 根据四个顶点坐标位置在img2图像画出变换后的边框
            img2 = cv2.polylines(img2, [np.int32(dst)], True, (255, 0, 0), 3, cv2.LINE_AA)

        else:
            print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
            matchesMask = None

        # 显示匹配结果
        draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                           singlePointColor=None,
                           matchesMask=matchesMask,  # draw only inliers
                           flags=2)
        img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
        plt.figure(figsize=(10, 8)), plt.imshow(img3, 'gray'), plt.show()
        # MatchImages.showit('gray', img3)

    @staticmethod
    def cv_SIFT_FLANN_Homography_matix(file1='./res/images/1.png', file2='./res/images/2.png',
                                       file3='./res/images/3.png'):
        """
        实际应用
        :return:
        """
        img1 = cv2.imread(file1, 0)
        img2 = cv2.imread(file2, 0)

        # 使用SIFT检测角点
        sift = cv2.xfeatures2d.SIFT_create()
        # 获取关键点和描述符
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)

        # 定义FLANN匹配器
        index_params = dict(algorithm=1, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        # 使用KNN算法匹配
        matches = flann.knnMatch(des1, des2, k=2)

        # 去除错误匹配
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        # 单应性实际应用
        # 改变数组的表现形式，不改变数据内容，数据内容是每个关键点的坐标位置
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        # findHomography 函数是计算变换矩阵
        # 参数cv2.RANSAC是使用RANSAC算法寻找一个最佳单应性矩阵H，即返回值M
        # 返回值：M 为变换矩阵，mask是掩模
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        # 获取img1的图像尺寸
        h, w = img1.shape
        # pts是图像img1的四个顶点
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        # 计算变换后的四个顶点坐标位置
        dst = cv2.perspectiveTransform(pts, M)

        # 图片替换
        img3 = cv2.imread(file3, 0)
        # 降维处理
        b = np.int32(dst).reshape(4, 2)
        x, y = img2.shape
        # 根据变换矩阵将图像img3进行变换处理
        res = cv2.warpPerspective(img3, M, (y, x))
        img_temp = img2.copy()
        # 将图像img2的替换区域进行填充处理
        cv2.fillConvexPoly(img_temp, b, 0)
        # 将变换后的img3图像替换到图像img2
        cv2.imshow('bb', img_temp)
        res = img_temp + res

        # plt.imshow(res), plt.show()
        cv2.imshow('aa', res)
        # cv2.imshow('1', img1)
        # cv2.imshow('2', img2)
        # cv2.imshow('3', img3)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def save_descriptor(folder, image_path, feature_detector):
        # 判断图片是否为npy格式
        if image_path.endswith("npy"):
            return
        # 读取图片并检查特征
        file = os.path.join(folder, image_path)
        # file = file.replace('\\', '/')
        # print(file)
        img = cv2.imread(file, 0)
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度处理图像

        keypoints, descriptors = feature_detector.detectAndCompute(img, None)
        # 设置文件名并将特征数据保存到npy文件
        descriptor_file = image_path.replace("png", "npy")
        np.save(os.path.join(folder, descriptor_file), descriptors)

    @staticmethod
    def create_descriptors(folder):
        """
        首先获取多个图片的全部图片的特征数据
        :param folder: 图片目录
        :return:
        """

        files = []
        # for (dirpath, dirnames, filenames) in walk(folder):
        #     files.extend(filenames)
        files = [f for f in os.listdir(folder)]  # 输出根path下的所有文件名到一个列表中
        # print(files)

        for f in files:
            if '.png' in f:
                MatchImages.save_descriptor(folder, f, cv2.xfeatures2d.SIFT_create())

    @staticmethod
    def matching(folder, file='E:/python/games/res/img_match/t9.jpg'):
        """
        根据图1与这些特征数据文件进行匹配，从而找出最佳匹配的图片
        :return:
        """

        query = cv2.imread(file, 0)
        if query is None:
            print('aaa', type(query))
            return

        descriptors = []
        # 获取特征数据文件名
        dirs = os.listdir(folder)  # 输出 path下的所有文件名到一个列表中

        for f in dirs:
            if f.endswith("npy"):
                descriptors.append(f)
        print(descriptors)

        # 使用SIFT算法检查图像的关键点和描述符
        sift = cv2.xfeatures2d.SIFT_create()
        query_kp, query_ds = sift.detectAndCompute(query, None)

        # 创建FLANN匹配器
        index_params = dict(algorithm=0, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        potential_culprits = {}
        for d in descriptors:
            # 将图像query与特征数据文件的数据进行匹配
            matches = flann.knnMatch(query_ds, np.load(os.path.join(folder, d)), k=2)
            # 清除错误匹配
            good = []
            for m, n in matches:
                if m.distance < 0.7 * n.distance:
                    good.append(m)
            # 输出每张图片与目标图片的匹配数目
            print("img is %s ! matching rate is (%d)" % (d, len(good)))
            potential_culprits[d] = len(good)

        # 获取最多匹配数目的图片
        max_matches = None
        potential_suspect = None
        for culprit, matches in potential_culprits.items():
            if max_matches is None or matches > max_matches:
                max_matches = matches
                potential_suspect = culprit

        print("potential suspect is %s" % potential_suspect.replace("npy", "").upper())

    @staticmethod
    def showit(title, img):
        if isinstance(img, np.ndarray):
            # cv2.imshow(title, img)  # 展示图片
            cv2.imshow(MatchImages.zh_ch(title), img)  # 展示图片
            cv2.waitKey(0)  # 等待按键按下
            # time.sleep(20)
            cv2.destroyAllWindows()  # 清除所有窗口

    @staticmethod
    def zh_ch(title):
        """
        显示中文时乱码的转换
        :param title:
        :return:
        """
        if isinstance(title, str):
            return title.encode("gbk").decode(errors="ignore")


class PickBlock(object):
    def __init__(self, parent=None):
        super(PickBlock, self).__init__()
        self.parent = parent

        self.file = 'E:/python/games/res/img_match/TeMEAN.png'
        self.f1 = 'E:/python/games/res/img_match/shapes.png'
        self.f2 = 'E:/python/games/res/img_match/yinzhang.png'

        # self.findBlackBlock()
        self.Hough_check(self.file, 0)
        # self.Hough_check('E:/python/games/res/img_match/yuan.png', 1)
        # self.Hough_check('E:/python/games/res/img_match/pingzi.png', 1)
        # self.findAllBlock()
        # self.cutCircles()
        # self.checkit(self.file)

    def findBlackBlock(self):
        # 读取图片
        image = cv2.imread(self.file)

        # 寻找到图片中的黑色形状块
        lower = np.array([0, 0, 0])
        upper = np.array([15, 15, 15])
        shapeMask = cv2.inRange(image, lower, upper)

        # 在mask中寻找轮廓
        cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        print("I found {} black shapes".format(len(cnts)))
        cv2.imwrite("Mask.png", shapeMask)
        cv2.imshow("Mask", shapeMask)

        # 循环遍历所有的轮廓
        for c in cnts:
            # draw the contour and show it
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        # cv2.imwrite("shape1.png", image)
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()  # 清除所有窗口

    def findAllBlock(self):
        img = cv2.imread(self.f1)
        # 转换为灰度图片
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 进行二值化处理
        ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # 寻找轮廓
        _, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # 绘制不同的轮廓
        draw_img0 = cv2.drawContours(img.copy(), contours, 0, (0, 255, 255), 3)
        draw_img1 = cv2.drawContours(img.copy(), contours, 1, (255, 0, 255), 3)
        draw_img2 = cv2.drawContours(img.copy(), contours, 2, (255, 255, 0), 3)
        draw_img3 = cv2.drawContours(img.copy(), contours, -1, (0, 0, 255), 3)

        # 打印结果
        print("contours:类型：", type(contours))
        print("第0 个contours:", type(contours[0]))
        print("contours 数量：", len(contours))

        print("contours[0]点的个数：", len(contours[0]))
        print("contours[1]点的个数：", len(contours[1]))

        # 显示并保存结果
        cv2.imshow("img", img)
        cv2.imshow("draw_img0", draw_img0)
        cv2.imshow("draw_img1", draw_img1)
        cv2.imshow("draw_img2", draw_img2)
        # cv2.imwrite("rect_result.png", draw_img3)
        cv2.imshow("draw_img3", draw_img3)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def cutCircles(self):
        def is_contour_bad(c):
            # 近似轮廓
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            # 判断当前的轮廓是不是矩形
            return not len(approx) == 4

        # 首先读取图片；然后进行颜色转换；最后进行边缘检测
        image = cv2.imread(self.file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 50, 100)
        cv2.imshow("Original", image)

        # 寻找图中的轮廓并设置mask
        cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        mask = np.ones(image.shape[:2], dtype="uint8") * 255

        # 循环遍历所有的轮廓
        for c in cnts:
            # 检测该轮廓的类型，在新的mask中绘制结果
            if is_contour_bad(c):
                cv2.drawContours(mask, [c], -1, 0, -1)

        # 移除不满足条件的轮廓并显示结果
        image = cv2.bitwise_and(image, image, mask=mask)
        cv2.imwrite("Mask.png", mask)
        cv2.imshow("Mask", mask)
        cv2.imwrite("result.png", image)
        cv2.imshow("After", image)
        cv2.waitKey(0)

    @staticmethod
    def checkit(file):
        def otsu_seg(img):
            ret_th, bin_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            return ret_th, bin_img

        def find_pole(bin_img):
            img, contours, hierarchy = cv2.findContours(bin_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            area = 0
            for i in range(len(contours)):
                area += cv2.contourArea(contours[i])
            area_mean = area / len(contours)
            mark = []
            for i in range(len(contours)):
                if cv2.contourArea(contours[i]) < area_mean:
                    mark.append(i)

            return img, contours, hierarchy, mark

        def draw_box(img, contours):
            img = cv2.rectangle(img,
                                (contours[0][0], contours[0][1]),
                                (contours[1][0], contours[1][1]),
                                (255, 255, 255),
                                3)
            return img

        img = cv2.imread(file)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, th = otsu_seg(gray)
        img_new, contours, hierarchy, mark = find_pole(th)
        for i in range(len(contours)):
            if i not in mark:
                left_point = contours[i].min(axis=1).min(axis=0)
                right_point = contours[i].max(axis=1).max(axis=0)
                img = draw_box(img, (left_point, right_point))

        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def Hough_check(imgfile, style=0):
        """
        霍夫变换算法可以快速、准确的检测出图片中的直线、圆和椭圆等多种形状
        :param imgfile:
        :param style:0-直线，1-圆，2-椭圆
        :return:
        """

        img = cv2.imread(imgfile)  # 读取图片
        output = img.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 彩色图片灰度化

        edges = cv2.Canny(gray, 100, 200)  # 执行边缘检测
        # 显示原始结果
        # cv2.imwrite('edges.png', edges)
        cv2.imshow('edge', edges)

        if style == 0:
            # 执行Hough直线检测
            lines = cv2.HoughLines(edges, 1, np.pi / 180, 160)

            if lines is None:
                print("no lines")
                return
            lines1 = lines[:, 0, :]
            for rho, theta in lines1:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * a)
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * a)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 1)

            # cv2.imwrite('line.png', img)
            cv2.imshow('line', img)

        elif style == 1:
            gaussian = cv2.GaussianBlur(gray, (3, 3), 0)
            circles1 = cv2.HoughCircles(gaussian, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=30, minRadius=15,
                                        maxRadius=80)
            print(np.shape(circles1))  # hough_gradient 霍夫梯度法
            circles = circles1[0, :, :]
            circles = np.uint16(np.around(circles))
            for i in circles[:]:
                cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 3)
                cv2.circle(img, (i[0], i[1]), 2, (255, 0, 255), 10)
            cv2.imshow('img', img)

            # 应用hough变换进行圆检测
            # circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)

            # # 确保至少发现一个圆
            # if circles is None:
            #     print("no circles")
            #     return
            #
            # # 进行取整操作
            # circles = np.round(circles[0, :]).astype("int")
            # # 循环遍历所有的坐标和半径
            # for (x, y, r) in circles:
            #     # 绘制结果
            #     cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            #     cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            #
            # cv2.imshow("output", np.hstack([img, output]))  # 显示结果

        elif style == 2:
            # 加载图片，转换成灰度图并检测边缘
            image_rgb = data.coffee()[0:220, 160:420]  # 裁剪原图像，不然速度非常慢
            image_gray = color.rgb2gray(image_rgb)
            edges = feature.canny(image_gray, sigma=2.0, low_threshold=0.55, high_threshold=0.8)

            # 执行椭圆变换
            result = transform.hough_ellipse(edges, accuracy=20, threshold=250, min_size=100, max_size=120)
            result.sort(order='accumulator')  # 根据累加器排序

            # 估计椭圆参数
            best = list(result[-1])  # 排完序后取最后一个
            yc, xc, a, b = [int(round(x)) for x in best[1:5]]
            orientation = best[5]

            # 在原图上画出椭圆
            cy, cx = draw.ellipse_perimeter(yc, xc, a, b, orientation)
            image_rgb[cy, cx] = (0, 0, 255)  # 在原图中用蓝色表示检测出的椭圆

            # #分别用白色表示canny边缘，用红色表示检测出的椭圆，进行对比
            # edges = color.gray2rgb(edges)
            # edges[cy, cx] = (250, 0, 0)

            fig2, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(8, 4))

            ax1.set_title('Original picture')
            ax1.imshow(image_rgb)

            ax2.set_title('Detect result')
            ax2.imshow(edges)

            plt.show()

        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    MatchImages()
    # AlikeImages()
    # PickBlock()
