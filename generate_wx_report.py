#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/4/24
# @File    : generate_wx_report.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import os

import argparse

from common.dateTimeTool import DateTimeTool
from common.fileTool import FileTool

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', help='类型，【取决于config.json中配置的outputs路径】', type=str)
    parser.add_argument('-environment', '--cmd_environment', help='环境', type=str, default="production")
    args = parser.parse_args()

    result_dir = f'output/{args.type}/report/{args.cmd_environment}/wx_report_' + DateTimeTool.getNowTime('%Y_%m_%d_%H_%M_%S_%f')
    source_dir = f'output/{args.type}/report_data/'
    cmd = f"minireport {source_dir} {result_dir}"
    os.system(cmd)
    FileTool.truncateDir(source_dir)
    FileTool.delete_dir_file(source_dir)
