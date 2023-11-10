#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from Wx.base.basedef import BaseDef


class Responsive(BaseDef):
    input_tap = "/view[1]/input"

    def input_tap_and_fill(self):
        self.send_key(self.input_tap, "www.baidu.com")
        # enter -》 回车
        self.get_element(self.input_tap).trigger("confirm",{"value":"cake"})
