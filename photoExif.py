#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Project: PyCharm
# @File    : photoExif.py
# @Author  : tiger
# @Email   : shdorado@126.com
# @Time    : 2020/3/30 15:22

import sys
import os
import exifread
# import piexif
from PIL.ExifTags import TAGS
from PIL import Image
import pyexiv2  #
import json
import math
import time
import re
from multiprocessing import Process, Pool
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from ui_photo_exif import Ui_MainWindow
from utilities import Utils


class GaugeSpeed(QtWidgets.QFrame):
    def __init__(self, parent=None, filename=None):
        super(PaintArea, self).__init__()
        self.parent = parent
        self.photo_file = filename

        self.label = None
        self.vl = None

        self._setup_ui()

    def set_file(self, filename):
        self.file_name = filename

    def _setup_ui(self):
        # ---------------------设置 frame--------------------- #
        # setFrameStyle(int style) - 同时设置边框和女阴影。style是QFrame.Shape和QFrame.Shadow的"|"组合。

        # 设置边框样式
        #     NoFrame，0：无边框
        #     Box，1：矩形框
        #     Panel，2：凸起或凹陷的面板
        #     WinPanel，3： Windows 2000风格的面板，可以是凸起或下沉。边框的宽度是2像素。此属性是为了与旧版本的Qt兼容而存在的;
        #     HLine，4：水平线(用作分隔符);
        #     VLine，5：垂直线(用作分隔符);
        #     StyledPanel，6：依据当前GUI类型，画一个矩形面板，可以凸起或下沉
        self.setFrameShape(QtWidgets.QFrame.Box)
        # 设置边框的阴影，只有加了这步才能设置边框颜色
        # 可选样式有Raised凸、Sunken凹、Plain直线（这个无法设置颜色）等
        self.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.setLineWidth(3)  # 设置边框宽度
        self.setMidLineWidth(2)  # 设置边框中间线宽
        self.setStyleSheet('background-color:skyblue')

        # ---------------------设置 label--------------------- #
        self.label = QtWidgets.QLabel()
        # self.label.setScaledContents(True)  # 让图片自适应label大小
        # self.label.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Raised)

        # # 设置边框样式 可选样式有Box Panel等
        # self.label.setFrameShape(QtWidgets.QFrame.Box)
        # # 设置阴影 只有加了这步才能设置边框颜色
        # # 可选样式有Raised凸、Sunken凹、Plain直线（这个无法设置颜色）等
        # self.label.setFrameShadow(QtWidgets.QFrame.Sunken)
        #
        # self.setLineWidth(2)  # 设置线条宽度
        self.label.setAlignment(QtCore.Qt.AlignCenter)  # 设置对齐方式为居中
        # # 设置背景颜色，包括边框颜色
        # # self.label.setStyleSheet("border-width: 6px;border-style: solid;border-color: rgb(255, 170, 0);")
        # # self.label.setStyleSheet('background-color: rgb(255, 0, 0)')
        # self.vl = QtWidgets.QVBoxLayout(self)
        # self.vl.setContentsMargins(0, 0, 0, 0)
        # self.vl.addWidget(self.label)

    def _scaled_photo(self):
        if not self.photo_file:
            return

        # 设置显示的图片
        image = QtGui.QImage(self.photo_file)
        pm = QtGui.QPixmap.fromImage(image)

        pm_size = QtCore.QSize(800, 600)
        # 按比例缩放, 默认不按比例
        return pm.scaled(pm_size, QtCore.Qt.KeepAspectRatio | QtCore.Qt.SmoothTransformation)

    def drawText(self, painter):
        for i in range(self.scaleMajor + 1):  # self.scaleMajor = 8, 8个主刻度
            # 正余弦计算
            sina = math.sin(startRad - i * deltaRad)
            cosa = math.cos(startRad - i * deltaRad)

            # 刻度值计算
            value = math.ceil((1.0 * i * (
                    (self.maxValue - self.minValue) / self.scaleMajor) + self.minValue))  # math.ceil(x)：返回不小于x的最小整数
            strValue = str(int(value))

            # 字符的宽度和高度
            textWidth = self.fontMetrics().width(strValue)
            textHeight = self.fontMetrics().height()

            # 字符串的起始位置。注意考虑到字符宽度和高度进行微调
            x = radius * cosa - textWidth / 2
            y = -radius * sina + textHeight / 4
            painter.drawText(x - offset, y, strValue + "M")

    def drawLine(self, painter):
        painter.rotate(self.startAngle)  # self.startAngle = 45,旋转45度
        steps = 8  # 8个刻度
        angleStep = (360.0 - self.startAngle - self.endAngle) / steps  # 刻度角

        painter.setPen(pen)
        painter.drawLine(0, radius - 5, 0, radius)
        painter.rotate(angleStep)

    def drawPointerIndicator(self, painter):
        painter.save()
        # 绘制指针
        radius = 68  # 指针长度
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.pointerColor)

        # (-5, 0), (0, -8), (5, 0)和（0, radius) 四个点绘出指针形状
        pts = QtGui.QPolygon()
        pts.setPoints(-5, 0, 0, -8, 5, 0, 0, radius)

        # 旋转指针，使得指针起始指向为0刻度处
        painter.rotate(self.startAngle)
        degRotate = (360.0 - self.startAngle - self.endAngle) / (self.maxValue - self.minValue) \
                    * (self.currentValue - self.minValue)
        painter.rotate(degRotate)
        painter.drawConvexPolygon(pts)
        painter.restore()

    def drawColorPie(self, painter):  # 绘制三色环
        painter.save()  # save()保存当前坐标系

        # 设置扇形部分区域
        radius = 99  # 半径
        painter.setPen(QtCore.Qt.NoPen)
        rect = QtCore.QRectF(-radius, -radius, radius * 2, radius * 2)  # 扇形所在圆区域

        # 计算三色圆环范围角度。green：blue：red = 1：2：1
        angleAll = 360.0 - self.startAngle - self.endAngle  # self.startAngle = 45, self.endAngle = 45
        angleStart = angleAll * 0.25
        angleMid = angleAll * 0.5
        angleEnd = angleAll * 0.25

        # 圆的中心部分填充为透明色，形成环的样式
        rg = QtGui.QRadialGradient(0, 0, radius, 0, 0)  # 起始圆心坐标，半径，焦点坐标
        ratio = 0.9  # 透明：实色 = 0.9 ：1

        # 绘制绿色环
        rg.setColorAt(0, QtCore.Qt.transparent)  # 透明色
        rg.setColorAt(ratio, QtCore.Qt.transparent)
        rg.setColorAt(ratio + 0.01, self.pieColorStart)
        rg.setColorAt(1, self.pieColorStart)

        painter.setBrush(rg)
        painter.drawPie(rect, (270 - self.startAngle - angleStart) * 16, angleStart * 16)

        # 绘制蓝色环
        rg.setColorAt(0, QtCore.Qt.transparent)
        rg.setColorAt(ratio, QtCore.Qt.transparent)
        rg.setColorAt(ratio + 0.01, self.pieColorMid)
        rg.setColorAt(1, self.pieColorMid)

        painter.setBrush(rg)
        painter.drawPie(rect, (270 - self.startAngle - angleStart - angleMid) * 16, angleMid * 16)

        # 绘制红色环
        rg.setColorAt(0, QtCore.Qt.transparent)
        rg.setColorAt(ratio, QtCore.Qt.transparent)
        rg.setColorAt(ratio + 0.01, self.pieColorEnd)
        rg.setColorAt(1, self.pieColorEnd)

        painter.setBrush(rg)
        painter.drawPie(rect, (270 - self.startAngle - angleStart - angleMid - angleEnd) * 16, angleEnd * 16)

        painter.restore()  # restore()恢复坐标系

    def paintEvent(self, event):
        # 坐标轴变换
        width = self.width()
        height = self.height()
        painter = QtGui.QPainter(self)  # 初始化painter
        painter.translate(width / 2, height / 2)  # 坐标轴变换，调用translate()将坐标原点平移至窗口中心

        # 坐标刻度自适应
        side = min(width, height)
        painter.scale(side / 200.0, side / 200.0)  # 本项目中将坐标缩小为side/200倍，即画出length=10的直线，其实际长度应为10*(side/200)。

        # 启用反锯齿，使画出的曲线更平滑
        painter.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.TextAntialiasing)

        p = QtGui.QPainter(self)
        # self.setPalette(QPalette(Qt.white))
        # self.setAutoFillBackground(True)
        # self.setMinimumSize(400, 400)
        # self.pen = QtGui.QPen()
        # self.brush = QtGui.QBrush()

        # p.setPen(self.pen)
        # p.setBrush(self.brush)
        # pm = self._update_photo()
        # if pm:
        #     px = pm.width()
        #     sx = self.width()
        #     if px == sx:  # 高没有充满,需要居中
        #         py = pm.height()
        #         sy = self.height()
        #         dy = (sy - py) // 2
        #         p.drawPixmap(0, dy, pm)
        #     else:  # 宽没有充满,需要居中
        #         dx = round((sx - px) / 2)
        #         print(sx, dx)
        #         p.drawPixmap(dx, 0, pm)

    def resizeEvent(self, event):
        pass


