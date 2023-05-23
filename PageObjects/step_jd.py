#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @File    : step_baidu_serach.py.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import base64
import os
import random
import re
from time import sleep

import cv2
import numpy as np
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from Common import logger
from Common.basepage import BasePage
from Common.config import configs
from Common.file_config import FileConfig
from Common.global_var import GlobalVar


class JD(BasePage):
    def buy_xiaomi(self):
        self.clear_text(loc=(By.XPATH, '//*[@id="key"]'), doc="清除搜索栏")
        self.input_text(loc=(By.XPATH, '//*[@id="key"]'), value="小米13")
        self.click(loc=(By.XPATH, '//i[text()=""]'), doc="点击搜索按钮")
        sleep(1)
        text_search = self.get_element_text(loc=(By.XPATH, '//div[@class="m-list"]'), doc="搜索结果列表的第一条数据")
        return text_search

    def login(self):
        self.click(loc=(By.XPATH, '//a[@class="link-login" and text()="你好，请登录"]'))
        self.wait_elevisible(loc=(By.XPATH, '//div[@class="qrcode-img"]//img'), doc="等待二维码可见")
        self.click(loc=(By.XPATH, "//a[text()='账户登录']"), doc="点击账户登录")
        self.input_text(loc=(By.XPATH, '//input[@id="loginname"]'), value=configs.jd.username, doc='输入账户')
        self.input_text(loc=(By.XPATH, '//input[@id="nloginpwd"]'), value=configs.jd.password, doc='输入密码')
        self.click(loc=(By.XPATH, '//a[@id="loginsubmit"]'), doc="点击登录")
        sleep(2)
        self.wait_elevisible(loc=(By.XPATH, '//div[@id="JDJRV-wrap-loginsubmit"]'), doc='等待滑动代码块可见')
        # 为了保证截图的准确性，我们需要等待一段时间，以确保页面完全加载完成
        sleep(2)
        # 开始反复滑动直到成功验证
        move_num = 1
        while True:
            sleep(1)
            if self.move():
                break
            move_num += 1
        # 等待登录成功
        logger.logging.info("登陆成功, 成功率为：{0} %".format((1 / move_num * 100)))
        sleep(1)

    def move(self):
        # 坐标
        coordinate = self.recognition()
        distance = int(coordinate / 1.285)

        # 轨迹
        tracks = self.get_tracks(distance)

        # 移动滑块
        self.slider_action(tracks)

        sleep(1)

        # 如果还停留登录页，则继续
        pattern = r"https://passport\.jd\.com/.*?/login.*"
        match = re.search(pattern, self.driver.current_url)
        if match:
            return False
        else:
            return True

    '''
    滑动录制
    '''

    def recognition(self):
        # 文件夹路径
        global_var = GlobalVar()
        path_sep = os.path.sep
        screenshot_path = FileConfig().get_path(type="pic") + f"{path_sep}{global_var.base_dir}{path_sep}"
        screenshot_dir = os.path.dirname(screenshot_path)
        # 不存在则先创建
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        # 选择所有 class 属性为 "JDJRV-bigimg" 的 div 元素下的 img 元素
        r1 = self.get_element_attribute(loc=(By.XPATH, "//div[@class='JDJRV-bigimg']/img"), attr="src")
        r1de = base64.b64decode(re.findall(";base64,(.*)", r1)[0])
        # 选择所有 class 属性为 "JDJRV-smallimg" 的 div 元素下的 img 元素
        r2 = self.get_element_attribute(loc=(By.XPATH, "//div[@class='JDJRV-smallimg']/img"), attr="src")
        r2de = base64.b64decode(re.findall(";base64,(.*)", r2)[0])
        # 保存图片
        with open(f"{screenshot_path}captcha1.png", 'wb') as f:
            f.write(r1de)
        with open(f"{screenshot_path}captcha2.png", 'wb') as f:
            f.write(r2de)
        sleep(1)
        cv2.imwrite(f"{screenshot_path}r3.jpg", cv2.imread(f"{screenshot_path}captcha1.png", 0))
        cv2.imwrite(f"{screenshot_path}r4.jpg", cv2.imread(f"{screenshot_path}captcha2.png", 0))
        cv2.imwrite(f"{screenshot_path}r4.jpg", abs(255 - cv2.cvtColor(cv2.imread(f"{screenshot_path}r4.jpg"), cv2.COLOR_BGR2GRAY)))
        result = cv2.matchTemplate(cv2.imread(f"{screenshot_path}r4.jpg"), cv2.imread(f"{screenshot_path}r3.jpg"), cv2.TM_CCOEFF_NORMED)
        x, y = np.unravel_index(result.argmax(), result.shape)

        cv2.rectangle(cv2.imread(f"{screenshot_path}r3.jpg"), (y + 20, x + 20), (y + 136 - 25, x + 136 - 25), (7, 249, 151), 2)
        logger.logging.info('识别坐标为: {}'.format(y))
        return y

    def get_random_float(self, min, max, digits=4):
        """
        :param min:
        :param max:
        :param digits:
        :return:
        """
        return round(random.uniform(min, max), digits)

    def get_tracks(self, distance):
        tracks = []
        mid1 = round(distance * random.uniform(0.1, 0.2))
        mid2 = round(distance * random.uniform(0.65, 0.76))
        mid3 = round(distance * random.uniform(0.84, 0.88))
        # 设置初始位置，初始速度，时间间隔
        current, v, t = 0, 0, 0.2
        # 四舍五入
        distance = round(distance)
        while current < distance:
            if current < mid1:
                a = random.randint(10, 15)
            elif current < mid2:
                a = random.randint(30, 40)
            elif current < mid3:
                a = -70
            else:
                a = random.randint(-25, -18)
            # 初速度 v0
            v0 = v
            # 当前速度 v = v0 + at
            v = v0 + a * t
            v = v if v >= 0 else 0
            # 一个质点在匀加速直线运动中的位移
            # ** 表示幂运算
            move = v0 * t + 1 / 2 * a * (t ** 2)
            move = round(move if move >= 0 else 1)
            # 当前位移
            current += move
            # 加入轨迹
            tracks.append(move)
        logger.logging.info("current={}, distance={}".format(current, distance))
        # 超出范围
        back_tracks = []
        out_range = distance - current
        if out_range < -8:
            sub = int(out_range + 8)
            back_tracks = [-1, sub, -3, -1, -1, -1, -1]
        elif out_range < -2:
            sub = int(out_range + 3)
            back_tracks = [-1, -1, sub]
        logger.logging.info("forward_tracks={}, back_tracks={}".format(tracks, back_tracks))
        return {'forward_tracks': tracks, 'back_tracks': back_tracks}

    def slider_action(self, tracks):
        # 获取滑块
        slider = self.get_element(loc=(By.XPATH, "//div[@class='JDJRV-slide-inner JDJRV-slide-btn']"))
        # 点击滑块并按住
        ActionChains(self.driver).click_and_hold(on_element=slider).perform()
        # 正向滑动
        for track in tracks['forward_tracks']:
            y_offset_random = random.uniform(-2, 4)
            ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=y_offset_random).perform()
        sleep(random.uniform(0.06, 0.5))

        # 反向滑动
        for track in tracks['back_tracks']:
            y_offset_random = random.uniform(-2, 2)
            ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=y_offset_random).perform()

        # 抖动
        ActionChains(self.driver).move_by_offset(
            xoffset=self.get_random_float(0, -1.67),
            yoffset=self.get_random_float(-1, 1)
        ).perform()
        ActionChains(self.driver).move_by_offset(
            xoffset=self.get_random_float(0, 1.67),
            yoffset=self.get_random_float(-1, 1)
        ).perform()

        sleep(self.get_random_float(0.6, 1))

        ActionChains(self.driver).release().perform()
        sleep(0.5)

