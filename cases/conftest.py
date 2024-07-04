#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @File    : conftest.py.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import pytest

# @pytest.fixture，框架提供的能力。将browser()打上注解，供别人做初始化的调用。
# @pytest.fixture(scope="class") 整个测试类只会执行一次fixture的前置和后置操作，所有的测试方法都将共用同一个fixture实例。
# 这通常适用于需要在多个测试方法之间共享资源的情况，例如数据库连接、浏览器实例等。
# @pytest.fixture(scope='session') 整个测试过程只会执行一次fixture的前置和后置操作，所有的测试类和测试方法都将共用同一个fixture实例。
# 这通常适用于需要在整个测试过程中共享资源的情况，例如登录凭证、全局配置等。


# 测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
# def pytest_collection_modifyitems(items):
#     """
#     测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
#     """
#     for item in items:
#         name = item.name.encode("utf-8").decode("unicode_escape")
#         node_id = item.nodeid.encode("utf-8").decode("unicode_escape")
#         logger.info(f'测试用例名称：{name}\n测试用例node_id：{node_id}')


# 添加自定义的命令行选项，例如指定测试环境、配置文件路径
# 添加命令行参数 --cmd_environment
def pytest_addoption(parser):
    parser.addoption("--cmd_environment",
                     action="store",
                     default="",
                     help="将自定义命令行参数`--cmd_environment`添加到pytest配置中")


# pytest_configure函数是pytest提供的一个钩子函数，它可以在pytest运行前对pytest进行配置
# 通过在该函数中添加代码，可以添加自定义的配置、marker、插件等
# def pytest_configure(config):
#     config.addinivalue_line("markers", 'P3')
#     config.addinivalue_line("markers", 'P1')


@pytest.fixture(scope='session')
def cmd_environment(request):
    environment: str = request.config.getoption("--cmd_environment")
    return environment
