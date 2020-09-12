import os
import random
import sys
import time
import string
import copy
import re
from PyQt5 import QtWidgets, QtCore, QtGui
from functools import partial
from ui_cipher import Ui_Form
from utilities import Utils
import unittest
import pyperclip

# 特征
NUMBER = re.compile(r'[0-9]')
LOWER_CASE = re.compile(r'[a-z]')
UPPER_CASE = re.compile(r'[A-Z]')
OTHERS = re.compile(r'[^0-9A-Za-z]')


def load_common_password():
    words = []
    with open("./res/10k_most_common.txt", "r") as f:
        for word in f:
            words.append(word.strip())
    return words


COMMON_WORDS = load_common_password()  # 常用密码


# 管理密码强度的类
class Strength(object):
    """
    密码强度三个属性：是否有效valid, 强度strength, 提示信息message
    """

    def __init__(self, valid, strength, message):
        self.valid = valid
        self.strength = strength
        self.message = message

    def __repr__(self):
        return self.strength

    def __str__(self):
        return self.message

    def __bool__(self):
        return self.valid


class Password(object):
    TERRIBLE = 0
    SIMPLE = 1
    MEDIUM = 2
    STRONG = 3

    @staticmethod
    def is_regular(input):
        regular = ''.join(['qwertyuiop', 'asdfghjkl', 'zxcvbnm'])
        return input in regular or input[::-1] in regular

    @staticmethod
    def is_by_step(input):
        delta = ord(input[1]) - ord(input[0])
        for i in range(2, len(input)):
            if ord(input[i]) - ord(input[i - 1]) != delta:
                return False
        return True

    @staticmethod
    def is_common(input):
        return input in COMMON_WORDS

    def __call__(self, input, min_length=6, min_type=3, level=STRONG):
        if len(input) < min_length:
            return Strength(False, "terrible", "密码太短了")
        if self.is_regular(input) or self.is_by_step(input):
            return Strength(False, "simple", "密码有规则")
        if self.is_common(input):
            return Strength(False, "simple", "密码很常见")
        types = 0
        if NUMBER.search(input):
            types += 1
        if LOWER_CASE.search(input):
            types += 1
        if UPPER_CASE.search(input):
            types += 1
        if OTHERS.search(input):
            types += 1
        if types < 2:
            return Strength(level <= self.SIMPLE, "simple", "密码太简单了")
        if types < min_type:
            return Strength(level <= self.MEDIUM, "medium", "密码还不够强")
        return Strength(True, "strong", "密码很强")


class Email(object):
    def __init__(self, email):
        self.email = email

    def is_valid_email(self):
        if re.match("^.+@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", self.email):
            return True
        return False

    def get_email_type(self):
        types = ['qq', '163', 'gmail', '126', 'sina']
        email_type = re.search('@\w+', self.email).group()[1:]
        if email_type in types:
            return email_type
        return 'wrong email'


password = Password()


class PasswordTool:
    """
        密码工具类
    """

    # 实例化函数
    def __init__(self, password=None):
        self.password = password
        self.strength_level = 0

    def __str__(self):  # 终端用户显示使用,有则代替repr的终端显示
        return f"密码等级: {self.strength_level}"

    __repr__ = __str__  # 所有环境下都统一显示

    # 类的方法

    def checkio(self, data):
        return True if re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$", data) and len(data) >= 10 else False

    def check_password(self, pwd):
        self.password = pwd
        self.strength_level = 0

        # 规则1：密码长度大于8
        if len(self.password) > 8:
            self.strength_level += 1
        # else:
        #     print('密码长度必须大于8位。')
        # 规则2：包含数字
        if self.check_number_exist():
            self.strength_level += 1
        # else:
        #     print('密码必须包含数字')
        # 规则3：包含字母
        if self.check_letter_exist():
            self.strength_level += 1
        # else:
        #     print('密码必须包含字母')
        # 规则4：包含大小写字母
        if self.check_upper_and_lower_exit():
            self.strength_level += 1
        # else:
        #     print('密码必须同时包含大小写字母')
        # 规则5：包含特殊字母
        if self.check_specal_symbol_exit():
            self.strength_level += 1
        # else:
        #     print('密码必须同时包含特殊字符')

        return self.strength_level

    def check_number_exist(self):
        """
        判断字符串中是否有数字
        :param password_str:
        :return:
        """
        has_number = False
        for c in self.password:
            if c.isnumeric():
                has_number = True
                break
        return has_number

    def check_letter_exist(self):
        """
        判断字符串中是否有字母
        :param password_str:
        :return:
        """
        has_letter = False
        for d in self.password:
            if d.isalpha():
                has_letter = True
                break
        return has_letter

    def check_upper_and_lower_exit(self):
        """
        判断是否同时有大小写字母
        :return:
        """
        has_upper_and_lower = False
        has_upper = False
        has_lower = False
        for m in self.password:
            if m.isupper():
                has_upper = True
                continue
            elif m.islower():
                has_lower = True
                if has_upper:
                    break
                else:
                    continue
            else:
                continue
        if has_upper and has_lower:
            has_upper_and_lower = True
        return has_upper_and_lower

    def check_specal_symbol_exit(self):
        has_special_symbol_exit = False
        # special_char_list = ['*', '#', '+', '!', '@', '$', '^', '%']
        special_char_list = Utils.get_chars(6)
        # print(len(special_char_list), special_char_list)
        for i in range(len(special_char_list)):
            # if self.password.find(special_char_list[i]):
            if special_char_list[i] in self.password:
                has_special_symbol_exit = True
                break

        return has_special_symbol_exit


