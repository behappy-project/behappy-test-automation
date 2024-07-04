#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/6/25
# @File    : __init__.py.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from pathlib import Path

import minium


class BaseCase(minium.MiniTest):
    """
    小程序测试用例基类
    """

    @classmethod
    def setUpClass(cls):
        super(BaseCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(BaseCase, cls).tearDownClass()

    def setUp(self):
        super(BaseCase, self).setUp()

    def tearDown(self):
        super(BaseCase, self).tearDown()
