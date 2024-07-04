#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/5/31
# @File    : base_encrypt_tool.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import base64
import hashlib


class BaseEncryptTool:

    @classmethod
    def md5Encode(cls, text):
        """
        md5加密，32位
        :param text:
        :return:
        """
        m = hashlib.md5()
        m.update(text.encode('utf-8'))
        return m.hexdigest()

    @classmethod
    def base64Encode(cls, text, encoding='utf-8'):
        return base64.b64encode(bytes(text, encoding=encoding))

    @classmethod
    def base64Decode(cls, base64Text, encoding='utf-8') -> str:
        return str(base64.b64decode(base64Text), encoding=encoding)

    @classmethod
    def hash_code(cls, text: str):
        h = 0
        if len(text) > 0:
            for item in text:
                h = 31 * h + ord(item)
            return h
        else:
            return 0

    @classmethod
    def sha1Encode(cls, src_str):
        """
        sha1加密
        :param src_str:
        :return desc_str:
        """
        return hashlib.sha1(src_str.encode('utf-8')).hexdigest()
