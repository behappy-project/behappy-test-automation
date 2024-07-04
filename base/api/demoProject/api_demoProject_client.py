#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/5/31
# @File    : api_demoProject_client.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from base.api.demoProject.api_demoProject_read_config import API_DemoProject_Read_Config
from base.api.demoProject.api_demoProject_db_clients import API_DemoProject_DB_Clients
from common.httpclient.doRequest import DoRequest


class API_DemoProject_Client(object):
    __instance = None
    __inited = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        """
        :param config_file_path:
        :param env:
        """
        if self.__inited is None:
            self.demoProjectConfig = API_DemoProject_Read_Config().config
            self.demoProjectDBClients = API_DemoProject_DB_Clients()
            self.doRequest = DoRequest(self.demoProjectConfig.url)

            self.__inited = True
