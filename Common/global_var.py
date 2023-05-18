#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @File    : global_var.py.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from datetime import datetime

'''
全局配置，单例
'''
class GlobalVar():
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            cls.__instance.browser = "chrome"
            cls.__instance.base_dir = datetime.now().strftime('%Y%m%d_%H_%M_%S')
        return cls.__instance

    def set_browser(self, value):
        self.__instance.browser = value

    def set_base_dir(self, value):
        self.__instance.base_dir = value
