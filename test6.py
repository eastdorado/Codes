#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Project : Puck
#  File    : test6
#  Date    : 2020/7/14 21:01
#  Site    : https://github.com/eastdorado
#  Author  : By cyh
#            QQ: 260125177
#            Email: 260125177@qq.com 
#  Copyright = Copyright (c) 2020 CYH
#  Version   = 1.0


# import sip
#
# sip.setapi('QString', 2)
# sip.setapi('QVariant', 2)
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from utilities import EllipseButton


class HoverButton(QToolButton):

    def __init__(self, parent=None):
        super(HoverButton, self).__init__(parent)
        # self.setMouseTracking(True)
        self.setStyleSheet('''border-image: url(./res/images/exit.gif)''')

    def resizeEvent(self, event):
        self.setMask(QRegion(self.rect(), QRegion.Ellipse))
        QToolButton.resizeEvent(self, event)

    def enterEvent(self, event):
        # print("Enter")
        self.setStyleSheet('''   
                                 border-image: url("./res/images/exit.gif") 10 10 2 2;
                                 border-top: 10px transparent;
                                 border-bottom: 10px transparent;
                                 border-right: 2px transparent;
                                 border-left: 2px transparent''')
        self.setGeometry(QRect(1100, 550, 160, 161))

    def leaveEvent(self, event):
        print('leave')
        self.setStyleSheet('''  
                                 border-image: url("./res/images/exit.gif") 10 10 2 2;
                                 border-top: 10px transparent;
                                 border-bottom: 10px transparent;
                                 border-right: 2px transparent;
                                 border-left: 2px transparent''')
        self.setGeometry(QRect(1100, 550, 140, 141))


