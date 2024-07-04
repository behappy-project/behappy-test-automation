#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/6/4
# @File    : projectConfig.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'


class ProjectConfig:
    def __init__(self):
        self.environment = 'production'
        self.project_path = None
        self.dev_tool_path = None
        # --- begin ---
        self.data_host = None
        self.data_username = None
        self.data_password = None
        # --- end ---
        self.mysql_host = None
        self.mysql_port = None
        self.mysql_username = None
        self.mysql_password = None
        self.mysql_db_name = None
