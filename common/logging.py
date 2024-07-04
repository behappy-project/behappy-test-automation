#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/6/4
# @File    : logger.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

from logging import DEBUG

from nb_log import get_logger, LogManager

logger = get_logger('default',
                    log_level_int=DEBUG,
                    do_not_use_color_handler=False,
                    log_file_size=100,
                    log_path='logs',
                    log_filename='nb_log.log',
                    is_add_stream_handler=True,
                    error_log_filename='error_nb_log.log')



