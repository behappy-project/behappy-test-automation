#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/17
# @File    : modules.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import ast
import random
import string
import yaml

from Common import logger


def generate_random_str(length=4, only_number=False):
    """
    随机抽取length个字符组成一个字符串
    :param only_number:
    :param length:
    :return:
    """
    if only_number:
        characters = string.digits
    else:
        characters = string.ascii_lowercase + string.digits
    # 生成a-z和0-9的所有字符
    # 从字符集中随机选择length个字符，生成随机字符串
    random_string = ''.join(random.choices(characters, k=length))
    return random_string

def add_space(s: str):
    """
    字符串中间添加空格
    :param s:
    :return:
    """
    s1 = []
    count = 0
    for i in s:
        s1.append(i)
        count += 1
        if count == len(s):
            continue
        s1.append(' ')
    return "".join(s1)

def save_dict_to_yaml(dict_value: dict, save_path: str):
    """
    dict保存为yaml
    """
    #save_path = os.path.join(os.getcwd(), save_path)  # Define save path with specific file path and name
    try:
        # directory = os.path.dirname(save_path)
        # if not os.path.exists(directory):
        #     os.makedirs(directory)
        # json 转dict ，只能处理 键是双引号的，所以这里先转字符串紧接着利用ast.literal_eval进行dict二次转换
        dict_value = ast.literal_eval(str(dict_value))
        with open(save_path, 'w+', encoding='utf-8') as file:
            # Add input validation to ensure only trusted data is being passed to yaml.dump
            if isinstance(dict_value, dict):
                yam_str = yaml.dump(dict_value, default_style='+', indent=1, default_flow_style=False, allow_unicode=True, explicit_start=True, explicit_end=True, sort_keys=True)
                print(yam_str)
                file.write(yam_str)
            else:
                print("Error: dict_value must be a dictionary")
    except Exception as e:
        # Add error handling to gracefully handle any errors that occur and provide useful feedback to the user
        print(f"Error: {e}")


def read_yaml_to_dict(yaml_path: str, ):
    with open(yaml_path, mode='r', encoding='utf-8') as file:
        dict_value = yaml.load(file.read(), Loader=yaml.FullLoader)
        return dict_value


def append_content(path: str, content: str):
    # https://blog.csdn.net/weixin_39038035/article/details/130988813
    content = content.encode('utf-8')
    with open(path, mode='ab') as file:
        file.write(content)
