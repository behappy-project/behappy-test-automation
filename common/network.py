#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/4/25
# @File    : network.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import socket

from common.logging import logger


class Network:
    @classmethod
    def get_local_ip(cls):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            host = s.getsockname()[0]
            return host
        except:
            logger.error('通过UDP协议获取IP出错')
            hostname = socket.gethostname()
            host = socket.gethostbyname(hostname)
        return host
