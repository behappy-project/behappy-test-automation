#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @File    : step_wx_serach.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from Common.Wx.basedef import BaseDef

from PageLocators.wx_page_locator import WxPageLocator as Wx

class WxPage(BaseDef):

    def input_tap_and_fill(self):
        self.send_key(Wx.input_tap, "www.baidu.com")
        # enter -》 回车
        self.get_element(Wx.input_tap).trigger("confirm",{"value":"cake"})