class Cypher(QtWidgets.QWidget):
    def __init__(self, parent=None, pwd_size=8):
        super(Cypher, self).__init__(parent)
        self.numerals_arabic = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                                10, 100, 1000, 10000, 100000000]
        self.numerals_roman = ['I(1)，V(5)，X(10)，L(50)，C(100)，D(500)，M(1000)']
        self.numerals_chinese_capital = ['零', '壹', '贰', '叁', '肆',
                                         '伍', '陆', '柒', '捌', '玖',
                                         '拾', '佰', '仟', '万', '亿']  # 大写
        self.numerals_chinese_lowercase = ['零', '一', '二', '三', '四',
                                           '五', '六', '七', '八', '九',
                                           '十', '百', '千', '万', '亿']  # 小写
        self.msg = [['强度：1/5', '检测提示：密码过于简单。', '（只要花点时间，就能破解你的密码了。）'],
                    ['强度：2/5', '检测提示：密码强度差。', '（建议在设置复杂点。）'],
                    ['强度：3/5', '检测提示：密码强度良好。', '（呵呵，标准安全密码了。）'],
                    ['强度：4/5', '检测提示：密码强度高。', '（嘎嘎，你的密码很安全了。）'],
                    ['强度：5/5', '检测提示：密码强度极高。', '（啊~~，暴力破解你的密码至少要1万年以上！）']]

        # 将大/小写的ASCII字符列表和数字组合起来
        self.char_set = set(string.ascii_letters + string.digits)
        self.char_mask = set()  # 要排除的字符集合
        self.ciphers = []
        self.cipher_length = 9  # 每个密码的长度
        self.ciphers_count = 3  # 批量产生密码的数量
        self.cipher_type = '随机密码'  # 密码类型
        self.code_type = 0x14  # PIN码的类型 '4位'：4  6位：6  '数字'：1  字符：2

        self.checker = PasswordTool()  # 密码强度的检测

        self.shell = self.set_ui()  # ui外壳
        self.shell.groupBox_5.setVisible(False)
        self.shell.groupBox_6.setVisible(False)
        self.shell.groupBox_7.setVisible(False)

    def set_ui(self):
        # self.resize(800, 600)
        # self.setWindowTitle("密码生成器")

        shell = Ui_Form()
        shell.setupUi(self)

        for i in range(1, shell.comboBox.maxCount() + 1):
            shell.comboBox.addItem(str(i))
        for i in range(1, shell.comboBox_2.maxCount() + 1):
            shell.comboBox_2.addItem(str(i))
        shell.comboBox.setCurrentIndex(self.cipher_length - 1)
        shell.comboBox_2.setCurrentIndex(self.ciphers_count - 1)

        # 把自动产生的槽移到此处
        shell.pushButton.clicked.connect(partial(self.slot_btn_clicked, '生成密码'))
        shell.pushButton_2.pressed.connect(partial(self.slot_btn_clicked, '复制密码'))
        shell.comboBox.currentIndexChanged['int'].connect(partial(self.slot_combo_selected, 'length'))
        shell.comboBox_2.currentIndexChanged['int'].connect(partial(self.slot_combo_selected, 'count'))
        shell.radioButton.pressed.connect(partial(self.slot_radio_clicked, '随机密码'))
        shell.radioButton_2.pressed.connect(partial(self.slot_radio_clicked, '易记密码'))
        shell.radioButton_3.pressed.connect(partial(self.slot_radio_clicked, 'PIN'))
        shell.radioButton_4.pressed.connect(partial(self.slot_radio_clicked, '4位'))  # '4位PIN'))
        shell.radioButton_5.pressed.connect(partial(self.slot_radio_clicked, '6位'))  # '6位PIN'))
        shell.radioButton_6.pressed.connect(partial(self.slot_radio_clicked, '数字'))  # '4位PIN'))
        shell.radioButton_7.pressed.connect(partial(self.slot_radio_clicked, '字符'))  # '6位PIN'))
        # shell.radioButton_4.released.connect(partial(self.slot_radio_released, '4位'))  # '4位PIN'))
        # shell.radioButton_5.released.connect(partial(self.slot_radio_released, '6位'))  # '6位PIN'))
        # shell.radioButton_6.released.connect(partial(self.slot_radio_released, '数字'))  # '4位PIN'))
        # shell.radioButton_7.released.connect(partial(self.slot_radio_released, '字符'))  # '6位PIN'))

        shell.checkBox_1.clicked.connect(self.slot_box_checked)  # '大写字母'
        shell.checkBox_2.clicked.connect(self.slot_box_checked)  # '小写字母'
        shell.checkBox_3.clicked.connect(self.slot_box_checked)  # '阿拉伯数字'
        shell.checkBox_8.clicked.connect(self.slot_box_checked)  # '可见字符'))
        shell.checkBox_4.clicked.connect(self.slot_box_checked)  # '小写汉字数字'))
        shell.checkBox_5.clicked.connect(self.slot_box_checked)  # '大写汉字数字'))
        shell.checkBox_7.clicked.connect(self.slot_box_checked)  # '排除字符'))
        shell.checkBox_6.clicked.connect(self.slot_box_checked)  # '特殊字符'))
        shell.checkBox_9.clicked.connect(self.slot_box_checked)  # '首字母大写'))
        shell.checkBox_10.clicked.connect(self.slot_box_checked)  # '完整词语'))
        # shell.checkBox_10.clicked['bool'].connect(partial(self.slot_box_checked, '完整词语'))
        # shell.lineEdit_2.textChanged['QString'].connect(partial(self.slot_text_changed, '排除字符'))
        # shell.lineEdit.textChanged['QString'].connect(partial(self.slot_text_changed, '特殊字符'))
        shell.textEdit.textChanged.connect(self.slot_edit_text_changed)
        # shell.textEdit.selectionChanged.connect(self.slot_selection_changed)
        # shell.textEdit.copyAvailable.connect(self.slot_text_copy)

        return shell

    def slot_btn_clicked(self, flag):
        if flag == '生成密码':
            if self.cipher_type == 'PIN':  # PIN码
                print(self.code_type)
                bits = self.code_type & 0x0F
                mold = (self.code_type & 0xF0) >> 4

                self.ciphers.clear()
                for i in range(self.ciphers_count):
                    code = [self.numerals_arabic[Utils.rand_int(0, 9)] for _ in range(bits)]
                    pin = Utils.get_pin(code, mold)
                    print('sgsd', bits, mold, code, pin)

                    self.ciphers.append(pin)

                self.shell.textEdit.clear()
                for each in self.ciphers:
                    self.shell.textEdit.append(str(each))
                self.shell.label_tip.setText("PIN 码是字符串，拷贝时根据类型自动转为数字或字符。")

            else:  # 随机码、易记密码
                if not self.char_set:
                    return
                # print('生成密码')

                num = len(self.char_set) - 1
                char_list = list(self.char_set)
                # print(char_list)
                self.ciphers.clear()
                for i in range(self.ciphers_count):
                    pwd = [char_list[Utils.rand_int(0, num)] for _ in range(self.cipher_length)]
                    s = "".join(pwd)  # list 转成字符串
                    level = self.checker.check_password(s) - 1
                    # print('level', level)
                    self.ciphers.append(s)
                    tip = '  '.join(self.msg[level])
                    self.shell.label_tip.setText(f"密码：{tip}")

                # print(self.ciphers)
                # pe = QtWidgets.QTextEdit()
                pe = self.shell.textEdit
                pe.clear()
                for each in self.ciphers:
                    pe.append(each)

        elif flag == '复制密码':
            # pe = QtWidgets.QTextEdit()
            pe = self.shell.textEdit

            text_cursor = pe.textCursor()
            text_cursor.select(QtGui.QTextCursor.LineUnderCursor)
            curText = text_cursor.selectedText()
            pyperclip.copy(curText)

            # ss = pe.toPlainText()
            # print(ss, ss.split('\n'))

    def slot_combo_selected(self, label, index):
        if label == 'length':
            self.cipher_length = index + 1
        elif label == 'count':
            self.ciphers_count = index + 1

    # def slot_radio_released(self, label):
    #     return
    #     if label == '4位':
    #         self.code_type -= 4
    #         # print('4位 %d' % self.code_type)
    #     elif label == '6位':
    #         self.code_type -= 6
    #         # print('6位 %d' % self.code_type)
    #     elif label == '数字':
    #         self.code_type -= 8
    #         # print('数字 %d' % self.code_type)
    #     elif label == '字符':
    #         self.code_type -= 9
    #         # print('字符 %d' % self.code_type)
    #     print(label, 'released. %d' % self.code_type)

    def slot_radio_clicked(self, label):
        # print(label)

        # 根据类型，决定部分控件的可见性
        if label == '随机密码':  # 随机码
            self.shell.groupBox_2.setVisible(True)
            self.shell.groupBox_5.setVisible(False)
            self.shell.groupBox_6.setVisible(False)
            self.shell.groupBox_7.setVisible(False)
            self.cipher_type = label
        elif label == '易记密码':  # 易记密码
            self.shell.groupBox_2.setVisible(False)
            self.shell.groupBox_5.setVisible(True)
            self.shell.groupBox_6.setVisible(False)
            self.shell.groupBox_7.setVisible(False)
            self.cipher_type = label
        elif label == 'PIN':  # PIN码，界面保持现状，仅选择数字
            self.shell.groupBox_2.setVisible(False)
            self.shell.groupBox_5.setVisible(False)
            self.shell.groupBox_6.setVisible(True)
            self.shell.groupBox_7.setVisible(True)
            self.cipher_type = label
        elif label == '4位':
            self.code_type &= 0xF0
            self.code_type += 4
        elif label == '6位':
            self.code_type &= 0xF0
            self.code_type += 6
        elif label == '数字':
            self.code_type &= 0x0F
            self.code_type |= 0x10
        elif label == '字符':
            self.code_type &= 0x0F
            self.code_type |= 0x20

        # print(label, 'clicked. %#x' % self.code_type)

    def slot_box_checked(self):
        # print(self.cipher_type)
        # 统一扫描所有选项，直接算出密码字符集
        self.char_set.clear()

        if self.cipher_type == '随机密码':  # 随机码
            if self.shell.checkBox_1.isChecked():  # 大写字母
                self.char_set.update(string.ascii_uppercase)
                # print(self.char_set | string.ascii_uppercase)  # 并集？
            if self.shell.checkBox_2.isChecked():  # 小写字母
                self.char_set.update(string.ascii_lowercase)
            if self.shell.checkBox_3.isChecked():  # 阿拉伯数字
                self.char_set.update(string.digits)
            if self.shell.checkBox_4.isChecked():  # 可见字符
                self.char_set.update(Utils.get_chars(6))
            if self.shell.checkBox_5.isChecked():  # 小写汉字数字
                print('小写汉字数字')
            if self.shell.checkBox_6.isChecked():  # 大写汉字数字
                print('大写汉字数字')
            if self.shell.checkBox_7.isChecked():  # 排除字符
                self.char_mask.clear()
                # print(self.shell.lineEdit_2.text())
                self.char_mask.update(self.shell.lineEdit_2.text())
                # print(self.char_mask)
                # self.char_set -= self.char_mask  # 差集？
                # # 更新集合s1的内容为s1-s2后的结果
                self.char_set.difference_update(self.char_mask)
                # s1.difference(s2) # 该操作对s1内容无影响
                # 判断集合是否与指定集合不存在交集
                # if self.char_set.isdisjoint(self.char_mask):
                #     print('已排除')
            if self.shell.checkBox_8.isChecked():  # 特殊字符
                self.char_set.update(self.shell.lineEdit.text())  # 更新
            #     # if text.issubset(self.char_set):  # 判断集合是否指定集合的子集
            #     #     print('已添加')
            #     # else:
            #     #     self.char_set.difference_update(text)
            #     #     print('已排除')

        elif self.cipher_type == '易记密码':  # 易记密码
            if self.shell.checkBox_9.isChecked():
                pass
                # self.char_set.update(string.ascii_uppercase)
            if self.shell.checkBox_10.isChecked():
                pass
                # self.char_set.update(string.ascii_uppercase)

        else:  # PIN码，则一切选择无效，界面保持现状
            if self.shell.checkBox_11.isChecked():
                self.code_type = 4  # '4位PIN'
            elif self.shell.checkBox_12.isChecked():
                self.code_type = 6  # '6位PIN'
            # elif self.shell.checkBox_13.isChecked():
            #     self.code_type = '4位验证码'
            # else:
            #     self.code_type = '6位验证码'

        # print(str(self.char_set))
        # self.shell.plainTextEdit.setPlainText(label + '  ' + str(self.char_set))

    # def slot_text_changed(self, label, text):
    #     print(type(label), label, text)
    #     if label == '排除字符':
    #         if self.shell.checkBox_7.isChecked():  # 有效
    #             self.char_mask.clear()
    #             self.char_mask.update(self.shell.lineEdit_2.text())
    #             # 更新集合s1的内容为s1-s2后的结果 # s1.difference(s2) # 该操作对s1内容无影响
    #             self.char_set.difference_update(self.char_mask)
    #         # print(self.char_mask)
    #     elif label == '特殊字符':
    #         if self.shell.checkBox_8.isChecked():
    #             self.char_set.update(self.shell.lineEdit.text())  # 更新
    #             # print(self.shell.lineEdit.text())
    #     else:
    #         pass

    def slot_edit_text_changed(self):
        # pe = QtWidgets.QTextEdit()
        pe = self.shell.textEdit
        text_cursor = pe.textCursor()
        # text_cursor.movePosition(QtGui.QTextCursor.Start)  # 将光标移动到起始位置
        # # 刚刚行全选完的行尾作为起始位置
        # text_cursor.setPosition(text_cursor.position(), QtCore.QTextCursor.MoveAnchor)
        # # 向后移动光标，选中一个字符
        # text_cursor.setPosition(text_cursor.position() + 1, QtCore.QTextCursor.KeepAnchor)
        # end_charactor = text_cursor.selectedText()
        # if end_charactor == " " or end_charactor == "\n":  # 行尾特殊字符处理
        #     pass

        text_cursor.select(QtGui.QTextCursor.LineUnderCursor)  # 选中要着色的内容

        curText = text_cursor.selectedText()

        fmt = QtGui.QTextCharFormat()
        fmt.setForeground(QtGui.QColor(QtCore.Qt.red))
        # text_cursor.mergeCharFormat(fmt)  # 设置文本格式
        # text_cursor.setCharFormat(fmt)
        # text_cursor.clearSelection()  # 撤销选中
        # text_cursor.movePosition(QtGui.QTextCursor.EndOfLine)  # cursor和anchor均移至末尾
        # text_cursor.insertText(" world", fmt)
        # curText = text_cursor.selectedText()
        if curText:
            level = self.checker.check_password(curText)
            tip = '  '.join(self.msg[level])
            self.shell.label_tip.setText(f"当前密码：{tip}")

        print('当前文本', len(curText), curText)

    # def slot_text_copy(self, status):
    #     print('文本选择')
    #     if status:
    #         self.shell.textEdit.copy()
    #         command = QtWidgets.QApplication.clipboard().text().upper()
    #         print(command)


def main():
    # cipher = Cypher()
    n = 0x14
    n &= 0xF0
    n += 6
    print(n.bit_length(), '%#x' % n)
    # print(bin(a), bin(b), bin(c))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Cypher()
    win.show()
    sys.exit(app.exec_())
    # main()