class CustomFileModel(QtWidgets.QFileSystemModel):
    def __init__(self, manager=None, *args, **kwargs):
        super(CustomFileModel, self).__init__(*args, **kwargs)
        self.check_list = []

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        if (section == 0) and (role == QtCore.Qt.DisplayRole):
            return "磁盘"
        else:
            return QtWidgets.QFileSystemModel.headerData(self, section, orientation, role)

    def flags(self, index):
        # index = QtCore.QModelIndex()
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        result = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        if index.column() == 0:  # 只让第一列显示checkbox
            result |= QtCore.Qt.ItemIsUserCheckable
        return result

    # def data(self, index, role=None):
    #     if not index.isValid():
    #         return None
    #
    #     item = index.internalPointer()
    #
    #     if role == QtCore.Qt.CheckStateRole:  # 被选中项是checkbox
    #         if item.parent() == self.rootDirectory():   # .rootItem:  # 如果是根的话，直接返回
    #             return None
    #         if item.childCount() > 0:  # 如果是有子项的话，直接返回，这个可以根据需要调整。当需要成组选择的时候，必须保留
    #             return None
    #         if index.column() == 0:
    #             for x in self.check_list:  # 检查该项是否在checkList中，如果在将其设为选中状态
    #                 if x == index:
    #                     return QtCore.Qt.Checked
    #             else:
    #                 return QtCore.Qt.Unchecked
    #     if role != QtCore.Qt.DisplayRole:
    #         return None
    #     return item.data(index.column())
    #

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.CheckStateRole and index.column() == 0:
            if value == QtCore.Qt.Unchecked:  # 撤销选中的情况
                self.check_list.remove(index)  # 将节点的index从checklist中移除
                # self.emit(QtCore.PYQT_SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                #           index, index)
                self.dataChanged.emit(index, index)
            else:  # 选中的情况
                self.check_list.append(index)  # 将节点的index加到checklist中
                # self.emit(QtCore.SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                #           index, index)
                self.dataChanged.emit(index, index)
            return True


class CustomSlider(QtWidgets.QSlider):
    def __init__(self, manager=None, *args, **kwargs):
        super(CustomSlider, self).__init__(*args, **kwargs)

        self.label = QtWidgets.QLabel(self)
        self.label.setFixedSize(QtCore.QSize(20, 20))

        # 设置游标背景为白色
        self.label.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.white)
        self.label.setPalette(palette)
        self.label.setAlignment(QtCore.Qt.AlignCenter);

        self.label.setVisible(False)
        self.label.move(self.x(), self.y() + 3)

    def mousePressEvent(self, mouse_event):
        if not self.label.isVisible():
            self.label.setVisible(True)
            self.label.setText(str(self.value()))

        QtWidgets.QSlider.mousePressEvent(self, mouse_event)

    def mouseReleaseEvent(self, mouse_event):
        if self.label.isVisible():
            self.label.setVisible(False)
        QtWidgets.QSlider.mouseReleaseEvent(self, mouse_event)

    def mouseMoveEvent(self, event):
        # s = QtCore.QPointF()
        s = event.windowPos()
        self.setMouseTracking(True)
        # print(type(s))
        self.label.setText(str(self.value()))
        # self.label.move(self.width()-self.label.width()*self.value()//(self.maximum()-self.minimum()), 3)
        self.label.move(int(s.x()), int(s.y()) + 3)
        QtWidgets.QSlider.mouseMoveEvent(self, event)


