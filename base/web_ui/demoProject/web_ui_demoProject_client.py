#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/5/31
# @File    : web_ui_demoProject_client.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from base.web_ui.demoProject.web_ui_demoProject_read_config import WEB_UI_DemoProject_Read_Config
from base.read_web_ui_config import Read_WEB_UI_Config
from common.selenium.browserOperator import BrowserOperator
from common.selenium.driverTool import DriverTool


class WEB_UI_DemoProject_Client:
    def __init__(self):
        self.config = Read_WEB_UI_Config().web_ui_config
        self.demoProjectConfig = WEB_UI_DemoProject_Read_Config().config

        self.driver = DriverTool.get_driver(self.config.is_remote, self.config.selenium_hub, self.config.current_browser)
        self.driver.get(self.demoProjectConfig.web_host + '/')
        self.browserOperator = BrowserOperator(self.driver)
