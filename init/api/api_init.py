#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/5/31
# @File    : api_init.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from common.fileTool import FileTool


def clear(need_clear: int,
          cmd_environment: str):
    if need_clear != 0:
        # 删除output/web_ui/chrome/report_data下所有数据
        FileTool.truncateDir('./output/api/report_data/' + cmd_environment)
