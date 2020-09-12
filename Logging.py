#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Project : Puck
#  File    : Logging
#  Date    : 2020/9/12 11:49
#  Site    : https://github.com/eastdorado
#  Author  : By cyh
#            QQ: 260125177
#            Email: 260125177@qq.com 
#  Copyright = Copyright (c) 2020 CYH
#  Version   = 1.0

import inspect
import logging
import logging.handlers
import os
import time
import datetime
import sys
import getpass


class LogConfig:
    def __init__(self, log_level=logging.INFO):
        if __name__ != "__main__":
            self.logger = self.get_file_logger(log_level=log_level)
        pass

    def get_console_logger(self):
        def _gen_file_logger_handler():
            _handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "[%(asctime)s %(msecs)03d][%(process)d][tid=%(thread)d][%(name)s]"
                "[%(levelname)s] %(message)s [%(filename)s"
                " %(funcName)s %(lineno)s] ", datefmt="%Y-%m-%d %H:%M:%S")
            _handler.setLevel(logging.INFO)
            _handler.setFormatter(formatter)
            return _handler

        def _gen_console_logger():
            _console_logger = logging.getLogger("console_logger")
            _console_logger.addHandler(handler)
            return _console_logger

        handler = _gen_file_logger_handler()
        console_logger = _gen_console_logger()
        return console_logger

    # 允许同时存在不同的logger，即可以传入不同log_file_name实例化不同logger即可实现不同类型日志写入不同文件
    # logger自带了线程锁，是线程安全的，所以多线程不用自己实现日志文件锁
    def get_file_logger(self, logger_name=None, log_file_name=None, log_level=logging.INFO):
        def _get_log_file_name():
            # 如果已定义有日志文件则直接原样返回
            if log_file_name:
                return log_file_name
            # 如果是直接运行的，那取当前文件名
            if __name__ == "__main__":
                caller_file_name = __file__
            # 如果是被调用的，则取上层调用文件文件名
            else:
                frame = inspect.stack()[3]
                module = inspect.getmodule(frame[0])
                caller_file_name = module.__file__
            inner_log_file_name = f"{os.path.basename(caller_file_name)[:-3]}.log"
            return inner_log_file_name

        def _make_sure_log_dir_exist():
            if not os.path.isdir(log_file_dir):
                os.mkdir(log_file_dir)

        def _gen_file_logger_handler():
            # 操作系统本身不允许文件名包含:等特殊字符，所以这里也不要用，不然赋给filename时会报错
            # nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
            file_path = f'{log_file_dir}/{log_file_name}'
            # formatter = logging.Formatter(
            #     "[%(asctime)s %(msecs)03d][%(process)d][tid=%(thread)d][%(name)s]
            #     [%(levelname)s] %(message)s [%(filename)s"
            #     " %(funcName)s %(lineno)s] ", datefmt="%Y-%m-%d %H:%M:%S")
            formatter = logging.Formatter(
                "%(asctime)s %(msecs)03d - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
            # filename----日志文件
            # when----更换日志文件的时间单位
            # interval----更换日志文件的时间单位个数；这里是7天换一个文件
            # backupCount----保存的旧日志文件个数；这里即只保留上一个日志文件
            # encoding----日志文件编码
            # 实际使用感觉，如果程序是crontab这样定时运行而不是一直运行着，那这个按时间滚动并不生效
            # _handler = logging.handlers.TimedRotatingFileHandler(
            #     filename=file_path,
            #     when='D',
            #     interval=7,
            #     backupCount=1,
            #     encoding='utf-8',
            # )
            # filename--日志文件
            # mode--日志文件打开模式
            # maxBytes--日志文件最大大小。每次调用打印日志时logging去检测日志大小是否达到设定的上限，如果达到则更换日志文件
            # backupCount--保存的旧日志文件个数。xxx表示当前日志文件，则xxx.1表示上一份日志文件、xxx.2表示上上份日志文件...
            # encoding----日志文件编码
            _handler = logging.handlers.RotatingFileHandler(
                filename=file_path,
                mode='a',
                maxBytes=1024 * 1024 * 100,
                backupCount=1,
                encoding='utf-8',
            )
            # 实际发现这里setLevel并不起作用
            # _handler.setLevel(logging.DEBUG)
            _handler.setFormatter(formatter)
            return _handler

        def _gen_file_logger():
            # 如果指定了logger_name那直接采用，如果没有使用日志文件名为logger_name
            nonlocal logger_name
            if not logger_name:
                logger_name = log_file_name
            _file_logger = logging.getLogger(logger_name)
            _file_logger.addHandler(handler)
            _file_logger.setLevel(log_level)
            return _file_logger

        log_file_name = _get_log_file_name()
        log_file_dir = r"E:\Codes\Logs"
        _make_sure_log_dir_exist()
        handler = _gen_file_logger_handler()
        file_logger = _gen_file_logger()

        return file_logger


class logs(object):
    def __init__(self):
        self.logger = logging.getLogger("")
        # 设置输出的等级
        LEVELS = {'NOSET': logging.NOTSET,
                  'DEBUG': logging.DEBUG,
                  'INFO': logging.INFO,
                  'WARNING': logging.WARNING,
                  'ERROR': logging.ERROR,
                  'CRITICAL': logging.CRITICAL}
        # 创建文件目录
        logs_dir = "logs2"
        if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
            pass
        else:
            os.mkdir(logs_dir)
        # 修改log保存位置
        timestamp = time.strftime("%Y-%m-%d", time.localtime())
        logfilename = '%s.txt' % timestamp
        logfilepath = os.path.join(logs_dir, logfilename)
        rotatingFileHandler = logging.handlers.RotatingFileHandler(filename=logfilepath,
                                                                   maxBytes=1024 * 1024 * 50,
                                                                   backupCount=5)
        # 设置输出格式
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        rotatingFileHandler.setFormatter(formatter)
        # 控制台句柄
        console = logging.StreamHandler()
        console.setLevel(logging.NOTSET)
        console.setFormatter(formatter)
        # 添加内容到日志句柄中
        self.logger.addHandler(rotatingFileHandler)
        self.logger.addHandler(console)
        self.logger.setLevel(logging.NOTSET)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)


