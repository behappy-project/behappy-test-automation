#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @File    : conftest.py.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from Common import config, logger


# @pytest.fixture，框架提供的能力。将browser()打上注解，供别人做初始化的调用。
# @pytest.fixture(scope="class") 整个测试类只会执行一次fixture的前置和后置操作，所有的测试方法都将共用同一个fixture实例。
# 这通常适用于需要在多个测试方法之间共享资源的情况，例如数据库连接、浏览器实例等。
# @pytest.fixture(scope='session') 整个测试过程只会执行一次fixture的前置和后置操作，所有的测试类和测试方法都将共用同一个fixture实例。
# 这通常适用于需要在整个测试过程中共享资源的情况，例如登录凭证、全局配置等。
@pytest.fixture(scope="class")
def browser(request):
    name = request.config.getoption("--browser")
    if name == "chrome":
        # 前置：打开浏览器
        # 修改页面加载策略
        desired_capabilities = DesiredCapabilities.CHROME
        # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        desired_capabilities["pageLoadStrategy"] = "none"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.set_capability("version", config.configs.driver.version)
        chrome_options.set_capability("platform", 'ANY')
        chrome_options.set_capability("javascriptEnabled", True)
        # 实例化对象
        # browser = webdriver.Chrome()
        browser = webdriver.Remote(command_executor=config.configs.driver.addr, options=chrome_options)
        # 窗口最大化
        browser.maximize_window()
        # 等待
        time.sleep(1)
        # 返回对象
        yield browser
    else:
        # 前置：打开浏览器
        # 修改页面加载策略
        desired_capabilities = DesiredCapabilities.EDGE
        # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        desired_capabilities["pageLoadStrategy"] = "none"
        browser = webdriver.Edge()
        # 窗口最大化
        browser.maximize_window()
        # 等待
        time.sleep(1)
        # 返回对象
        yield browser

    def fn():
        logger.logging.info("全部用例执行完, teardown driver!")
        # 后置：关闭浏览器
        browser.quit()

    request.addfinalizer(fn)
    return browser


# 写每条case，的时候都会传入refresh方法
# 如 test_a_channel_search(self, refresh):
# 则执行顺序，就是在正式执行case执行之前，先执行refresh这个方法
@pytest.fixture
def refresh(browser):
    yield browser
    # 刷新页面
    browser.refresh()
    # 操作1
    # browser.find_element(*LP.s).click()
    # 操作2
    # browser.find_element(*LP.che).click()
    time.sleep(1)


# pytest_configure函数是pytest提供的一个钩子函数，它可以在pytest运行前对pytest进行配置
# 通过在该函数中添加代码，可以添加自定义的配置、marker、插件等
def pytest_configure(config):
    config.addinivalue_line("markers", 'smoke')
    config.addinivalue_line("markers", 'P0')
    config.addinivalue_line("markers", 'P1')


# 测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
def pytest_collection_modifyitems(items):
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        # print(item.nodeid)
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")


# 添加自定义的命令行选项，例如指定测试环境、配置文件路径
# 添加命令行参数 --browser
def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="browser option: firefox or chrome"
    )
