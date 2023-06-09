#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @File    : keep_strong.py.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import os

import requests
import yaml


class KeepStrong():

    def server_probing(self):
        """服务器探活操作"""
        # 获取yaml文件路径
        yamlPath = os.path.abspath("./TestDatas/check_url.yaml")
        f = open(yamlPath, 'r', encoding='utf-8')
        cfg = f.read()
        d = yaml.safe_load(cfg)
        url = d["URL"]
        status_list = 0
        list_len = int(len(url))
        for i in url:
            status = int(requests.get(i).status_code)
            if status == 200:
                status_list = status_list + 1
            else:
                status_list = status_list + 0
        if status_list == list_len:
            return True
        else:
            return False
