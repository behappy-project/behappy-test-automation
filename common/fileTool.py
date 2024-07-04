#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/4/25
# @File    : fileTool.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import ast
import base64
import os
import re

import ddddocr

ocr = ddddocr.DdddOcr(show_ad=False, beta=True)
import ujson
import yaml
# requests库依赖会安装charset_normalizer
from charset_normalizer import detect
import shutil
from common.logging import logger


class FileTool:

    @classmethod
    def getChardet(cls, filePath):
        """
        获取文件编码格式，比如utf-8、GB2312
        :param filePath:
        :return:
        """
        with open(filePath, 'rb') as f:
            cur_encoding = detect(f.read())['encoding']
            f.close()
        return cur_encoding

    @classmethod
    def writeObjectIntoFile(cls, obj, filePath, encoding='utf-8'):
        """
        将对象转为json字符串，写入到文件
        :param obj:
        :param filePath:
        :return:
        """
        str = ujson.dumps(obj)
        with open(filePath, 'w', encoding=encoding) as f:
            f.write(str)
            f.close()

    @classmethod
    def readJsonFromFile(cls, filePath, encoding='utf-8'):
        """
        从文件里读取json字符串
        :param filePath:
        :return:
        """
        with open(filePath, 'r', encoding=encoding) as f:
            result = f.read()
            f.close()
        result = ujson.loads(result)
        return result

    @classmethod
    def truncateFile(cls, fielPath, encoding='utf-8'):
        """
        清空文件
        :param fielPath:
        :return:
        """
        with open(fielPath, 'r+', encoding=encoding) as f:
            f.truncate()
            f.close()

    @classmethod
    def truncateDir(cls, dirPath, regexs=None):
        """
        清空整个目录的内容
        :param dirPath:
        :param regexs: 正则匹配的文件名，以数组存放多个正则表达式
        :return:
        """
        for path, dirs, files in os.walk(dirPath):
            for file in files:
                filePath = os.path.join(path, file)
                if regexs:
                    pattern = '|'.join(regexs)
                    if re.match(pattern, file):
                        os.remove(filePath)
                else:
                    os.remove(filePath)

    @classmethod
    def delete_dir_file(cls, dir_path):
        """
        删除整个目录
        :param dir_path:
        :return:
        """
        """
        递归删除文件夹下文件和子文件夹里的文件，不会删除空文件夹
        :param dir_path: 文件夹路径
        :return:
        """
        if not os.path.exists(dir_path):
            return
        # 判断是不是一个文件路径，并且存在
        if os.path.isfile(dir_path) and os.path.exists(dir_path):
            os.remove(dir_path)  # 删除单个文件
        else:
            file_list = os.listdir(dir_path)
            for file_name in file_list:
                cls.delete_dir_file(os.path.join(dir_path, file_name))
        # 递归删除空文件夹
        if os.path.exists(dir_path):
            os.rmdir(dir_path)

    @classmethod
    def replaceFileLineContent(cls, filePath, match_keyword, old, new, encoding='utf-8'):
        """
        根据关键字匹配文档中的行，对行内容进行替换
        :param filePath: 文档路径
        :param match_keyword: 用于匹配文档中包含的关键字行
        :param old: 匹配的行中包含的字符串
        :param new: 用于替换匹配的行中的旧字符串
        :return:
        """
        with open(filePath, 'r', encoding=encoding) as f:
            new_lines = []
            lines = f.readlines()
            for line in lines:
                if match_keyword in line:
                    line = line.replace(old, new)
                new_lines.append(line)
            f.close()

            with open(filePath, 'w+', encoding=encoding) as f:
                f.writelines(new_lines)
                f.close()

    @classmethod
    def replaceFileContent(cls, filePath, old, new, replaceNum=-1, replaceOffset=0, encoding='utf-8'):
        """
        替换文档中的内容,支持替换全部、替换指定前几个、替换第N个
        :param filePath: 文档路径
        :param old: 要替换的字符串
        :param new: 要替换的新字符串
        :param replaceNum: 从头开始替换。-1代表替换所有；-2代表该参数无效，replaceOffset参数生效
        :param replaceOffset: 替换第几个，下标从0开始，
        :return:
        """
        with open(filePath, 'r', encoding=encoding) as f:
            content = f.read()
            if int(replaceNum) == -1:
                content = content.replace(old, new)
            elif not int(replaceNum) == -2:
                # 参数为整数
                replaceNum = abs(replaceNum)
                content = re.sub(old, new, content, replaceNum)
            else:
                # 参数为-2
                index = 0
                # 存储查找到的次数
                times = 0
                while True:
                    # 第一次查找匹配所在的位置
                    if index == 0:
                        index = content.find(old)
                        if index == -1:
                            break
                        else:
                            times = times + 1
                    else:
                        # 从上一次匹配的位置开始查找下一次匹配的位置
                        index = content.find(old, index + 1)
                        if index == -1:
                            break
                        else:
                            times = times + 1

                    if times == int(replaceOffset) + 1:
                        preContent = content[:index]
                        centerContent = new
                        suffContent = content[index + len(old):]
                        content = preContent + centerContent + suffContent
                        break

            with open(filePath, 'w+', encoding=encoding) as f:
                f.writelines(content)
                f.close()

    @classmethod
    def replaceFileContentWithLBRB(cls, filePath, new, lbStr, rbStr, replaceOffset=0, encoding='utf-8'):
        """
        根据左右字符串匹配要替换的文档内容，支持多处匹配只替换一处的功能
        :param filePath: 文档路径
        :param new: 要替换的新字符串
        :param lbStr: 要替换内容的左侧字符串
        :param rbStr: 要替换内容的右侧字符串
        :param replaceOffset: 需要将第几个匹配的内容进行替换，下标从0开始，所有都替换使用-1
        :return:
        """
        if lbStr == '' and rbStr == '':
            return
        regex = '([\\s\\S]*?)'
        r = re.compile(lbStr + regex + rbStr)
        with open(filePath, 'r', encoding=encoding) as f:
            content = f.read()
            match_results = r.findall(content)
            if int(replaceOffset) == -1:
                for result in match_results:
                    # 为了防止匹配的内容在其他地方也有被替换掉，故需要将匹配的前后字符串加上
                    content = content.replace(lbStr + result + rbStr, lbStr + new + rbStr)
            elif len(match_results) >= replaceOffset and len(match_results) != 0:
                # 用于记录匹配到关键字的位置
                index = None
                for i in range(len(match_results)):
                    if i == 0:
                        # 第一次查找匹配所在的位置
                        index = content.find(lbStr + match_results[i] + rbStr)
                    else:
                        # 从上一次匹配的位置开始查找下一次匹配的位置
                        index = content.find(lbStr + match_results[i] + rbStr, index + 1)
                    if i == int(replaceOffset):
                        preContent = content[:index]
                        centerContent = lbStr + new + rbStr
                        suffContent = content[index + len(lbStr + match_results[i] + rbStr):]
                        content = preContent + centerContent + suffContent
                        break
            f.close()

            with open(filePath, 'w+', encoding=encoding) as f:
                f.writelines(content)
                f.close()

    @classmethod
    def appendContent(cls, filePath, content, encoding='utf-8'):
        with open(filePath, 'a', encoding=encoding) as f:
            f.write(content)
            f.close()

    @classmethod
    def getRootPath(cls, project_name:str):
        """
        获得项目根路径
        :param project_name: 项目名称
        :return:
        """
        # 获取文件目录
        curPath = os.path.abspath(os.path.dirname(__file__))
        # 获取项目根路径，内容为当前项目的名字
        rootPath = curPath[:curPath.find(project_name) + len(project_name)]
        return rootPath

    @classmethod
    def convertBase64ToFile(cls, base64_str: str, file_path: str, ):
        """
        将base64字符串还原成图片保存
        :param encoding:
        :param file_path:
        :param base64_str:[base64_str="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgA********] 传参应该是去除`data:image/png;base64,`的部分
        :return:
        """
        head, context = base64_str.split(",")
        with open(file_path, 'wb', ) as f:
            imgdata = base64.b64decode(context)
            f.write(imgdata)
            f.close()

    @classmethod
    def convertFileToBase64(cls, file_path: str, encoding: str = 'utf-8') -> str:
        """
        将base64字符串还原成图片保存
        :param encoding:
        :param file_path:
        :return:
        """
        with open(file_path, 'rb') as f:
            image_base64 = base64.b64encode(f.read())
            return str(image_base64, encoding=encoding)

    @classmethod
    def convert_category_yaml(cls, yaml_path: str = './test_data/category.yaml') -> dict:
        with open(yaml_path, mode="r", encoding="utf-8", ) as f:
            try:
                dictYaml = yaml.load(f, Loader=yaml.FullLoader)
                category_dict = {}
                for item in dictYaml:
                    key = (item["category_name"], item["category_code"])
                    category_dict[key] = item
                return category_dict
            except yaml.YAMLError as e:
                logger.error('convert_category_yaml convert yaml error: ', e)

    @classmethod
    def ocr_basic(cls, img_path: str) -> str:
        with open(img_path, 'rb') as f:
            image = f.read()
            result = ocr.classification(image, png_fix=True)
            f.close()
        return result

    @classmethod
    def save_dict_to_yaml(cls, dict_value: dict, save_path: str):
        """
        dict保存为yaml
        """
        # save_path = os.path.join(os.getcwd(), save_path)  # Define save path with specific file path and name
        try:
            # directory = os.path.dirname(save_path)
            # if not os.path.exists(directory):
            #     os.makedirs(directory)
            dict_value = ast.literal_eval(str(dict_value))
            with open(save_path, 'w+', encoding='utf-8') as file:
                # Add input validation to ensure only trusted data is being passed to yaml.dump
                if isinstance(dict_value, dict):
                    yam_str = yaml.dump(dict_value, default_style='+', indent=1, default_flow_style=False,
                                        allow_unicode=True, explicit_start=True, explicit_end=True, sort_keys=True)
                    logger.debug(yam_str)
                    file.write(yam_str)
                else:
                    logger.error("Error: dict_value must be a dictionary")
        except Exception as e:
            # Add error handling to gracefully handle any errors that occur and provide useful feedback to the user
            logger.error(f"Error: {e}")

    @classmethod
    def read_yaml_to_dict(cls, yaml_path: str, ):
        with open(yaml_path, mode='r', encoding='utf-8') as file:
            dict_value = yaml.load(file.read(), Loader=yaml.FullLoader)
            return dict_value

    @classmethod
    def append_file_content(cls, path: str, content: str):
        """
        文件内append内容
        :param path:
        :param content:
        :return:
        """
        content = content.encode('utf-8')
        with open(path, mode='ab') as file:
            file.write(content)
