#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @File    : basepage.py.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import calendar as cal
import datetime
import json
import os
import time

import allure
# import win32gui
# import win32con
import pyautogui
from PIL import Image
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Common import logger
from Common.file_config import FileConfig
from Common.global_var import GlobalVar


# 任何一个步骤都会做到  捕获异常、日志输出、失败截图
class BasePage:
    # 包含了PageObjects当中，用到所有的selenium底层方法。
    # 还可以包含通用的一些元素操作，如alert,iframe,windows...
    # 还可以自己额外封装一些web相关的断言
    # 实现日志记录、实现失败截图
    def __init__(self, driver: WebDriver):
        self.driver = driver

    # 等待元素可见
    def wait_elevisible(self, loc, timeout=120, frequency=0.5, doc=""):
        """
        :param loc:
        :param timeout:
        :param frequency:
        :param doc:
        :return:
        """
        start_time = time.time()
        try:
            element = WebDriverWait(self.driver, timeout, frequency). \
                until(lambda driver: driver.find_element(*loc))
        except (NoSuchElementException, NoSuchWindowException, TimeoutException, ElementNotVisibleException) as e:
            logger.logging.exception("等待{}元素可见超时".format(loc))
            self.do_save_screenshot(doc)
            raise e
        else:
            isVisible = EC.visibility_of_element_located(loc)
            end_time = time.time()
            duration = end_time - start_time
            if isVisible:
                logger.logging.info("等待{}元素可见,耗时{}".format(loc, duration))
                return element
            else:
                logger.logging.info("等待{}元素不可见,耗时{}".format(loc, duration))

    # 查找元素
    def is_element_exsits(self, loc, doc=""):
        """
        :param loc:
        :param doc:
        :return:
        """
        try:
            ele = self.driver.find_element(*loc)
        except (NoSuchElementException, TimeoutException) as e:
            logger.logging.warning("该元素 {} 不存在！".format(loc))
            self.do_save_screenshot(doc)
            return False
        else:
            logger.logging.info("查找{}的元素{}成功。".format(doc, loc))
            return True

    # 查找元素
    def get_element(self, loc, doc=""):
        """
        :param loc:
        :param doc:
        :return:
        """
        try:
            ele = self.driver.find_element(*loc)
        except (NoSuchElementException, TimeoutException) as e:
            logger.logging.exception("等待 {} 元素存在，失败！".format(loc))
            self.do_save_screenshot(doc)
            raise e
        else:
            logger.logging.info("查找{}的元素{}成功。".format(doc, loc))
            return ele

    # 查找元素是否显示
    def get_element_isDisplay(self, loc, doc=""):
        """
        :param loc:
        :param doc:
        :return:
        """
        try:
            self.get_element_text(loc, doc="", timeout=2)
        except (NoSuchElementException, TimeoutException) as e:
            logger.logging.warning("页面{}元素不存在！".format(loc))
            self.do_save_screenshot(doc)
            return False
        else:
            logger.logging.info("页面{}元素存在！".format(doc, loc))
            return True

    # 输入框输入文本
    def input_text(self, loc, value, timeout=60, frequency=0.5, doc=""):
        """
        :param loc:
        :param value:
        :param timeout:
        :param frequency:
        :param doc:
        :return:
        """
        # 元素可见# 找它
        self.wait_elevisible(loc, timeout, frequency, doc)
        ele = self.get_element(loc, doc)
        try:
            ele.send_keys(value)
        except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:
            logger.logging.exception("向{}元素输入{}失败".format(loc, value))
            self.do_save_screenshot(doc)
            raise e
        else:
            logger.logging.info("向{}元素输入{}成功".format(loc, value))

    # 清除输入框中的文本
    def clear_text(self, loc, timeout=60, frequency=0.5, doc=""):
        """
        :param loc:
        :param value:
        :param timeout:
        :param frequency:
        :param doc:
        :return:
        """
        # 元素可见# 找它
        self.wait_elevisible(loc, timeout, frequency, doc)
        ele = self.get_element(loc, doc)
        try:
            ele.clear()
        except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:
            logger.logging.exception("清除{}内容失败".format(loc))
            self.do_save_screenshot(doc)
            raise e
        else:
            logger.logging.info("清除{}内容成功".format(loc))

    # 点击
    def click(self, loc, timeout=8, frequency=0.5, doc=""):
        """
        :param loc:
        :param timeout:
        :param frequency:
        :param doc:
        :return:
        """
        # 元素可见# 找它
        time.sleep(0.5)
        self.wait_elevisible(loc, timeout, frequency, doc)
        ele = self.get_element(loc, doc)
        try:
            ele.click()
        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
            logger.logging.exception("向{}元素点击失败".format(loc))
            self.do_save_screenshot(doc)
            raise e
        else:
            logger.logging.info("向{}元素点击成功".format(loc))

    # 点击, 解决element click intercepted的问题
    def click_by_js(self, loc, timeout=8, frequency=0.5, doc=""):
        """
        :param loc:
        :param timeout:
        :param frequency:
        :param doc:
        :return:
        """
        # 元素可见# 找它
        time.sleep(0.5)
        self.wait_elevisible(loc, timeout, frequency, doc)
        ele = self.get_element(loc, doc)
        try:
            self.driver.execute_script("(arguments[0]).click()", ele)
        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
            logger.logging.exception("向{}元素点击失败".format(loc))
            self.do_save_screenshot(doc)
            raise e
        else:
            logger.logging.info("向{}元素点击成功".format(loc))

    # 获取元素文本值
    def get_element_text(self, loc, timeout=8, frequency=0.5, doc=""):
        """
        :param loc:
        :param timeout:
        :param frequency:
        :param doc:
        :return:
        """
        # 元素可见# 找它
        self.wait_elevisible(loc, timeout, frequency, doc)
        ele = self.get_element(loc, doc)
        try:
            text = ele.text
        except (NoSuchElementException, TimeoutException) as e:
            logger.logging.exception("获取{}元素文本值失败".format(loc))
            self.do_save_screenshot(doc)
            raise e
        else:
            logger.logging.info("获取{}元素文本值成功".format(loc))
            return text

    # 获取元素属性
    def get_element_attribute(self, loc, attr, timeout=60, frequency=0.5, doc=""):
        """
        :param loc:
        :param attr:
        :param timeout:
        :param frequency:
        :param doc:
        :return:
        """
        # 元素可见# 找它
        self.wait_elevisible(loc, timeout, frequency, doc)
        ele = self.get_element(loc, doc)
        try:
            value = ele.get_attribute(attr)
        except (NoSuchElementException, TimeoutException) as e:
            logger.logging.exception("获取{}元素属性值失败".format(loc))
            self.do_save_screenshot(doc)
            raise e
        else:
            logger.logging.info("获取{}元素属性值成功".format(loc))
            return value

    # 查找多个元素
    def get_elements(self, loc, doc=""):
        """
        :param loc:
        :param doc:
        :return:
        """
        try:
            ele = self.driver.find_elements(*loc)
        except (NoSuchElementException, TimeoutException) as e:
            logger.logging.exception("等待 {} 元素存在，失败！".format(loc))
            self.do_save_screenshot(doc)
            raise e
        else:
            logger.logging.info("查找{}的元素{}成功。".format(doc, loc))
            return ele

    # 获取列表数据长度
    def get_list_length(self, loc, timeout=60, frequency=0.5, doc=""):
        """
        :param loc:
        :param timeout:
        :param frequency:
        :param doc:
        :return:
        """
        # 元素可见# 找它
        self.wait_elevisible(loc, timeout, frequency, doc)
        ele = self.get_elements(loc, doc)
        try:
            value = len(ele)
        except (NoSuchElementException, TimeoutException) as e:
            logger.logging.exception("获取{}元素属性值失败".format(loc))
            self.do_save_screenshot(doc)
            raise e
        else:
            logger.logging.info("获取{}元素属性值成功".format(loc))
            return value

    # 截图
    def do_save_screenshot(self, doc=""):
        """
        :param doc:
        :return:
        """
        global_var = GlobalVar()
        cur_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
        # file = screenshot_dir+"/{}_{}.png".format(doc,cur_time)
        path_sep = os.path.sep
        # 文件夹路径
        screenshot_path = FileConfig().get_path(type="screenshots") + f"{path_sep}{global_var.base_dir}{path_sep}"
        screenshot_dir = os.path.dirname(screenshot_path)
        # 不存在则先创建
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        # 图片路径
        file = f"{screenshot_path}{doc}_{cur_time}.png"
        try:
            self.driver.save_screenshot(file)
            logger.logging.info("操作保存图片：{}".format(file))
            allure.attach.file(source=file, name=doc, attachment_type=allure.attachment_type.PNG)
        except (NoSuchElementException, TimeoutException) as e:
            logger.logging.exception("网页截图操作失败")
        else:
            logger.logging.info("网页截图成功，存储路径为{}".format(file))

    # 上传文件
    # def upload_file(self, filepath, doc=""):
    #     try:
    #         # 一级窗口"#32770","打开"
    #         dialog = win32gui.FindWindow("#32770", "打开")
    #         ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, "ComboBoxEx32", None)  # 二级
    #         comboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, "ComboBox", None)  # 三级
    #         # 编辑按钮
    #         edit = win32gui.FindWindowEx(comboBox, 0, 'Edit', None)  # 四级
    #         # 打开按钮
    #         button = win32gui.FindWindowEx(dialog, 0, 'Button', "打开(&O)")  # 四级
    #         # 往编辑当中，输入文件路径 。
    #         win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, filepath)  # 发送文件路径
    #         win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击打开按钮
    #     except (NoSuchElementException, TimeoutException) as e:
    #         logger.logging.exception("上传文件{}失败".format(filepath))
    #         self.do_save_screenshot(doc)
    #         raise e
    #     else:
    #         logger.logging.info("上传文件{}成功".format(filepath))

    # 打开新的窗口
    def open_new_window(self, url: str, window_title: str = "new_window", doc=""):
        try:
            # 执行JavaScript代码在当前窗口中打开新窗口
            self.driver.execute_script(f"window.open('{url}', '{window_title}')")
            # 切换到新窗口
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[-1])
        except BaseException as e:
            logger.logging.exception("打开新的窗口失败")
            self.do_save_screenshot(doc)
            raise e
        else:
            logger.logging.info("打开新的窗口成功")

    # 切换窗口
    # -1切换到最新窗口；0切换到第一个窗口；
    def switch_window(self, index: int = -1, doc=""):
        try:
            # 获取所有的window列表
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[index])
        except (NoSuchElementException, TimeoutException) as e:
            logger.logging.exception("切换窗口失败")
            self.do_save_screenshot(doc)
            raise e
        else:
            logger.logging.info("切换窗口成功")

    # 获取多个元素的文本值（新增方法）
    def get_elements_text_value(self, loc, doc=""):
        """
        :param loc:
        :param doc:
        :return:
        """
        try:
            check_results = []
            eles = self.driver.find_elements(*loc)
            for ele in eles:
                check_results.append(ele.text)
        except (NoSuchElementException, TimeoutException) as e:
            logger.logging.exception("获取 {} 元素文本值存在，失败！".format(loc))
            self.do_save_screenshot(doc)
            raise e
        else:
            logger.logging.info("获取{}的元素{}文本值成功。".format(doc, loc))
            return check_results

    # 获取当前日期
    def get_date(self):
        return time.strftime("%Y-%m-%d", time.localtime(time.time()))

    # 获取元素默认值
    def get_default_value(self, loc, timeout=60, frequency=0.5, doc=""):
        """
        :param loc:
        :param timeout:
        :param frequency:
        :param doc:
        :return:
        """
        # 元素可见# 找它
        self.wait_elevisible(loc, timeout, frequency, doc)
        ele = self.get_element(loc, doc)
        try:
            default_value = ele.get_attribute('value')
        except (NoSuchElementException, TimeoutException) as e:
            logger.logging.exception("获取{}元素文本值失败".format(loc))
            self.do_save_screenshot(doc)
            raise e
        else:
            logger.logging.info("获取{}元素文本值成功".format(loc))
            return default_value

    # 输入框输入文本形式上传文件
    def input_text_uploadfile(self, loc, value, timeout=60, frequency=0.5, doc=""):
        """
        :param loc:
        :param value:
        :param timeout:
        :param frequency:
        :param doc:
        :return:
        """
        # 元素可见# 找它
        ele = self.get_element(loc, doc)
        try:
            ele.send_keys(value)
        except (NoSuchElementException, TimeoutException) as e:
            logger.logging.exception("向{}元素输入{}失败".format(loc, value))
            self.do_save_screenshot(doc)
            raise e
        else:
            logger.logging.info("向{}元素输入{}成功".format(loc, value))

    # 获取当月的第一天和最后一天
    def get_first_and_last_day(self):
        i = datetime.datetime.now()
        FORMAT = "%d-%d-%d\t%d-%d-%d"
        d = cal.monthrange(i.year, i.month)
        list = str(FORMAT % (i.year, i.month, 1, i.year, i.month, d[1])).split("\t")
        list = "-".join(list).split("-")
        for count in range(len(list)):
            if len(list[count]) == 1:
                list[count] = "0" + str(list[count])
                print(list[count])
        list = "-".join(list)
        return list

    # 距离今天N天的未来某一天
    def future_oneday(self, countdays):
        today = time.time()
        future_five = today + countdays * 86400
        future_one_date = time.strftime('%Y-%m-%d', time.localtime(future_five))
        return future_one_date

    # 键盘删除
    def keyboard_clear(self, loc, count=2, timeout=60, frequency=0.5, doc=""):
        """
        :param loc:
        :param value:
        :param timeout:
        :param frequency:
        :param doc:
        :return:
        """
        # 元素可见# 找它
        self.wait_elevisible(loc, timeout, frequency, doc)
        ele = self.get_element(loc, doc)
        try:
            for one in range(count):
                ele.send_keys(Keys.BACK_SPACE)
        except (NoSuchElementException, TimeoutException) as e:
            logger.logging.exception("向{}元素输入删除键失败".format(loc))
            self.do_save_screenshot(doc)
            raise e
        else:
            logger.logging.info("向{}元素输入删除键成功".format(loc))

    # 获取当前cookie
    def get_cookies(self):
        """获取当前页面所有的cookie"""
        allcookie = self.driver.get_cookies()
        return allcookie

    # 注入cookie
    def put_cookie(self, allcookie):
        """注入cookie"""
        for i in allcookie:
            self.driver.add_cookie(i)

    def save_cookies_to_file(self, file: str = 'cookies.txt'):
        # 首先获取cookies保存至本地
        cookies = self.get_cookies()
        # 转换成字符串保存
        json_cookies = json.dumps(cookies)
        # 保存到txt文件
        with open(file, 'w') as f:
            f.write(json_cookies)

    def add_exist_cookie(self, file: str = 'cookies.txt', domain: str = ''):
        with open(file, 'r', encoding='utf8') as f:
            cookies = json.loads(f.read())
        # 给浏览器添加cookies
        for i, cookie in enumerate(cookies):
            cookies[i] = {
                'domain': domain or cookie['domain'],
                'name': cookie['name'],
                'value': cookie['value'],
                "expiry": 4114659613,
                'path': cookie['path'],
                'sameSite': cookie['sameSite'],
                'httpOnly': cookie['httpOnly'],
                'secure': cookie['secure']
            }
        self.put_cookie(cookies)
        # 刷新网页，cookies才会成功
        self.driver.refresh()

    # 滑动页面到底部
    def slide_to_bottom(self):
        """滑动页面到底部"""
        js = "var q=document.documentElement.scrollTop=100000"
        self.driver.execute_script(js)
        time.sleep(1)

    # 滑动页面到顶部
    def slide_to_top(self):
        """滑动页面到顶部"""
        js = "var q=document.documentElement.scrollTop=0"
        self.driver.execute_script(js)
        time.sleep(1)

    # 验证码截取，保存
    def save_code_image(self, captcha_location: str = '', file: str = '/tmp/captcha.png'):
        self.driver.get_screenshot_as_file(str)
        element_code_img = self.driver.find_element(by=By.XPATH, value=captcha_location)
        left = element_code_img.location['x']
        top = element_code_img.location['y']
        right = left + element_code_img.size['width']
        bottom = top + element_code_img.size['height']
        im = Image.open(file)
        im = im.crop((left, top, right, bottom))
        im.save(file)

    def ops_cookies(self, cookie, login_url):
        # 清除cookie
        self.driver.delete_all_cookies()
        # 获取domain
        start = login_url.find('//') + 2  # 获取域名开始的位置
        domain = login_url[start:len(login_url)]  # 截取域名
        cookie_arr = str(cookie).split(";")
        cookies = []
        for i, cookie in enumerate(cookie_arr):
            _ = cookie.strip().split("=")
            name = _[0]
            value = _[1]
            cookies.append({
                'domain': domain,
                'name': name,
                'value': value,
                "expiry": 4114659613,
                'path': "/",
                'sameSite': 'None',
                'httpOnly': True,
                'secure': False
            })
        # 写入cookie
        self.put_cookie(cookies)

    def file_upload_by_pyautogui(self, location, file: str):
        """
        文件上传
        :param location:
        :param file:
        :return:
        """
        # https://stackoverflow.com/questions/8665072/how-to-upload-file-picture-with-selenium-python
        # (By.XPATH, "//button[@title='Open file selector']")
        element_present = EC.presence_of_element_located(location)  # Example xpath
        WebDriverWait(self.driver, 10).until(element_present).click()  # This opens the windows file selector
        # 'C:/path_to_file'
        pyautogui.write(file)
        # enter or 1
        pyautogui.press('enter')

    def asserts(self, expr, message: str = "校验错误", doc: str = ''):
        try:
            assert expr
        except AssertionError:
            # 断言失败时执行
            self.do_save_screenshot(doc)
            raise AssertionError(message)
