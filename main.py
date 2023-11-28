#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @File    : main.py.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import pytest

from Common.clear_cache import *
from Common.file_config import FileConfig
from Common.global_var import GlobalVar
from PageObjects.step_wx_serach import WxPage

# 如果需要本地开发/测试小程序，将此处置为True
is_wx = True
project_path = "D:\\Project\\study-vue-project\\weapp-qrcode"
dev_tool_path = "D:\\Software\\微信web开发者工具\\cli.bat"

if __name__ == '__main__':
    """
    本地开发执行文件
    :return:
    """
    if is_wx:

        import minium
        mini = minium.Minium({
            "project_path": project_path,
            "dev_tool_path": dev_tool_path
        })

        # base_def = BaseDef(mini)
        weapp_u_query = WxPage(mini)
        weapp_u_query.input_tap_and_fill()
        mini.shutdown()
    else:
        global_var = GlobalVar()
        formatted_time = global_var.base_dir
        # 执行mark
        tag = 'P3 or P1'
        # cpu_count
        # num = "2"
        num = "auto"
        # 判断缓存文件是否存在，删除历史结果数据
        if os.path.exists("{}\.pytest_cache".format(FileConfig().base_dir)) or os.path.exists(
                "{}/.pytest_cache".format(FileConfig().base_dir)):
            clear_cache()

        # 执行main文件
        pytest.main(["-v", "-m", tag, "--html=Outputs/pytest_report/%s/index.html" % formatted_time,
                     "--alluredir=Outputs/allure_report", "-n", num])

        # 生成allure报告
        if platform.system() == "Windows":
            command_1 = "cd {}".format(FileConfig().get_path(type="allure_report"))
            command_2 = "allure generate {0} -o {1} --clean".format(FileConfig().get_path(type="allure_report"),
                                                                    formatted_time)
            command_3 = "for %i in (*.json *.txt) do if exist %i del /f /q \"%i\""
            os.system('{0}&&{1}&&{2}'.format(command_1, command_2, command_3))
        else:
            command_1 = "cd {}".format(FileConfig().get_path(type="allure_report"))
            command_2 = "allure generate {0} -o {1} --clean".format(FileConfig().get_path(type="allure_report"),
                                                                    formatted_time)
            command_3 = "find . -maxdepth 1 -type f \( -name '*.json' -o -name '*.txt' \) -delete"
            os.system('{0}&&{1}&&{2}'.format(command_1, command_2, command_3))
