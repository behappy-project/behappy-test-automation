#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from time import sleep
import minium


class BaseDef(minium.MiniTest):

    def __init__(self, mini):
        super().__init__()
        self.mini = mini

    def navigate_to_open(self, route):
        """以导航的方式跳转到指定页面,不允许跳转到 tabbar 页面,支持相对路径和绝对路径, 小程序中页面栈最多十层"""
        # self.logger.info(f"页面跳转到{route}!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.mini.app.navigate_to(route)

    def redirect_to_open(self, route):
        """关闭当前页面，重定向到应用内的某个页面,不允许跳转到 tabbar 页面"""
        self.mini.app.redirect_to(route)

    def relaunch_to_open(self, route):
        """关闭所有页面，打开到应用内的某个页面"""
        self.mini.app.relaunch(route)

    def switch_tab_open(self, route):
        """跳转到 tabBar 页面,会关闭其他所有非 tabBar 页面"""
        self.mini.app.switch_tab(route)

    def current_path(self) -> str:
        """获取当前页面route"""
        return self.page.path

    # 单个元素定位
    def get_element(self, element, max_timeout=15):
        """
        :param element: 传入的元素
        :return: 返回单个元素
        """
        try:
            ele = self.page.wait_for(element, max_timeout=max_timeout)
            if ele:
                return self.page.get_element(element, max_timeout=max_timeout)

            else:
                print(
                    f"################################找不到元素该元素{element}########################################")
                raise
        except AttributeError as e:
            self.mini.logger.error(f"找不到该元素{element}，无法点击!!,报错原因{e}")
            raise

    # 多个元素定位
    def get_elements(self, element, max_timeout=15):
        """
        :param element: 传入的元素
        :return: 返回单个元素
        """
        try:
            ele = self.page.wait_for(element, max_timeout=max_timeout)
            if ele:
                return self.page.get_elements(element, max_timeout=max_timeout)

            else:
                print(
                    f"################################找不到元素该元素{element}########################################")
                raise
        except AttributeError as e:
            self.mini.logger.error(f"找不到该元素{element}，无法点击!!,报错原因{e}")
            raise

    # 判断某个元素是否存在
    def element_is_exists(self, element, max_timeout=15):
        self.mini.logger.info(f"目前在断言元素{element}")
        self.page.wait_for(element, max_timeout=max_timeout)
        return self.page.element_is_exists(element, max_timeout=max_timeout)

    # 文本框输入
    def send_key(self, element, text: str, max_timeout=15):
        sleep(1)

        try:
            for i in range(10):
                ele = self.page.wait_for(element, max_timeout=max_timeout)
                if ele:
                    self.mini.logger.info(f"目前在输入元素{element}")
                    ele_text = self.page.get_element(element, max_timeout=max_timeout)
                    ele_text.input(text)
                    return
                else:
                    self.mini.logger.error(f"找不到该元素{element}，无法点击!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            raise RuntimeError(f"找不到该元素{element}，超过等待时间，用例执行失败")
        except AttributeError as e:
            self.mini.logger.error(f"找不到该元素{element}，无法输入!!!,,报错原因{e}")
            raise

    def scroll(self, scroll_top, duration=300):
        """
        :param scroll_top: 高度，单位 px
        :param duration:滚动动画时长，单位 ms
        :return:
        """
        self.page.scroll_to(scroll_top, duration)

    # 操作弹窗
    def handle_modal(self, text):
        self.mini.native.handle_modal(btn_text=text)

    def tap(self, element, max_timeout=15):
        """
        :param element: 要点击的元素
        :return:
        """
        sleep(1)
        try:
            for i in range(10):
                ele = self.page.wait_for(element, max_timeout=max_timeout)
                if ele:
                    self.logger.info(f"目前在点击元素{element},点击方式Tap")
                    ele_tap = self.page.get_element(element, max_timeout=max_timeout)
                    ele_tap.tap()
                    sleep(0.7)
                    return
                else:
                    self.mini.logger.error(f"找不到该元素{element}，无法点击!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            raise RuntimeError(f"找不到该元素{element}，超过等待时间，用例执行失败")

        except AttributeError as e:
            self.mini.logger.error(f"找不到该元素{element}，无法输入!!!,,报错原因{e}")
            raise

    def show_action_sheets(self, item):
        """
        :param item:输入选择的sheet的文字
        :return:
        """
        self.mini.native.handle_action_sheet(item)