class MyArea(QWidget):
    def __init__(self):
        super(MyArea, self).__init__()

        self.Shape = ["Rectangle", 'Rounded Rectangle', "Ellipse"]

        self.setAutoFillBackground(True)
        self.setMinimumSize(400, 400)

        self.pal = QPalette(Qt.darkBlue)
        self.setPalette(self.pal)  # 设置背景色

        self.pen = QPen()
        self.brush = QBrush()

        button = QPushButton('hello', self)  # 重写paintEvent不会影响该对象的子控件
        ll = QListWidget(self)

        for i in range(21):
            item = QListWidgetItem(
                QIcon(), str('选 项 %s' % i), ll)

    def paintEvent(self, QPaintEvent):
        width, height = self.width(), self.height()
        painter = QPainter(self)
        # p.setPen(self.pen)
        # p.setBrush(self.brush)
        # 设置反锯齿
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform |
                               QPainter.Qt4CompatiblePainting)
        painter.setPen(Qt.red)  # 设置画笔颜色
        # 画弦, 该弦在QRect(10.0, 30.0, 80.0, 60.0)的内切椭圆上，
        # 并且起始角度为30(3点钟为0度，逆时针为正)，跨度为120
        # painter.drawChord(10, 30, 80, 60, 30 * 16, 120 * 16)
        #
        # # 有多种画法，这里是指定圆心和x、y轴的半径;当x、y相等时就是画圆了
        # painter.drawEllipse(QPoint(width // 2, height // 2),
        #                     width // 2 - 10,
        #                     height // 2 - 10)

        # painter.drawRect(width / 2, height / 2, 100, 100)  # 以矩形左上角为顶点开画
        # # 在矩形内切椭圆上画，3点钟为0度，逆时针为正，角度要乘以16(参考文档)
        # painter.drawPie(width / 2 - 50, height / 2 - 50, 100, 100, 30 * 16, 120 * 16)
        # painter.save()  # 保存painter当前状态，后续紧跟一个restore()方法还原到这个状态
        # painter.setPen(Qt.white)
        # painter.drawRect(50, 50, 80, 100)  # 画一个白色的矩形
        # painter.restore()  # 还原到前一个保存状态
        # painter.drawRect(150, 150, 50, 50)  # 用前一个保存的painter状态，画一个矩形
        painter.translate(width / 2, height / 2)  # 将坐标第原点移动到中心.
        # 还有setTransform()方法用于指定某个轴旋转，这个旋转可以让图形从屏幕里面到外边旋转，配合闹钟可以做出动画。
        painter.drawRect(0, 0, 100, 100)
        # painter.resetMatrix()  # 还原到默认坐标系
        painter.translate(-width / 2, -height / 2)  # 还原到默认坐标系
        painter.drawEllipse(0, 0, 100, 100)

        # 掩码设置,就是底图透明，漏洞
        # intersected  两个区域相交的部分
        # subtracted  不包含r的区域，减法
        # xored 并集去掉交集，异或
        # self.pix = self.pix.scaled(int(windowWidth), int(windowHeight))
        # self.setMask(self.pix.mask())#用图片作为掩码
        maskRegion = QRegion(-7, -30, width + 14, height + 67)
        self.setMask(maskRegion.subtracted(QRegion(width / 2 - 70,
                                                   height / 2 - 30, 140, 60, QRegion.Ellipse)))

        # 裁剪,在裁剪区域内画图可见
        # setClipRegion()方法会自动设置setClipping()为true。
        # 当此次绘画结束后；如果后续绘画的区域没有在裁剪区域内，则不会显示；
        # 这时需要在裁剪绘画结束后调用setClipping()传入false，使裁剪失效，这样就可以正常显示了
        painter.setClipRegion(QRegion(width / 2 - 100, height / 2 - 100, 200, 200))  # 设置一个裁剪区域
        painter.setPen(Qt.white)
        painter.drawRect(painter.clipRegion().boundingRect())
        painter.setPen(Qt.yellow)
        painter.setBrush(QBrush(Qt.red))
        painter.drawEllipse(width / 2 - 80, height / 2 - 80, 200, 200)  # 超出裁剪区域的不画

        #画圆环这里我想到的有两种方法；一、是画一个红色的大圆，再到中间画一个黑色(或透明)的小圆。
        # 二、是构造一个圆环的QRegion使用QPainter的setClipRegion()方法使得只有在圆环区域内图形才能显示。
        # 这里我使用的是第二种方法。
        # QRegion
        # r1(width() / 2 - 50, height() / 2 - 50, 100, 100, QRegion::Ellipse);
        # QRegion
        # r2(width() / 2 - 100, height() / 2 - 100, 200, 200, QRegion::Ellipse);
        # painter.setClipRegion(r2 - r1);
        # painter.fillRect(r2.boundingRect(), QBrush(Qt::red))

        # # 用QPainterPath一次画多个图案
        # QPainterPath
        # path;
        # path.addText(10, 10, painter.font(), "Qt");
        # path.moveTo(10, 50);
        # path.lineTo(120, 50);
        # path.addRoundedRect(10, 80, 80, 80, 5, 5);
        # painter.drawPath(path)

        # 使用QPainterPath的arcMoveTo和arcTo画弧或扇形
        # arcMoveTo其实就是为了设置arcTo绘画的起点，两个函数都是以一个矩形的内切椭圆的形式传参。如果是扇形的话
        # QPainterPath
        # path;
        # path.arcMoveTo(width() / 2 - 100, height() / 2 - 100, 200, 200, 30); // 将path的起点移到一个椭圆(
        #     以3点钟为0度，逆时针为正)距离角度0点为30度的椭圆上，该椭圆是rect(100, 280, 120, 120)
        # 的内切椭圆
        # path.arcTo(width() / 2 - 100, height() / 2 - 100, 200, 200, 30, 120);
        # painter.drawPath(path);

        # # 我们只需要设置起画起点在椭圆中心就可以了，因为arcTo是先从QPainterPath起点到以传入参数应该起画的点之间连接再开画。
        # # 这里并不是一个完整的扇形，因为arcTo是画弧的；画完不会连接此次绘画的起点，这里需要我们手动连接，最简单的方法是调用
        # # QPainterPath的closeSubpath()
        # # 直接将Path绘画终点与起点闭合。
        # path.moveTo(width() / 2, height() / 2);
        # path.arcTo(width() / 2 - 100, height() / 2 - 100, 200, 200, 30, 120);
        # path.closeSubpath();
        # painter.drawPath(path)

        # 使用QPainterPath画贝塞尔曲线
        # QPainterPath
        # cubPath;
        # cubPath.cubicTo(170, 50, 90, 200, width(), height()); // 传入点1(170, 50)，点2(90, 200)，endPoint（width(), heigt()）
        # cubPath.addEllipse(170 - 3, 50 - 3, 6, 6); // 以点1为圆心画圆
        # cubPath.addText(180, 60, painter.font(), QStringLiteral("Point1")); // 标记点1
        # cubPath.addEllipse(90 - 3, 200 - 3, 6, 6); // 以点2为圆心画圆
        # cubPath.addText(100, 210, painter.font(), QStringLiteral("Point2")); // 标记点2
        # painter.setBrush(QBrush(Qt::lightGray));如果加个画刷颜色就可以变成这样
        # painter.drawPath(cubPath)

        return
        rect = QRect(50, 100, 300, 200)
        points = [QPoint(150, 100), QPoint(300, 150), QPoint(350, 250), QPoint(100, 300)]
        startAngle = 30 * 16
        spanAngle = 120 * 16

        path = QPainterPath()
        path.addRect(150, 150, 100, 100)
        path.moveTo(100, 100)
        path.cubicTo(300, 100, 200, 200, 300, 300)
        path.cubicTo(100, 300, 200, 200, 100, 100)

        if self.shape == "Line":
            p.drawLine(rect.topLeft(), rect.bottomRight())
        elif self.shape == "Rectangle":
            p.drawRect(rect)
        elif self.shape == 'Rounded Rectangle':
            p.drawRoundedRect(rect, 25, 25, Qt.RelativeSize)
        elif self.shape == "Ellipse":
            p.drawEllipse(rect)
        elif self.shape == "Polygon":
            p.drawPolygon(QPolygon(points), Qt.WindingFill)
        elif self.shape == "Polyline":
            p.drawPolyline(QPolygon(points))
        elif self.shape == "Points":
            p.drawPoints(QPolygon(points))
        elif self.shape == "Pie":
            p.drawPie(rect, startAngle, spanAngle)
        elif self.shape == "Arc":
            p.drawArc(rect, startAngle, spanAngle)
        elif self.shape == "Chord":
            p.drawChord(rect, startAngle, spanAngle)
        elif self.shape == "Path":
            p.drawPath(path)
        elif self.shape == "Text":
            p.drawText(rect, Qt.AlignCenter, "Hello Qt!")
        elif self.shape == "Pixmap":
            p.drawPixmap(150, 150, QPixmap("images/qt-logo.png"))


