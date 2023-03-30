# 
# -*- coding: utf-8 -*-
# ---
# @Project: webui_frame
# @Software: PyCharm
# @File: keyword_run.py
# @Author: lxs
# @Time: 2023/3/6 14:49
# 1.根据testcases中所有测试用例的个数，去依次执行测试用例
import re

import allure
import pytest
import os

from common.driver import GlobalDriver
from common.file_load import read_yml
from setting import DIR_NAME
# 存放业务变量
actions_variables = {}
# 存放测试用例中的变量
testcases_variable = {}

@pytest.mark.parametrize
# 2.如何解析出testcases里面有多少条测试用例
def get_all_cases():
    testcases_files = os.listdir(DIR_NAME+'/keyword/testcases')
    # 存放所有测试用例的列表
    testcases_list = []
    for testcase_file in testcases_files:
        testcase_yml_info = read_yml(f'/keyword/testcases/{testcase_file}')
        testcases_info = testcase_yml_info.get('testcases')
        for testcase_info in testcases_info:
            # 单独的一条测试用例的信息
            case = testcase_info['testcase']
            # 测试用例的名字
            case_name = case['name']
            # 执行测试用例需要用的内容
            testcases_list.append([case_name, case])
    return testcases_list
# 3.解析每条测试用例中的内容
def exec_case(case):
    '''
    执行每条测试用例
    case:{}
    :param case:
    :return:
    '''
    # 获取测试用例业务的yml文件的路径
    action = case['action']
    # 多参数化的变量进行判断
    if 'params' in case:
        params_content = case['params']
        # 读取业务的名字
        action_name = read_yml(action).get('name')
        # 把变量存储到测试用例的变量集合中
        testcases_variable[action_name] = params_content
    # 执行测试用例中的业务
    exec_actions(action)
    # 断言
    for validate in case['validate']:  # 列表
        # validate变量是字典
        # 获取断言的类型type
        type = validate['type']
        # 预期值
        expect = validate['expect']
        if type == 'page_contains':
            pytest.assume(GlobalDriver.driver.page_contains(expect))

# 4.解析每个action业务里面的内容
def exec_actions(action):
    '''
    执行测试用例中的业务
    :param action: '/keyword/actions/buyer_login.yml'
    :return:
    '''
    global pages_info, ele_info, param_name
    # 所有buyer_login.yml里面的内容
    actions_info = read_yml(action)
    # 业务的名字
    action_name = actions_info.get('name')
    # 配置文件的路径
    pagefile = actions_info.get('pagefile')
    # 读取配置文件的所有内容
    pagefile_info = read_yml(pagefile)
    # 判断一下是否有变量
    if 'variables' in actions_info:
        variables = actions_info['variables']
        # 存储到所有的业务变量中
        actions_variables[action_name] = variables
    # 业务的步骤进行读取
    steps = actions_info['steps']  # 列表
    for step in steps:
        if 'page' in step:
            page_name = step['page']
            pages_info = pagefile_info.get(page_name)
        if 'element' in step:
            element_name = step['element']
            ele_info = pages_info.get(element_name)  # alt+enter键 自动定义全局变量
        operate_name = step['operate']
        if 'param' in step:
            param_name = step['param']  # '${username}'
            # 解析变量
            param_name = regex_sub(action_name, param_name)
        # 利用反射：字符串'click'operate_name->函数->调用他-实现操作元素的功能
        if hasattr(GlobalDriver.driver, operate_name):
            # 获取方法->函数的名字/方法的名字()调用
            func = getattr(GlobalDriver.driver, operate_name)
            # 调用func()
            # 参数:参数如何传递(不包括self)
            # 获取到所有的参数(包括self)
            count = func.__code__.co_argcount - 1
            if count > 1:
                func(ele_info, param_name)
            elif count == 0:
                func()
            elif count == 1:
                if ele_info:
                    func(ele_info)
                elif param_name:
                    func(param_name)
# 4.1 变量解析的问题
def regex_sub(action_name, param_name):
    '''
    1. 检索变量${xxx}     =>拿到xxx这个内容
    ${username}
    2. 变量替换
    :param action_name: 业务名字
    :param param_name: 需要解析的参数的值
    :return:
    '''
    global value
    # 正则表达式只能对字符串进行检索和替换
    results = re.findall(r'\$\{(.+?)\}', str(param_name))
    for key in results:
        # 做替换->key对应的value值是什么，${username}->具体的值
        if action_name in testcases_variable:
            target_variable = testcases_variable[action_name]
            if key in target_variable:
                value = target_variable[key]
            elif action_name in actions_variables:
                target_variables = actions_variables[action_name]
                if key in target_variables:
                    value = target_variables[key]
                else:
                    raise Exception('没有对应的变量的值')
        elif action_name in actions_variables:
            target_variables = actions_variables[action_name]
            if key in target_variables:
                value = target_variables[key]
            else:
                raise Exception('没有对应的变量的值')
        else:
            raise Exception('没有对应的变量的值')

        param_name = re.sub(r'\$\{' + key + r'\}', value, str(param_name))
        return param_name

@allure.title('{case_name}')
@pytest.mark.parametrize('case_name,case',get_all_cases())
def test_keyword(case_name,case):
    '''

    :param case_name:
    :param case: 每条测试用例的详细信息
    :return:
    '''
    exec_case(case)