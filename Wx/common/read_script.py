#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import json
import os

object_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
file = os.path.join(object_path, "script/script.json").replace("\\", "/")


def get_path(file):
    # 用于获取当前目录的根目录路径
    def find_project_root():
        current_dir = os.getcwd()
        while not os.path.exists(os.path.join(current_dir, 'README.md')):
            if current_dir == os.path.dirname(current_dir):
                return None  # 达到文件系统根目录但未找到项目根目录
            current_dir = os.path.dirname(current_dir)
        return (current_dir + "/Wx/").replace('\\', '/')

    root = find_project_root()

    with open(file, encoding="UTF-8") as f:
        data = json.load(f)

    # 读取脚本文件中的commands字段
    for path in data['commands']:
        if 'path' in path:
            # 获取path字段的值，用于生成目录
            path_parts = path["path"].split('/')
            current_path = os.path.join(root, "pages")
            existing_directories = set()

            for part in path_parts:
                if part not in ['pro', 'page', 'homepage']:
                    # 更改文件名，python文件名不能用-起名
                    part = str(part).replace("-", "_")
                    current_path = os.path.join(current_path, part)
                    # 判断文件夹是否存在
                    if part not in existing_directories:
                        os.makedirs(current_path, exist_ok=True)
                        py_file = os.path.join(current_path, f"{part}.py")
                        # 判断文件是否存在
                        if os.path.exists(py_file):
                            pass
                        else:
                            open(py_file, 'w').close()
                    existing_directories.add(part)


# 获取target元素和文字
def get(file):
    with open(file, encoding="UTF-8") as f:
        data = json.load(f)
    for command in data['commands']:
        if 'target' in command and command["command"] == "tap":
            target = command['target']
            text = command["text"]
            path = command["path"]
            print("按钮名称：" + (text or '空'), "\n")
            print("所属页面【元素所在的页面路径】：" + path, "\n")
            print("xpath表达式【目标元素的xpath表达式】：" + target, "\n")
        elif 'target' in command and command["command"] == "input":
            input = command["target"]
            print("input输入框按钮：" + input, "\n")
        elif 'target' in command and command["command"] == "confirm":
            input = command["target"]
            print("此处回车：" + input, "\n")


get(file)
get_path(file)
