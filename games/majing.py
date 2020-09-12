#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @Product: PyCharm
#  @Project: python
#  @File    : majing.py
#  @Author  : big
#  @Email   : shdorado@126.com
#  @Time    : 2020/6/26 13:16
#  功能：

import copy
import sys
import os
import time
#
# import cv2
# import numpy as np

from utilities import Utils


class MjData:
    # LINE = str(sys._getframe().f_lineno)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 项目根目录

    def __init__(self):
        # self.tiles_dot = []  # 饼子
        # self.tiles_bamboo = []  # 条子
        # self.tiles_character = []  # 万子
        # self.tiles_wind = ['东风', '南风', '西风', '北风']    # 番子： the honor tiles (dragon+wind)
        # self.tiles_dragon = ['红中', '发财', '白板']  # 中发白：red dragon、green dragon、white dragon
        # self.tiles = (11, 12, 13, 14, 15, 16, 17, 18, 19,  # 万 各4张
        #               11, 12, 13, 14, 15, 16, 17, 18, 19,
        #               11, 12, 13, 14, 15, 16, 17, 18, 19,
        #               11, 12, 13, 14, 15, 16, 17, 18, 19,
        #               21, 22, 23, 24, 25, 26, 27, 28, 29,  # 饼 各4张
        #               21, 22, 23, 24, 25, 26, 27, 28, 29,
        #               21, 22, 23, 24, 25, 26, 27, 28, 29,
        #               21, 22, 23, 24, 25, 26, 27, 28, 29,
        #               31, 32, 33, 34, 35, 36, 37, 38, 39,  # 条 各4张
        #               31, 32, 33, 34, 35, 36, 37, 38, 39,
        #               31, 32, 33, 34, 35, 36, 37, 38, 39,
        #               31, 32, 33, 34, 35, 36, 37, 38, 39,
        #               41, 42, 43, 44, 45, 46, 47,  # 东南西北 中发白 各4张
        #               41, 42, 43, 44, 45, 46, 47,
        #               41, 42, 43, 44, 45, 46, 47,
        #               41, 42, 43, 44, 45, 46, 47,
        #               51, 52, 53, 54, 55, 56, 57, 58)  # 春夏秋冬，梅兰菊竹 各1张
        # 数据格式:类型=value/10, 数值=value%10
        # self.majmap = {"0": "一万", "1": "二万", "2": "三万", "3": "四万", "4": "五万",
        #                "5": "六万", "6": "七万", "7": "八万", "8": "九万",
        #                "10": "一饼", "11": "二饼", "12": "三饼", "13": "四饼", "14": "五饼",
        #                "15": "六饼", "16": "七饼", "17": "八饼", "18": "九饼",
        #                "20": "一条", "21": "二条", "22": "三条", "23": "四条", "24": "五条",
        #                "25": "六条", "26": "七条", "27": "八条", "28": "九条",
        #                "30": "东风", "31": "南风", "32": "西风", "33": "北风", "34": "红中",
        #                "35": "发财", "36": "白板",
        #                "40": "春", "41": "夏", "42": "秋", "43": "冬", "44": "梅",
        #                "45": "兰", "46": "菊", "47": "竹"}
        # g_tiles = ((0x01, "一万"), (0x02, "二万"), (0x03, "三万"), (0x04, "四万"),
        #            (0x05, "五万"), (0x06, "六万"), (0x07, "七万"), (0x08, "八万"), (0x09, "九万"),
        #            (0x11, "一饼"), (0x12, "二饼"), (0x13, "三饼"), (0x14, "四饼"),
        #            (0x15, "五饼"), (0x16, "六饼"), (0x17, "七饼"), (0x18, "八饼"), (0x19, "九饼"),
        #            (0x21, "一条"), (0x22, "二条"), (0x23, "三条"), (0x24, "四条"),
        #            (0x25, "五条"), (0x26, "六条"), (0x27, "七条"), (0x28, "八条"), (0x29, "九条"),
        #            (0x31, "东风"), (0x32, "南风"), (0x33, "西风"), (0x34, "北风"),
        #            (0x35, "红中"), (0x36, "发财"), (0x37, "白板"),
        #            (0x41, "春"), (0x42, "夏"), (0x43, "秋"), (0x44, "冬"),
        #            (0x45, "梅"), (0x46, "兰"), (0x47, "菊"), (0x48, "竹"))

        self.tiles_id = (0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,  # 万
                         0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19,  # 筒
                         0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29,  # 条
                         0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37,  # 东南西北，中发白
                         0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48)  # 春夏秋冬，梅兰菊竹

        self.tiles_name = ("一万", "二万", "三万", "四万", "五万", "六万", "七万", "八万", "九万",
                           "一饼", "二饼", "三饼", "四饼", "五饼", "六饼", "七饼", "八饼", "九饼",
                           "一条", "二条", "三条", "四条", "五条", "六条", "七条", "八条", "九条",
                           "东风", "南风", "西风", "北风", "红中", "发财", "白板",
                           "春", "夏", "秋", "冬", "梅", "兰", "菊", "竹")

        self._pic_path = 'E:/Neworld/games/res/ma_yellow'
        self.tiles_pic = ('man1.png', 'man2.png', 'man3.png', 'man4.png', 'man5.png',
                          'man6.png', 'man7.png', 'man8.png', 'man9.png',
                          'pin1.png', 'pin2.png', 'pin3.png', 'pin4.png', 'pin5.png',
                          'pin6.png', 'pin7.png', 'pin8.png', 'pin9.png',
                          'bamboo1.png', 'bamboo2.png', 'bamboo3.png', 'bamboo4.png', 'bamboo5.png',
                          'bamboo6.png', 'bamboo7.png', 'bamboo8.png', 'bamboo9.png',
                          'wind-east.png', 'wind-south.png', 'wind-west.png', 'wind-north.png',
                          'dragon-chun.png', 'dragon-green.png', 'dragon-haku.png', ' ', ' ',
                          'season-spring.png', 'season-summer.png', 'season-autumn.png', 'season-winter.png',
                          'flower-plum.png', 'flower-orchid.png', 'flower-chrysanthemum.png', 'flower-bamboo.png')

        # _g_pic_path = 'E:/python/games/res/img_match'
        # g_tiles_pic = ('character1.png', 'character2.png', 'character3.png', 'character4.png', 'character5.png',
        #                'character6.png', 'character7.png', 'character8.png', 'character9.png',
        #                'dot1.png', 'dot2.png', 'dot3.png', 'dot4.png', 'dot5.png',
        #                'dot6.png', 'dot7.png', 'dot8.png', 'dot9.png',
        #                'bamboo1.png', 'bamboo2.png', 'bamboo3.png', 'bamboo4.png', 'bamboo5.png',
        #                'bamboo6.png', 'bamboo7.png', 'bamboo8.png', 'bamboo9.png',
        #                'windEast.png', 'windSouth.png', 'windWest.png', 'windNorth.png',
        #                'dragonRed.png', 'dragonGreen.png', 'dragonWhite.png', ' ', ' ',
        #                'flower1', 'flower2', 'flower3', 'flower4', 'flower5', 'flower6', 'flower7', 'flower8')

        # _g_pic_path = 'E:/python/games/res/ma_gray'
        # g_tiles_pic = ('character_1.png', 'character_2.png', 'character_3.png', 'character_4.png', 'character_5.png',
        #                'character_6.png', 'character_7.png', 'character_8.png', 'character_9.png',
        #                'circle_1.png', 'circle_2.png', 'circle_3.png', 'circle_4.png', 'circle_5.png',
        #                'circle_6.png', 'circle_7.png', 'circle_8.png', 'circle_9.png',
        #                'bamboo_1.png', 'bamboo_2.png', 'bamboo_3.png', 'bamboo_4.png', 'bamboo_5.png',
        #                'bamboo_6.png', 'bamboo_7.png', 'bamboo_8.png', 'bamboo_9.png',
        #                'wind_east.png', 'wind_south.png', 'wind_west.png', 'wind_north.png',
        #                'dragon_red.png', 'dragon_green.png', 'dragon_white.png', ' ', ' ',
        #                'season_spring.png', 'season_summer.png', 'season_autumn.png', 'season_winter.png',
        #                'flower_plum.png', 'flower_orchid.png', 'flower_chrysanthemum.png', 'flower_bamboo.png')

    def test(self):
        # for i in range(-1, 75):
        #     print(i, self.is_valid(i))
        # print(len(self.tiles_id))
        # for i in range(len(self.tiles_id)):
        #   self._tile_is(i)
        # for each in self.tiles_id:
        #     print(self.id2name(each))
        # for each in self.tiles_name:
        #     print(self.name2id(each))
        # for i in range(-2, 0x50):
        #     # index = (DataMj.value2index(i))
        #     # print('%#x' % i, index, DataMj.name_is(index))
        #     print(DataMj.id2name(i))

        for each in self.tiles_id:
            print(self.suit_color(each), self.suit_rank(each))

    # region 功能函数
    def _tile_is(self, index):  # 非id
        ret = '非法下标'
        if -1 < index < 42:  # 合法的才显示，非法的忽略
            ret = self.tiles_id[index], self.tiles_name[index]
        print(index, ret)
        return ret

    # id 有效性判断
    def is_valid(self, tile_id):
        return tile_id in self.tiles_id

    def id2name(self, tile_id):
        if self.is_valid(tile_id):
            return self.tiles_name[self.tiles_id.index(tile_id)]

    def name2id(self, name):
        if name in self.tiles_name:
            return self.tiles_id[self.tiles_name.index(name)]

    # 打印手牌
    def card2names(self, card):
        if not isinstance(card, list) and len(card) == 0:  # 合法的才显示，非法的忽略
            print('print_list:非法的 cards')
            return
        tmp = []
        for each in card:
            tmp.append(self.id2name(each[0]))
        print(tmp)

    # 手牌图片
    def card2pics(self, card):
        if not isinstance(card, list) or len(card) == 0:  # 合法的才显示，非法的忽略
            print('print_list:非法的 card')
            return
        if not self.is_valid(card[0][0]):
            return

        tmp = []
        for each in card:
            tmp.append(f'{self._pic_path}/{self.tiles_pic[self.tiles_id.index(each[0])]}')
        # print(tmp)
        return tmp

    # 识别手牌
    def names2card(self, names):
        if not names:  # 合法的才显示，非法的忽略
            return
        tmp = []
        for each in names:
            ret = self.name2id(each)
            tmp.append([ret, 0])

        # print(tmp)
        return tmp

    # 手牌的图片
    def names2pics(self, names):
        if not names:  # 合法的才显示，非法的忽略
            return
        tmp = []
        for each in names:
            tmp.append(f'{self._pic_path}/{self.tiles_pic[self.tiles_name.index(each)]}')

        # print(tmp)
        return tmp

    # 获得配牌的花色
    def suit_color(self, tile_id):
        ret = None
        if self.is_valid(tile_id) and tile_id < 0x30:  # 非字牌、花牌  id 有效性判断
            # ret = tile_id & 0x00F0  # 花色(配牌) 筒、条、万
            ret = tile_id >> 4  # 万、筒、条
        return ret

    # 获得配牌的数字
    def suit_rank(self, tile_id):
        ret = None
        if self.is_valid(tile_id) and tile_id < 0x30:  # 非字牌、花牌
            ret = tile_id & 0x000F  # 获得牌面的大小 一~九
        return ret

    # def value2index(tile_id=0x00):
    #     """
    #     通过牌的 name和 pic 获得索引和名称
    #     :param tile_id:
    #     :return:
    #     """
    #
    #     index = -1
    #
    #     # if tile_id < 1 or tile_id > 0x48:
    #     #     return index - 1
    #     if DataMj.is_valid(tile_id):
    #         rank = tile_id & 0x0F  # 获得牌面的大小
    #
    #         if tile_id < 0x31:
    #             # print('value = ', value)
    #             if 0 < rank < 10:
    #                 color = tile_id >> 4  # 获得牌的花色/类型
    #                 index = color * 9 + rank - 1  # * 9
    #                 # index = (color << 3) + color + value  # * 9
    #         elif tile_id < 0x38:
    #             index = 26 + rank
    #         elif 0x40 < tile_id:
    #             index = 33 + rank
    #
    #     # print("%#x, %d" % (tile_id, index))
    #     return index

    # def index2value(index):
    #     tile_name = ((index // 9) << 4) | (index % 9)
    #     return tile_name

    # @staticmethod
    # def get_name_pic(ID):
    #     """
    #     根据ID获得麻将牌的名称与图片文件名称
    #     :param ID:
    #     :return: [名称，文件名]
    #     """
    #
    #     ret = None
    #     index = MjData.value2index(ID)
    #
    #     if 0 <= index < 44:
    #         if index == 34 or index == 35:  # 补位的不算
    #             return ret, ret
    #
    #         name = MjData.g_tiles_name[index]
    #         file = None
    #         kind = (index // 9)
    #         value = (index % 9) + 1
    #         if kind == 0:
    #             file = ''.join(['character', str(value), '.png'])
    #         elif kind == 1:
    #             file = ''.join(['dot', str(value), '.png'])
    #         elif kind == 2:
    #             file = ''.join(['bamboo', str(value), '.png'])
    #         elif kind == 3:
    #             tmp = ('windEast.png', 'windSouth.png', 'windWest.png', 'windNorth.png',
    #                    'dragonRed.png', 'dragonGreen.png', 'dragonWhite.png')
    #             file = tmp[value - 1]
    #         else:  # 春、夏、秋、冬、梅、兰、竹、菊
    #             file = ''.join(['flower', str(value), '.png'])
    #
    #         file = os.path.join(MjData._g_pic_path, file)
    #         file = file.replace('\\', '/')
    #
    #         return name, file
    #
    #     else:
    #         return ret, ret
    # endregion

    # region 手牌的排序
    @staticmethod
    def bubble_sort(arr, left=None, right=None):  # 冒泡排序
        if not isinstance(arr, list):
            return

        lenth = len(arr)
        if lenth < 2:
            print(str(sys._getframe().f_lineno), 'error')
            return

        left = 0 if not isinstance(left, (int, float)) else left
        right = lenth if not isinstance(right, (int, float)) else right

        left = 0 if left < 0 else (lenth if left > lenth else left)
        right = 0 if right < 0 else (lenth if right > lenth else right)

        if left == right:
            return

        if left > right:
            left, right = right, left

        # print(left, right)

        for i in range(left + 1, right):
            for j in range(left, right - i):
                if arr[j].ID > arr[j + 1].ID:
                    arr[j].index, arr[j + 1].index = arr[j + 1].index, arr[j].index
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

        return arr

    # sys.setrecursionlimit(100000)  # 例如这里设置递归深度为十万
    @staticmethod
    def quick_sort_card(arr, left=None, right=None):
        if not isinstance(arr, list):
            return

        lenth = len(arr)
        if lenth < 2:
            print(str(sys._getframe().f_lineno), 'error')
            return

        left = 0 if not isinstance(left, (int, float)) else left
        right = lenth - 1 if not isinstance(right, (int, float)) else right

        left = 0 if left < 0 else (lenth - 1 if left >= lenth else left)
        right = 0 if right < 0 else (lenth - 1 if right >= lenth else right)

        if left == right:
            return

        if left > right:
            left, right = right, left

        partitionIndex = MjData.partition(arr, left, right)
        MjData.quick_sort_card(arr, left, partitionIndex - 1)
        MjData.quick_sort_card(arr, partitionIndex + 1, right)

        return arr

    @staticmethod
    def partition(arr, left, right):
        pivot = left
        index = pivot + 1
        i = index
        while i <= right:
            if arr[i].ID < arr[pivot].ID:
                MjData.swap_it(arr, i, index)
                index += 1
            i += 1
        MjData.swap_it(arr, pivot, index - 1)

        return index - 1

    @staticmethod
    def swap_it(arr, i, j):
        arr[i].index, arr[j].index = arr[j].index, arr[i].index
        arr[i], arr[j] = arr[j], arr[i]

    @staticmethod
    def sortArray(arr):
        if not isinstance(arr, list) or len(arr) == 0:
            return
        arr.sort(key=(lambda x: x[0]))  # 对二维列表进行排序,按第一项
    # endregion


