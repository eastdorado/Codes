#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Project: PyCharm
# @File    : test2.py
# @Author  : tiger
# @Email   : shdorado@126.com
# @Time    : 2020/5/27 15:06

import threading, time

event = threading.Event()


def lighter():
    """0<count<5为绿灯，5<count<10为红灯，count>10重置标志位 """
    event.set()  #
    count = 0
    while True:
        if 5 < count < 10:
            event.clear()
            print("\033[1;41m red light is on \033[0m")
        elif count > 10:
            event.set()
            count = 0
        else:
            print("\033[1;42m darkgreen light is on \033[0m")
        time.sleep(1)
        count += 1


def car(name):
    """红灯停，绿灯行"""
    while True:
        if event.is_set():
            print("[%s] is running..." % name)
            time.sleep(0.25)
        else:
            print("[%s] sees red light,need to wait three seconds" % name)
            event.wait()
            print("\033[1;34;40m green light is on,[%s]start going \033[0m" % name)


light = threading.Thread(target=lighter, )
light.start()

car1 = threading.Thread(target=car, args=("Xiaoxiong",))
car1.start()
