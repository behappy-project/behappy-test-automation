#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @File    : clear_cache.py.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import os
import platform
import shutil

from Common.file_config import FileConfig


# 删除文件
def delete_file(*path):
    # 清除输入结果中的内容
    for path in [*path]:
        all_log_files = os.listdir(path)
        all_log_files.sort()
        # 遍历
        for num in range(len(all_log_files)):
            if os.path.basename(os.path.join(path, all_log_files[num])) != "__init__.py":
                try:
                    os.remove(os.path.join(path, all_log_files[num]))
                except:
                    shutil.rmtree(os.path.join(path, all_log_files[num]))


# 清除历史数据
def clear_cache():
    # 清除上一次pytest运行缓存
    if platform.system() == "Windows":
        cache_dir = os.path.join(FileConfig().base_dir + "\.pytest_cache")
    # Linux系统
    else:
        cache_dir = os.path.join(FileConfig().base_dir + "/.pytest_cache")
    shutil.rmtree(cache_dir)


if __name__ == "__main__":
    pass
