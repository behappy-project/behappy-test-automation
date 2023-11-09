#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/11/7
# @File    : first_test.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import sys

import minium

sys.path.append("..")
from Wx.pages.pages.responsive.responsive import Responsive


class FirstTest(minium.MiniTest):
    """
    测试
    """

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.Responsive = Responsive(self)

    def test_get_system_info(self):
        sys_info = self.mini.get_system_info()
        self.logger.info(f'SDKVersion is: {sys_info.get("SDKVersion")}')  # 可以使用self.logger打印一些log
        self.assertIn("SDKVersion", sys_info)

    def test_create_qr_code(self):
        """
        创建二维码
        :return:
        """
        self.Responsive.input_tap_and_fill()
