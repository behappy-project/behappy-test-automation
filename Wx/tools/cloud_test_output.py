#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import json
import time
import requests


class MiniTestApi:
    """
    可用于集成CICD流程中
    待创建测试任务结束后发送报告到企业微信
    """

    def __init__(self, user_token, group_en_id):
        self.token = user_token  # 需要填写自己的token
        self.group_en_id = group_en_id  # 项目英文ID
        self.minitest_api = 'https://minitest.weixin.qq.com/thirdapi'

    def third_auto_task(self):
        """
        创建测试任务
        :return:
        """
        config = {
            "assert_capture": True,
            "auto_relaunch": False,
            "auto_authorize": False,
            "audits": False,
            "compile_mode": ""
        }

        data = {
            'token': self.token,
            'group_en_id': self.group_en_id,
            'test_type': 2,  # 1:monkey 2:minium 3:录制回放 4:快速monkey 5:启动性能分析
            'platforms': 'ios',
            'wx_id': '',  # 小程序appid，一般不需要填写，但是如果是第三方服务商，则需要填写授权小程序的appid
            'wx_version': 2,  # 小程序版本，1：线上版本 2：体验版本 3：开发版本
            'desc': 'Minium测试',
            'test_plan_id': "",  # 测试计划id
            'dev_account_no': 1,
            'minium_config': config,
            "virtual_accounts": ""
        }
        resp = requests.post(
            self.minitest_api + '/plan',
            json=data
        )
        resp = resp.json()
        print(resp)
        return resp["data"]["plan_id"]

    def share_url(self, planId):
        """
        分享测试报告
        :param planId:
        :return:
        """
        data = {
            'token': self.token,
            'group_en_id': self.group_en_id,
            'plan_id': planId,
        }
        resp = requests.get(
            self.minitest_api + '/share_url',
            params=data
        )
        resp = resp.json()
        return resp["data"]["share_url"]

    def add_case_plan(self):
        """
        新增测试计划
        :return {'msg': "添加测试计划成功", 'rtn': 0}
        """
        plan_config = {
            "pkg_list": [
                {
                    "case_list": [
                        "test_*"
                    ],
                    "pkg": "testcase.*"
                }
            ]
        }  # 参照文档 https://minitest.weixin.qq.com/#/minium/Python/framework/suite 进行编写

        data = {
            'token': self.token,
            'group_en_id': self.group_en_id,
            'test_plan_name': 'api自定义Minium',  # 测试计划名称
            'test_plan_config': json.dumps(plan_config)
        }

        resp = requests.post(url=self.minitest_api + '/case_plan', json=data)
        print(resp.json())

        return resp.json()

    def get_task(self, plan_id):
        """
        获取云测任务的执行结果
        :param plan_id:
        :return:
        """
        data = {
            'token': self.token,
            'group_en_id': self.group_en_id,
            'plan_id': plan_id,
        }

        max_retries = 10
        retry_count = 0

        while retry_count < max_retries:
            try:
                resp = requests.get(
                    self.minitest_api + '/plan',
                    params=data
                )
                res = resp.json()

                status_text = res["data"]["status_text"]
                if status_text == "测试结束":
                    report_url = minitest_client.share_url(plan_id)
                    create_time = res["data"]["create_time"]
                    finish_time = res["data"]["finish_time"]
                    total_case_num = res["data"]["total_case_num"]
                    success_case_num = res["data"]["success_case_num"]
                    minitest_client.sendMessge(report_url, create_time, finish_time, total_case_num, success_case_num)
                    print("测试完成")
                    break
                else:
                    print("还在测试中，等待...")
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(300)
            except Exception as e:
                print("发生异常：", str(e))
                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(300)
                else:
                    raise e

        return None

    def sendMessge(self, report_url, create_time, finish_time, total_case_num, success_case_num, sendKey):
        """
        :param passed: 通过的用例数
        :param failed: 失败的用例数
        :param broken: 报错的用例数
        :param sendKey: 企微机器人key
        :return:
        """

        Webhook = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={sendKey}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content":
                    '''<font color=\"warning\">提醒！小程序UI自动化测试反馈\n请相关同事注意，及时跟进！</font>\n
                        > 云测报告链接：[minium 测试报告,请点击后进入查看]({})
                        > 用例开始时间: <font color=\"info\">{}</font>\n
                        > 用例结束时间: <font color=\"info\">{}</font>\n
                        > 用例总数: <font color=\"comment\">{}</font>\n
                        > 通过用例数: <font color=\"info\">{}</font>\n
                        > 失败用例数: <font color=\"warning\">{}</font>\n
                 '''.format(report_url, create_time, finish_time, total_case_num, success_case_num,
                            (total_case_num - success_case_num))
            }
        }

        requests.post(url=Webhook, headers=headers, json=data)


if __name__ == '__main__':
    minitest_client = MiniTestApi('xx', 'xx')
    # print("开始创建测试任务")
    plan_id = minitest_client.third_auto_task()
    # print("查询任务状态")
    minitest_client.get_task(plan_id)
