# 
# -*- coding: utf-8 -*-
# ---
# @Project: webui_frame
# @Software: PyCharm
# @File: search_result.py
# @Author: lxs
# @Time: 2023/3/5 21:38
from pages.base_page import BuyerPage
from pages.buyer.goalgoods_page import GoodsDetailPage


class SearchResultPage(BuyerPage):
    '''
    首页进行元素操作，首先需要先定位到元素，再点击输入操作所以需要driver对象，--driver.py
    '''

    def click_target_goods(self):
        ele_info = self.page_info.get('目标商品')
        self.driver.click(ele_info)
        # 窗口切换
        self.driver.switch_window()
        return GoodsDetailPage(self.driver)