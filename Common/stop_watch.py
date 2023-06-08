#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/6/6
# @File    : stop_watch.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import time


class StopWatch:
    """
    eg:
    # 创建 Stopwatch 对象
    stopwatch = StopWatch()
    # 启动计时器
    stopwatch.start()
    # 停止计时器
    stopwatch.stop()
    # do something
    # 计算时间
    stopwatch.elapsed_time()
    """
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self):
        self.end_time = time.perf_counter()

    def elapsed_time(self):
        if self.start_time is None:
            raise RuntimeError("Stopwatch has not been started.")
        if self.end_time is None:
            return time.perf_counter() - self.start_time
        else:
            return self.end_time - self.start_time