class Mahjong:
    def __init__(self, parent=None):
        # noinspection PyArgumentList
        super(Mahjong, self).__init__()
        self.parent = parent

        # 牌局的总体参数
        self.data = MjData()
        self.tiles_count = 108  # 麻将牌的总数 144, 136, 108
        # self.delay = 10  # 叫牌后的停顿时间

        # self.players = ('东方', '南方', '西方', '北方')
        self.player_names = ('东座', '南座', '西座', '北座')

        self.dealer = 1  # 庄家方位 0：东 1：南，1始终是本家，
        self.dice = 99  # 骰子  points 点数    cheat 抽老千
        self.lots = 0  # 出牌的手数，可以判断各人打出的牌数
        self.speaker = None  # 目前的出牌者
        # self.speaker = self.dealer  # 目前的出牌者
        self.hot_tile = [0, 0]  # 目前的出牌

        self.oker = None  # 鬼牌，钻石牌
        # self.tile_ejected = None  # 弹起的牌
        # self.tile_shadow = None  # 本家叫/热牌的影子牌

        # 数据区
        self.round = []  # 一圈/一局的暗牌, 仅有牌号和标志位(0:正常 1:明牌 2:牌卡弹出)
        # self.card_players = [[0] * 14 for i in range(4)]  # 四家的牌面，每张牌含牌号、翻牌等标志、控件
        self.card_players = [[[0, 0]] * 13 for i in range(4)]  # 四家的牌面最多18张，可以添加到。每张牌含牌号和状态。
        # 每张牌的状态，0:摸牌，1:碰牌，2:暗杠，3:绕杠，4:明杠，5:吃牌 9:出牌
        # print(self.card_players[0])

        # self.card_ground = [[0], [0], [0], [0]]  # 四家落地牌，各家桌上废牌
        self.dark_cards = []  # 暗牌，除自己手牌和落地牌外的看不见的牌

        self.para = [10, 2, 1]  # 计算每张牌的分值
        self.scale = 50
        self.lost = 10  # 流局阀值

        self.speaker_changed = False
        self.winning = False  # 已胡牌
        self.begin = False
        # self.can_discard = False  # 本家可以出牌否

        # self.id_discarded = 0  # 打出的牌在队列中的序号

        # self.img_ex(r'E:\Neworld\games\res\ma_yellow\man8.png')

        # 功能区
        # self.event_discarded = threading.Event()  # 出牌信号
        # self.event_can_draw = threading.Event()  # 摸牌信号
        """
        Event用法：
        event = threading.Event()  # 设置一个事件实例
        event.set()  # 设置标志位     放开通道
        event.clear()  # 清空标志位      关闭通道
        event.wait()  # 等待设置标志位    if event.is_set()开通 …… else …… 阻塞了：通道被关，等待开启
        """

        # self.init_board()

        # tmp = []
        # for i in range(4, -10, -1):
        #     tmp.append((i, i % 4))
        # print(tmp)

    # 洗牌，砌牌，全部 ID
    def shuffling(self):
        tmp = []
        for i in range(4):
            tmp.extend(self.data.tiles_id[0:27])
            if self.tiles_count > 108:
                tmp.extend(self.data.tiles_id[27:34])
        if self.tiles_count > 136:
            tmp.extend(self.data.tiles_id[34:42])

        self.dark_cards = sorted(tmp)  # 都算暗牌

        self.round.clear()
        # 随机洗牌
        for i in range(self.tiles_count):
            index = Utils.rand_int(0, self.tiles_count - i - 1)
            self.round.append(tmp[index])
            tmp.pop(index)

        # i = 3
        # while i > 0:
        #     random.shuffle(self.round)
        #     i = i - 1
        # print(len(self.round), self.round)

        # print(self.data.cards2names(sorted(self.round)))  # 返回新的排序队列，原队列不排序
        # self.round.sort()  # 不返回任何东西，自身排序
        # print(self.round)
        # print(self.card_players)
        # self.data.cards2names(self.round)
        # self.data.cards2names(self.dark_cards)

    # 起牌
    def deal(self):
        """
        抓牌顺时针抓,打牌逆时针打
        :return:
        """
        if self.tiles_count < 54:  # 不够起牌的
            return

        self.dealer %= 4  # 轮流坐庄 4人麻将

        # 庄家掷骰子找到二次掷骰人，并确定开门方向
        # die1 = random.randint(1, 12)
        die_1 = Utils.rand_int(1, 12)
        door = (self.dealer + die_1 - 1) % 4  # 开门方向
        # 二次掷骰子
        # die2 = random.randint(1, 12)
        die_2 = Utils.rand_int(1, 12)
        dice = (door + 1) * 34 - die_2 * 2
        # zero = dice % self.tiles_count      # 开始摸牌的位置
        new_round = self.round[dice:]
        new_round.extend(self.round[:dice])
        self.round = new_round  # 重新起算
        # print(dice, len(self.round))
        # print(self.data.cards2names(sorted(self.round)))  # 返回新的排序队列，原队列不排序

        self.lots = 0
        # 给玩家发牌，顺时针抓牌
        for k in range(3):  # 发三次牌，每人每次拿连续的4张
            for i in range(4):
                player_id = (i + self.dealer) % 4  # 循环坐庄
                for j in range(4):
                    # # 牌号、牌卡控件、翻牌等标志
                    # ID = self.round[self.lots]  # 牌号，兼做排序用
                    index = j + 4 * k  # 槽位
                    # player_id 也代表卡牌类型
                    # self.card_players[player_id][index] = Tile(self, ID, player_id, index)
                    # self.card_players[player_id][index][0] = self.round.pop(0)  # 牌号，兼做排序用
                    self.card_players[player_id][index] = [self.round.pop(0), 0]  # 牌号，兼做排序用
                    # print(player_id, index, self.card_players[player_id][index])
                    self.lots += 1

        # 每人再模一张，叫牌空置
        for i in range(4):
            player_id = (i + self.dealer) % 4  # 从庄家开始
            self.card_players[player_id][12] = [self.round.pop(0), 0]  # 返回弹出值
            # self.card_players[player_id][12] = Tile(self, self.round[self.lots], player_id, 12)
            # self.card_players[player_id][13] = Tile(self, 999, 4 + player_id, 13)  # 叫牌，确保排在最后，每台不用清零
            # self.tile_shadow = Tile(self, 999, 1, 13)  # 把影子牌实例化
            self.lots += 1

            # for j in range(13, 18):
            #     self.card_players[player_id][j] |= 0xff  # 叫牌，确保排在最后，每台不用清零

            self.card_players[player_id].sort()  # 排序
            # self.data.sortArray(self.card_players[player_id])

        # 庄家不多摸，现在从庄家开始摸牌再发牌
        self.speaker = self.dealer  # 目前的摸/出牌者

        # for i in range(4):
        #     # print(self.card_players[i])
        #     self.data.cards2names(self.card_players[i])

    # 牌局循环
    def playing(self):
        """
            检测到哪家摸牌了，接着叫牌，也就是出牌
            :return:
        """
        self.begin = True
        while True:  # 逆时针打牌
            if len(self.round) <= self.lost or self.winning:  # 荒牌或胡牌
                break

            # 话事者摸牌
            if self.draw():
                continue

            self.hot_tile[1] = 9  # 说明热牌被打出来了，等待后面的 胡杠碰吃

            # 听牌比杠牌和碰牌优先
            if self.ting():
                continue

            # 杠和碰平级，所以从下家开始往后
            for i in range(self.speaker + 3, self.speaker, -1):  # 从下家开始
                speaker = i % 4

                if self.kong(speaker):  # 明杠，别人杠
                    self.speaker_changed = True
                    break

                if self.pung(speaker):  # peng
                    self.speaker_changed = True
                    break

            if self.speaker_changed:
                self.speaker_changed = False
                continue

            # # 吃牌最后
            if self.chow():
                pass
            # else:
            #     # self.speaker += 3  # 右手是下家，让下家摸牌、出牌 下家接手
            #     # self.speaker %= 4  # 确保不溢出
            # print(f"{self.player_names[self.speaker]} 说话")

        self.begin = False

        if self.winning:
            self.scoring(self.speaker)
        else:
            print('荒牌，流局了!')

    # 摸牌
    def draw(self):
        self.lots += 1

        self.hot_tile = [self.round.pop(0), 0]  # 进张
        self.speaker %= 4  # 确保不溢出

        win_cards = [item[0] for item in self.card_players[self.speaker]]
        win_cards.append(self.hot_tile[0])  # 进张了
        win_cards.sort()
        # print(self.card_players[self.speaker])
        # self.data.card2names(win_cards)

        print(f'{self.player_names[self.speaker]} 进张：{self.data.id2name(self.hot_tile[0])}')

        # if self.speaker == 1:  # 南座，得停止，等待命令
        # self.parent.show_cards(win_cards)
        # time.sleep(5)

        if self.win(win_cards):  # 判断自摸胡牌没有
            self.winning = True
            return True  # 胡牌

        if self.kong(self.speaker):  # 判断自摸杠牌
            if self.winning:  # （连杠）杠上开花
                return True  # 胡牌
        else:  # 需要出牌
            cards = self.card_players[self.speaker]
            cards.append(self.hot_tile)  # 进张了
            cards.sort()
            self._hot_update(cards)

        return False  # 没有胡牌

    # # 摸牌
    # def draw(self):
    #     """
    #             检测到哪家摸牌了，接着叫牌，也就是出牌
    #             :return:
    #             """
    #
    #     while True:
    #         if self.lots >= self.tiles_count or self.isWin:  # 荒牌或胡牌
    #             break
    #
    #         if not self.event_can_draw.is_set():
    #             self.event_can_draw.wait()
    #         else:
    #             ground_tiles = self.lots - 52  # 已经打出的落地牌的数量，包括当前的叫牌
    #             print(f'{self.speaker}摸牌, 地牌数:{ground_tiles}')
    #             # DataMj.write_log(string, 'red')
    #
    #             if self.speaker == 1:  # 显示本家的影子牌
    #                 self.card_players[1][13].resurfacing(self.round[self.lots], 5)  # 真身进张
    #                 self.lots += 1  # 进张了
    #                 self.tile_shadow.resurfacing(self.card_players[1][13].ID, 5)  # 影子深拷贝一份
    #                 self.tile_shadow.setVisible(True)
    #                 self.can_discard = True  # 可以出牌了，等待本家脑袋算法选择后，鼠标触发 出牌
    #                 self.event_can_draw.clear()
    #             else:  # 其他家智能出牌
    #                 self.card_players[self.speaker][13].resurfacing(self.round[self.lots], 4 + self.speaker)
    #                 self.lots += 1  # 进张了
    #
    #                 self.collect_melds()  # 这里要经过算法处理，看是否听、胡，或者出牌，打出的应该是废张，而非简单的进牌
    #
    #                 self.card_players[self.dealer][13].setVisible(True)  # 亮 13牌即等于出13牌
    #                 self.event_discarded.set()  # 叫醒 胡对杠吃 程序

    # 数番
    def scoring(self, speaker):
        print(f'第{self.lots}手，{self.player_names[speaker]} \033[7;32m胡牌\033[7;32m\033[0m !\033[0m')
        self.card_players[speaker].append(self.hot_tile)
        self.card_players[speaker].sort()
        self.data.card2names(self.card_players[speaker])
        # print((self.card_players[speaker]))

    # 设置或获取 牌的标志位
    @staticmethod
    def _state(tile_id=0, state=-1):
        # 每张牌的状态，0: 摸牌，1: 出牌，2: 碰牌，3: 吃牌，4: 明杠，5: 绕杠 6: 暗杠
        return (0xff & tile_id) | (state << 8) if -1 < state < 7 else (tile_id & 0xF00) >> 8

    # 热牌的更新
    def _hot_update(self, cards):
        # cards.append(self.hot_tile)  # 加入热牌
        # cards.sort()  # 且排序

        player_cards = [item[0] for item in cards]
        index = self._cards_score(player_cards)  # 分值最小的牌，需要打出去
        self.hot_tile = cards[index]
        self.hot_tile[1] = 9  # 出牌
        cards.pop(index)  # 打出去了

        print(f'{self.player_names[self.speaker]} 出牌：{self.data.id2name(self.hot_tile[0])}')
        self.speaker += 3  # 下家接手
        self.speaker %= 4  # 确保不溢出
        # print(f"{self.player_names[self.speaker]} 说话")

        # i = self.dark_cards.index(self.hot_tile[0])
        # self.dark_cards.pop(i)  # 变成明牌

    # 选废牌
    def _cards_score(self, player_cards, print_it=False):
        # player_cards：手上的牌
        # x+/-3:0   x+/-2:10   x+/-1:20   x:100
        # xxxx:400   xxx:300   xx:200   x x+1 x+2:130   x x+1:120   x x+2:110

        scores = []

        # dark = []+self.dark_cards  # 每家的暗牌不一样，要减去自己牌。 未出现过的牌
        dark = copy.deepcopy(self.dark_cards)  # 深拷贝
        for each in player_cards:
            if each in dark:
                dark.pop(dark.index(each))
        # dark = list(set(self.dark_cards) - set(player_cards))
        # print('cha', len(dark), len(self.dark_cards), len(player_cards))
        # print(dark, '\n', self.dark_cards, '\n', player_cards)

        for c in player_cards:
            score = 0
            for cc in player_cards:
                gap = abs(cc - c)
                if c > 0x30:
                    if gap == 0:  # 风、龙、花牌 成双
                        score += self.para[gap] * self.scale
                else:
                    if gap < 3:
                        score += self.para[gap] * self.scale

            for cc in dark:  # 未出现的牌中还有比较多的A，B,那么凑出AAA或ABC牌的几率加大了
                gap = abs(cc - c)
                if c > 0x30:
                    if gap == 0:  # 风、龙、花牌 成双
                        score += self.para[gap]
                else:
                    if gap < 3:
                        score += self.para[gap]

            scores.append(score)

        if print_it:
            print(scores)

        return scores.index(min(scores))

    # 和、胡，胡牌判断，player_cards: 手牌，需要从小到大排列
    def win(self, player_cards, is_win=False):
        # 递归算法：配对成功的弹出，一直到手上牌都弹出为止
        if len(player_cards) == 0 and is_win:
            return True

        rst = False
        # AA
        if not is_win and len(player_cards) >= 2 and player_cards[0] == player_cards[1]:
            list1 = [] + player_cards
            list1.pop(0)
            list1.pop(0)
            rst = self.win(list1, True)

        # AAA
        if not rst and len(player_cards) >= 3 and player_cards[0] == player_cards[1] == player_cards[2]:
            list1 = [] + player_cards
            list1.pop(0)
            list1.pop(0)
            list1.pop(0)
            rst = self.win(list1, is_win)

        # AAAA
        if not rst and len(player_cards) >= 4 and \
                player_cards[0] == player_cards[1] == player_cards[2] == player_cards[3]:
            list1 = [] + player_cards
            list1.pop(0)
            list1.pop(0)
            list1.pop(0)
            list1.pop(0)
            rst = self.win(list1, is_win)

        # ABC
        if not rst and len(player_cards) >= 3:
            list1 = []
            a = player_cards[0]
            if a > 0x30:  # 风、龙、花牌
                return rst

            b = False
            c = False
            for i in range(1, len(player_cards)):
                if not b and player_cards[i] == a + 1:
                    b = True
                elif not c and player_cards[i] == a + 2:
                    c = True
                else:
                    list1.append(player_cards[i])

            if b and c:
                rst = self.win(list1, is_win)

        return rst

    # 听牌
    def ting(self):
        for i in range(self.speaker + 3, self.speaker, -1):  # 从下家开始
            speaker = i % 4
            new_cards = [item[0] for item in self.card_players[speaker]]
            new_cards.append(self.hot_tile[0])
            new_cards.sort()
            if self.win(new_cards):  # 放炮了
                print(f"{self.player_names[self.speaker]} \033[1;35m放炮\033[1;35m\033[0m 于 \033[0m"
                      f"\033[5;31m{self.data.id2name(self.hot_tile[0])}\033[5;31m\033[0m ! \033[0m")
                self.speaker = speaker
                self.winning = True  # 放炮胡
                return True
            # else:
            #     new_cards.pop(new_cards.index(self.hot_tile))  # 再次把热牌弹出去

        return False

    # 杠
    def kong(self, speaker):
        """
            明杠：①玩家手中有三张一样的牌，其它玩家打出了第四张一样的牌，玩家可以选择杠牌，这种叫做直杠，只收一家的筹码；
                ②玩家手上已经碰了三张一样的牌，当玩家自己又摸起了第四张一样的牌，这时可以选择杠牌，这种叫做绕杠，这种杠牌可以收三家的筹码。
            :param speaker:
            :return:
        """

        st_hot = self.hot_tile[1]  # 状态，0:摸牌，1:碰牌，2:暗杠，3:绕杠，4:明杠，5:吃牌 9:出牌
        st_tile = -1  # 杠牌里最高的状态

        tmp = [self.hot_tile]
        cards = self.card_players[speaker]

        for j in range(len(cards)):
            st = cards[j][1]
            if st > 1:  # 只有手中的牌是碰牌或摸牌才能杠，吃来的手牌不能杠
                continue

            if self.hot_tile[0] == cards[j][0]:  # 同样的牌
                if st_hot == 9 and st == 1:  # 只能明杠别人打出的热牌，且不能再杠碰来的手牌
                    continue
                tmp.append(cards[j])
                st_tile = st if st > st_tile else st_tile

        if len(tmp) > 3:  # 这里要不要杠是个杠的策略问题，再细化
            if st_hot == 9:
                print(f"\033[0m{self.player_names[speaker]}\033[0m \033[1;33m明杠\033[1;33m "
                      f"\033[0m{self.player_names[self.speaker]} 的 \033[0m"
                      f"\033[5;32m{self.data.id2name(self.hot_tile[0])}\033[5;32m \033[0m!\033[0m")
            elif st_tile == 1:
                print(f"\033[0m{self.player_names[speaker]}\033[0m \033[1;34m绕杠\033[1;34m "
                      f"\033[5;32m{self.data.id2name(self.hot_tile[0])}\033[5;32m \033[0m!\033[0m")
            else:
                print(f"\033[0m{self.player_names[speaker]}\033[0m \033[1;35m暗杠\033[1;35m "
                      f"\033[5;32m{self.data.id2name(self.hot_tile[0])}\033[5;32m \033[0m!\033[0m")

            self.speaker = speaker  # 杠后成为当前发牌者

            for each in tmp:
                each[1] = 4 if st_hot == 9 else 3 if st_tile == 1 else 2  # 2:暗杠，3:绕杠，4:明杠

            # self.hot_tile[1] = 4 if st_hot == 9 else 3 if st_tile == 1 else 2  # 2:暗杠，3:绕杠，4:明杠
            cards.append(self.hot_tile)  # 加入热牌，且排序
            tail = [self.round.pop(), 0]  # 屁股上摸一张牌
            cards.append(tail)
            self.hot_tile = tail

            # 判断是否杠上开花，或连杠后杠上开花
            cards.sort()
            player_cards = [item[0] for item in cards]
            if self.win(player_cards) or self.kong(speaker):
                print(f"摸尾得 {self.data.id2name(tail[0])}，杠上开花！")
                self.winning = True  # 杠上开花
                return True  # 表示不用再出牌了

            else:  # 没有杠后胡牌和再杠，就要出牌
                self._hot_update(cards)
                # index = self._cards_score(cards)  # 分值最小的牌，需要打出去
                # self.hot_card = cards[index]
                # cards.pop(index)  # 打出去了
                #
                # print(f'{self.player_names[self.speaker]} 出牌：{self.data.id2name(self.hot_card)}')
                # self.speaker += 3  # 下家接手
                #
                # i = self.dark_cards.index(self.hot_card)
                # self.dark_cards.pop(i)  # 变成明牌
            return True  # 表示已经杠牌并出牌了

        return False  # 表示需要出牌

    # 碰
    def pung(self, speaker):
        # 碰碰胡在ting()里处理过了

        tmp = [self.hot_tile]

        # speaker = i % 4
        cards = self.card_players[speaker]

        for j in range(len(cards)):
            if self.hot_tile[0] == cards[j][0] and cards[j][1] == 0:  # 仅自摸的牌可以碰
                tmp.append(cards[j])

        if len(tmp) > 2:  # 这里要不要碰是个策略问题，再细化
            print(f"\033[0m{self.player_names[speaker]}\033[0m \033[1;31m碰\033[1;31m "
                  f"\033[0m{self.player_names[self.speaker]} 的 \033[0m"
                  f"\033[5;32m{self.data.id2name(self.hot_tile[0])}\033[5;32m \033[0m!\033[0m")

            self.speaker = speaker  # 碰后成为当前发牌者

            for each in tmp:
                each[1] = 1  # 牌的状态，0:摸牌，1:碰牌，2:暗杠，3:绕杠，4:明杠，5:吃牌 9:出牌

            cards.append(self.hot_tile)  # 加入热牌，且排序
            cards.sort()

            self._hot_update(cards)
            # index = self._cards_score(cards)  # 分值最小的牌，需要打出去
            # self.hot_tile = cards[index]
            # cards.pop(index)  # 打出去了
            # print(f'{self.player_names[self.speaker]} 出牌：{self.data.id2name(self.hot_tile)}')
            # self.speaker += 3  # 下家接手
            #
            # i = self.dark_cards.index(self.hot_tile)
            # self.dark_cards.pop(i)  # 变成明牌

            return True  # 重新选择了发牌者

        return False  # 轮流完了，还是没有碰掉，则继续吃的判断

    # 吃
    def chow(self):
        """
            左边是上家，坐你右边的是下家，坐你对面的是对家
            只能吃上家的牌
            :return:
        """
        if self.hot_tile[0] > 0x30:  # 字牌、花牌不能吃
            return False

        # return False

        speaker = (self.speaker + 1) % 4  # 左手上家 已经移动过了
        # speaker = (self.speaker + 3) % 4  # 右手下家可以吃热牌
        cards = self.card_players[self.speaker]
        # print('吃牌判断', self.player_names[speaker], self.player_names[self.speaker])
        cbd_list = []  # 手牌里与热牌同类型的所有牌
        sequences = []  # 顺子集合        一组 Meld 	一个顺子、刻子或杠子

        rank = self.data.suit_rank(self.hot_tile[0])  # 牌面的大小 一~九
        color = self.data.suit_color(self.hot_tile[0])  # 花色(配牌) 筒、条、万
        # print(rank, '%#x' % color, '%#x' % self.hot_card, self.data.id2name(self.hot_card))
        # self.data.cards2names(cards)

        for each in cards:
            if color == self.data.suit_color(each[0]):
                cbd_list.append(each[0])

        size = len(cbd_list)
        # self.data.cards2names(cbd_list)

        if size >= 2:
            for i in range(0, size - 1):
                if self.data.suit_rank(cbd_list[i]) == rank - 2 and self.data.suit_rank(cbd_list[i + 1]) == rank - 1:
                    sequences.append([cbd_list[i], cbd_list[i + 1], self.hot_tile[0]])
                if self.data.suit_rank(cbd_list[i]) == rank - 1 and self.data.suit_rank(cbd_list[i + 1]) == rank + 1:
                    sequences.append([cbd_list[i], self.hot_tile[0], cbd_list[i + 1]])
                if self.data.suit_rank(cbd_list[i]) == rank + 1 and self.data.suit_rank(cbd_list[i + 1]) == rank + 2:
                    sequences.append([self.hot_tile[0], cbd_list[i], cbd_list[i + 1]])

        # 假设吃B，已有ABC
        if size >= 3:
            for i in range(1, size - 1):
                if self.data.suit_rank(cbd_list[i - 1]) == rank - 1 and \
                        self.data.suit_rank(cbd_list[i]) == rank and \
                        self.data.suit_rank(cbd_list[i + 1]) == rank + 1:
                    sequences.append([cbd_list[i - 1], self.hot_tile[0], cbd_list[i + 1]])

        # 假设吃B，已有ABBC
        if size >= 4:
            for i in range(1, size - 2):
                if self.data.suit_rank(cbd_list[i - 1]) == rank - 1 and \
                        self.data.suit_rank(cbd_list[i]) == rank and \
                        self.data.suit_rank(cbd_list[i + 2]) == rank + 1:
                    sequences.append([cbd_list[i - 1], self.hot_tile[0], cbd_list[i + 1]])

        # 假设吃B，已有ABBBC
        if size >= 5:
            for i in range(1, size - 3):
                if self.data.suit_rank(cbd_list[i - 1]) == rank - 1 and \
                        self.data.suit_rank(cbd_list[i]) == rank and \
                        self.data.suit_rank(cbd_list[i + 3]) == rank + 1:
                    sequences.append([cbd_list[i - 1], self.hot_tile[0], cbd_list[i + 1]])

        # 假设吃B，已有ABBBBC
        if size >= 6:
            for i in range(1, size - 4):
                if self.data.suit_rank(cbd_list[i - 1]) == rank - 1 and \
                        self.data.suit_rank(cbd_list[i]) == rank and \
                        self.data.suit_rank(cbd_list[i + 4]) == rank + 1:
                    sequences.append([cbd_list[i], self.hot_tile[0], cbd_list[i + 1]])

        if len(sequences) > 0:
            print(f"\033[0m{self.player_names[self.speaker]}\033[0m \033[1;36m吃\033[1;36m "
                  f"\033[0m{self.player_names[speaker]} 的 \033[0m"
                  f"\033[5;32m{self.data.id2name(self.hot_tile[0])}\033[5;32m \033[0m!\033[0m")
            # print('所有顺子：', len(sequences), sequences)
            # for each in sequences:
            #     self.data.cards2names(each)有问题，没有状态参数

            self.hot_tile[1] = 5
            cards.append(self.hot_tile)  # 加入热牌，且排序
            cards.sort()
            self._hot_update(cards)

            return True

        return False

    def clear_round(self):
        self.round.clear()
        self.hot_tile = [0, 0]
        self.lots = 0
        self.speaker = 1
        self.card_players = [[[0, 0]] * 13 for i in range(4)]

    # # 开启打牌的各种线程了
    # def startover(self):
    #     self.event_can_draw.set()
    #     self.event_discarded.clear()
    #     drawing = threading.Thread(target=self.draw, )  # 进程1，等待进程2完成
    #     drawing.start()
    #
    #     checking = threading.Thread(target=self.Win_Pung_Kong_Chow, )  #
    #     checking.start()
    #
    # # 本家出牌
    # def discard(self, tile):
    #     if not tile or not self.can_discard:
    #         print(str(sys._getframe().f_lineno), "discard error")
    #         return
    #     # print(tile)
    #     ID_src, index_src = tile.ID, tile.index
    #
    #     if index_src < 13:  # 叫牌摸到即扔，不插入排序
    #         hot_ID = self.card_players[1][13].ID  # 叫牌的
    #         # tile.resurfacing(hot_ID)
    #         self.swap_tiles(tile, self.tile_shadow)  # 先把影子牌置换掉,影子代替叫牌，不影响热牌
    #         # 再重新排序
    #         if tile.ID == hot_ID:
    #             pass
    #         elif tile.ID > hot_ID:  # 左边插入
    #             if index_src == 0:  # 边缘的直接替换
    #                 pass
    #             else:
    #                 for i in range(index_src, 0, -1):
    #                     if self.card_players[1][i].ID < self.card_players[1][i - 1].ID:
    #                         self.swap_tiles(self.card_players[1][i], self.card_players[1][i - 1])
    #                     else:
    #                         break
    #         else:  # 右边插入
    #             if index_src == 12:  # 边缘的直接替换
    #                 pass
    #             else:
    #                 for i in range(index_src, 12):
    #                     if self.card_players[1][i].ID > self.card_players[1][i + 1].ID:
    #                         self.swap_tiles(self.card_players[1][i], self.card_players[1][i + 1])
    #                     else:  # 就地扎根
    #                         break
    #
    #     self.tile_shadow.setVisible(False)  # 藏影子
    #     self.card_players[1][13].setVisible(True)  # 现真身 亮牌即出牌
    #     self.can_discard = False  # 不能再出牌了
    #
    #     self.event_discarded.set()  # 叫醒点炮检测程序
    #
    # # 凑牌成组 把各家牌整成顺子、刻子或杠子
    # def collect_melds(self):
    #     pass
    #
    # # 上家叫牌后, 胡？碰？杠？吃？
    # def Win_Pung_Kong_Chow(self):
    #     """
    #     这里要找到上家出的叫牌，然后逐一经过算法处理，杠、碰、吃、胡等
    #     :return:
    #     """
    #
    #     while True:
    #         if self.lots >= self.tiles_count or self.isWin:  # 荒牌或胡牌
    #             break
    #
    #         if not self.event_discarded.is_set():
    #             self.event_discarded.wait()
    #         else:
    #             # 先轮流看另外3家要不要这张牌
    #             print(self.lots, 'lots')
    #             # discarder = (self.dealer - self.lots) % 4  # 即将出牌者  负数取模也正好符合 逆时针转
    #             left_speaker = (self.speaker + 1) % 4  # 上家 opponent on the left  顺时针前进一位
    #             hot = self.card_players[left_speaker][13]  # 上家的出牌
    #             print(f'现在轮到{self.players[self.speaker]}({self.speaker})摸牌。'
    #                   f'上家{self.players[left_speaker]}({left_speaker})出牌:{DataMj.get_name_pic(hot.ID)[0]}')
    #
    #             hot.setVisible(False)  # 隐藏上家的叫牌
    #
    #             if self.Win(hot.ID):  # 胡？
    #                 # 结束
    #                 # self.begin = False
    #                 self.isWin = True
    #                 self.event_can_draw.clear()
    #                 self.event_discarded.clear()
    #
    #             ret = self.Pung(hot.ID)
    #             if ret[0]:  # 碰？
    #                 # 明牌，并接着发牌
    #                 self.speaker = ret[1]
    #             else:
    #                 ret = self.Kong(hot.ID)
    #                 if ret[0]:  # 杠？
    #                     self.speaker = ret[1]
    #                 else:
    #                     ret = self.Kong(hot.ID)
    #                     if ret[0]:  # 吃？
    #                         self.speaker = ret[1]
    #                     else:  # 都不要则是废牌，扔到地上
    #                         # self.killer(hot.ID, self.speaker + 12)
    #                         # print('hhhh')
    #                         self.speaker = (self.speaker + 3) % 4  # 该下一家出牌了
    #
    #                         self.event_can_draw.set()  # 设置摸牌信号
    #                         self.event_discarded.clear()  # 清除已出牌信号
    #
    #             # time.sleep(1)  # 每秒扫描一次
    #             # 检测天胡的存在
    #             # self.can_discard = True  # 14张，可以出牌了

    # 显示所有玩家的牌面
    # def show_cards(self):
    #     for i in range(13):
    #         tile = self.card_players[0][i]
    #         if tile:
    #             tile.setVisible(True)
    #             tile.move(self.x() + self.width() - 100, self.margin + 160 + i * 40)
    #             # tile.setGeometry(, self.margin + 40 + i * 40, tile.width(), tile.height())
    #
    #         tile = self.card_players[1][i]
    #         if tile:
    #             tile.setVisible(True)
    #             tile.move(90 + self.margin + i * Tile.g_W, self.height() - 30 - Tile.g_H - self.margin)
    #
    #         tile = self.card_players[2][i]
    #         if tile:
    #             tile.setVisible(True)
    #             tile.move(self.x() + 70, self.margin + 160 + i * 40)
    #             # tile.setGeometry(self.x() + 70, self.margin + 160 + i * 40, tile.width(), tile.height())
    #
    #         tile = self.card_players[3][i]
    #         if tile:
    #             tile.setVisible(True)
    #             tile.move(180 + self.margin + i * 62, 30)
    #
    #     # 设置各家热牌的位置和形状。
    #     hot = self.card_players[0][13]
    #     # hot.setVisible(True)
    #     # hot.move(940, 160)
    #     hot.move(self.x() + self.width() - 200, self.margin + 160)
    #
    #     hot = self.card_players[1][13]
    #     # hot.setVisible(True)
    #     # hot.move(self.x()+self.width() -140, 580)
    #     hot.move(90 + self.margin + 13 * Tile.g_W, self.height() - 140 - Tile.g_H - self.margin)
    #
    #     hot = self.card_players[2][13]
    #     # hot.setVisible(True)
    #     hot.move(self.x() + 120, self.margin + 130 + 13 * 40)
    #
    #     hot = self.card_players[3][13]
    #     # hot.setVisible(True)
    #     hot.move(180 + self.margin, 125)
    #
    #     # self.card_scrap.setVisible(True)
    #     self.tile_shadow.move(115 + self.margin + 13 * Tile.g_W, self.height() - 30 - Tile.g_H - self.margin)
    #
    # # 废牌到地上
    # def killer(self, ID, kind):
    #     tile = Tile(self, ID, kind, 13)
    #     if self.speaker == 0:  # 东方
    #         pass
    #     elif self.speaker == 1:  # 南方
    #         # num = (self.lots - 53) // 4  # 出牌的第几圈，等于打出牌的数量轮回
    #         num = (self.lots - 53)  # 出牌的第几圈，等于打出牌的数量轮回 这不准确
    #         x, y = num % 8, num // 8
    #         # 移到出牌区
    #         tile.setGeometry(380 + x * tile.width(), 450 + y * (tile.height() - 13), tile.width(),
    #                          tile.height())
    #         tile.setVisible(True)
    #     # else:
    #     #     self.can_discard = True
    #
    # # 打印牌面
    # def print_card(self, player_ID):
    #     if self.card_players[player_ID]:
    #         temp = []
    #         temp1 = []
    #         for each in self.card_players[player_ID]:
    #             if DataMj.is_valid(each.ID):
    #                 temp.append(DataMj.g_tiles_name[DataMj.value2index(each.ID)])
    #                 temp1.append(each.index)
    #         print(temp)
    #         print(temp1)
    #
    # def swap_tiles(self, tile_src, tile_dst):
    #     if not tile_dst or not tile_src:
    #         return
    #
    #     # 先换槽位
    #     self.card_players[1][tile_src.index], self.card_players[1][tile_dst.index] = \
    #         self.card_players[1][tile_dst.index], self.card_players[1][tile_src.index]
    #
    #     # 再换牌卡
    #     tile_src.index, tile_dst.index = tile_dst.index, tile_src.index
    #     sx, sy = tile_src.x(), tile_src.y()
    #     tile_src.move(tile_dst.x(), tile_dst.y())
    #     tile_dst.move(sx, sy)

    @staticmethod
    def write_log(content, colour='white', skip=False):
        """
        写入日志文件
        :param content: 写入内容
        :param colour: 颜色
        :param skip: 是否跳过打印时间
        :return:
        """
        # 颜色代码
        colour_dict = {
            'red': 31,  # 红色
            'green': 32,  # 绿色
            'yellow': 33,  # 黄色
            'blue': 34,  # 蓝色
            'purple_red': 35,  # 紫红色
            'bluish_blue': 36,  # 浅蓝色
            'white': 37,  # 白色
        }
        choice = colour_dict.get(colour)  # 选择颜色

        path = os.path.join(MjData.BASE_DIR, "/res/output_1.log")  # 日志文件
        print(MjData.BASE_DIR, path)
        with open(path, mode='a+', encoding='utf-8') as f:
            if skip is False:  # 不跳过打印时间时
                content = time.strftime('%Y-%m-%d %H:%M:%S') + ' ' + content

            info = "\033[1;{};1m{}\033[0m".format(choice, content)
            print(info)
            f.write(content + "\n")


def main():
    # mj = MjData()
    # mj.test()

    mahing = Mahjong()
    mahing.shuffling()
    mahing.deal()
    mahing.playing()

    # cards = [0x01, 0x01, 0x24, 0x23, 0x22, 0x2, 0x3, 0x04, 0x33, 0x33, 0x33, 0x17, 0x19, 0x18]
    # names = ['一饼', '二饼', '三万', '三万', '四万', '四万', '四条', '五条', '六条', '七条', '七条', '八条', '八条']
    # mahing.hot_card = DataMj.name2id('三条')
    # print(mahing.hot_card, DataMj.id2name(mahing.hot_card))
    #
    # cards = DataMj.creat_cards_by_names(names)
    # cards.sort()
    # DataMj.print_list_names(cards)
    # mahing.chow(cards)
    #
    # mahing.cards_score(cards, True)
    # print(mahing.match(cards))

    # i = DataMj.g_tile_ids[9]
    # print(type(i), sys.getsizeof(i))


if __name__ == '__main__':
    main()
