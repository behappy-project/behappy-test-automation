#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/5/31
# @File    : createElement.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from pojo.elementInfo import ElementInfo


class CreateElement:

    @classmethod
    def create(cls, locator_type, locator_value: str, expected_value: str = None, wait_type=None,
               wait_expected_value=None,
               wait_seconds=30):
        elementInfo = ElementInfo()
        elementInfo.locator_type = locator_type
        elementInfo.locator_value = locator_value
        elementInfo.expected_value = expected_value
        elementInfo.wait_type = wait_type
        elementInfo.wait_seconds = wait_seconds
        elementInfo.wait_expected_value = wait_expected_value
        return elementInfo
