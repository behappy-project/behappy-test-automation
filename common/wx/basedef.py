#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/6/3
# @File    : basedef.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import time
from time import sleep
import minium
import base64
from minium import MiniElementNotFoundError

from common.fileTool import FileTool


class BaseDef():

    def __init__(self, mini: minium.MiniTest):
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
        return self.mini.page.path

    def upload_vin_pic(self, image_name, upload_button):
        """
        vin图片上传
        :param image_name : eg: xxx.jpg  # 运行这个case时需要在根目录下有名为xxx.jpg的图片
        :param upload_button : 上传按钮
        :return:
        """
        image_path = rf'{FileTool.getRootPath("TestAutomation")}\test_data\vin_pic\{image_name}'
        with open(image_path, "rb") as fd:
            c = fd.read()
            image_b64data = base64.b64encode(c).decode("utf8")
        self.mini.app.mock_choose_image(image_name, image_b64data)
        time.sleep(1)
        self.tap(upload_button)

    # 单个元素定位
    def get_element(self, element, max_timeout=10):
        """
        :param element: 传入的元素
        :return: 返回单个元素
        """
        try:
            ele = self.mini.page.wait_for(element, max_timeout=max_timeout)
            if ele:
                return self.mini.page.get_element(element, max_timeout=max_timeout, auto_fix=True)
            else:
                self.mini.app.logger.error(
                    f"################################找不到元素该元素{element}########################################")
                raise RuntimeError(f"找不到该元素{element}，超过等待时间，用例执行失败")
        except AttributeError as e:
            self.mini.logger.error(f"找不到该元素{element}!!,报错原因{e}")
            raise e

    # 多个元素定位
    def get_elements(self, element, max_timeout=10):
        """
        :param element: 传入的元素
        :return: 返回单个元素
        """
        try:
            ele = self.mini.page.wait_for(element, max_timeout=max_timeout)
            if ele:
                return self.mini.page.get_elements(element, max_timeout=max_timeout, auto_fix=True)
            else:
                self.mini.app.logger.error(
                    f"################################找不到元素该元素{element}########################################")
                raise MiniElementNotFoundError(element, f"找不到该元素{element}，超过等待时间，用例执行失败")
        except AttributeError as e:
            self.mini.logger.error(f"找不到该元素{element}!!,报错原因{e}")
            raise e

    # 判断某个元素是否存在
    def element_is_exists(self, element, max_timeout=3):
        self.mini.logger.info(f"目前在断言元素{element}")
        for i in range(3):
            ele = self.mini.page.wait_for(element, max_timeout=max_timeout)
            if ele:
                return self.mini.page.element_is_exists(element, max_timeout=max_timeout)
        self.mini.app.logger.warning(f"wait_for未能找到该元素{element}")
        return self.mini.page.element_is_exists(element, max_timeout=max_timeout)

    # 文本框输入
    def send_key(self, element, text: str, max_timeout=10):
        try:
            for i in range(10):
                ele = self.mini.page.wait_for(element, max_timeout=max_timeout)
                if ele:
                    self.mini.logger.info(f"目前在输入元素{element}")
                    ele_text = self.mini.page.get_element(element, max_timeout=max_timeout, auto_fix=True)
                    ele_text.input(text)
                    return
                else:
                    self.mini.logger.error(f"找不到该元素{element}，无法输入!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            self.mini.page.get_element(element, max_timeout=max_timeout, auto_fix=True).input(text)
        except Exception as e:
            self.mini.logger.error(f"找不到该元素{element}，无法输入!!!,,报错原因: {e}")
            raise e

    def scroll(self, scroll_top, duration=300):
        """
        :param scroll_top: 高度，单位 px
        :param duration:滚动动画时长，单位 ms
        :return:
        """
        self.mini.page.scroll_to(scroll_top, duration)

    # 操作弹窗
    def handle_modal(self, text):
        self.mini.native.handle_modal(btn_text=text)

    def tap(self, element, max_timeout=10):
        """
        :param max_timeout:
        :param element: 要点击的元素
        :return:
        """
        try:
            for i in range(10):
                ele = self.mini.page.wait_for(element, max_timeout=max_timeout)
                if ele:
                    self.mini.logger.info(f"目前在点击元素{element},点击方式Tap")
                    ele_tap = self.mini.page.get_element(element, max_timeout=max_timeout, auto_fix=True)
                    ele_tap.tap()
                    sleep(0.7)
                    return
                else:
                    self.mini.logger.error(f"找不到该元素{element}，无法点击!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            # 最后再次尝试点击
            self.mini.page.get_element(element, max_timeout=max_timeout, auto_fix=True).tap()
        except Exception as e:
            self.mini.logger.error(f"找不到该元素{element}，无法输入!!!,,报错原因: {e}")
            raise e

    def show_action_sheets(self, item):
        """
        :param item:输入选择的sheet的文字
        :return:
        """
        self.mini.native.handle_action_sheet(item)
