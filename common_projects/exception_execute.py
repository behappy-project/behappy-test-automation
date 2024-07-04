#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/6/14
# @File    : exception_execute.py
# @Software: IntelliJ IDEA

from __future__ import unicode_literals

__author__ = 'xiaowu'

import functools
import traceback

import ujson

from common.custom_exception import CustomError
from common.dateTimeTool import DateTimeTool
from common.selenium.browserOperator import BrowserOperator
from common.wx.basedef import BaseDef


def wrap_exception(func):
    """
    统一异常处理
    :param func:
    :return:
    """

    @functools.wraps(func)
    def wrap(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            # do something
            raise e

    return wrap


def handle_exception(e: Exception,
                     custom_err_prefix: str,
                     projectConfig,
                     global_operator: BaseDef | BrowserOperator = None,
                     table_name="err_record",
                     **kwargs):
    if not isinstance(e, CustomError):
        # 存储db
        error_info = str(e) + traceback.format_exc()
        # insert err db data TODO
        # 补充信息 TODO
        comment = {
            "错误信息补充": "待补充"
        }
        if isinstance(global_operator, BrowserOperator):
            # 截图处理
            global_operator.snapAndGetPath('global_error_catch')
            global_operator.attach_comment(
                ujson.dumps(comment, ensure_ascii=False, default=DateTimeTool.datetime_to_json))
        else:
            global_operator.mini.capture()
            # 补充信息
            global_operator.mini.logger.error(
                f"补充信息：{ujson.dumps(comment, ensure_ascii=False, default=DateTimeTool.datetime_to_json)}")
    raise e
