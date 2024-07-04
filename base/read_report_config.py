#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/5/31
# @File    : read_report_config.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from pojo.report_config import Report_Config
import configparser as ConfigParser


@DeprecationWarning
class Read_Report_Config(object):
    __instance = None
    __inited = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            self.report_config = self._readConfig('config/report.conf')
            self.__inited = True

    def _readConfig(self, configFile):
        configParser = ConfigParser.ConfigParser()
        configParser.read(configFile, encoding='utf-8')
        report_config = Report_Config()
        return report_config
