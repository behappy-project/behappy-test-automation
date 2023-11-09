#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from .basedef import *


class BasePage(minium.MiniTest):
    """测试用例基类"""

    @classmethod
    def tearDownClass(cls):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass
