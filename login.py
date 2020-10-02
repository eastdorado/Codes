#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Project : Puck
#  File    : login
#  Date    : 2020/9/28 20:03
#  Site    : https://github.com/eastdorado
#  Author  : By cyh
#            QQ: 260125177
#            Email: 260125177@qq.com 
#  Copyright = Copyright (c) 2020 CYH
#  Version   = 1.0

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import datetime
from dateutil.parser import parse
from cipher import Cypher
from SoftKeyBoard import *


class LogonPage(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(LogonPage, self).__init__()

        # region 注册页面
        bl_h_admin = QtWidgets.QHBoxLayout()
        lb = QtWidgets.QLabel('昵称:')
        le = QtWidgets.QLineEdit()
        bl_h_admin.addWidget(lb)
        bl_h_admin.addWidget(le)

        bl_h_mail = QtWidgets.QHBoxLayout()
        lb = QtWidgets.QLabel('邮箱:')
        le = QtWidgets.QLineEdit()
        bl_h_mail.addWidget(lb)
        bl_h_mail.addWidget(le)

        bl_h_phone = QtWidgets.QHBoxLayout()
        lb = QtWidgets.QLabel('手机:')
        le = QtWidgets.QLineEdit()
        bl_h_phone.addWidget(lb)
        bl_h_phone.addWidget(le)

        # cipher = QtWidgets.QAction()
        # cipher.setIcon(QtGui.QIcon(r'E:\Codes\res\images\569970.gif'))
        # cipher.triggered.connect(lambda: self.slot_pwd_builders(cipher))

        bl_h_pwd = QtWidgets.QHBoxLayout()
        lb = QtWidgets.QLabel('密码:')
        le = QtWidgets.QLineEdit()
        le.setPlaceholderText('登录密码需足够强壮')
        # le.addAction(cipher, QtWidgets.QLineEdit.TrailingPosition)  # LeadingPosition:左侧
        cipher = QtWidgets.QPushButton('密码')
        cipher.setStyleSheet('border:none;')
        cipher.clicked.connect(lambda: self.slot_pwd_builders(le))
        bl_tmp = QtWidgets.QHBoxLayout()
        bl_tmp.setContentsMargins(0, 0, 0, 0)
        bl_tmp.addWidget(cipher, 0, QtCore.Qt.AlignRight)
        le.setLayout(bl_tmp)
        bl_h_pwd.addWidget(lb)
        bl_h_pwd.addWidget(le)

        bl_h_repeat = QtWidgets.QHBoxLayout()
        lb = QtWidgets.QLabel('密码:')
        le = QtWidgets.QLineEdit()
        le.setPlaceholderText('重复以确认你的密码')
        # le.addAction(cipher, QtWidgets.QLineEdit.TrailingPosition)  # LeadingPosition:左侧
        cipher = QtWidgets.QPushButton('密码')
        cipher.setStyleSheet('border:none;')
        cipher.clicked.connect(lambda: self.slot_pwd_builders(le))
        bl_tmp = QtWidgets.QHBoxLayout()
        bl_tmp.setContentsMargins(0, 0, 0, 0)
        bl_tmp.addWidget(cipher, 0, QtCore.Qt.AlignRight)
        le.setLayout(bl_tmp)
        bl_h_repeat.addWidget(lb)
        bl_h_repeat.addWidget(le)

        bl_h_verify = QtWidgets.QHBoxLayout()
        lb = QtWidgets.QLabel('验证码:')
        le = QtWidgets.QLineEdit()
        lb1 = QtWidgets.QLabel('验证码')
        lb1.setAlignment(QtCore.Qt.AlignCenter)
        lb1.setMinimumWidth(100)
        bl_h_verify.addWidget(lb)
        bl_h_verify.addWidget(le)
        bl_h_verify.addWidget(lb1)

        bl_h_order = QtWidgets.QHBoxLayout()
        pb_logon = QtWidgets.QPushButton('注册')
        pb_logon.setStyleSheet('/*border-top-left-radius:5px; border-bottom-right-radius:5px;*/'
                               'font-size:20px;font-weight:bold;font-family:Microsoft YaHei;')
        pb_cancel = QtWidgets.QPushButton('取消')
        pb_cancel.setStyleSheet('/*border-top-left-radius:5px; border-bottom-right-radius:5px;*/'
                                'font-size:20px;font-weight:bold;font-family:Microsoft YaHei;')
        pb_cancel.clicked.connect(self.close)
        bl_h_order.addWidget(pb_logon)
        bl_h_order.addSpacing(10)
        bl_h_order.addWidget(pb_cancel)
        # endregion

        # region 主界面
        self.resize(350, 300)
        self.setStyleSheet('color:green; /*background:rgba(150,150,150, 255);*/'
                           'font-size:18px;font-weight:bold;font-family:NSimSun;')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)
        self.setWindowOpacity(1.00)  # 设置窗口透明度

        self.parent = args[0]

        bl_v = QtWidgets.QVBoxLayout(self)
        bl_v.setContentsMargins(30, 30, 30, 30)

        bl_v.addLayout(bl_h_admin)
        bl_v.addLayout(bl_h_mail)
        bl_v.addLayout(bl_h_phone)
        bl_v.addLayout(bl_h_pwd)
        bl_v.addLayout(bl_h_repeat)
        bl_v.addLayout(bl_h_verify)
        bl_v.addSpacing(10)
        bl_v.addLayout(bl_h_order)
        # endregion

    @staticmethod
    def slot_pwd_builders(le):
        # le = QtWidgets.QLineEdit("dsaf")
        # print('自动生成密码', le.text())
        Cypher().show()


