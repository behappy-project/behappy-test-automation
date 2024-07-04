#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/5/31
# @File    : indexPage.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from page_objects.web_ui.demoProject.elements.indexPageElements import IndexPageElements
from page_objects.web_ui.demoProject.pages.searchPage import SearchPage


class IndexPage:
    def __init__(self, browserOperator):
        self._browserOperator = browserOperator
        self._indexPageElements = IndexPageElements()
        self._browserOperator.explicit_wait_page_title(self._indexPageElements.title)
        self._browserOperator.snapAndGetPath('indexPage')

    def _input_search_kw(self, kw):
        self._browserOperator.sendText(self._indexPageElements.search_input, kw)
        self._browserOperator.snapAndGetPath('input_search_kw')

    def _click_search_button(self):
        self._browserOperator.click(self._indexPageElements.search_button)
        self._browserOperator.snapAndGetPath('click_search_button')

    def search_kw(self, kw):
        self._input_search_kw(kw)
        self._click_search_button()
        if kw.strip():
            return SearchPage(self._browserOperator, kw + '_百度搜索')
        return IndexPage(self._browserOperator)

    def getElements(self):
        return self._indexPageElements
