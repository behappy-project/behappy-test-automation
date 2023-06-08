#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/6/6
# @File    : request.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import requests


class HTTPClient:
    """
    requests 封装
    eg:
    # 创建 HTTPClient 对象
    client = HTTPClient('https://jsonplaceholder.typicode.com', default_headers={'User-Agent': 'Mozilla/5.0'})

    # 发送 GET 请求
    response = client.get('/posts/1')
    print(response.status_code)
    print(response.json())

    # 发送 POST 请求
    data = {'title': 'foo', 'body': 'bar', 'userId': 1}
    response = client.post('/posts', json=data)
    print(response.status_code)
    print(response.json())

    # 带着 Cookie 发送请求
    cookies = {'sessionid': 'abc123'}
    response = client.get('/profile', cookies=cookies)
    print(response.status_code)
    print(response.json())

    # 带着自定义请求头发送请求
    headers = {'Authorization': 'Bearer abc123'}
    response = client.get('/protected', headers=headers)
    print(response.status_code)
    print(response.json())

    # 自定义超时时间发送请求
    response = client.get('/slow', timeout=10)
    print(response.status_code)
    print(response.json())
    """
    def __init__(self, base_url, default_headers=None, default_cookies=None, timeout=3):
        self.base_url = base_url
        self.default_headers = default_headers or {}
        self.default_cookies = default_cookies or {}
        self.timeout = timeout

    def request(self, method, endpoint, headers=None, cookies=None, params=None, data=None, json=None, timeout=None):
        url = self.base_url + endpoint
        headers = {**self.default_headers, **(headers or {})}
        cookies = {**self.default_cookies, **(cookies or {})}
        timeout = timeout or self.timeout
        response = requests.request(method, url, headers=headers, cookies=cookies, params=params, data=data, json=json,
                                    timeout=timeout)
        return response

    def get(self, endpoint, headers=None, cookies=None, params=None, timeout=None):
        return self.request('GET', endpoint, headers=headers, cookies=cookies, params=params, timeout=timeout)

    def post(self, endpoint, headers=None, cookies=None, params=None, data=None, json=None, timeout=None):
        return self.request('POST', endpoint, headers=headers, cookies=cookies, params=params, data=data, json=json,
                            timeout=timeout)

    def put(self, endpoint, headers=None, cookies=None, params=None, data=None, json=None, timeout=None):
        return self.request('PUT', endpoint, headers=headers, cookies=cookies, params=params, data=data, json=json,
                            timeout=timeout)

    def delete(self, endpoint, headers=None, cookies=None, params=None, timeout=None):
        return self.request('DELETE', endpoint, headers=headers, cookies=cookies, params=params, timeout=timeout)
