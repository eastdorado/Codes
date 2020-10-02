#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Project : Puck
#  File    : CallDll
#  Date    : 2020/9/28 18:16
#  Site    : https://github.com/eastdorado
#  Author  : By cyh
#            QQ: 260125177
#            Email: 260125177@qq.com 
#  Copyright = Copyright (c) 2020 CYH
#  Version   = 1.0

# import sys
import os
import ctypes
from ctypes.wintypes import HWND, DWORD
from utilities import MyLog


class CallDll:
    _DLL = None
    log = MyLog()

    def __init__(self, win_dll=None):
        # os.add_dll_directory(r"E:\Codes\res\dll")
        # self.log.debug(win_dll)
        if win_dll:
            self.load_dll(win_dll)

    @staticmethod
    def load_dll(win_dll=None):
        try:
            # # dll 是 __stdcall 格式的调用时
            # CallDll._DLL = ctypes.windll.LoadLibrary(win_dll)
            # CallDll._DLL = ctypes.WinDLL(win_dll)

            # # dll 是 __cdecl 格式的调用时：
            CallDll._DLL = ctypes.cdll.LoadLibrary(win_dll)
            # CallDll._DLL = ctypes.CDLL(win_dll)

            CallDll.log.debug(type(CallDll._DLL))

        except Exception as e:
            CallDll.log.debug('dll需要64位的 但是你的这个文件是32位', e)
        finally:
            return CallDll._DLL

    @staticmethod
    def call_dll(win):
        # 调用 api
        hWnd = HWND(int(win.winId()))  # 直接HWND(self.winId())会报错
        gradientColor = DWORD(0x50F2F2F2)  # 设置和亚克力效果相叠加的背景颜色

        CallDll._DLL.setBlur(hWnd, gradientColor)
        # dll.setBlur(hWnd, gradientColor)


def main():
    caller = CallDll()
    caller.load_dll(r'C:\Windows\pyshellext.amd64.dll')


if __name__ == '__main__':
    main()
