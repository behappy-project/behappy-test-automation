#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/5/31
# @File    : api_demoProject_read_config.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from common.fileTool import FileTool
from pojo.api.demoProject.demoProjectConfig import DemoProjectConfig
import configparser as ConfigParser
import os


class API_DemoProject_Read_Config(object):
    __instance = None
    __inited = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            self.config = self._readConfig('config/demoProject/api_demoProject_test.conf')
            self.__inited = True

    def _readConfig(self, configFile):
        config = ConfigParser.ConfigParser()
        config.read(configFile, encoding='utf-8')
        demoProjectConfig = DemoProjectConfig()
        demoProjectConfig.url = config.get('servers', 'url')
        return demoProjectConfig
