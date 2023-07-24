#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/5/14
# @File    : runner.py.py
# @Software: IntelliJ IDEA

__author__ = 'xiaowu'

import sys

import pytest

from Common.clear_cache import *
from Common.file_config import FileConfig
from Common.global_var import GlobalVar

"""
一、支持脚本运行方式
1、支持运行所有的case
2、支持运行一个或多个文件下的case
3、支持运行带有标签的case
4、支持运行具体的某一条case


二、总工程执行方式:

python3 runner.py 参数1 参数2 参数3
参数1:
第一个参数 case 执行类型，'all', 'choose', 'tag'，'single'
type = sys.argv[1]

参数2：
第二个参数要执行的文件名称或者标签名称, 多个文件逗号分割


"""

if __name__ == '__main__':
    input_list = sys.argv
    global_var = GlobalVar()
    formatted_time = global_var.base_dir
    if "chrome" in input_list:
        input_list.remove("chrome")
        global_var.set_browser("chrome")
    elif "edge" in input_list:
        input_list.remove("edge")
        global_var.set_browser("edge")
    else:
        pass

    # 判断缓存文件是否存在，删除历史结果数据
    if os.path.exists("{}\.pytest_cache".format(FileConfig().base_dir)) or os.path.exists(
            "{}/.pytest_cache".format(FileConfig().base_dir)):
        clear_cache()

    # 第一个参数 case 执行类型，'all', 'choose', 'tag'
    caseType = input_list[1]
    # caseName = sys.argv[2]
    # 第二个参数要执行的caseName, 多个文件逗号分割

    if caseType == 'all':
        # 执行所有case
        # 直接执行pytest.main() 【自动查找当前目录下，以test_开头的文件或者以_test结尾的py文件】

        if len(input_list) == 2:
            pytest.main(
                ["-v", "--html=Outputs/pytest_report/{0}/index.html".format(formatted_time),
                 "--alluredir=Outputs/allure_report"])
        elif len(input_list) == 3:
            if "--reruns" in input_list:
                pytest.main(
                    ["-v", "--html=Outputs/pytest_report/{0}/index.html".format(formatted_time),
                     "--alluredir=Outputs/allure_report",
                     "--reruns", "1"])
            else:
                num = input_list[2] or "auto"
                # num 是并发
                # -n auto：可以自动检测到系统的CPU核数；从测试结果来看，检测到的是逻辑处理器的数量，即假12核
                pytest.main(["-v", "--html=Outputs/pytest_report/{0}/index.html".format(formatted_time),
                             "--alluredir=Outputs/allure_report", "-n", num])

        elif len(input_list) == 4:
            a = ["runner.py", "all", "--reruns"]
            num = list(set(input_list).difference(set(a)))[0]
            pytest.main(["-v", "--html=Outputs/pytest_report/{0}/index.html".format(formatted_time),
                         "--alluredir=Outputs/allure_report", "--reruns", "1", "-n", num])

        else:
            pytest.main(
                ["-v", "--html=Outputs/pytest_report/{0}/index.html".format(formatted_time),
                 "--alluredir=Outputs/allure_report", ])

    elif caseType == 'choose':
        caseName = input_list[2]
        # 执行部分文件的case
        # python3 runner.py choose test_1_service,test_1_service
        # 设置pytest的执行参数 pytest.main(['--html=./report.html','test_login.py'])【执行test_login.py文件，并生成html格式的报告】
        # pytest.main(['--html=./report.html', 'test_login.py'])

        case_list = caseName.split(',')
        case = []

        for i in case_list:
            case_name = "./TestCases/{}".format(caseName)
            case.append(case_name)
        if len(case) == 1:
            caseName = "./TestCases/{}".format(caseName)
            # caseName="/Users/a58/Documents/58auto/web_ui_test/pytest_Web_Framework_V1/TestCases/{}".format(caseName)
            pytest.main(
                ["-v", "--html=Outputs/pytest_report/{0}/index.html".format(formatted_time),
                 "--alluredir=Outputs/allure_report",
                 caseName])

        else:
            caseStr = []
            for i in case_list:
                case_name = "{}/TestCases/{}".format(FileConfig().base_dir, i)
                caseStr.append(case_name)

            # pytest.main(caseStr)
            list1 = ["-v", "--html=Outputs/pytest_report/{0}/index.html".format(formatted_time),
                     "--alluredir=Outputs/allure_report"]
            list2 = list1 + caseStr
            # pytest.main(
            #     ["-v", "--html=Outputs/pytest_report/{0}/index.html".format(formatted_time), "--alluredir=Outputs/allure_report", str(caseStr)])
            pytest.main(list2)

    elif caseType == 'tag':
        # 执行带标签的case，如果需要执行多个tag，使用逗号分割
        # python3 runner.py tag P1,P3
        # sudo python3 runner.py tag P1,P3
        tagName = input_list[2].replace(",", " or ")
        if len(input_list) == 3:
            pytest.main(["-v", "-m", tagName, "--html=Outputs/pytest_report/{0}/index.html".format(formatted_time),
                         "--alluredir=Outputs/allure_report"])
        elif len(input_list) == 4:
            if "--reruns" in input_list:
                pytest.main(["-v", "-m", tagName, "--html=Outputs/pytest_report/{0}/index.html".format(formatted_time),
                             "--alluredir=Outputs/allure_report", "--reruns", "1"])
            else:
                num = input_list[3] or "auto"
                pytest.main(["-v", "-m", tagName, "--html=Outputs/pytest_report/{0}/index.html".format(formatted_time),
                             "--alluredir=Outputs/allure_report", "-n", num])
        else:
            pytest.main(["-v", "-m", tagName, "--html=Outputs/pytest_report/{0}/index.html".format(formatted_time),
                         "--alluredir=Outputs/allure_report", "-n", "2", "--reruns", "1"])

    elif caseType == 'single':
        filename = sys.argv[2]
        classname = sys.argv[3]
        casename = sys.argv[4]

        # 文件名称 test_3_mytest3.py，类名称test_3_mytest3。运行case会报错，避免这种情况，类名称为TestService就可以正常运行

        pytest.main(
            ["-v", './TestCases/{}::{}::{}'.format(filename, classname, casename),
             "--html=Outputs/pytest_report/{0}/index.html".format(formatted_time),
             "--alluredir=Outputs/allure_report"])

    elif caseType == 'severity':
        severity = sys.argv[2]
        """逗号隔开"""
        pytest.main(
            ["-v", "-q", "--html=Outputs/pytest_report/{0}/index.html".format(formatted_time),
             "--alluredir=Outputs/allure_report", "--allure-severities={}".format(severity)])


    else:
        pass

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
