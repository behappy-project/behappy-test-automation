#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/4/24
# @File    : browserOperator.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import asyncio
import time
import pyautogui
import ujson
import threading
import traceback
from selenium.webdriver import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from base.read_web_ui_config import Read_WEB_UI_Config
from common.dateTimeTool import DateTimeTool
from common.logging import logger
from page_objects.createElement import CreateElement
from page_objects.web_ui.locator_type import Locator_Type
from pojo.elementInfo import ElementInfo
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from page_objects.web_ui.wait_type import Wait_Type as Wait_By
from PIL import Image
from selenium.webdriver.support import expected_conditions
import allure
import os


class BrowserOperator:
    """
    类中的element参数可以有selenium.webdriver.remote.webelement.WebElement和pojo.elementInfo.ElementInfo类型
    """

    def __init__(self, driver: WebDriver):
        self._config = Read_WEB_UI_Config().web_ui_config
        self._driver = driver

    def _change_element_to_webElement_type(self, element, highlight_seconds=5):
        if isinstance(element, ElementInfo):
            webElement = self.getElement(element, highlight_seconds)
        elif isinstance(element, WebElement):
            webElement = element
        elif isinstance(element, str):
            # 默认为xpath
            element_info = CreateElement.create(Locator_Type.XPATH, element, wait_type=Wait_By.PRESENCE_OF_ELEMENT_LOCATED)
            webElement = self.getElement(element_info, highlight_seconds)
        else:
            return element
        return webElement

    def is_element_exists(self, element, highlight_seconds=5):
        """
        判断元素是否存在
        :param highlight_seconds:
        :param element:
        :param loc:
        :param doc:
        :return:
        """
        try:
            self._change_element_to_webElement_type(element, highlight_seconds)
        except (NoSuchElementException, TimeoutException) as e:
            return False
        else:
            return True

    def get(self, url):
        self._driver.get(url)

    def get_by_ssl_popup(self, url, x: int, y: int):
        """
        用于需要证书校验的地址，但需要注意的是这样依赖就无法使用headless方式跑自动化
        :param x: 确认按钮的x像素, 谷歌浏览器默认为：1078
        :param y: 确认按钮的y像素, 谷歌浏览器默认为：355
        :param url:
        :return:
        """
        def threaded_get_url():
            # Calls the website
            self._driver.get(url)

        def threaded_press_enter():
            time.sleep(2)
            # 点击确认按钮
            pyautogui.leftClick(x, y)
        # Calling the website and pressing 10 times in the same time
        thread_press_enter = threading.Thread(target = threaded_press_enter)
        thread_press_enter.start()
        thread_get_url = threading.Thread(target = threaded_get_url)
        thread_get_url.start()

    def row_cell_get_table_text(self, element, row, cell, highlight_seconds=5):
        """
        根据输入的行列值，获取该行列单元格中的文本。
        :param highlight_seconds:
        :param element: 定位到table的定位语句[eg: //table[@id='myTable']]
        :param row: 行
        :param cell: 列
        :return: 单元格文本
        """
        element = "%s/tbody/tr[%s]/td[%s]" % (element, row, cell)
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            return webElement.text

    def text_get_table_row_cell(self, element, text):
        """
        通过xpath定位的方式，根据参数text中的文本返回文本所在的行列
        :param text:
        :param element: 定位到table的定位语句
        """
        # 获取行数，由于部分表格表头是用th而不是用td，可能会出现计算错误。因此这里先除去表头
        table_tr = self._driver.find_elements(by=By.XPATH, value=element + "/tbody/tr")[1:]
        row = len(table_tr)
        # 获取列数
        table_td = self._driver.find_elements(by=By.XPATH, value=element + "/tbody/tr/td")
        cell = int(len(table_td) / row)
        # 遍历table中的所有文本，并匹配的值返回所在的行列
        # xpath中下标取值从1开始，除去表头，需要从2开始
        for i in range(2, row + 2):
            for j in range(1, cell + 1):
                tl = element + "/tbody/tr[" + str(i) + "]/td[" + str(j) + "]"
                table_text = self._driver.find_element(by=By.XPATH, value=tl).text
                if text == table_text:
                    return i, j

    def get_current_url(self):
        return self._driver.current_url

    def getTitle(self):
        return self._driver.title

    def getText(self, element, highlight_seconds=5):
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            return webElement.text

    def click(self, element, highlight_seconds=5):
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            webElement.click()

    def submit(self, element, highlight_seconds=5):
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            webElement.submit()

    def backspace_clear(self, element, deviation=3, highlight_seconds=5):
        """
        退格原理清除输入框中的内容
        :param highlight_seconds:
        :param element: 元素
        :param deviation: 退格数偏差,默认会多输入3个以确保可靠度
        """
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            quantity = len(webElement.get_attribute("value")) + deviation
            for _ in range(quantity):
                webElement.send_keys(Keys.BACKSPACE)

    def clear_with_send(self, element, text: str, highlight_seconds=5):
        """
        清空输入框并且输入内容
        :param highlight_seconds:
        :param element: 需要操作的元素
        :param text: 输入的内容
        """
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            # 发送全选快捷键
            webElement.send_keys(Keys.CONTROL, "a")
            webElement.send_keys(text)

    def sendText(self, element, text, highlight_seconds=5):
        text = text
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            webElement.clear()
            webElement.send_keys(text)

    def send_keys(self, element, keys, highlight_seconds=5):
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            self._driver._is_remote = False
            webElement.send_keys(keys)
            self._driver._is_remote = True

    def is_displayed(self, element, highlight_seconds=5):
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            flag = webElement.is_displayed()
            return flag

    def is_enabled(self, element, highlight_seconds=5):
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            flag = webElement.is_enabled()
            return flag

    def is_selected(self, element, highlight_seconds=5):
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            flag = webElement.is_selected()
            return flag

    def select_dropDownBox_by_value(self, element, value, highlight_seconds=5):
        """
        适用单选下拉框
        :param element:
        :param value:
        :return:
        """
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            webElement = Select(webElement)
            webElement.select_by_value(value)

    def select_dropDownBox_by_text(self, element, text, highlight_seconds=5):
        """
        适用单选下拉框
        :param element:
        :param text:
        :return:
        """
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            webElement = Select(webElement)
            webElement.select_by_visible_text(text)

    def select_dropDownBox_by_index(self, element, index, highlight_seconds=5):
        """
        适用单选下拉框,下标从0开始
        :param element:
        :param index:
        :return:
        """
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            webElement = Select(webElement)
            webElement.select_by_index(index)

    def select_dropDownBox_by_values(self, element, values, highlight_seconds=5):
        """
        适用多选下拉框
        :param element:
        :param values:以数组传参
        :return:
        """
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            webElement = Select(webElement)
            webElement.deselect_all()
            for value in values:
                webElement.select_by_value(value)

    def select_dropDownBox_by_texts(self, element, texts, highlight_seconds=5):
        """
        适用多选下拉框
        :param element:
        :param texts:以数组传参
        :return:
        """
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            webElement = Select(webElement)
            webElement.deselect_all()
            for text in texts:
                webElement.select_by_visible_text(text)

    def select_dropDownBox_by_indexs(self, element, indexs, highlight_seconds=5):
        """
        适用多选下拉框，下标从0开始
        :param element:
        :param indexs: 以数组传参
        :return:
        """
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            webElement = Select(webElement)
            webElement.deselect_all()
            for index in indexs:
                webElement.select_by_index(index)

    def get_window_handles(self):
        """获得窗口句柄
        Returns:
            [type]: [description]
        """
        return self._driver.window_handles

    def get_current_window_handle(self):
        """获得当前的窗口句柄
        Returns:
            [type]: [description]
        """
        return self._driver.current_window_handle

    def open_new_window(self, url: str, window_name: str = "new_window"):
        """
        打开新的窗口
        :param url:
        :param window_name:
        :return:
        """
        # 执行JavaScript代码在当前窗口中打开新窗口
        self._driver.execute_script(f"window.open('{url}', '{window_name}')")
        # 切换到新窗口
        windows = self._driver.window_handles
        self._driver.switch_to.window(windows[-1])

    def switch_to_window(self, window_name):
        self._driver.switch_to.window(window_name)

    def maximize_window(self):
        """放大窗口
        """
        self._driver.maximize_window()

    def switch_to_frame(self, frame_reference):
        """_summary_

        Args:
            frame_reference (_type_): 支持窗口名、frame索引、(i)frame元素
        """
        frame_reference = self._change_element_to_webElement_type(frame_reference)
        self._driver.switch_to.frame(frame_reference)

    def switch_to_parent_frame(self):
        self._driver.switch_to.parent_frame()

    def page_forward(self):
        self._driver.forward()

    def page_back(self):
        self._driver.back()

    def web_alert(self, action_type='accept'):
        """
        :action_type accept、dismiss
        :return:
        """
        if action_type:
            action_type.lower()
        alert = self._driver.switch_to.alert
        if action_type == 'accept':
            alert.accept()
        elif action_type == 'dismiss':
            alert.dismiss()

    def get_alert_text(self):
        alert = self._driver.switch_to.alert
        return alert.text

    def snapAndGetPath(self, file_name: str = ''):
        file_name = DateTimeTool.getNowTime('%Y%m%d%H%M%S%f_') + file_name
        allure.attach(name=file_name,
                      body=self._driver.get_screenshot_as_png(),
                      attachment_type=allure.attachment_type.PNG)
        return file_name

    def attach_comment(self, comment: str = ""):
        """
        :param comment:
        :return:
        """
        name = '补充信息'
        allure.attach(name=name,
                      body=comment,
                      attachment_type=allure.attachment_type.TEXT)

    def refresh(self):
        self._driver.refresh()

    def uploadFile(self, element, filePath, highlight_seconds=5):
        """
        适用于元素为input且type="file"的文件上传
        :param element:
        :param filePath:
        :return:
        """
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            webElement.send_keys(os.path.abspath(filePath))

    def get_property(self, element, property_name, highlight_seconds=5):
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            return webElement.get_property(property_name)

    def get_attribute(self, element, attribute_name, highlight_seconds=5):
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            return webElement.get_attribute(attribute_name)

    def get_element_outer_html(self, element):
        return self.get_attribute(element, 'outerHTML')

    def get_element_inner_html(self, element):
        return self.get_attribute(element, 'innerHTML')

    def get_page_source(self):
        return self._driver.page_source

    def get_element_rgb(self, element, x_percent=0, y_percent=0):
        """
        获得元素上的rgb值,默认返回元素左上角坐标轴
        :param element
        :param x_percent x轴百分比位置,范围0~1
        :param y_percent y轴百分比位置,范围0~1
        """
        img = Image.open(self.save_element_image(element, 'element_rgb'))
        pix = img.load()
        width = img.size[0]
        height = img.size[1]
        return pix[width * x_percent, height * y_percent]

    def save_element_image(self, element, image_file_name="default", highlight_seconds=0):
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        left = webElement.location['x']
        top = webElement.location['y']
        right = webElement.location['x'] + webElement.size['width']
        bottom = webElement.location['y'] + webElement.size['height']
        # 进行屏幕截图
        image_file_name = DateTimeTool.getNowTime('%Y%m%d%H%M%S%f_') + '%s.png' % image_file_name
        if not os.path.exists('output/tmp/' + self._config.current_browser):
            os.mkdir('output/tmp/' + self._config.current_browser)
        image_file_name = os.path.abspath(
            'output/tmp/' + self._config.current_browser + '/' + image_file_name)
        self._driver.get_screenshot_as_file(image_file_name)
        img = Image.open(image_file_name)
        # 验证码图片裁切并保存
        img = img.crop((left, top, right, bottom))
        img.save(image_file_name)
        return image_file_name

    # def get_captcha(self, element, language='eng'):
    #     """
    #     识别图片验证码，如需使用该方法必须配置jpype1、字体库等依赖环境
    #     :param element: 验证码图片元素
    #     :param language: eng:英文,chi_sim:中文
    #     :return:
    #     """
    #     # 为防止截图包含高亮影响识别，元素不进行高亮
    #     # 识别图片验证码
    #     from common.captchaRecognitionTool import CaptchaRecognitionTool
    #     captcha_image_file_name = self.save_element_image(element, 'captcha')
    #     captcha = CaptchaRecognitionTool.captchaRecognition(captcha_image_file_name, language)
    #     captcha = captcha.strip()
    #     captcha = captcha.replace(' ', '')
    #     return captcha

    def get_table_data(self, element, data_type='text'):
        """
        以二维数组返回表格每一行的每一列的数据[[row1][row2][colume1,clume2]]
        :param element:
        :param data_type: text-返回表格文本内容,html-返回表格html内容,webElement-返回表格元素
        :return:
        """
        if isinstance(element, ElementInfo):
            # 由于表格定位经常会出现【StaleElementReferenceException: Message: stale element reference: element is not attached to the page document 】异常错误,
            # 解决此异常只需要用显示等待，保证元素存在即可，显示等待类型中visibility_of_all_elements_located有实现StaleElementReferenceException异常捕获,
            # 所以强制设置表格定位元素时使用VISIBILITY_OF
            element.wait_type = Wait_By.VISIBILITY_OF
            webElement = self.getElement(element)
        elif isinstance(element, WebElement):
            webElement = element
        else:
            return None
        table_data = []
        table_trs = webElement.find_elements(By.TAG_NAME, 'tr')
        try:
            # 为防止表格内的内容变化导致无法获取内容,进行异常捕获
            for tr in table_trs:
                tr_data = []
                tr_tds = tr.find_elements(By.TAG_NAME, 'td')
                if data_type.lower() == 'text':
                    for td in tr_tds:
                        tr_data.append(td.text)
                elif data_type.lower() == 'html':
                    for td in tr_tds:
                        tr_data.append(td.get_attribute('innerHTML'))
                elif data_type.lower() == 'webelement':
                    tr_data = tr_tds
                table_data.append(tr_data)
        except StaleElementReferenceException as e:
            logger.error('获取表格内容异常:' + e.msg)
        return table_data

    def scroll_to_show(self, element, highlight_seconds=5, is_top_align=True):
        """
        滚动页面直至元素可见
        :param element:
        :param highlight_seconds:
        :param is_top_align: 是否元素与窗口顶部对齐，否则与窗口底部对齐
        :return:
        """
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            if is_top_align:
                self._driver.execute_script("arguments[0].scrollIntoView();", webElement)
            else:
                self._driver.execute_script("arguments[0].scrollIntoView(false);", webElement)

    def move_by_offset(self, x, y):
        """鼠标左键点击，x为横坐标，y为纵坐标

        Args:
            x ([type]): [description]
            y ([type]): [description]
        """
        ActionChains(self._driver).move_by_offset(x, y).click().perform()

    def getElement(self, elementInfo, highlight_seconds=5):
        """
        定位单个元素
        :param highlight_seconds:
        :param elementInfo:
        :return:
        """
        webElement = None
        locator_type = elementInfo.locator_type
        locator_value = elementInfo.locator_value
        wait_type = elementInfo.wait_type
        wait_seconds = elementInfo.wait_seconds
        wait_expected_value = elementInfo.wait_expected_value
        if wait_expected_value:
            wait_expected_value = wait_expected_value

        # 查找元素,为了保证元素被定位,都进行显式等待
        if wait_type == Wait_By.TITLE_IS:
            webElement = WebDriverWait(self._driver, wait_seconds).until(
                expected_conditions.title_is(wait_expected_value))
        elif wait_type == Wait_By.TITLE_CONTAINS:
            webElement = WebDriverWait(self._driver, wait_seconds).until(
                expected_conditions.title_contains(wait_expected_value))
        elif wait_type == Wait_By.PRESENCE_OF_ELEMENT_LOCATED:
            webElement = WebDriverWait(self._driver, wait_seconds).until(
                expected_conditions.presence_of_element_located((locator_type, locator_value)))
        elif wait_type == Wait_By.ELEMENT_TO_BE_CLICKABLE:
            webElement = WebDriverWait(self._driver, wait_seconds).until(
                expected_conditions.element_to_be_clickable((locator_type, locator_value)))
        elif wait_type == Wait_By.ELEMENT_LOCATED_TO_BE_SELECTED:
            webElement = WebDriverWait(self._driver, wait_seconds).until(
                expected_conditions.element_located_to_be_selected((locator_type, locator_value)))
        elif wait_type == Wait_By.VISIBILITY_OF:
            webElements = WebDriverWait(self._driver, wait_seconds).until(
                (expected_conditions.visibility_of_all_elements_located((locator_type, locator_value))))
            if len(webElements) > 0:
                webElement = webElements[0]
        else:
            if locator_type == By.ID:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element(By.ID, locator_value))
            elif locator_type == By.NAME:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element(By.NAME, locator_value))
            elif locator_type == By.LINK_TEXT:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element(By.LINK_TEXT, locator_value))
            elif locator_type == By.XPATH:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element(By.XPATH, locator_value))
            elif locator_type == By.PARTIAL_LINK_TEXT:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element(By.PARTIAL_LINK_TEXT, locator_value))
            elif locator_type == By.CSS_SELECTOR:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element(By.CSS_SELECTOR, locator_value))
            elif locator_type == By.CLASS_NAME:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element(By.CLASS_NAME, locator_value))
            elif locator_type == By.TAG_NAME:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element(By.TAG_NAME, locator_value))
        if not wait_type == Wait_By.TITLE_IS and not wait_type == Wait_By.TITLE_CONTAINS:
            self.highLight(webElement, highlight_seconds)
        return webElement

    def getElements(self, elementInfo, highlight_seconds=5):
        """
        定位多个元素
        :param highlight_seconds:
        :param elementInfo:
        :return:
        """
        webElements = None
        locator_type = elementInfo.locator_type
        locator_value = elementInfo.locator_value
        wait_type = elementInfo.wait_type
        wait_seconds = elementInfo.wait_seconds

        # 查找元素,为了保证元素被定位,都进行显式等待
        if wait_type == Wait_By.PRESENCE_OF_ELEMENT_LOCATED:
            webElements = WebDriverWait(self._driver, wait_seconds).until(
                expected_conditions.presence_of_all_elements_located((locator_type, locator_value)))
        elif wait_type == Wait_By.VISIBILITY_OF:
            webElements = WebDriverWait(self._driver, wait_seconds).until(
                expected_conditions.visibility_of_all_elements_located((locator_type, locator_value)))
        else:
            if locator_type == By.ID:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements(By.ID, locator_value))
            elif locator_type == By.NAME:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements(By.NAME, locator_value))
            elif locator_type == By.LINK_TEXT:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements(By.LINK_TEXT, locator_value))
            elif locator_type == By.XPATH:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements(By.XPATH, locator_value))
            elif locator_type == By.PARTIAL_LINK_TEXT:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements(By.PARTIAL_LINK_TEXT, locator_value))
            elif locator_type == By.CSS_SELECTOR:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements(By.CSS_SELECTOR, locator_value))
            elif locator_type == By.CLASS_NAME:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements(By.CLASS_NAME, locator_value))
            elif locator_type == By.TAG_NAME:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements(By.TAG_NAME, locator_value))
        for webElement in webElements:
            self.highLight(webElement, highlight_seconds)
        return webElements

    def getSubElement(self, parent_element, sub_elementInfo, highlight_seconds=5):
        """
        获得元素的单个子元素
        :param highlight_seconds:
        :param parent_element: 父元素
        :param sub_elementInfo: 子元素,只能提供pojo.elementInfo.ElementInfo类型
        :return:
        """
        if isinstance(parent_element, ElementInfo):
            webElement = self.getElement(parent_element)
        elif isinstance(parent_element, WebElement):
            webElement = parent_element
        else:
            return None
        if not isinstance(sub_elementInfo, ElementInfo):
            return None

        # 通过父元素查找子元素
        locator_type = sub_elementInfo.locator_type
        locator_value = sub_elementInfo.locator_value
        wait_seconds = sub_elementInfo.wait_seconds

        # 查找元素,为了保证元素被定位,都进行显式等待
        if locator_type == By.ID:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element(By.ID, locator_value))
        elif locator_type == By.NAME:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element(By.NAME, locator_value))
        elif locator_type == By.LINK_TEXT:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element(By.LINK_TEXT, locator_value))
        elif locator_type == By.XPATH:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element(By.XPATH, locator_value))
        elif locator_type == By.PARTIAL_LINK_TEXT:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element(By.PARTIAL_LINK_TEXT, locator_value))
        elif locator_type == By.CSS_SELECTOR:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element(By.CSS_SELECTOR, locator_value))
        elif locator_type == By.CLASS_NAME:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element(By.CLASS_NAME, locator_value))
        elif locator_type == By.TAG_NAME:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element(By.TAG_NAME, locator_value))
        else:
            return None
        self.highLight(subWebElement, highlight_seconds)
        return subWebElement

    def getSubElements(self, parent_element, sub_elementInfo, highlight_seconds=5):
        """
        获得元素的多个子元素
        :param highlight_seconds:
        :param parent_element: 父元素
        :param sub_elementInfo: 子元素,只能提供pojo.elementInfo.ElementInfo类型
        :return:
        """
        if isinstance(parent_element, ElementInfo):
            webElement = self.getElement(parent_element)
        elif isinstance(parent_element, WebElement):
            webElement = parent_element
        else:
            return None
        if not isinstance(sub_elementInfo, ElementInfo):
            return None

        # 通过父元素查找多个子元素
        locator_type = sub_elementInfo.locator_type
        locator_value = sub_elementInfo.locator_value
        wait_seconds = sub_elementInfo.wait_seconds

        # 查找元素,为了保证元素被定位,都进行显式等待
        if locator_type == By.ID:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements(By.ID, locator_value))
        elif locator_type == By.NAME:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements(By.NAME, locator_value))
        elif locator_type == By.LINK_TEXT:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements(By.LINK_TEXT, locator_value))
        elif locator_type == By.XPATH:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements(By.XPATH, locator_value))
        elif locator_type == By.PARTIAL_LINK_TEXT:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements(By.PARTIAL_LINK_TEXT, locator_value))
        elif locator_type == By.CSS_SELECTOR:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements(By.CSS_SELECTOR, locator_value))
        elif locator_type == By.CLASS_NAME:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements(By.CLASS_NAME, locator_value))
        elif locator_type == By.TAG_NAME:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements(By.TAG_NAME, locator_value))
        else:
            return None
        for subWebElement in subWebElements:
            self.highLight(subWebElement, highlight_seconds)
        return subWebElements

    def explicit_wait_page_title(self, elementInfo):
        """
        显式等待页面title
        :param elementInfo:
        :return:
        """
        self.getElement(elementInfo)

    def highLight(self, webElement, seconds=5):
        try:
            # 进行StaleElementReferenceException异常捕获
            self._driver.execute_script("element = arguments[0];" +
                                        "original_style = element.getAttribute('style');" +
                                        "element.setAttribute('style', original_style + \";" +
                                        " border: 3px dashed rgb(250,0,255);\");" +
                                        "setTimeout(function(){element.setAttribute('style', original_style);}, " + str(
                seconds * 1000) + ");",
                                        webElement)
        except StaleElementReferenceException as e:
            logger.error('高亮StaleElementReferenceException异常:' + e.msg)

    def arguments_click(self, element, highlight_seconds=5):
        """
        使用arguments[0].click();的方式点击按钮
        :param element:
        :param highlight_seconds:
        :return:
        """
        webElement = self._change_element_to_webElement_type(element, highlight_seconds)
        if webElement:
            self._driver.execute_script("arguments[0].click();", webElement)

    @property
    def driver(self):
        return self._driver

    def get_cookies(self):
        """
        获取当前cookie
        :return:
        """
        """获取当前页面所有的cookie"""
        allcookie = self._driver.get_cookies()
        return allcookie

    # 注入cookie
    def put_cookie(self, allcookie):
        """注入cookie"""
        for i in allcookie:
            self._driver.add_cookie(i)

    def save_cookies_to_file(self, file: str = 'cookies.txt'):
        # 首先获取cookies保存至本地
        cookies = self.get_cookies()
        # 转换成字符串保存
        json_cookies = ujson.dumps(cookies)
        # 保存到txt文件
        with open(file, 'w') as f:
            f.write(json_cookies)

    def add_exist_cookie(self, file: str = 'cookies.txt', domain: str = ''):
        """
        添加已存在cookie
        :param file:
        :param domain:
        :return:
        """
        with open(file, 'r', encoding='utf8') as f:
            cookies = ujson.loads(f.read())
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
        self._driver.refresh()

    def ops_cookies(self, cookie, login_url):
        # 清除cookie
        self._driver.delete_all_cookies()
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

    def close(self):
        self._driver.close()
