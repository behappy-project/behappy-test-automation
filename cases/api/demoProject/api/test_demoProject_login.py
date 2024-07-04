#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/5/31
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import allure

from common.hamcrest.hamcrest import assert_that
from base.api.demoProject.api_demoProject_client import API_DemoProject_Client
import pytest


@pytest.fixture(scope="session")
def project_client():
    return API_DemoProject_Client()


@pytest.fixture(scope="session")
def login_path(project_client, cmd_environment):
    # set up environment...
    _login_path = '/horizon/auth/login/'
    return _login_path


@pytest.fixture(scope="session")
def teardown(project_client):
    yield  # Allow tests to use project_client.browserOperator
    # do something when end the testing


@allure.feature("模块：Demo")
class TestLogin:

    @allure.story("测试GetIndex")
    def test_get_index(self, project_client, login_path):
        httpResponse = project_client.doRequest.get(login_path)
        assert_that(200).is_equal_to(httpResponse.status_code)

    @allure.story("测试SearchKw")
    @pytest.mark.search_kw
    def test_search_kw(self, project_client, login_path):
        params = {'wd': 'apitest'}
        httpResponse = project_client.doRequest.get(login_path, params)
        assert_that(200).is_equal_to(httpResponse.status_code)