class PaintArea(QWidget):
    def __init__(self):
        super(PaintArea, self).__init__()
        self.Shape = ["Line", "Rectangle", 'Rounded Rectangle', "Ellipse", "Pie", 'Chord',
                      "Path", "Polygon", "Polyline", "Arc", "Points", "Text", "Pixmap"]
        self.setPalette(QPalette(Qt.white))
        self.setAutoFillBackground(True)
        self.setMinimumSize(400, 400)
        self.pen = QPen()
        self.brush = QBrush()

    def setShape(self, s):
        self.shape = s
        self.update()

    def setPen(self, p):
        self.pen = p
        self.update()

    def setBrush(self, b):
        self.brush = b
        self.update()

    def paintEvent(self, QPaintEvent):
        p = QPainter(self)
        p.setPen(self.pen)
        p.setBrush(self.brush)

        rect = QRect(50, 100, 300, 200)
        points = [QPoint(150, 100), QPoint(300, 150), QPoint(350, 250), QPoint(100, 300)]
        startAngle = 30 * 16
        spanAngle = 120 * 16

        path = QPainterPath();
        path.addRect(150, 150, 100, 100)
        path.moveTo(100, 100)
        path.cubicTo(300, 100, 200, 200, 300, 300)
        path.cubicTo(100, 300, 200, 200, 100, 100)

        if self.shape == "Line":
            p.drawLine(rect.topLeft(), rect.bottomRight())
        elif self.shape == "Rectangle":
            p.drawRect(rect)
        elif self.shape == 'Rounded Rectangle':
            p.drawRoundedRect(rect, 25, 25, Qt.RelativeSize)
        elif self.shape == "Ellipse":
            p.drawEllipse(rect)
        elif self.shape == "Polygon":
            p.drawPolygon(QPolygon(points), Qt.WindingFill)
        elif self.shape == "Polyline":
            p.drawPolyline(QPolygon(points))
        elif self.shape == "Points":
            p.drawPoints(QPolygon(points))
        elif self.shape == "Pie":
            p.drawPie(rect, startAngle, spanAngle)
        elif self.shape == "Arc":
            p.drawArc(rect, startAngle, spanAngle)
        elif self.shape == "Chord":
            p.drawChord(rect, startAngle, spanAngle)
        elif self.shape == "Path":
            p.drawPath(path)
        elif self.shape == "Text":
            p.drawText(rect, Qt.AlignCenter, "Hello Qt!")
        elif self.shape == "Pixmap":
            p.drawPixmap(150, 150, QPixmap("images/qt-logo.png"))