class Exif:
    exif_key_flag = {  # Exif标识
        'Exif版本': 'ExifVersion', 'FlashPix 版本': 'FlashPixVersion', '色域、色彩空间': 'ColorSpace',
        '图像的有效宽度': 'PixelXDimension', '图像的有效高度': 'PixelYDimension',
        '图像构造': 'ComponentsConfiguration', '压缩时每像素色彩位': 'CompressedBitsPerPixel',
        '制造商设置的信息': 'MakerNote', '用户评论': 'UserComment',
        '关联的声音文件': 'RelatedSoundFile', '创建时间': 'DateTimeOriginal',
        '数字化创建时间': 'DateTimeDigitized', '日期时间（秒）': 'SubsecTime',
        '原始日期时间（秒）': 'SubsecTimeOriginal', '原始日期时间数字化（秒）': 'SubsecTimeDigitized',
        '曝光时间': 'ExposureTime', '光圈值': 'FNumber',
        '曝光程序': 'ExposureProgram', '光谱灵敏度': 'SpectralSensitivity',
        '感光度': 'ISOSpeedRatings', '光电转换功能': 'OECF',
        '快门速度': 'ShutterSpeedValue', '镜头光圈': 'ApertureValue',
        '亮度': 'BrightnessValue', '曝光补偿': 'ExposureBiasValue',
        '最大光圈': 'MaxApertureValue', '物距': 'SubjectDistance',
        '测光方式': 'MeteringMode', '光源': 'Lightsource',
        '闪光灯': 'Flash', '主体区域': 'SubjectArea',
        '焦距': 'FocalLength', '闪光灯强度': 'FlashEnergy',
        '空间频率反应': 'SpatialFrequencyResponse', '焦距平面X轴解析度': 'FocalPlaneXResolution',
        '焦距平面Y轴解析度': 'FocalPlaneYResolution', '焦距平面解析度单位': 'FocalPlaneResolutionUnit',
        '主体位置': 'SubjectLocation', '曝光指数': 'ExposureIndex',
        '图像传感器类型': 'SensingMethod', '源文件': 'FileSource',
        '场景类型（1 == 直接拍摄）': 'SceneType', 'CFA 模式': 'CFAPattern',
        '自定义图像处理': 'CustomRendered', '曝光模式': 'ExposureMode',
        '白平衡（1 == 自动，2 == 手动）': 'WhiteBalance', '数字变焦': 'DigitalZoomRation',
        '35毫米胶片焦距': 'FocalLengthIn35mmFilm', '场景拍摄类型': 'SceneCaptureType',
        '场景控制': 'GainControl', '对比度': 'Contrast',
        '饱和度': 'Saturation', '锐度': 'Sharpness',
        '设备设定描述': 'DeviceSettingDescription', '主体距离范围': 'SubjectDistanceRange',
        '无名': 'InteroperabilityIFDPointer', '图像唯一ID': 'ImageUniqueID'}
    exif_key_GPS = {  # GPS信息
        '南北纬': 'GPSLatitudeRef', '纬度': 'GPSLatitude',
        '东西经': 'GPSLongitudeRef', '经度': 'GPSLongitude',
        '海拔参照值': 'GPSAltitudeRef', '海拔': 'GPSAltitude',
        'GPS 时间戳': 'GPSTimeStamp', '测量的卫星': 'GPSSatellites',
        '接收器状态': 'GPSStatus', '测量模式': 'GPSMeasureMode',
        '测量精度': 'GPSDOP', '速度单位': 'GPSSpeedRef',
        'GPS 接收器速度': 'GPSSpeed', '移动方位参照': 'GPSTrackRef',
        '移动方位': 'GPSTrack', '图像方位参照': 'GPSImgDirectionRef',
        '图像方位': 'GPSImgDirection', '地理测量资料': 'GPSMapDatum',
        '目标纬度参照': 'GPSDestLatitudeRef', '目标纬度': 'GPSDestLatitude',
        '目标经度参照': 'GPSDestLongitudeRef', '目标经度': 'GPSDestLongitude',
        '目标方位参照': 'GPSDestBearingRef', '目标方位': 'GPSDestBearing',
        '目标距离参照': 'GPSDestDistanceRef', '目标距离': 'GPSDestDistance',
        'GPS 处理方法名': 'GPSProcessingMethod', 'GPS 区功能变数名': 'GPSAreaInformation',
        'GPS 日期': 'GPSDateStamp', 'GPS 修正': 'GPSDifferential'}
    exif_key_image = {  # 图片相关
        '宽度': 'ImageWidth', '型号': 'Model',
        '高度': 'ImageHeight', '拍摄方向': 'Orientation',
        '时间': 'DateTime', '色相配置': 'YCbCrPositioning',
        '分辨率单位': 'ResolutionUnit', '无名': 'ExifOffset'}

    def latitude_and_longitude_convert_to_decimal_system(*arg):
        """
        经纬度转为小数, 作者尝试适用于iphone6、ipad2以上的拍照的照片，
        :param arg:
        :return: 十进制小数
        """
        return float(arg[0]) + (
                (float(arg[1]) + (float(arg[2].split('/')[0]) / float(arg[2].split('/')[-1]) / 60)) / 60)

    def find_GPS_image(pic_path):
        GPS = {}
        date = ''
        with open(pic_path, 'rb') as f:
            tags = exifread.process_file(f)
            for tag, value in tags.items():
                if re.match('Image Make', tag):
                    print('[*] 品牌信息: ' + str(value))
                if re.match('Image Model', tag):
                    print('[*] 具体型号: ' + str(value))
                if re.match('EXIF LensModel', tag):
                    print('[*] 摄像头信息: ' + str(value))
                if re.match('GPS GPSLatitudeRef', tag):
                    GPS['GPSLatitudeRef'] = str(value)
                elif re.match('GPS GPSLongitudeRef', tag):
                    GPS['GPSLongitudeRef'] = str(value)
                elif re.match('GPS GPSAltitudeRef', tag):
                    GPS['GPSAltitudeRef'] = str(value)
                elif re.match('GPS GPSLatitude', tag):
                    try:
                        match_result = re.match('\[(\w*),(\w*),(\w.*)/(\w.*)\]', str(value)).groups()
                        GPS['GPSLatitude'] = int(match_result[0]), int(match_result[1]), int(match_result[2])
                    except:
                        deg, min, sec = [x.replace(' ', '') for x in str(value)[1:-1].split(',')]
                        GPS['GPSLatitude'] = latitude_and_longitude_convert_to_decimal_system(deg, min, sec)
                elif re.match('GPS GPSLongitude', tag):
                    try:
                        match_result = re.match('\[(\w*),(\w*),(\w.*)/(\w.*)\]', str(value)).groups()
                        GPS['GPSLongitude'] = int(match_result[0]), int(match_result[1]), int(match_result[2])
                    except:
                        deg, min, sec = [x.replace(' ', '') for x in str(value)[1:-1].split(',')]
                        GPS['GPSLongitude'] = latitude_and_longitude_convert_to_decimal_system(deg, min, sec)
                elif re.match('GPS GPSAltitude', tag):
                    GPS['GPSAltitude'] = str(value)
                elif re.match('.*Date.*', tag):
                    date = str(value)
        # print({'GPS_information':GPS, 'date_information': date})
        print('[*] 拍摄时间: ' + date)
        return {'GPS_information': GPS, 'date_information': date}

    def find_address_from_GPS(GPS):
        """
        使用Geocoding API把经纬度坐标转换为结构化地址。
        :param GPS:
        :return:
        """
        secret_key = ''
        if not GPS['GPS_information']:
            return '该照片无GPS信息'
        lat, lng = GPS['GPS_information']['GPSLatitude'], GPS['GPS_information']['GPSLongitude']
        print('[*] 经度: ' + str(lat) + ', 纬度: ' + str(lng))
        baidu_map_api = "http://api.map.baidu.com/geocoder/v2/?ak={0}&callback=renderReverse&location={1},{2}s&output=json&pois=0".format(
            secret_key, lat, lng)
        response = requests.get(baidu_map_api)
        content = response.text.replace("renderReverse&&renderReverse(", "")[:-1]
        # print(content)
        baidu_map_address = json.loads(content)
        formatted_address = baidu_map_address["result"]["formatted_address"]
        # province = baidu_map_address["result"]["addressComponent"]["province"]
        # city = baidu_map_address["result"]["addressComponent"]["city"]
        # district = baidu_map_address["result"]["addressComponent"]["district"]
        return formatted_address


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    # region 初始化与动态区
    def __init__(self):
        super(MainWindow, self).__init__()
        # self.pool = Pool()  # 进程池，默认跟cpu核心一样多

        # self.ml = QtWidgets.QVBoxLayout(self)
        self.label = None
        self.show_speed = 5  # 每秒翻看一张
        self.ext_filter = 'Photo Files (*.png *.xpm *.jpg *.jpeg, *.bmp);;All Files (*);;'
        self.suffix = ['.jpg', '.jpeg', '.bmp', '.png', '*.xpm']
        self.photo_file = r'I:\照片\2006年\son-06年\100_0003.jpg'
        self.search_path = []  # 需要搜索的目录列表
        self.cur_path = ''  # 当前的路径
        self.cur_files = []  # 当前路径下的文件
        self.cur_index = 0
        self.ROOT = ''
        self.save_file = 'e:\\fileslist.txt'
        self.Icon_size_max = QtCore.QSize(50, 50)  # 列表框的设置
        self.grid_size = QtCore.QSize(80, 80)
        self.hint_size = QtCore.QSize(80, 100)
        self.auto_play = False
        self.sub_dir = False

        # TODO(tiger) Change this to use relations
        # vl = QtWidgets.QVBoxLayout(self)
        # self.pa = PaintArea(self, self.photo_file)
        # vl.addWidget(self.pa)

        self._setup_ui()

    def __del__(self):
        # print('User 对象被回收---')
        class_name = self.__class__.__name__
        print(class_name, '销毁')
        # self.pool.terminate()
        # self.pool.join()

    # def poolNotEmpty(self):
    #     return len(self.pool._cache) > 1    # pool._cache 是当前有任务的进程数， ==1表示所有任务结束

    def _setup_ui(self):
        self.setupUi(self)
        # self.setWindowTitle('照片exif信息')
        # self.setGeometry(0, 0, 800, 600)
        # self.setFixedSize(1500, 756)
        self.center()
        self._init_photo()
        self._init_tree_view()
        self._init_list_view()
        self._init_dial()

        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _init_photo(self):
        # self.wg_photo.setStyleSheet('background-color:#37474F')
        self.wg_photo.setFixedSize(QtCore.QSize(1052, 650))  # 黄金分割
        self.vl_photo = QtWidgets.QVBoxLayout(self.wg_photo)
        self.vl_photo.setContentsMargins(2, 0, 0, 0)
        self.vl_photo.setSpacing(0)
        self.lb_photo = QtWidgets.QLabel()
        # # 设置背景颜色，包括边框颜色
        # self.lb_photo.setStyleSheet("border-width: 6px;border-style: solid;border-color: rgb(255, 170, 0);")
        # self.lb_photo.setStyleSheet('background-color:Thistle')
        # 同时设置边框和女阴影。style是QFrame.Shape和QFrame.Shadow的"|"组合。
        self.lb_photo.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Raised)
        # 设置边框样式
        #     NoFrame，0：无边框
        #     Box，1：矩形框
        #     Panel，2：凸起或凹陷的面板
        #     WinPanel，3： Windows 2000风格的面板，可以是凸起或下沉。边框的宽度是2像素。此属性是为了与旧版本的Qt兼容而存在的;
        #     HLine，4：水平线(用作分隔符);
        #     VLine，5：垂直线(用作分隔符);
        #     StyledPanel，6：依据当前GUI类型，画一个矩形面板，可以凸起或下沉
        # self.lb_photo.setFrameShape(QtWidgets.QFrame.Box)
        # 设置边框的阴影，只有加了这步才能设置边框颜色
        # 可选样式有Raised凸、Sunken凹、Plain直线（这个无法设置颜色）等
        # self.lb_photo.setFrameShadow(QtWidgets.QFrame.Sunken)
        # self.label.setScaledContents(True)  # 让图片自适应label大小
        self.lb_photo.setLineWidth(2)  # 设置边框宽度
        self.lb_photo.setAlignment(QtCore.Qt.AlignCenter)  # 设置对齐方式为居中
        self.vl_photo.addWidget(self.lb_photo)

    def _init_list_view(self):
        # self.list_wg.setModel(self.model)
        # self.list_wg.setRootIndex(self.model.index(self.ROOT))
        self.list_wg.setSpacing(20)  # 设置单元项间距
        self.list_wg.setViewMode(QtWidgets.QListView.IconMode)  # 设置显示模式，图片在上，名字在下，横向排列
        self.list_wg.setIconSize(self.Icon_size_max)  # 设置图标的大小：
        self.list_wg.setGridSize(self.grid_size)  # 设置网格的大小：
        self.list_wg.setResizeMode(QtWidgets.QListView.Adjust)  # 设置自动适应布局调整（Adjust适应，Fixed不适应），默认不适应
        # 设置图标可不可以移动，默认是可移动的，但可以改成静态的：
        self.list_wg.setMovement(QtWidgets.QListView.Static)

    def _init_tree_view(self):
        self.model = CustomFileModel()  # QtWidgets.QFileSystemModel()
        # 设置过滤器
        ffilter = ["*.png", '*.jpg', '*.jpeg', '*.gif', '*.tiff',
                   '*.raw', '*.BMP', '*.exif', '*.FPX']
        self.model.setNameFilterDisables(False)  # 不符合名字过滤要求的隐藏而不是disable
        self.model.setNameFilters(ffilter)
        self.model.setFilter(QtCore.QDir.Dirs | QtCore.QDir.Files |
                             QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot)
        # self.model.sort(QtCore.Qt.AscendingOrder)
        # self.model.sort(QtCore.QDir.DirsFirst | QtCore.QDir.IgnoreCase | QtCore.QDir.Name)
        self.model.setRootPath(self.ROOT)
        # self.model.sort(0, QtCore.Qt.AscendingOrder)
        # self.tree.setSortingEnabled(False)  # 禁用自带排序

        # self.tree.setRootIndex(self.model.index(''))
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(self.ROOT))
        self.tree_view.setAnimated(True)
        self.tree_view.setIndentation(20)
        self.tree_view.setSortingEnabled(True)
        # self.tree.header().setSortIndicatorShown(QtCore.Qt.AscendingOrder)
        self.tree_view.header().setDefaultAlignment(QtCore.Qt.AlignCenter)  # 列头文字默认居中对齐
        self.tree_view.header().setSortIndicator(0, QtCore.Qt.AscendingOrder)  # 按第1列升序排序
        # self.tree.header().setDropIndicatorShown(True)
        # self.tree.setWindowTitle("Dir View")

        self.tree_view.setColumnHidden(3, True)  # 隐藏不需要的
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(1, True)

        font = QtGui.QFont("monospace", 12)
        font.setStyleHint(QtGui.QFont.TypeWriter)
        self.tree_view.setFont(font)

        # self.tree.resizeColumnToContents(0)
        self.tree_view.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tree_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tree_view.setAutoFillBackground(True)
        # self.tree.setStyleSheet("background-color: (255, 100, 5, 255)")
        # self.tree.setColor(QtGui.QColor(255, 100, 0, 255))
        # self.tree.horizontalHeader()

        # 设置列数
        # self.tree.setColumnCount(2)
        # 设置树形控件头部的标题
        # self.tree.setHeaderLabels(['Key', 'Value'])
        # 设置根节点
        # root = QtWidgets.QTreeWidgetItem(self.tree)
        # root.setText(0, 'Root')
        # root.setIcon(0, QtGui.QIcon('.res/images/1.gif'))
        self.tree_view.setAlternatingRowColors(True)  # 每间隔一行颜色不一样，当有qss时该属性无效
        # self.tree.setFocusPolicy(QtCore.Qt.NoFocus)     # 去掉鼠标移到单元格上时的虚线
        self.tree_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)  # 多行选择
        self.tree_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self._slot_context_menu)

        # create context menu
        self.popMenu = QtWidgets.QMenu(self)
        qss = "/*菜单项*/" \
              "QMenu{color:rgb(255,255,255);background-color:#0f2033;border:none;}" \
              "QMenu::item{font-size: 10pt;color:rgb(255,255,255);background-color:rgb(76,131,215);" \
              "width:60px;height:25px;padding-left:20px;border:2px solid rgb(70,125,200);}" \
              "QMenu::item:selected{color:rgb(255,255,255);background-color:#1a9b81;}" \
              "QMenu::separator{height:1px;background-color:rgba(255,255,255,1);" \
              "margin-left:5px;margin-right:5px;}" \
              "QMenu::indicator:unchecked{border:1px solid rgb(180,180,180);}"
        # qss = "QMenu {background-color:rgba(17,24,47,1);border:1px solid rgba(82,130,164,1);}" \
        #       "QMenu::item {min-width:50px;font-size: 12px;color: rgb(225,225,225);" \
        #       "background:rgba(75,120,154,0.5);border:1px solid rgba(82,130,164,1);" \
        #       "padding:1px 1px;margin:1px 1px;}" \
        #       "QMenu::item:selected {background:rgba(82,130,164,1);" \
        #       "border:1px solid rgba(82,130,164,1);}  /*选中或者说鼠标滑过状态*/" \
        #       "QMenu::item:pressed {background:rgba(82,130,164,0.4);border:1px solid rgba(82,130,164,1);/*摁下状态*/}"
        # qss = "QMenu {background-color:rgb(89,87,87); /*整个背景*/" \
        #       "border: 3px solid rgb(235,110,36);/*整个菜单边缘*/}" \
        #       "QMenu::item {font-size: 10pt;color: rgb(225,225,225);  /*字体颜色*/" \
        #       "border: 3px solid rgb(60,60,60);    /*item选框*/" \
        #       "background-color:rgb(89,87,87);" \
        #       "padding:16px 16px; /*设置菜单项文字上下和左右的内边距，效果就是菜单中的条目左右上下有了间隔*/" \
        #       "margin:2px 2px;/*设置菜单项的外边距*/}" \
        #       "QMenu::item:selected {background-color:rgb(235,110,36);/*选中的样式*/}" \
        #       "QMenu::item:pressed {/*菜单项按下效果*/border: 1px solid rgb(60,60,61);" \
        #       "background-color: rgb(220,80,6);}"
        self.popMenu.setStyleSheet(qss)
        # action = QtWidgets.QAction(QtGui.QIcon("./res/images/dst11.gif"), '搜索', self)
        # action.setShortcut('Ctrl+Q')
        # action.setToolTip('在当前目录下搜索')
        self.action_search.setStatusTip('搜索已选目录及其子目录中所有的已选类型文件')
        self.action_search.triggered.connect(lambda: self._slot_action_triggered(self.action_search))
        self.action_select_all.setStatusTip('把目录树中已经选择的目录作为搜索目录')
        self.action_select_all.triggered.connect(lambda: self._slot_action_triggered(self.action_select_all))

        self.popMenu.addAction(self.action_search)
        self.popMenu.addSeparator()  # 添加一个分隔线
        self.popMenu.addAction(self.action_select_all)

    def _init_dial(self):
        self.setMouseTracking(True)
        self.dial.setFixedSize(100, 100)  # 2
        self.dial.setRange(1, 9)  # 3
        self.dial.setValue(self.show_speed)
        self.dial.setNotchesVisible(True)  # 4
        self.dial.valueChanged.connect(self._solt_dial_changed)  # 5
        self.dial_label = QtWidgets.QLabel(str(self.show_speed), self.dial)
        self.dial_label.setFont(QtGui.QFont('Arial Black', 26))
        self.dial_label.setStyleSheet("color:blue")
        self.dial_label.setAlignment(QtCore.Qt.AlignCenter)
        self.dial_label.setFixedWidth(20)
        self.dial_label.move(round(self.dial.width() / 2.5) + 1, round(self.dial.height() / 3) - 8)

    def _update_photo(self):
        if not self.photo_file:
            return

        # size = QtCore.QSize(950, 700)
        size = QtCore.QSize(self.wg_photo.width(), self.wg_photo.height())
        # print(size, self.size())
        pm = QtGui.QPixmap.fromImage(QtGui.QImage(self.photo_file))
        s_pm = pm.scaled(size, QtCore.Qt.KeepAspectRatio | QtCore.Qt.SmoothTransformation)
        # 按比例缩放, 默认不按比例

        self.lb_photo.resize(s_pm.size())
        self.lb_photo.setPixmap(s_pm)

        self.__show_photo_exif()

    def _update_list_view(self):
        # print('_update_list_view', self.cur_path)
        if self.cur_path:
            print('=========================================')
            print('开始搜索目录')
            start = time.perf_counter()

            self._worker_path_searching()  # 每次循环将会用空闲出来的子进程去调用目标

            end = time.perf_counter()
            print(f'用时：{end - start}')
            print('-----------------------------------------')

            print('=========================================')
            print('list Widget开始添加项目')
            start = time.perf_counter()

            self.list_wg.clear()
            self.__add_list_items()
            # p = threading.Thread(target=self.__add_list_items)
            # p.start()

            end = time.perf_counter()
            print(f'用时：{end - start}')
            print('-----------------------------------------')

    # endregion

    # region 内部功能区
    def __add_list_items(self):
        # """
        # 把exif里保存的缩略图用于list中
        # :return:
        # """

        # 读取缩略图
        for each in self.cur_files:
            # exif_dict = piexif.load(each)
            # thumbnail = exif_dict.pop("thumbnail")
            # if thumbnail is not None:
            #     pix1 = QtGui.QPixmap()
            #     pix1.loadFromData(thumbnail, "JPG")
            #     icon = QtGui.QIcon(pix1.scaled(self.Icon_size_max, QtCore.Qt.KeepAspectRatio,
            #     QtCore.Qt.SmoothTransformation))
            #     item = QtWidgets.QListWidgetItem(icon, os.path.split(each)[-1])
            #     self.list_wg.addItem(item)
            #     item.setSizeHint(self.hint_size)  # 设置单元项为固定的宽度和高度
            # else:
            pm = QtGui.QPixmap(each)
            dirs, filename = os.path.split(each)
            item = QtWidgets.QListWidgetItem(QtGui.QIcon(pm.scaled(self.Icon_size_max)), filename)
            self.list_wg.addItem(item)
            item.setSizeHint(self.hint_size)  # 设置单元项为固定的宽度和高度

    def __show_photo_exif(self):
        if not self.photo_file:
            return

        try:
            # with open(self.photo_file.encode('utf-8'), 'rb') as f:
            #     tags = exifread.process_file(f)
            tags = self.get_exif_data(self.photo_file)

            # keys = [r'DateTimeOriginal', 'Make', r'Model', r'FocalLength', r'LensModel']
            # tags = self._get_some_exifs(self.photo_file, keys)
            # print('here', tags)
            # for tag, value in tags.items():
            #     if re.match('Image Make', tag):
            #         print('[*] 品牌信息: ' + str(value))
            #     if re.match('Image Model', tag):
            #         print('[*] 具体型号: ' + str(value))
            #     if re.match('EXIF LensModel', tag):
            #         print('[*] 摄像头信息: ' + str(value))
                # if re.match('GPS GPSLatitudeRef', tag):
                #     GPS['GPSLatitudeRef'] = str(value)
                # elif re.match('GPS GPSLongitudeRef', tag):
                #     GPS['GPSLongitudeRef'] = str(value)
                # elif re.match('GPS GPSAltitudeRef', tag):
                #     GPS['GPSAltitudeRef'] = str(value)
                # elif re.match('GPS GPSLatitude', tag):

            if not tags:
                self.lb_photo_time.setText(f"拍摄时间：")
                self.lb_camera.setText(f"相机厂商：")
                self.lb_model.setText(f"相机型号：")

                img = QtGui.QImage(self.photo_file)
                size = Utils.getFileInfo(self.photo_file)['文件大小']
                self.lb_weight.setText(f"文件大小：{size}")
                self.lb_photo_size.setText(f"相片尺寸：{img.width(), img.height()}")
                self.lb_resolution.setText(f"分辨率单位：{'像素'}")
                # print('width=', img.width())
                return

            # 打印照片其中一些信息
            creat_time = tags['DateTimeOriginal']
            # print('here', (creat_time))
            maker, model = tags['Make'], tags['Model']
            self.lb_photo_time.setText(f"拍摄时间：{creat_time}")
            self.lb_camera.setText(f"相机厂商：{maker}")
            self.lb_model.setText(f"相机型号：{model}  焦距：{tags['FocalLength']}")
            # print('time:', creat_time)

            w = tags['ExifImageWidth']
            h = tags['ExifImageHeight']
            r = tags['ResolutionUnit']
            # size = int(w) * h
            unit = ['', '像素/Pixels', '英寸/Inch']
            size = Utils.getFileInfo(self.photo_file)['文件大小']
            self.lb_weight.setText(f"文件大小：{size}")
            self.lb_photo_size.setText(f"相片尺寸：{w, h}")
            self.lb_resolution.setText(f"分辨率单位：{unit[r]}")

            # lat_ref = tags["GPS GPSLatitudeRef"].printable
            # lat = tags["GPS GPSLatitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
            # lat = float(lat[0]) + float(lat[1]) / 60 + float(lat[2]) / float(lat[3]) / 3600
            # if lat_ref != "N":
            #     lat = lat * (-1)
            # # 经度
            # lon_ref = tags["GPS GPSLongitudeRef"].printable
            # lon = tags["GPS GPSLongitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
            # lon = float(lon[0]) + float(lon[1]) / 60 + float(lon[2]) / float(lon[3]) / 3600
            # if lon_ref != "E":
            #     lon = lon * (-1)
        except KeyError:
            return "ERROR:请确保照片包含经纬度等EXIF信息。"
        # else:
        #     print("经纬度：", lat, lon)
        #     return lat, lon

    def __get_selected_dirs(self):
        """
        获取tree的当前选项集，再转换成相应的字符串路径集合
        :return: self.search_path 字符串路径集合
        """

        items = self.tree_view.selectedIndexes()
        if items:
            self.search_path.clear()
            for each in items:
                path = self.model.filePath(each)
                if self.model.fileInfo(each).isDir():
                    self.search_path.append(path)

    def get_location(self):
        # url = 'http://api.map.baidu.com/reverse_geocoding/v3/?ak={}&output=json' \
        #       '&coordtype=wgs84ll&location={},{}'.format(self.ak, *self.location)
        # response = requests.get(url).json()
        # status = response['status']
        # if status == 0:
        #     address = response['result']['formatted_address']
        #     print('详细地址：', address)
        # else:
        print('baidu_map error', self.cur_path)

    # def read_exif(self):
    #     imgpath, filename = os.path.split(self.photo_file)
    #     fd = open(self.photo_file, 'rb')
    #     tags = exifread.process_file(fd)
    #     fd.close()
    #     # 显示图片所有的exif信息
    #     # print("showing res of getExif: \n")
    #     print(type(tags))
    #     # print(tags["GPS GPSLatitudeRef"])
    #     print(tags['EXIF ExifVersion'])
    #
    #     res1 = []
    #     for each in tags:
    #         res1.append(f'{each}={tags[each]}\n')
    #     # print(len(res1), res1)
    #     #
    #     res2 = json.dumps(res1, cls=ComplexEncoder)  # 先把字典转成json
    #     with open(r'd:\stus.txt', 'w') as f:  # 打开文件
    #         f.write(res2)
    #     #     json.dumps(tags, cls=ComplexEncoder)
    #     # f = open(r'd:\stus.txt', 'w', encoding='utf-8')
    #     # json.dump(tags, f, 4, ensure_ascii=False)
    #
    #     # for each in tags:
    #     # print(type(each))
    #
    #     # print(tags['ImageWidth'])  # 获取图片宽度信息
    #     # print(tags['Image Orientation'])  # 照片拍摄方向
    #
    #     # print("\n\n\n\n");
    #     # FIELD = 'EXIF DateTimeOriginal'
    #     # if FIELD in tags:
    #     #     print("str(tags[FIELD]): %s" % (str(tags[FIELD])))  # 获取到的结果格式类似为：2018:12:07 03:10:34
    #     #     print("str(tags[FIELD]).replace(':', '').replace(' ', '_'): %s" % (
    #     #         str(tags[FIELD]).replace(':', '').replace(' ', '_')))  # 获取结果格式类似为：20181207_031034
    #     #     print("os.path.splitext(filename)[1]: %s" % (os.path.splitext(filename)[1]))  # 获取了图片的格式，结果类似为：.jpg
    #     #     new_name = str(tags[FIELD]).replace(':', '').replace(' ', '_') + os.path.splitext(filename)[1]
    #     #     print("new_name: %s" % (new_name))  # 20181207_031034.jpg
    #     #
    #     #     time = new_name.split(".")[0][:13]
    #     #     new_name2 = new_name.split(".")[0][:8] + '_' + filename
    #     #     print("filename: %s" % filename)
    #     #     print("%s的拍摄时间是: %s年%s月%s日%s时%s分" % (filename, time[0:4], time[4:6], time[6:8], time[9:11], time[11:13]))
    #     #
    #     #     # 可对图片进行重命名
    #     #     # new_full_file_name = os.path.join(imgpath, new_name2)
    #     #     # print(old_full_file_name," ---> ", new_full_file_name)
    #     #     # os.rename(old_full_file_name, new_full_file_name)
    #     # else:
    #     #     print('No {} found'.format(FIELD), ' in: ', self.photo_file)

    @staticmethod
    def _get_some_exifs(filename, key_list):
        try:
            if not isinstance(key_list, list):
                return
            # with open(filename.encode('utf-8'), 'rb') as f:
            #     tags = exifread.process_file(f)
            with pyexiv2.Image(filename, encoding='gbk') as img:
                tags = img.read_exif()
            # img = Image.open(filename)
            # tags = {TAGS[k]: v for k, v in img._getexif().items() if k in TAGS}
            # print(tags)
            if tags:
                my_dict = {}
                for each in key_list:
                    my_dict[r"f'{each}'"] = tags[each]
                    # pat = re.compile(f'{each}', re.I)  # 不区分大小写
                    # print(pat)
                    # for tag, value in tags.items():
                    #     # print(re.match(pat, tag))
                    #     if re.match(each, tag):
                    #         my_dict[each] = value
                return my_dict
            return None
        except Exception as e:
            return f"ERROR: {e}。"

    def get_exif(self, fn):
        img = Image.open(fn)
        exif = {TAGS[k]: v for k, v in img._getexif().items() if k in TAGS}
        return exif

    def get_exif_data(self, fname):
        """Get embedded EXIF data from image file."""
        ret = {}
        try:
            img = Image.open(fname)
            if hasattr(img, '_getexif'):
                exifinfo = img._getexif()
                if exifinfo is not None:
                    for tag, value in exifinfo.items():
                        decoded = TAGS.get(tag, tag)
                        ret[decoded] = value
        except IOError:
            print('IOERROR ' + fname)
        return ret

    def _worker_path_searching(self, is_current=True):
        try:
            self.cur_index = 0      # 不能自动播放了，否则会不同步
            self.auto_play = False
            self.cb_auto_show.setChecked(False)
            if is_current:
                # print(self.sub_dir)
                if self.cur_path:
                    if self.sub_dir:
                        self.cur_files = Utils.getFiles(self.cur_path, self.suffix)
                    else:
                        self.cur_files = Utils.files_in_dir(self.cur_path, self.suffix, True)
            else:
                # print(self.search_path)
                for each in self.search_path:
                    if self.sub_dir:
                        self.cur_files += Utils.getFiles(each, self.suffix)
                    else:
                        self.cur_files += Utils.files_in_dir(each, self.suffix, True)

            with open(self.save_file, 'w') as w_file:  # 打开文件，如果文件不存在，则创建
                Utils.cout_list(self.cur_files, True, fh=w_file)  # 输出到文件

        except IOError as err:  # 异常处理
            print("File error: " + str(err))
        # finally:
            # print(f'search end, 总数：{0}')

    def _worker_auto(self):
        while self.auto_play:
            self.photo_file = self.cur_files[self.cur_index]
            # print(f'cur file = {self.photo_file}')
            self._update_photo()
            self.cur_index = self.cur_index + 1 if self.cur_index < len(self.cur_files) - 1 else 0
            time.sleep(self.show_speed)

    # endregion

    # region 信号槽区
    def _slot_check_changed(self, index):
        self.auto_play = True if self.cb_auto_show.isChecked() else False
        self.sub_dir = True if self.cb_sub_dir.isChecked() else False
        # print(self.auto_play, self.sub_dir)
        if not self.cur_files:
            return

        if self.auto_play and self.cur_path:
            # p = Process(target=self._worker_auto)
            p = threading.Thread(target=self._worker_auto)
            p.start()

            # po = Pool(1)
            # Pool.apply_async(要调用的目标,(传递给目标的参数元祖,))
            # 每次循环将会用空闲出来的子进程去调用目标
            # po.apply(self._worker_auto)
            # po.close()  # 关闭进程池，关闭后po不再接收新的请求
            # po.join()  # 等待po中所有子进程执行完成，必须放在close语句之后

    def _solt_dial_changed(self):
        self.dial_label.setText(str(self.dial.value()))
        self.show_speed = self.dial.value()

    def _slot_action_triggered(self, action):
        name = action.objectName()
        print(name)

        if name == 'action_search' and self.search_path:  # 保存
            for i in range(len(self.search_path)):
                self.pool.apply_async(self._worker_path_searching, (False, i))  # 每次循环将会用空闲出来的子进程去调用目标

        elif name == 'action_select_all':  # 把当前下的所有路径归入搜索库
            self.__get_selected_dirs()
        #     self.photo_file = self.model.filePath(action)
        # filename, _ = QtWidgets.QFileDialog.getOpenFileName(
        #     self, '选择照片', r'', self.ext_filter, r'I:\照片',
        #     QtWidgets.QFileDialog.DontUseNativeDialog)
        # if not os.path.isfile(filename):
        #     return
        # self.photo_file = filename
        # self._update_photo()
        # self.read_exif()

    def _slot_btn_clicked(self, action):
        if not self.cur_files:
            return

        self.cur_index = self.cur_index + 1 if self.cur_index < len(self.cur_files) - 1 else 0
        # print(self.cur_index)
        self.photo_file = self.cur_files[self.cur_index]
        self._update_photo()
        #     self.photo_file = self.model.filePath(action)
        # filename, _ = QtWidgets.QFileDialog.getOpenFileName(
        #     self, '选择照片', r'', self.ext_filter, r'I:\照片',
        #     QtWidgets.QFileDialog.DontUseNativeDialog)
        # if not os.path.isfile(filename):
        #     return
        # self.photo_file = filename
        # self._update_photo()
        # self.read_exif()

    def _slot_list_clicked(self, item):
        # item = QtWidgets.QListWidgetItem()
        # print('no', )
        if item.text():
            self.photo_file = os.path.join(self.cur_path, item.text())
            self._update_photo()

    def _slot_tree_clicked(self, index):
        # item = self.model.fileInfo(index)
        # info = QtCore.QFileInfo()
        # print(info.filePath())
        if self.model.fileInfo(index).isFile():
            self.photo_file = self.model.filePath(index)
            self._update_photo()
        else:
            self.__get_selected_dirs()
            for each in self.search_path:
                self.cur_path = each    # self.search_path[0]
                self._update_list_view()
            # print(type(index), self.model.filePath(index))
            # self.list_view.setRootIndex(self.model.index(self.model.filePath(index)))
            # self.list_view.setRootIndex(index)

    def _slot_context_menu(self, point):
        index = self.tree_view.indexAt(point)
        # index = QtCore.QModelIndex()
        # print(index.row())  # 当前目录的第几项
        if index.row() < 0:
            return

        self.popMenu.exec_(self.tree_view.mapToGlobal(point))  # show context menu

    def resizeEvent(self, event):
        palette = QtGui.QPalette()
        pix = QtGui.QPixmap('res/images/background.jpg')
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(palette)

        self._update_photo()

    # def closeEvent(self, event):
    #     # self.po.close()     # 关闭进程池，关闭后po不再接收新的请求
    #     # self.po.join()      # 等待po中所有子进程执行完成，必须放在close语句之后
    #
    #     # # 创建一个消息盒子（提示框）
    #     # quitMsgBox = QtWidgets.QMessageBox()
    #     # # 设置提示框的标题
    #     # quitMsgBox.setWindowTitle('确认窗口')
    #     # # 设置提示框的内容
    #     # quitMsgBox.setText('你确定退出吗？')
    #     # # 创建两个点击的按钮，修改文本显示内容
    #     # buttonY = QtWidgets.QPushButton('确定')
    #     # buttonN = QtWidgets.QPushButton('取消')
    #     # # 将两个按钮加到这个消息盒子中去，并指定yes和no的功能
    #     # quitMsgBox.addButton(buttonY, QtWidgets.QMessageBox.YesRole)
    #     # quitMsgBox.addButton(buttonN, QtWidgets.QMessageBox.NoRole)
    #     # quitMsgBox.exec_()
    #     #
    #     # # 判断返回值，如果点击的是Yes按钮，我们就关闭组件和应用，否则就忽略关闭事件
    #     # if quitMsgBox.clickedButton() == buttonY:
    #         event.accept()
    #     # else:
    #     #     event.ignore()

    # endregion


