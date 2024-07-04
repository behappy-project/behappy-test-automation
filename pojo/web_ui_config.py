#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/4/24
# @File    : web_ui_config.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'


class WEB_UI_Config:
    def __init__(self):
        self.selenium_hub = None
        self.is_remote = None
        self.test_browsers = []
        self.current_browser = None
        self.download_dir = None
        self.is_chrome_headless = None
        self.is_firefox_headless = None