class testShadow(QFrame):
    shadow_Margins = QMargins(15, 15, 15, 15)

    def __init__(self, parent=None):
        super(testShadow, self).__init__(parent)

        self.resize(800, 600)
        layout = QHBoxLayout(self)

        self.setAcceptDrops(True)

        button = EllipseButton()
        layout.addWidget(button)

        # button.resize(100, 100)
        # button.setStyleSheet(
        #     '''color: rgb(137, 221, 255);
        #         background-color: rgb(37, 121, 255);
        #
        #         border-style:none;
        #         border:0px solid #3f3f3f;
        #         min-height:200px;max-height:200px;
        #         min-width:200px;max-width:200px;
        #         padding:0px;
        #         border-radius:100;
        #         ''')
        # self.button = HoverButton(self)
        # self.button.setGeometry(QRect(1100, 550, 140, 141))
        # self.button.setStyleSheet('''background: transparent;
        #                                 border-image: url("./res/images/exit.gif") 3 10 3 10;
        #                                 border-top: 3px transparent;
        #                                 border-bottom: 3px transparent;
        #                                 border-right: 10px transparent;
        #                                 border-left: 10px transparent;
        #                                 ''')
        button.setObjectName('button')
        button.set('./res/images/girl1.png')
        return
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 将Form设置为透明
        # self.setWindowFlag(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)  # 将Form设置为无边框

        # 设置具体阴影
        shadow = QGraphicsDropShadowEffect(self)  # 阴影
        shadow.setOffset(3, 3)  # 阴影宽度
        shadow.setColor(QColor(0, 0, 0, 255))  # 阴影颜色
        shadow.setBlurRadius(5)  # 阴影半径，虚化程度
        # vl.setContentsMargins(50, 50, 50, 50) # 重要，设置阴影的距离

        self.opacity = QGraphicsOpacityEffect(self)  # 透明
        self.opacity.setOpacity(0.5)  # 透明度

        # render = QGraphicsColorizeEffect(self)
        #
        # self.blur = QGraphicsBlurEffect(self)  # 虚化
        # self.blur.setBlurRadius(50)
        # pixItem = QGraphicsPixmapItem()
        # pixItem.setPixmap(QPixmap('./res/images/water.png').scaled(300, 200))
        # pixItem.setGraphicsEffect(self.blur)
        # pixItem.setFlag(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

        qss_back = '''
            background-image: url(./res/images/background11.jpg);
            border-radius:30px;     /*画出圆角*/
            background-repeat: no-repeat;       /*背景不要重复*/
            background-position: center center;      /*图片的位置，居中，靠左对齐*/
            
            min-width: 1000px;      /*屏幕宽度在1000px以内时，图片大小保持不变*/
            position:absolute;      /*固定在屏幕的最上方和最左方*/
            top: 0;             /*固定在屏幕的最上方和最左方*/
            left: 0;            /*固定在屏幕的最上方和最左方*/
            width:100%;     /*屏幕一样的大小，从而达到全屏效果*/
            height:100%;
        
            /* 下面都不识别*/
            /*z-index:-10;            最下层级, 背景图片
            zoom: 1;*/
            /*background-size: cover;
            -webkit-background-size: cover;
            -o-background-size: cover;          让图片随屏幕大小同步缩放*/
        '''

        wg = QWidget()
        # wg = QLabel()
        wg.setStyleSheet('background-image: url(./res/images/background1.jpg);'
                         'border-radius:30px;     /*画出圆角*/'
                         'background-repeat: no-repeat;       /*背景不要重复*/'
                         'width:100%;     /*屏幕一样的大小，从而达到全屏效果*/'
                         'height:100%;'
                         'background-position: center center;      /*图片的位置，居中，靠左对齐*/')

        # wg.setGraphicsEffect(self.shadow)
        # wg.setGraphicsEffect(self.opacity)

        lv = QVBoxLayout(self)
        lv.setContentsMargins(self.shadow_Margins)

        self.btn = QPushButton("Button")
        self.combo = QComboBox()

        lv.addWidget(wg)
        lv.addWidget(self.btn)
        lv.addWidget(self.combo)

        # the same QGraphicsEffect can not be shared by other widgets
        # 无法共享相同的QGraphicsEffect

        for children in self.findChildren(QWidget):
            shadow = QGraphicsDropShadowEffect(blurRadius=15, xOffset=5, yOffset=5, color=QColor(0, 0, 0, 255))
            children.setGraphicsEffect(shadow)

        # self.setStyleSheet("{background-image: url(./res/images/background0.jpg);"
        #                    "border-radius:30px;}")

        # vl.setContentsMargins(50, 50, 50, 50)
        #
        # label = QLabel(self)
        # label.resize(100, 100)
        # label.setText("Text Label")
        # label.setAlignment(Qt.AlignCenter)
        # # label.setFrameShape(QFrame.Box)
        # label.setStyleSheet('border-width: 0px;border-style: solid;'
        #                     'border-color: rgb(255, 170, 0);background-color: rgb(100,149,237);')
        #
        # button = QPushButton('dagl')
        #
        # vl.addWidget(label)
        # vl.addWidget(button)

        # button.setGraphicsEffect(self.opacity)
        # label.setGraphicsEffect(self.shadow)

    # def paintEvent(self, event):
    #     # # 主窗体无边框时是加载不了样式的，仅在子控件上实现样式。
    #     # # 要在主窗体本身实现样式，需要在paintEvent事件中加上如下代码，设置底图也是一样的
    #     # opt = QStyleOption()
    #     # opt.initFrom(self)
    #     # p = QPainter(self)
    #     # p.setRenderHint(QPainter.Antialiasing)  # 反锯齿
    #     # self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
    #     # super(LeftTabWidget, self).paintEvent(event)
    #
    #     # 不通过样式，直接设置圆角，通用，且不继承于子控件
    #     painter = QPainter(self)
    #
    #     painter.setRenderHint(QPainter.Antialiasing)  # 反锯齿
    #     painter.setBrush(QBrush(QPixmap('./res/images/background12.jpg')))
    #     # painter.setBrush(QBrush(Qt.white))
    #     painter.setPen(Qt.transparent)
    #
    #     rect = self.rect()
    #     rect.setWidth(rect.width() - 1)
    #     rect.setHeight(rect.height() - 1)
    #     painter.drawRoundedRect(rect, 15, 15)
    #     # 也可用QPainterPath 绘制代替 painter.drawRoundedRect(rect, 15, 15)
    #     # painterPath= QPainterPath()
    #     # painterPath.addRoundedRect(rect, 15, 15)
    #     # painter.drawPath(painterPath)
    #
    #     # 底图
    #     # pix = QPixmap('./res/images/background11.jpg')
    #     # painter.drawPixmap(self.rect(), pix)
    #
    #     # super(testShadow, self).paintEvent(event)


