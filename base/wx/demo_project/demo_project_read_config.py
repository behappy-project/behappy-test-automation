#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/6/4
# @File    : web_ui_project_read_config.py.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from pojo.wx.weapp_u_sopei_project.projectConfig import ProjectConfig
import configparser


class Demo_Project_Read_Config(object):
    __instance = None
    __inited = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            self.config = self._readConfig('config/wx_demo_project/wx.conf')
            self.__inited = True

    def _readConfig(self, configFile):
        config = configparser.ConfigParser()
        config.read(configFile, encoding='utf-8')
        projectConfig = ProjectConfig()
        projectConfig.project_path = config.get('servers', 'project_path')
        projectConfig.dev_tool_path = config.get('servers', 'dev_tool_path')
        projectConfig.data_username = config.get('servers', 'data_username')
        projectConfig.data_password = config.get('servers', 'data_password')
        projectConfig.mysql_host = config.get('DB', 'mysql_host')
        projectConfig.mysql_port = config.get('DB', 'mysql_port')
        projectConfig.mysql_username = config.get('DB', 'mysql_username')
        projectConfig.mysql_password = config.get('DB', 'mysql_password')
        projectConfig.mysql_db_name = config.get('DB', 'mysql_db_name')
        return projectConfig