class Mylog(object):
    # 根文件夹
    root_dir = sys.path[0]
    # 根目录
    root_path = sys.path[0] + os.path.sep
    # 系统目录分割线
    sys_sep = os.path.sep
    # 配置
    option = {
        'level': 0,  # 日志级别：  0：全部，1：调试，2：警告，3：错误 NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL
        'is_open': True,  # 是否开启，如果关闭则不输出也不记录日志
        'is_print': True,  # 是否print输出
        'is_write': True,  # 是否记录到日志文件
        'is_prefix': True,  # 是否在每条日志内容前面加前缀
        'level_1_prefix': 'Test: ',  # 如果开启了每条日志前加前缀，设置日志级别为1的前缀
        'level_2_prefix': 'Warning: ',  # 如果开启了每条日志前加前缀，设置日志级别为2的前缀
        'level_3_prefix': 'Error: ',  # 如果开启了每条日志前加前缀，设置日志级别为3的前缀
        'root_dir_name': 'mylog',  # 存放日志文件的根文件夹名称
        'dir_name': ''  # 自定义存放日志文件的文件名称，此文件夹是在 root_dir_name 文件夹下
    }

    def __init__(self, config=None):
        if config is not None:
            self.option.update(dict(config))

        # 日志保存的文件夹（全路径）
        save_dir = self.root_path + self.option['root_dir_name']

        # 创建文件夹
        if os.path.isdir(save_dir) is not True:
            os.mkdir(save_dir)
        if len(self.option['dir_name']) > 0:
            save_dir += self.sys_sep + self.option['dir_name']
            if os.path.isdir(save_dir) is not True:
                os.mkdir(save_dir)

        self.save_dir = save_dir
        self.save_path = save_dir + self.sys_sep

    '''
    输入日志／记录日志
    '''

    def log(self, content='', level=0):
        self._print_log(content, level)
        self._write_log(content, level)

    '''
    输入日志
    '''

    def _print_log(self, content, level):
        if self.option['is_open'] is True and self.option['is_print'] is True:
            if self.option['level'] == 0 or self.option['level'] == level:
                if level > 0:
                    content = self.option['level_' + str(level) + '_prefix'] + content
                print(content)

    '''
    记录日志
    '''

    def _write_log(self, content, level):
        if self.option['is_open'] is True and self.option['is_print'] is True:
            if self.option['level'] == 0 or self.option['level'] == level:
                if self.option['is_prefix'] is True:
                    today = datetime.date.today()
                    file_name = str(today) + '.log'
                    now = time.strftime("%H:%M:%S")
                    log_file = self.save_path + file_name
                    if level > 0:
                        content = self.option['level_' + str(level) + '_prefix'] + content
                    if os.path.isfile(log_file):
                        save_file = open(log_file, 'a')
                    else:
                        save_file = open(log_file, 'w')
                    save_file.write(str(now) + "\r\n" + content + "\r\n")
                    save_file.close()


