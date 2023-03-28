# 
# -*- coding: utf-8 -*-
# ---
# @Project: webui_frame
# @Software: PyCharm
# @File: goalgoodspage.py
# @Author: chenhuaishu
# @Time: 2023/3/5 21:41
from pages.base_page import BuyerPage
from pages.buyer.selectorder_page import SelectOrderPage


class GoodsDetailPage(BuyerPage):
    '''
    首页进行元素操作，首先需要先定位到元素，再点击输入操作所以需要driver对象，--driver.py
    '''

    def click_buy_now(self):
        ele_info = self.page_info.get('立即购买')
        self.driver.click(ele_info)
        return SelectOrderPage(self.driver)