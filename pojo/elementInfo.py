#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/4/24
# @File    : elementInfo.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'


class ElementInfo:
    def __init__(self):
        self.locator_type = None
        self.locator_value: str = ""
        self.expected_value = None
        self.wait_type = None
        self.wait_seconds = None
        self.wait_expected_value = None
