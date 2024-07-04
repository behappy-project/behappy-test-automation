#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/4/25
# @File    : dictTool.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'


class Dict(dict):
    """
    Simple dict but support access as x.y style.
    """

    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


class DictTool:
    @classmethod
    def sorted_dict_in_list(cls, datas):
        """
        将数组内的字典按字母进行排序
        :param datas:
        :return:
        """
        new_datas = []
        for data in datas:
            new_data = {}
            for key in sorted(data):
                new_data.update({key: data[key]})
            new_datas.append(new_data)
        return new_datas

    @classmethod
    def sorted_dict(cls, data):
        list = []
        for key in data:
            list.append(key)
        data_result = {}
        list.sort()
        for i in list:
            data_result[i] = data[i]
        return data_result

    @classmethod
    def to_dict(cls, data):
        D = Dict()
        for k, v in data.items():
            D[k] = cls.to_dict(v) if isinstance(v, dict) else v
        return D
