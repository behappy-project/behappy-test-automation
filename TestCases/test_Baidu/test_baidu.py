#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @File    : test_baidu.py.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import os

import allure
import pytest

from Common import logger
from PageObjects.step_baidu_serach import BaiduPage as BD

root = os.path.dirname(os.path.abspath(__file__))


@allure.feature("模块：百度搜索")
class TestChannel:

    # function 默认参数传递，autouse=True 自动调用fixture功能
    @pytest.fixture(scope="class", autouse=True)
    def setup(self, browser):
        # `browser`对应这conftest中的browser实例
        # 将browser实例赋值给全局变量driver，以便在测试类中的所有测试方法中都可以使用
        global driver
        driver = browser
        driver.get('https://www.baidu.com')

    @pytest.mark.P3
    @allure.story("搜索搜狗")
    def test_search_sougou(self, refresh):
        """
        操作：搜索搜狗
        断言：结果列表展示搜狗
        """

        result_text = BD(refresh).search_sougou()
        logger.logging.info("搜索结果：{}".format(result_text))
        assert result_text == '搜狗'

    @pytest.mark.P1
    @allure.story("搜索淘宝")
    def test_search_taobao(self, refresh):
        """
        操作：搜索淘宝
        断言：结果列表展示淘宝
        """
        result_text = BD(refresh).search_taobao()
        assert result_text == '淘宝网 - 淘！我喜欢'
