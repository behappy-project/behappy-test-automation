#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/4/24
# @File    : run_web_ui_test.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import sys
import os
import time

import argparse


from common.dateTimeTool import DateTimeTool
from common.logging import logger
from init.web_ui.web_ui_init import clear as clear_web_ui

if __name__ == '__main__':
    # case_type：
    # - byCases: 执行对应的case文件中的指定cases：test_weapp_u_adapt_lsc1
    # - byFile: 执行对应case文件中的所有cases：test_Weapp_U.test_data_assert
    # - bySuite: 按照`wx-suite.json`文件中的配置执行所有case：wx-suite.json
    # configJson: 对应多账号
    # - mode parallel: 并行模式，每个开发者工具按后台优先级算法进行分配
    parser = argparse.ArgumentParser()
    parser.add_argument('-ct', '--case_type', help='执行case类型[可选值: byCases,byFile,bySuite]', type=str)
    parser.add_argument('-cf', '--case_file', help='执行case文件[eg: test_Weapp_U.test_data_assert]', type=str)
    parser.add_argument('-cn', '--case_name', help='执行case名称[eg: test_weapp_case]', type=str)
    parser.add_argument('-cj', '--config_json', help='configJson文件路径[eg: config/wx_u_project/config.json]',
                        type=str)
    parser.add_argument('-cs', '--config_suite', help='suiteJson文件路径[eg: config/wx_u_project/suite.json]',
                        type=str)
    parser.add_argument('-environment', '--cmd_environment', help='环境', type=str, default="production")
    parser.add_argument('-l', '--local', help='是否是本地开发[调试阶段，默认为True]', type=int, default=1)
    parser.add_argument('-nc', '--need_clear', help='是否清除测试case产生的数据', type=int, default=1)
    args = parser.parse_args()

    logger.debug('%s开始初始化......' % DateTimeTool.getNowTime())
    logger.debug('%s结束初始化......' % DateTimeTool.getNowTime())
    logger.debug('%s开始测试......' % DateTimeTool.getNowTime())

    if args.local == 1:
        import minium
        from common.wx.basedef import BaseDef
        from base.wx.demo_project.demo_project_client import Demo_Project_Client

        Demo_Project_Client().projectConfig.environment = args.cmd_environment
        config = Demo_Project_Client().projectConfig

        mini = minium.Minium({
            "project_path": config.project_path,
            "dev_tool_path": config.dev_tool_path,
        })

        base_def = BaseDef(mini)
        mini.shutdown()
    else:
        match args.case_type:
            case 'byCases':
                caseFile = args.case_file
                caseName = args.case_name
                configJson = args.config_json
                cmd = f"minitest -m cases.wx.{caseFile} --case {caseName} -c {configJson}"
            case "byFile":
                caseFile = args.case_file
                configJson = args.config_json
                suiteJson = args.config_suite
                cmd = f"minitest -m cases.wx.{caseFile} -s {suiteJson} -c {configJson} --mode parallel"
            case "bySuite":
                configJson = args.config_json
                suiteJson = args.config_suite
                cmd = f"minitest -s {suiteJson} -c {configJson} --mode parallel"
            case _:
                logger.error("执行指令错误~")
                sys.exit(0)
        os.system(cmd)

    logger.debug('%s结束测试......' % DateTimeTool.getNowTime())
