#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/4/24
# @File    : generate_wx_test_report.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import platform
import subprocess

import argparse

from common.custom_multiprocessing import Custom_Pool
from common.dateTimeTool import DateTimeTool
from common.logging import logger
from init.web_ui.web_ui_init import clear as clear_web_ui


def generate_windows_reports(report_dir, test_time, cmd_environment):
    generate_report_command = 'allure generate %s/report_data/%s -o %s/report/%s/web_ui_report_%s' % (
    report_dir, cmd_environment, report_dir, cmd_environment, test_time)
    subprocess.check_output(generate_report_command, shell=True)
    # open_report_command = 'start cmd.exe @cmd /c "allure open -p %s %s/report/web_ui_report_%s"' % (
    # port, report_dir, test_time)
    # subprocess.check_output(open_report_command, shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ie', help='是否针对ie生成报告', type=bool, default=False)
    parser.add_argument('-c', '--chrome', help='是否针对chrome生成报告', type=bool, default=True)
    parser.add_argument('-f', '--firefox', help='是否针对firefox生成报告', type=bool, default=False)
    parser.add_argument('-nc', '--need_clear', help='是否清除测试case产生的数据', type=int, default=0)
    parser.add_argument('-environment', '--cmd_environment', help='环境', type=str, default='other')
    args = parser.parse_args()
    ie = False
    chrome = False
    firefox = False
    if args.ie:
        ie = args.ie
    if args.chrome:
        chrome = args.chrome
    if args.firefox:
        firefox = args.firefox
    test_time = DateTimeTool.getNowTime('%Y_%m_%d_%H_%M_%S_%f')
    if 'Windows' == platform.system():
        # 初始化进程池
        p_pool = Custom_Pool(3)
        if ie:
            logger.debug('%s生成ie报告' % (DateTimeTool.getNowTime()))
            p = p_pool.apply_async(generate_windows_reports, ('output/web_ui/ie', test_time, args.cmd_environment))
        if chrome:
            logger.debug('%s生成chrome报告' % (DateTimeTool.getNowTime()))
            p = p_pool.apply_async(generate_windows_reports, ('output/web_ui/chrome', test_time, args.cmd_environment))
        if firefox:
            logger.debug('%s生成firefox报告' % (DateTimeTool.getNowTime()))
            p = p_pool.apply_async(generate_windows_reports, ('output/web_ui/firefox', test_time, args.cmd_environment))
        p_pool.close()
        p_pool.join()
    else:
        # 获得当前allure所有进程id
        get_allure_process_ids_command = "ps -ef|grep -i allure\\.CommandLine|grep -v grep|awk '{print $2}'"
        allure_process_ids = subprocess.check_output(get_allure_process_ids_command, shell=True)
        allure_process_ids = allure_process_ids.decode('utf-8')
        allure_process_ids = allure_process_ids.split('\n')
        if ie:
            logger.debug('%s生成ie报告' % (DateTimeTool.getNowTime()))
            generate_report_command = 'allure generate output/web_ui/ie/report_data/%s -o output/web_ui/ie/report/%s/web_ui_report_%s' % (
                args.cmd_environment, args.cmd_environment, test_time)
            subprocess.check_output(generate_report_command, shell=True)
            # open_report_command = 'nohup allure open -p %s output/web_ui/ie/report/web_ui_report_%s >logs/generate_web_ui_test_ie_report_%s.log 2>&1 &' % (
            # ieport, test_time, test_time)
            # subprocess.check_output(open_report_command, shell=True)
        if chrome:
            logger.debug('%s生成chrome报告' % (DateTimeTool.getNowTime()))
            generate_report_command = 'allure generate output/web_ui/chrome/report_data/%s -o output/web_ui/chrome/report/%s/web_ui_report_%s' % (
                args.cmd_environment, args.cmd_environment, test_time)
            subprocess.check_output(generate_report_command, shell=True)
            # open_report_command = 'nohup allure open -p %s output/web_ui/chrome/report/web_ui_report_%s >logs/generate_web_ui_test_chrome_report_%s.log 2>&1 &' % (
            # chromeport, test_time, test_time)
            # subprocess.check_output(open_report_command, shell=True)
        if firefox:
            logger.debug('%s生成firefox报告' % (DateTimeTool.getNowTime()))
            generate_report_command = 'allure generate output/web_ui/firefox/report_data/%s -o output/web_ui/firefox/report/%s/web_ui_report_%s' % (
                args.cmd_environment, args.cmd_environment, test_time)
            subprocess.check_output(generate_report_command, shell=True)
            # open_report_command = 'nohup allure open -p %s output/web_ui/firefox/report/web_ui_report_%s >logs/generate_web_ui_test_firefox_report_%s.log 2>&1 &' % (
            # firefoxport, test_time, test_time)
            # subprocess.check_output(open_report_command, shell=True)
    # 清理数据
    clear_web_ui(args.need_clear, args.cmd_environment)
    logger.debug('%s结束......' % DateTimeTool.getNowTime())
