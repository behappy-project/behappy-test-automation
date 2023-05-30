#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/22
# @File    : test_buy_xiaomi.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import allure
import pytest

from Common import logger
from PageObjects.step_jd import JD


global driver


@allure.feature("模块：京东")
class TestJd:

    @pytest.fixture(scope="class", autouse=True)
    def setup(self, browser):
        globals()['driver'] = browser
        driver.get('https://www.jd.com/')

    @pytest.mark.JD
    @allure.story("买小米")
    def test_search_sougou(self, browser):
        """
        操作：搜索搜狗
        断言：结果列表展示搜狗
        """
        JD(browser).login()
        result_text = JD(browser).buy_xiaomi()
        logger.logging.info("搜索结果：{}".format(result_text))
