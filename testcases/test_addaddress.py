# 
# -*- coding: utf-8 -*-
# ---
# @Project: webui_frame
# @Software: PyCharm
# @File: test_addaddr.py
# @Author: lxs
# @Time: 2023/3/5 11:50
import allure
import pytest
import pytest_assume.plugin

from actions.add_address import AddAddress
from actions.login import Login
from common.driver import InitDriver, GlobalDriver
from common.file_load import read_excel

# 参数化数据--读取Excel中的参数化数据
data = read_excel('/data/mtxshop.xlsx', '添加地址')
class TestAddress:
    # # 添加地址-依赖登录
    # def setup_class(self):
    #     # 实例化driver对象
    #     self.driver = InitDriver('Chrome')
    #     # 地址
    #     self.driver.get('http://www.mtxshop.com:3000/')
    #     # 调用登录业务
    #     Login(self.driver).buyer_login()
    # # TODO：每条测试用例执行完成后都要回到首页，执行次数与测试用例个数一致
    # def teardown_method(self):
    #     self.driver.get('http://www.mtxshop.com:3000/')
    # # TODO：所有测试用例执行完成之后，关闭浏览器
    # def teardown_class(self):
    #     self.driver.quit()
    # allure动态获取测试用例名字
    # @allure.title('{casename}')
    # @pytest.mark.parametrize('casename, name,tel, select_address, detail_address,other_name,assert_name',
    #                          data)
    def test_choose_address(self,casename,name,tel, select_address, detail_address,other_name,assert_name):

        # 需要调用添加地址的业务
        AddAddress(GlobalDriver.driver).add_address()
        # 断言
        pytest.assume(GlobalDriver.driver.page_contains('保存成功'))
        # 需要调用添加地址的业务
        # AddAddress(GlobalDriver.driver).add_address(name = name,
        #                                             tel = tel,
        #                                             select_address=select_address,
        #                                             detail_address=detail_address,
        #                                             other_name=other_name)
        # # 断言
        # pytest.assume(GlobalDriver.driver.page_contains(assert_name))
    def test_not_choose_address(self):

        # 需要调用添加地址的业务
        AddAddress(GlobalDriver.driver).add_address(select_address=False)
        # 断言
        pytest.assume(GlobalDriver.driver.page_contains('请选择地址地区11'))
