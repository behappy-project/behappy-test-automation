#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/4/24
# @File    : run_web_ui_test.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from base.read_web_ui_config import Read_WEB_UI_Config
from common.dateTimeTool import DateTimeTool
from common.fileTool import FileTool
from common.httpclient.doRequest import DoRequest
from common.logging import logger
from common.pytest import deal_pytest_ini_file
from init.web_ui.web_ui_init import clear as clear_web_ui
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.remote.command import Command
import argparse
import ujson
import pytest
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--keyword', help='只执行匹配关键字的用例，会匹配文件名、类名、方法名', type=str)
    parser.add_argument('-d', '--dir', help='指定要测试的目录', type=str)
    parser.add_argument('-m', '--markexpr', help='只运行符合给定的mark表达式的测试', type=str)
    parser.add_argument('-s', '--capture', help='是否在标准输出流中输出日志,1:是、0:否,默认为0', type=str)
    parser.add_argument('-r', '--reruns', help='失败重跑次数,默认为0', type=str)
    parser.add_argument('-lf', '--lf', help='是否运行上一次失败的用例,1:是、0:否,默认为0', type=str)
    parser.add_argument('-clr', '--clr', help='是否清空已有测试结果,1:是、0:否,默认为0', type=str)
    # 测试并发数,由于ie浏览器并发下经常定位不到,故测试ie浏览器时建议设置为1
    parser.add_argument('-n', '--num', help='并发测试进程数,默认串行', type=str)
    parser.add_argument('-environment', '--cmd_environment', help='环境', type=str, default='other')
    parser.add_argument('-nc', '--need_clear', help='是否清除测试case产生的数据', type=int, default=1)
    args = parser.parse_args()

    logger.debug('%s开始初始化......' % DateTimeTool.getNowTime())
    config = Read_WEB_UI_Config().web_ui_config
    doRquest = DoRequest(config.selenium_hub)
    if int(config.is_remote) == 1:
        try:
            logger.debug('%s开始检测selenium server是否可用......' % DateTimeTool.getNowTime())
            httpResponseResult = doRquest.get('/status')
            if httpResponseResult.status_code == 200:
                logger.debug('%sselenium server状态为可用......' % DateTimeTool.getNowTime())
            else:
                logger.error('%sselenium server状态为不可用' % DateTimeTool.getNowTime())
                sys.exit('%sselenium server状态为不可用' % DateTimeTool.getNowTime())
        except:
            logger.error('%sselenium server状态为不可用' % DateTimeTool.getNowTime())
            sys.exit('%sselenium server状态为不可用' % DateTimeTool.getNowTime())

    # 处理pytest文件
    deal_pytest_ini_file()

    logger.debug('%s初始化完成......' % DateTimeTool.getNowTime())

    logger.debug('%s开始测试......' % DateTimeTool.getNowTime())
    exit_code = 0
    for current_browser in config.test_browsers:
        logger.debug('%s开始%s浏览器测试......' % (DateTimeTool.getNowTime(), current_browser))
        # 由于pytest的并发插件xdist采用子进程形式，当前主进程的单例在子进程中会重新创建，所以将每次要测试的浏览器信息写入到文件中，
        # 保证子进程能够正确读取当前要测试的浏览器
        FileTool.replaceFileContent('config/web_ui_config.conf', '\r\n', '\n')
        FileTool.replaceFileContentWithLBRB('config/web_ui_config.conf', '=' + current_browser, 'current_browser', '\n')
        # 执行pytest前的参数准备
        pytest_execute_params = ['-c', 'config/pytest.ini', '-v', '--alluredir',
                                 'output/web_ui/' + current_browser + '/report_data/' + args.cmd_environment + '/']
        # 判断目录参数
        dir = 'cases/web_ui/'
        if args.dir:
            dir = args.dir
        # 判断关键字参数
        if args.keyword:
            pytest_execute_params.append('-k')
            pytest_execute_params.append(args.keyword)
        # 判断markexpr参数
        if args.markexpr:
            pytest_execute_params.append('-m')
            pytest_execute_params.append(args.markexpr.replace(",", " or "))
        # 判断是否输出日志
        if args.capture:
            if int(args.capture):
                pytest_execute_params.append('-s')
        # 判断是否失败重跑
        if args.reruns:
            if int(args.reruns):
                pytest_execute_params.append('--reruns')
                pytest_execute_params.append(args.reruns)
        # 判断是否只运行上一次失败的用例
        if args.lf:
            if int(args.lf):
                pytest_execute_params.append('--lf')
        # 判断是否清空已有测试结果
        if args.clr:
            if int(args.clr):
                pytest_execute_params.append('--clean-alluredir')
        # 是否执行并发测试
        if args.num:
            pytest_execute_params.append('-n')
            pytest_execute_params.append(args.num)
            pytest_execute_params.append('--dist')
            pytest_execute_params.append('load')

        # 环境
        pytest_execute_params.append('--cmd_environment')
        pytest_execute_params.append(args.cmd_environment)

        pytest_execute_params.append(dir)
        tmp_exit_code = pytest.main(pytest_execute_params)
        if not tmp_exit_code == 0:
            exit_code = tmp_exit_code
        logger.debug('%s结束%s浏览器测试......' % (DateTimeTool.getNowTime(), current_browser))

    if int(config.is_remote) == 1:
        logger.debug('%s清除未被关闭的浏览器......' % DateTimeTool.getNowTime())
        try:
            httpResponseResult = doRquest.get('/sessions')
            if httpResponseResult.status_code == 200:
                httpResLoads = ujson.loads(httpResponseResult.body)
                if httpResLoads['value'] and len(httpResLoads['value']) > 0:
                    conn = RemoteConnection(config.selenium_hub, True)
                    for session in httpResLoads['value']:
                        session_id = session['id']
                        conn.execute(Command.QUIT, {'sessionId': session_id})
            else:
                logger.error('%s清除未关闭浏览器异常:\r\n%s' % (DateTimeTool.getNowTime(), httpResponseResult.body))
        except Exception as e:
            logger.error('%s清除未关闭浏览器异常:\r\n%s' % (DateTimeTool.getNowTime(), e.args.__str__()))
        logger.debug('%s清除未被关闭的浏览器完成......' % DateTimeTool.getNowTime())

    clear_web_ui(args.need_clear, args.cmd_environment)

    logger.debug('%s结束测试......' % DateTimeTool.getNowTime())
