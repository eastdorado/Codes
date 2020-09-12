#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @项目名称: games
# @File    : test.py
# @Time    : 2020/1/19 16:05
# @Author  : big
# @Email   : shdorado@126.com

class test:
    def consumer(self):  # 1
        r = ''  # 2
        while True:  # 3
            n = yield r  # 4
            if not n:  # 5
                return  # 6
            print('[CONSUMER] Consuming %s...' % n)  # 7
            r = '200 OK'  # 8
            # 9
            # 10

    def produce(self, c):  # 11
        c.send(None)  # 12
        n = 0  # 13
        while n < 5:  # 14
            n = n + 1  # 15
            print('[PRODUCER] Producing %s...' % n)  # 16
            r = c.send(n)  # 17
            # next(c)
            print('[PRODUCER] Consumer return: %s' % r)  # 18
        c.close()  # 19


if __name__ == "__main__":
    t = test()
    c = t.consumer()
    t.produce(c)
    # c = consumer()  # 1、定义生成器，consumer并不执行
    # produce(c)  # 2、运行produce函数
