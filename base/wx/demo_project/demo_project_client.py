#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/6/4
# @File    : web_ui_project_client.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from base.wx.demo_project.demo_project_read_config import Demo_Project_Read_Config


class Demo_Project_Client:
    def __init__(self):
        self.projectConfig = Demo_Project_Read_Config().config
