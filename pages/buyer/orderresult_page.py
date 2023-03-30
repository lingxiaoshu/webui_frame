# 
# -*- coding: utf-8 -*-
# ---
# @Project: webui_frame
# @Software: PyCharm
# @File: orderresult_page.py
# @Author: lxs
# @Time: 2023/3/5 21:49
from pages.base_page import BuyerPage


class OrderResultPage(BuyerPage):
    '''
    首页进行元素操作，首先需要先定位到元素，再点击输入操作所以需要driver对象，--driver.py
    '''

    def click_order_info(self):
        ele_info = self.page_info.get('查看订单')
        self.driver.click(ele_info)
    def get_trade_sn(self):
        ele_info = self.page_info.get('交易号')
        # 获取文本内容

        return OrderResultPage(ele_info)