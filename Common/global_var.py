#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @File    : global_var.py.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'


class GlobalVar():
    type = "chrome"

    def set_value(self, value):
        GlobalVar.type = value

    def get_value(self):
        # 获得一个全局变量，不存在则提示读取对应变量失败
        return GlobalVar.type