class LoginPage(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(LoginPage, self).__init__(*args, **kwargs)
        self.soft_keyboard = SoftKeyBoard()
        self.soft_keyboard.signal_send_text.connect(self.slot_receive_key)
        # self.soft_keyboard.hide()

        # region 登录页面
        logo = QtGui.QIcon(r'E:\Codes\res\images\569942.gif')
        user = QtWidgets.QComboBox(self, minimumWidth=200)
        user.addItem(logo, 'C')
        user.addItems(['Java', 'C#', 'PHP'])
        user.setItemIcon(1, logo)
        # user.setEditable(True)
        mold = QtWidgets.QComboBox(self, minimumWidth=50)
        mold.addItems(['昵称', '邮箱', '手机'])

        bl_h_a = QtWidgets.QHBoxLayout()
        bl_h_a.addWidget(user)
        bl_h_a.addWidget(mold)

        self.pwd = QtWidgets.QLineEdit(self, minimumWidth=200)
        # pwd.textChanged.connect(lambda: self.slot_validate_input(pwd))
        reg_ex = QtCore.QRegExp("[0-9]+.?[0-9]{,2}")
        input_validator = QtGui.QRegExpValidator(reg_ex, self.pwd)
        # self.pwd.setValidator(input_validator)

        self.pwd.setPlaceholderText('请输入密码')
        self.pwd.setFixedHeight(25)
        self.pwd.setStyleSheet('border: 2px solid #EEE;border-radius: 4px;padding-right: 14px;'
                               '/*min-height: 25px; max-height: 25px;*/'
                               'font-size:20px;font-weight:bold;font-family:KaiTi;')
        # pwd.setStyleSheet("QLineEdit {border: 2px solid #EEE;border-radius: 4px;padding-right: 14px;}"
        #                   "QLineEdit:focus {border-color: #bbbec4;}"
        #                   "QLineEdit QPushButton {width:  16px;height: 16px;qproperty-flat: true;margin-right: "
        #                   "4px;border: none;border-width: 0;"
        #                   "border-image: url(E:/Codes/res\images/569970.gif) 0 0 0 0 stretch stretch;} ")

        self.selectApply = QtWidgets.QAction(self.pwd)
        self.selectApply.setIcon(QtGui.QIcon(r'E:\Codes\res\images\569970.gif'))
        self.selectApply.triggered.connect(self.slot_soft_keyboard)
        self.pwd.addAction(self.selectApply, QtWidgets.QLineEdit.TrailingPosition)  # LeadingPosition:左侧

        bl_h_s = QtWidgets.QHBoxLayout()
        bl_h_s.addStretch()
        bl_h_s.addWidget(QtWidgets.QCheckBox('自动登录'))
        bl_h_s.addWidget(QtWidgets.QCheckBox('记住密码'))

        pb_login = QtWidgets.QPushButton('登录')
        pb_logon = QtWidgets.QPushButton('注册')
        pb_logon.clicked.connect(self.slot_call_logon)
        pb_logon.setStyleSheet('color: green')
        pb_cancel = QtWidgets.QPushButton('退出')
        pb_cancel.clicked.connect(self.close)

        bl_h_o = QtWidgets.QHBoxLayout()
        bl_h_o.addWidget(pb_login)
        # bl_h_o.addSpacing(20)
        bl_h_o.addWidget(pb_logon)
        bl_h_o.addWidget(pb_cancel)
        # endregion

        # region 主界面
        self.resize(350, 300)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)
        # self.setWindowOpacity(0.75)  # 设置窗口透明度
        self.setObjectName('lg')
        self.setStyleSheet('#lg{background:rgba(0,100,250, 100);'
                           'background-repeat: no-repeat; background-position: center center;}'
                           'QComboBox{font-size:20px;font-weight:bold;font-family:Roman times;'
                           'height: 36px; color: white; background: rgba(25,25,25, 150);'
                           '/*min-height: 30px; max-height: 30px;*/}'
                           'QCheckBox{color: skyblue; font-size:16px;font-weight:bold;font-family:NSimSun;}'
                           'QPushButton{color: red; font-size:20px;font-weight:bold;font-family:Microsoft YaHei;'
                           '/*border: 2px solid #EEE;border-radius: 4px;padding-right: 14px;*/}')

        bl_v = QtWidgets.QVBoxLayout(self)
        bl_v.setContentsMargins(30, 30, 30, 30)
        bl_v.addLayout(bl_h_a)
        bl_v.addWidget(self.pwd)
        bl_v.addLayout(bl_h_s)
        bl_v.addSpacing(10)
        bl_v.addLayout(bl_h_o)
        # endregion

    def slot_soft_keyboard(self):
        """调用软键盘"""
        self.soft_keyboard.show()
        x = self.x() + self.pwd.x() + self.pwd.width() - self.soft_keyboard.width()
        y = self.y() + self.pwd.y() + self.pwd.height() + 1
        self.soft_keyboard.move(x, y)

    def slot_call_logon(self):
        LogonPage(self).show()

    # def slot_validate_input(self, le):
    #     reg_ex = QtCore.QRegExp("[0-9]+.?[0-9]{,2}")
    #     input_validator = QtGui.QRegExpValidator(reg_ex, le)
    #     le.setValidator(input_validator)

    def processing_func_key(self, text):
        """ 处理功能键 """
        if text == 'up':
            self.login_window.focusPreviousChild()

        elif text == 'down':
            self.login_window.focusNextChild()

        elif text == 'left':
            self.login_window.now_editline.cursorBackward(False, 1)

        elif text == 'right':
            self.login_window.now_editline.cursorForward(False, 1)

        elif text == 'backspace':
            self.login_window.now_editline.backspace()

        elif text == 'enter':
            if self.login_window.btn_keyboard.hasFocus():  # 隐藏键盘
                # ~ self.slot_switch_keyboard()
                pass

            elif self.login_window.btn_login.hasFocus():  # 登录
                self.login_window.slot_btn_login_clicked()

            elif self.login_window.btn_regist.hasFocus():  # 注册
                self.login_window.slot_btn_regist_clicked()

            elif self.login_window.le_user.hasFocus():  # 在用户框时进入密码框
                self.login_window.focusNextChild()

            elif self.login_window.le_passwd.hasFocus():  # 在密码框时登录
                self.login_window.focusNextChild()
                self.login_window.slot_btn_login_clicked()

        elif text == 'esc':
            self.soft_keyboard.close()

        elif text == 'clear':
            self.pwd.clear()

    def slot_receive_key(self, text):
        """ 接收键盘发来的信息, 并发送到相应输入框 """
        if len(text) == 1:  # 非功能键
            self.pwd.insert(text)
        else:
            self.processing_func_key(text)


