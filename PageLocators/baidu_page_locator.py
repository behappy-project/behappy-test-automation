#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @File    : baidu_page_locator.py.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from selenium.webdriver.common.by import By


class BaiduPageLocator:
    """
    百度首页的页面元素

    """
    # 输入框搜索内容
    searchValue = (By.ID, "kw")

    # 搜索按钮
    searchBtn = (By.ID, "su")

    # 搜索结果第一条数据
    list_name = (By.XPATH, '//*[@id="1"]/div/div[1]/h3/a')