# 自定义Splash类
class MySplash(QWidget):
    def __init__(self):
        super(MySplash, self).__init__()
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 设置背景透明
        self.setWindowFlags(Qt.FramelessWindowHint)  # 设置无边框
        self.setGeometry(700, 190, 800, 800)
        self.text = "初始化程序...0%"

    def paintEvent(self, QPaintEvent):
        p = QPainter(self)
        p.setPen(QPen())
        p.setBrush(QBrush())
        p.drawPixmap(0, 0, QPixmap("./res/images/1.png"))  # 加载自己的图片
        p.drawText(QRect(26, 342, 200, 100), Qt.AlignCenter, self.text)  # showMesage

    def setText(self, text):
        self.text = text
        self.paintEvent(QPaintEvent)


# 启动界面显示时间的设置
def load_Message(splash):
    import time
    for i in range(1, 5):  # 显示时间4秒
        time.sleep(1)  # 睡眠
        splash.setText("初始化程序...{0}%".format(25 * i))
        splash.update()
        qApp.processEvents()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    # main = testShadow()
    main = MyArea()
    main.show()

    # splash = MySplash()
    # splash.show()  # 显示启动界面
    # qApp.processEvents()
    # load_Message(splash)  # 加载文字进度信息
    # splash.close()  # 隐藏启动界面

    sys.exit(app.exec_())

    # import cv2
    # cap = cv2.VideoCapture(r'C:\Users\big\Desktop\家庭哑铃计划/运动前动态拉伸动作.mp4')
    #
    # while cap.isOpened():
    #     ret, frame = cap.read()
    #     if not ret:
    #         print("Can't receive frame (stream end?). Exiting ...")
    #         break
    #
    #     # # show gray picture
    #     # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #     # cv2.imshow('frame', gray)
    #     cv2.imshow(None, frame)
    #     if cv2.waitKey(40) & 0xFF == ord('q'):
    #     # if cv2.waitKey(1) == ord('q'):
    #         break
    #
    # cap.release()
    # cv2.destroyAllWindows()
