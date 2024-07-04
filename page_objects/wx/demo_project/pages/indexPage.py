#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/6/4
# @File    : indexPage.py.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import time
import os

import ujson

from common.dateTimeTool import DateTimeTool
from pojo.wx.weapp_u_sopei_project.projectConfig import ProjectConfig
from common.custom_exception import CustomError
from common.fileTool import FileTool
from common.hamcrest.hamcrest import assert_that
from common.mysqlclient.mysqlclient import MysqlClient
from common.wx.basedef import BaseDef
from page_objects.wx.demo_project.elements.indexPageElements import IndexPageElements


class IndexPage:
    def __init__(self, base_operator: BaseDef):
        self._base_operator = base_operator
        self._indexPageElements = IndexPageElements()

    def test(self, projectConfig: ProjectConfig):
        # do something
        pass

