#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @File    : step_baidu_serach.py.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from time import sleep

import pytest

from Common.basepage import BasePage
from PageLocators.baidu_page_locator import BaiduPageLocator as BD


class BaiduPage(BasePage):
    def search_sougou(self):
        self.clear_text(BD.searchValue, doc="清除搜索栏")
        self.input_text(BD.searchValue, "搜狗", doc="输入框输入搜狗")
        self.click(BD.searchBtn, doc="点击搜索按钮")
        sleep(1)
        text_search = self.get_element_text(BD.list_name, doc="搜索结果列表的第一条数据")
        return text_search

    def search_taobao(self):
        self.clear_text(BD.searchValue, doc="清除搜索栏")
        self.input_text(BD.searchValue, "淘宝", doc="输入框输入淘宝")
        self.click(BD.searchBtn, doc="点击搜索按钮")
        sleep(1)
        text_search = self.get_element_text(BD.list_name, doc="搜索结果列表的第一条数据")
        return text_search
