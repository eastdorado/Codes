#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Product: PyCharm
# @Project: python
# @File    : realRandom.py
# @Author  : big
# @Email   : shdorado@126.com
# @Time    : 2020/6/25 14:25
# 功能：随机数产生


import time
import numpy as np
import random
import string
import uuid


# def random_cpu(accuracy=5):
#     time_list = []
#     for i in range(accuracy + 10):
#         start = time.time()
#         for j in range(100):
#             print('')
#         time_list.append(time.time() - start)
#     accuracy_list = []
#     for accuracy_one in range(accuracy):
#         accuracy_list.append(2 ** accuracy_one)
#         # accuracy_list.append(2 << accuracy_one)  # A << B = A * (2 ** B)
#     print(time_list)
#
#     cpu_interval_bool_list = (np.array(time_list) / (sum(time_list) / (accuracy + 10))) > 1
#     print(cpu_interval_bool_list)
#     print(np.array(accuracy_list))
#     return 1 / sum(np.array(accuracy_list) * cpu_interval_bool_list[5:-5])
#
#
# def random_gen():
#     num_num = 10
#     n_list = []
#     while True:
#
#         random_cp = round(random_cpu(accuracy=15) * 2 ** 15)
#         if 0 < random_cp <= 10:
#             if random_cp not in n_list:
#
#                 n_list.append(random_cp)
#                 if len(n_list) >= 10:
#                     return n_list
#
#
# def generate_code(self):
#     code_finall = 0
#     for one_num in self.random_gen():
#         code_finall += one_num * 10 ** self.random_gen().index(one_num)
#
#     return code_finall


# def generate_int(num_min, num_max):
#     seed = time.time()
#     sr = random.SystemRandom(seed)
#     # print(type(sr))
#
#     ret = sr.randint(num_min, num_max)
#     # print(ret)
#
#     return ret


def generate_float(num_min, num_max, n=2):
    # 小数位数
    seed = time.time()
    sr = random.SystemRandom(seed)
    # print(type(sr))

    ret = sr.uniform(num_min, num_max)
    # ret = sr.random()

    ret = round(ret, n)  # n位小数，碰到.5，前一位小数是奇数，则直接舍弃，如果偶数则向上取舍
    # print('{:04.2f}'.format(sr.random()))

    return ret


# 生成随机字符串 密码学意义上更加安全的版本
def generate_str1(size=10):
    char_set = string.ascii_uppercase + string.ascii_lowercase + string.digits
    # print(char_set)  # 将大/小写的ASCII字符列表和数字组合起来

    seed = time.time()
    sr = random.SystemRandom(seed)
    # print(type(sr))

    random_string = ''.join(sr.choice(char_set) for _ in range(size))

    # 首字母不能是数字
    random_string = generate_str1(size) if random_string[0].isdigit() else random_string
    print(random_string)

    return random_string


# 使用Python内置的uuid库 生成随机字符串
def generate_str2(size=10):
    random_string = str(uuid.uuid4()).replace("-", "")  # Remove the UUID '-'
    size = len(random_string) if size > len(random_string) else size
    random_string = random_string[0:size]
    print(type(random_string))

    # 首字母不能是数字
    random_string = generate_str2(size) if random_string[0].isdigit() else random_string
    print(random_string)

    return random_string


def main():
    # generate_str2()
    generate_int(0, 1)
    # generate_float(0, 10)
    # print(random_cpu())
    # for i in range(10):
    #     print(random_gen())

    # seed = time.time()
    # r1 = random.SystemRandom(seed)
    # r2 = random.SystemRandom(seed)
    # print(seed)
    # for i in range(3):
    #     print('{} {}'.format(r1.randint(0, 100), r2.random()))
    #     # print('{:04.2f} {:04.3f}'.format(r1.random(), r2.random()))


if __name__ == '__main__':
    main()