class LoginWin(QtWidgets.QFrame):
    def __init__(self, *args, **kwargs):
        super(LoginWin, self).__init__(*args, **kwargs)
        self.resize(600, 500)

        icon = QtWidgets.QToolButton()
        icon.setIcon(QtGui.QIcon(r'E:\Codes\res\images\1126157.gif'))
        icon.setIconSize(QtCore.QSize(50, 50))
        bl_h_i = QtWidgets.QHBoxLayout()
        bl_h_i.addWidget(icon)

        title = QtWidgets.QLabel('个人密码保存系统：米库')
        right = QtWidgets.QLabel('V1.0.1')
        bl_h_t = QtWidgets.QHBoxLayout()
        bl_h_t.addWidget(title)
        bl_h_t.addWidget(right)

        wg = QtWidgets.QWidget()
        wg.setFixedSize(self.width(), 200)
        wg.setStyleSheet('background-image:url(./res/background/bk5.jpg);'
                         'background-repeat: no-repeat;'
                         'background-position: center center;')
        wg.setWindowOpacity(0.85)  # 设置窗口透明度
        bl_h_c = QtWidgets.QHBoxLayout()
        bl_h_c.addWidget(wg)

        setting = QtWidgets.QPushButton('系统设置')
        setting.setIcon(QtGui.QIcon(r'E:\Codes\res\images\setting.gif'))
        setting.setIconSize(QtCore.QSize(30, 30))

        status = QtWidgets.QLabel('日期：')
        tt = QtWidgets.QToolButton()
        tt.setIcon(QtGui.QIcon(r'E:\Codes\res\images\1190300.gif'))
        bl_h_s = QtWidgets.QHBoxLayout()
        bl_h_s.addWidget(tt)
        bl_h_s.addWidget(status)

        bl_v_main = QtWidgets.QVBoxLayout(self)
        bl_v_main.setAlignment(QtCore.Qt.AlignHCenter)
        bl_v_main.addLayout(bl_h_i)
        bl_v_main.addLayout(bl_h_t)
        bl_v_main.addLayout(bl_h_c)
        bl_v_main.addWidget(setting)
        bl_v_main.addLayout(bl_h_s)
        # bl_v_main.addStretch(1)  # 设置伸缩量为1

    # def paintEvent(self, event):
    # opt = QStyleOption()
    # opt.initFrom(self)
    # p = QPainter(self)
    # p.setRenderHint(QPainter.Antialiasing)  # �����
    # self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
    # # super(Canvas, self).paintEvent(event)

    # painter = QtGui.QPainter(self)
    # painter.setRenderHint(QPainter.Antialiasing)  # �����

    # src = cv2.imread(r'E:\Codes\res\background\bk7.jpg')  # opencv读取图片
    # img = cv2.GaussianBlur(src, (0, 0), self.val)
    # # 若ksize不为(0, 0)，则按照ksize计算，后面的sigmaX没有意义。若ksize为(0,
    # # 0)，则根据后面的sigmaX计算ksize
    # img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
    # _image = QtGui.QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3,
    #                       QtGui.QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
    # jpg_out = QtGui.QPixmap(_image).scaled(self.imgLabel.width(), self.imgLabel.height())  # 设置图片大小
    # # painter.setBrush(QtGui.QBrush(jpg_out))

    # img = QtGui.QImage(r'E:\Codes\res\background\bk7.jpg')
    # w, h = self.width(), self.height()
    # ratio_w = img.width() / w
    # ratio_h = img.height() / h

    # is_w = True if ratio_w < ratio_h else False
    # img_new = img.scaledToWidth(h) if is_w else img.scaledToHeight(w)

    # painter.setBrush(QtGui.QBrush(QtGui.QPixmap.fromImage(img_new)))  # ���õ�ͼ�ķ�ʽ֮һ

    # painter.setBrush(QBrush(Qt.blue))
    # painter.setPen(QtCore.Qt.transparent)

    # rect = self.rect()
    # rect.setWidth(rect.width() - 1)
    # rect.setHeight(rect.height() - 1)
    # painter.drawRoundedRect(rect, 20, 20)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # win = LogonPage(None)
    win = LoginPage()
    win.show()
    sys.exit(app.exec_())
