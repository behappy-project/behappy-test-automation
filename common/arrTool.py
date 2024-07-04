#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/6/13
# @File    : commonTool.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'


class ArrTool:

    @classmethod
    def find_next_element(cls, arr: list, target=None):
        """
        查询集合中某元素右侧挨着的元素，如果该元素是最右侧的，则返回第一个
        如果target是空的，则arr[0]
        :param arr:
        :param target:
        :return:
        """
        if len(arr) == 0:
            return None if target is None else target
        if target is None or len(str(target)) == 0:
            return arr[0]
        if target in arr:
            index = arr.index(target)
            if index == len(arr) - 1:
                return arr[0]  # 如果是最右侧的元素，返回第一个元素
            else:
                return arr[index + 1]  # 返回右侧挨着的元素
        return target  # 如果目标元素不在集合中，返回None
