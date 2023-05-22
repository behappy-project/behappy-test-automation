#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @File    : logger.py.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import logging
import os
import time
from logging.handlers import RotatingFileHandler

from Common.file_config import FileConfig

fmt = " %(asctime)s  %(levelname)s %(filename)s %(funcName)s [ line:%(lineno)d ] %(message)s"
datefmt = '%a, %d %b %Y %H:%M:%S'
handler_1 = logging.StreamHandler()
curTime = time.strftime("%Y-%m-%d %H%M", time.localtime())
handler_2 = RotatingFileHandler(FileConfig().get_path(type="logs") + "{0}TestAutomation_{1}.log".format(os.path.sep, curTime),
                                backupCount=20, encoding='utf-8')
print(handler_2)
# 设置rootlogger 的输出内容形式，输出渠道
logging.basicConfig(format=fmt, datefmt=datefmt, level=logging.INFO, handlers=[handler_1, handler_2])
