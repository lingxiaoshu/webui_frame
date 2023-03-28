# 
# -*- coding: utf-8 -*-
# ---
# @Project: webui_frame
# @Software: PyCharm
# @File: test_addaddr.py
# @Author: chenhuaishu
# @Time: 2023/3/5 11:50
import allure
import pytest
import pytest_assume.plugin

from actions.add_address import AddAddress
from actions.create_order import CreateOrder
from actions.login import Login
from common.driver import InitDriver, GlobalDriver
from common.file_load import read_excel

# 参数化数据--读取Excel中的参数化数据
# data = read_excel('/data/mtxshop.xlsx', '添加地址')
class TestOrder:
    def test_create_order(self):
        orderresultpage = CreateOrder(GlobalDriver.driver).create_order()
        # 断言--提示信息
        pytest.assume(GlobalDriver.driver.page_contains('订单状态刷新可能会延迟'))
        # 断言--数据
        trade_sn = orderresultpage.get_trade_sn()
        orderinfo = '订单编号：' + trade_sn
        orderresultpage.click_order_info()
        pytest.assume(GlobalDriver.driver.page_contains(orderinfo))