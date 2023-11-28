#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @File    : config.py.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import os


class Dict(dict):
    '''
    Simple dict but support access as x.y style.
    '''

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


def toDict(d):
    D = Dict()
    for k, v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D


# 全局配置,先读取环境变量.
# 使用eg：config.db1.host
configs = toDict({
    'db1': {
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': int(os.environ.get('DB_PORT', 3306)),
        'user': os.environ.get('DB_USER', 'root'),
        'password': os.environ.get('DB_PASSWORD', 'root'),
        'db': os.environ.get('DB1_NAME', 'db1')
    },
    'db2': {
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': int(os.environ.get('DB_PORT', 3306)),
        'user': os.environ.get('DB_USER', 'root'),
        'password': os.environ.get('DB_PASSWORD', 'root'),
        'db': os.environ.get('DB2_NAME', 'db2')
    },
    'driver': {
        # 驱动位置
        'path': os.environ.get('DRIVER_PATH', 'D:/Software/chromedriver-win64/chromedriver.exe'),
    },
    'flag': {
        'env': os.environ.get('FLAG_ENV', 'Release')
    }
})
