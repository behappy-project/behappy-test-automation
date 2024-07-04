#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/6/25
# @File    : weapp_u_adapt_project.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import sys

import minium
from minium import MiniCommandError

from cases.wx import BaseCase
from common.logging import logger
from common.wx.basedef import BaseDef
from common_projects.exception_execute import handle_exception
from base.wx.demo_project.demo_project_client import Demo_Project_Client
from page_objects.wx.demo_project.pages.indexPage import IndexPage


class TestDataAssert(BaseCase):

    def __init__(self, methodName='runTest'):
        super(TestDataAssert, self).__init__(methodName)

    def setUp(self):
        super(TestDataAssert, self).setUp()
        self._project_client = Demo_Project_Client()
        self._base_def = BaseDef(self)
        self._index_page = IndexPage(self._base_def)
        # 暂时仅支持单环境 TODO
        cmd_environment = self._project_client.projectConfig.environment
        if cmd_environment == 'production':
            self._project_client.projectConfig.data_host = "xxx"
        else:
            self._project_client.projectConfig.data_host = "xxx"

    def test_data_assert(self):
        """
        描述：test_u_data_assert
        """
        self._index_page.test(self._project_client.projectConfig)
