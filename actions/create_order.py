# 
# -*- coding: utf-8 -*-
# ---
# @Project: webui_frame
# @Software: PyCharm
# @File: create_order.py
# @Author: chenhuaishu
# @Time: 2023/3/6 11:24
from common.driver import InitDriver
from pages.buyer.home_page import HomePage


class CreateOrder:
    def __init__(self, driver:InitDriver):
        self.driver = driver
    def create_order(self, goods_name = '纯牛奶'):
        # 首页-点击登录链接
        homepage = HomePage(self.driver)
        homepage.input_search_text(goods_name)
        searchresultpage = homepage.click_search_btn()
        goodsdetailpage = searchresultpage.click_target_goods()
        selectorderpage = goodsdetailpage.click_buy_now()
        selectorderpage.click_chose_address()
        orderresultpage = selectorderpage.click_order()
        # 为了做断言，orderresultpage需要有返回值
        return orderresultpage