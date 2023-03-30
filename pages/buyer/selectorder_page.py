# 
# -*- coding: utf-8 -*-
# ---
# @Project: webui_frame
# @Software: PyCharm
# @File: selectorder_page.py
# @Author: lxs
# @Time: 2023/3/5 21:43
from pages.base_page import BuyerPage
# from pages.buyer.orderresult_page import OrderResultPage


class SelectOrderPage(BuyerPage):
    '''
    首页进行元素操作，首先需要先定位到元素，再点击输入操作所以需要driver对象，--driver.py
    '''

    def click_chose_address(self):
        ele_info = self.page_info.get('选择收货地址')
        self.driver.click(ele_info)
    def click_order(self):
        ele_info = self.page_info.get('提交订单')
        self.driver.click(ele_info)
        return OrderResultPage(self.driver)

class OrderResultPage(BuyerPage):
    '''
    首页进行元素操作，首先需要先定位到元素，再点击输入操作所以需要driver对象，--driver.py
    '''

    def click_order_info(self):
        ele_info = self.page_info.get('查看订单')
        self.driver.click(ele_info)
    def get_trade_sn(self):
        ele_info = self.page_info.get('交易号')
        trade_sn = self.driver.get_text(ele_info)
        return trade_sn
