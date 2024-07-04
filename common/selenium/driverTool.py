#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/4/24
# @File    : driverTool.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import pyautogui

from base.read_web_ui_config import Read_WEB_UI_Config
from selenium import webdriver
from selenium.webdriver.ie import webdriver as ie_webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium.webdriver.chrome.options import Options as Chrome_Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.ie.service import Service as IEService
from selenium.webdriver.firefox.service import Service as FireFoxService


class DriverTool:

    @classmethod
    def get_driver(cls, is_remote, selenium_hub, browser_type):
        """
        ie和firefox仅支持remote
        :param is_remote:
        :param selenium_hub:
        :param browser_type:
        :return:
        """
        driver = None
        browser_type = browser_type.lower()
        download_file_content_types = "application/octet-stream,application/vnd.ms-excel,text/csv,application/zip,application/binary"

        if browser_type == 'ie':
            opt = ie_webdriver.Options()
            opt.force_create_process_api = True
            opt.ensure_clean_session = True
            opt.add_argument('-private')
            ie_capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
            ie_capabilities.update(opt.to_capabilities())
            driver = webdriver.Remote(selenium_hub,
                                      keep_alive=False,
                                      options=opt)
        elif browser_type == 'firefox':
            firefox_profile = FirefoxProfile()
            # firefox_profile参数可以在火狐浏览器中访问about:config进行查看
            firefox_profile.set_preference('browser.download.folderList', 2)  # 0是桌面;1是“我的下载”;2是自定义
            firefox_profile.set_preference('browser.download.dir', Read_WEB_UI_Config().web_ui_config.download_dir)
            firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', download_file_content_types)
            firefox_options = Firefox_Options()
            if Read_WEB_UI_Config().web_ui_config.is_firefox_headless.lower() == 'true':
                firefox_options.add_argument('--headless')
            firefox_options.profile = firefox_profile
            firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
            firefox_capabilities.update(firefox_options.to_capabilities())

            driver = webdriver.Remote(selenium_hub,
                                      keep_alive=False,
                                      options=firefox_options)
        elif browser_type == 'chrome':
            chrome_options = Chrome_Options()
            prefs = {'download.default_directory': Read_WEB_UI_Config().web_ui_config.download_dir,
                     'profile.default_content_settings.popups': 0}

            chrome_options.add_experimental_option('prefs', prefs)
            chrome_options.add_argument('--ignore-certificate-errors')

            width, height = pyautogui.size()
            chrome_options.add_argument('--window-size=%sx%s' % (width, height))
            chrome_options.add_argument('--disable-gpu')
            # 隐藏滚动条, 应对一些特殊页面
            chrome_options.add_argument('--hide-scrollbars')
            if Read_WEB_UI_Config().web_ui_config.is_chrome_headless.lower() == 'true':
                chrome_options.add_argument('--headless')

            chrome_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
            chrome_capabilities.update(chrome_options.to_capabilities())

            if int(is_remote) == 0:
                service = ChromeService(executable_path=selenium_hub)
                driver = webdriver.Chrome(service=service, options=chrome_options, keep_alive=False)
            else:
                driver = webdriver.Remote(selenium_hub,
                                          keep_alive=False,
                                          options=chrome_options)
        else:
            return driver
        driver.maximize_window()
        driver.delete_all_cookies()
        return driver