def get_path(src_dir, suffix):
    dir_file = []
    tmp = []
    for root, dirs, files in os.walk(src_dir):
        for each in dirs:
            son = get_path(os.path.join(root, each), suffix)
            if son:
                tmp.append(each)
                tmp.append(son)

        for each in files:
            if each.endswith(suffix):
                tmp.append(each)

    # dir_file.append([src_dir, tmp])
    dir_file.append(tmp)
    return dir_file


def get_exif(fn):
    img = Image.open(fn)
    exif = {TAGS[k]: v for k, v in img._getexif().items() if k in TAGS}
    return exif


def _get_some_exifs(filename, key_list):
    try:
        if not isinstance(key_list, list):
            return
        tags = None
        with open(filename.encode('utf-8'), 'rb') as f:
            tags = exifread.process_file(f)
        # with pyexiv2.Image(filename, encoding='gbk') as img:
        #     tags = img.read_exif()
        # img = Image.open(filename)
        # tags = {TAGS[k]: v for k, v in img._getexif().items() if k in TAGS}
        print(tags)
        if tags:
            my_dict = {}
            if not key_list:
                return tags
            for each in key_list:
                pat = re.compile(f'{each}$', re.I)  # 不区分大小写
                for tag, value in tags.items():
                    if re.match(pat, tag):
                        my_dict[each] = value
            return my_dict
        return None
    except Exception as e:
        return f"ERROR: {e}。"


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    # file = r'I:\照片\picture原始\100KV610\100_6287.JPG'
    # dic = None
    # pyexiv2.set_log_level(4)
    # with pyexiv2.Image(file, encoding='gbk') as img:
    #     dic = img.read_exif()
    # dic = get_exif(file)
    # dic = _get_some_exifs(file, [])
    # print(len(dic))
    # # print(dic)
    # pat = re.compile(r'.+CompressedBitsPerPixel', re.I)  # 不区分大小写
    # for tag, value in dic.items():
    #     # print(tag)
    #     if re.match(pat, tag):
    #         print(tag, value)

    # dic = win.get_exif_data(r'I:\照片\picture原始\100KV610\100_6287.JPG')
    # pattern = re.compile(r'Make$', re.I)  # 不区分大小写
    # for tag, value in tags.items():
    #     if re.match(pattern, tag):
    #         print('[*] 品牌信息: ' + str(value))

    # Utils.cout_dict(dic, r'd:\exif.json')
    # print('end')
    sys.exit(app.exec_())

    # ret = getFiles(r'I:\新建文件夹\我的作品', ('doc', 'txt'))
    # # print(type(ret), len(ret), ret)
    # # ret = get_path(r'I:\新建文件夹\我的作品', ('doc', 'txt'))
    # print_list(ret, True)
    # print(len(ret))
    # try:
    #     with open('d:\\dirs_list.txt', 'w') as w_file:
    #         # 打开文件，如果文件不存在，则创建
    #         print_list(ret, True, fh=w_file)      # 输出到文件
    # except IOError as err:       # 异常处理
    #     print("File error: " + str(err))
    # file = 'dda.ga'
    # ret = file.endswith('.gA')
    # print(ret)
