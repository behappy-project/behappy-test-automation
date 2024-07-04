#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/5/31
# @File    : searchPage.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from page_objects.web_ui.demoProject.elements.searchPageElements import SearchPageElements


class SearchPage:
    def __init__(self, browserOperator, title):
        self._browserOperator = browserOperator
        self._searchPageElements = SearchPageElements()
        self._searchPageElements.title.wait_expected_value = title
        self._browserOperator.explicit_wait_page_title(self._searchPageElements.title)
        self._browserOperator.snapAndGetPath('searchPage')

    def _input_search_kw(self, kw):
        self._browserOperator.sendText(self._searchPageElements.search_input, kw)
        self._browserOperator.snapAndGetPath('input_search_kw')

    def _click_search_button(self):
        self._browserOperator.click(self._searchPageElements.search_button)
        self._browserOperator.snapAndGetPath('click_search_button')

    def search_kw(self, kw):
        self._input_search_kw(kw)
        self._click_search_button()
        if kw.strip():
            return SearchPage(self._browserOperator, kw + '_百度搜索')

    def getElements(self):
        return self._searchPageElements