# 定义MyLog类
class MyLog1(object):
    '''这个类用于创建一个自用的log'''

    def __init__(self):  # 类MyLog的构造函数
        user = getpass.getuser()  # 返回用户的登录名
        self.logger = logging.getLogger(user)  # 返回一个特定名字的日志
        self.logger.setLevel(logging.DEBUG)  # 对显示的日志信息设置一个阈值低于DEBUG级别的不显示
        logFile = './' + sys.argv[1][0:-3] + '.log'  # 日志文件名
        formatter = logging.Formatter('%(asctime)-12s $(levelname)-8s %(name)-10s %(message)-12s')

        '''日志显示到屏幕上并输出到日志文件内'''
        logHand = logging.FileHandler(logFile)  # 输出日志文件，文件名是logFile
        logHand.setFormatter(formatter)  # 为logHand以formatter设置格式
        logHand.setLevel(logging.ERROR)  # 只有错误才被记录到logfile中

        logHandSt = logging.StreamHandler()  # class logging.StreamHandler(stream=None)
        # 返回StreamHandler类的实例，如果stream被确定，使用该stream作为日志输出，反之，使用
        # sys.stderr
        logHandSt.setFormatter(formatter)  # 为logHandSt以formatter设置格式

        self.logger.addHandler(logHand)  # 添加特定的handler logHand到日志文件logger中
        self.logger.addHandler(logHandSt)  # 添加特定的handler logHandSt到日志文件logger中

        '''日志的5个级别对应以下的五个函数'''

    def debug(self, msg):
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(msg)  # 避免msg里有调用函数，可能额外增加计数器了，造成混乱
        # self.logger.debug(msg)  # Logs a message with level DEBUG on this logger.
        # The msg is the message format string

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warn(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


# 把日志输出到控制台， 还要写入日志文件
class Logger:
    # 性能开关，为提升性能可以关闭这些
    # logging._srcfile = None   模块、程序之类的开关
    logging.logThreads = 0
    logging.logMultiprocessing = 0
    logging.logProcesses = 0
    logging.thread = None  # 程序是单进程时可以关闭

    path = "E:/Codes/Logs"

    # 设置输出的等级
    LEVELS = {'NOTSET': logging.NOTSET,
              'DEBUG': logging.DEBUG,
              'INFO': logging.INFO,
              'WARNING': logging.WARNING,
              'ERROR': logging.ERROR,
              'CRITICAL': logging.CRITICAL}

    # 用字典保存日志输出格式
    format_dict = {0: logging.Formatter('%(message)s'),
                   1: logging.Formatter('%(name)s - %(message)s'),
                   2: logging.Formatter('%(filename)s - %(module)s - %(lineno)d - %(levelname)s - %(message)s'),
                   3: logging.Formatter('%(thread)d - %(threadName)s - %(process)d - %(message)s'),
                   4: logging.Formatter('%(funcName)s - %(created)f - %(levelname)s - %(message)s'),
                   5: logging.Formatter('%(pathname)s - %(levelno)s - %(levelname)s - %(message)s'),
                   6: logging.Formatter('%(asctime)s - %(msecs)d - %(relativeCreated)d - %(levelname)s - %(message)s')}

    def __init__(self, log_file, log_tags='', log_level='DEBUG', log_format=0):
        """
            指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        """
        # 创建一个logger
        self.logger = logging.getLogger(log_tags)
        self.logger.setLevel(self.LEVELS[log_level])

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(f'{self.path}/{log_file}', mode='w')  # 覆盖
        fh.setLevel(self.LEVELS[log_level])

        # 再创建一个handler，用于输出到控制台
        # ch = logging.StreamHandler()
        # ch.setLevel(self.LEVELS[log_level])

        # 定义handler的输出格式
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = self.format_dict[int(log_format)]
        fh.setFormatter(formatter)
        # ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        # self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger

    def debug(self, msg):
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(msg)  # 避免msg里有调用函数，可能额外增加计数器了，造成混乱
            # self.logger.debug(msg)  # Logs a message with level DEBUG on this logger.
            # The msg is the message format string

    def info(self, msg):
        if self.logger.isEnabledFor(logging.DEBUG):
            # 避免msg里有调用函数，可能额外增加计数器了，造成混乱
            self.logger.info(msg)

    def warning(self, msg):
        if self.logger.isEnabledFor(logging.WARNING):
            # 避免msg里有调用函数，可能额外增加计数器了，造成混乱
            self.logger.warning(msg)

    def error(self, msg):
        if self.logger.isEnabledFor(logging.ERROR):
            # 避免msg里有调用函数，可能额外增加计数器了，造成混乱
            self.logger.error(msg)

    def critical(self, msg):
        if self.logger.isEnabledFor(logging.CRITICAL):
            # 避免msg里有调用函数，可能额外增加计数器了，造成混乱
            self.logger.critical(msg)

    # 再通过以下方式调用，便是一个简单的日志系统了
    # logger = Logger(log_file='log.txt', log_tags="fox", log_level='DEBUG', log_format=1).get_logger()
    # logger = Logger(log_file='log.txt', log_tags="fox", log_level='DEBUG', log_format=1)


def main():
    # logger = LogConfig().get_console_logger()
    # log_file_name不同，返回的是不同的logger，这样就可以方便地定义多个logger
    logger = LogConfig().get_file_logger('test', 'test.log')
    logger.debug('print by debug')
    logger.info('print by info')
    logger.warning('print by warning')


if __name__ == '__main__':
    main()
    log = Logger(log_file='test.log', log_tags="fox", log_level='DEBUG', log_format=2)
    log.debug('dgdsg')
    log.info('dgdsg')
    log.warning('dgdsg')
