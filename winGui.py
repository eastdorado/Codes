#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @项目名称: python
# @File    : winGui.py
# @Time    : 2020/3/6 21:47
# @Author  : big
# @Email   : shdorado@126.com

import sys
import wx


class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(600, 400))

        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        self.Show(True)


app = wx.App(False)
frame = MyFrame(None, 'Small editor')
app.MainLoop()