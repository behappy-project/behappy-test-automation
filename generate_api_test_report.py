#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/5/31
# @File    : generate_api_test_report.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from base.read_report_config import Read_Report_Config
from common.dateTimeTool import DateTimeTool
from common.logging import logger
from common.network import Network
from common.strTool import StrTool
import argparse
import multiprocessing
import platform
import subprocess

from init.api.api_init import clear as api_clear


def generate_windows_reports(test_time):
    generate_report_command = 'allure generate output/api/report_data -o output/api/report/api_report_%s' % test_time
    subprocess.check_output(generate_report_command, shell=True)
    # open_report_command = 'start cmd.exe @cmd /c "allure open -p %s output/api/report/api_report_%s"' % (
    # port, test_time)
    # subprocess.check_output(open_report_command, shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-nc', '--need_clear', help='是否清除测试case产生的数据', type=int, default=0)
    parser.add_argument('-environment', '--cmd_environment', help='环境', type=str, default='other')
    args = parser.parse_args()

    test_time = DateTimeTool.getNowTime('%Y_%m_%d_%H_%M_%S_%f')
    if 'Windows' == platform.system():
        logger.debug('%s生成报告' % (DateTimeTool.getNowTime()))
        process = multiprocessing.Process(target=generate_windows_reports, args=(test_time,))
        process.start()
        process.join()
    else:
        logger.debug('%s生成报告' % (DateTimeTool.getNowTime()))
        generate_report_command = 'allure generate output/api/report_data/%s -o output/api/report/%s/api_report_%s' % (
            test_time)
        subprocess.check_output(generate_report_command, shell=True)
        # open_report_command = 'nohup allure open -p %s output/api/report/api_report_%s >logs/generate_api_test_report_%s.log 2>&1 &' % (
        # port, test_time, test_time)
        # subprocess.check_output(open_report_command, shell=True)
    # 清理数据
    api_clear(args.need_clear, args.cmd_environment)
