#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/5/31
# @File    : indexPageElements.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from page_objects.createElement import CreateElement
from page_objects.web_ui.wait_type import Wait_Type as Wait_By
from page_objects.web_ui.locator_type import Locator_Type


class IndexPageElements:
    def __init__(self):
        self.path = '/'
        self.title = CreateElement.create(None, None, None, Wait_By.TITLE_IS, '百度一下，你就知道')
        self.search_input = CreateElement.create(Locator_Type.ID, 'kw', wait_type=Wait_By.PRESENCE_OF_ELEMENT_LOCATED)
        self.search_button = CreateElement.create(Locator_Type.ID, 'su', wait_type=Wait_By.PRESENCE_OF_ELEMENT_LOCATED)
