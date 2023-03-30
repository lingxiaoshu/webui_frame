# 
# -*- coding: utf-8 -*-
# ---
# @Project: webui_frame
# @Software: PyCharm
# @File: personcenter_page.py
# @Author: lxs
# @Time: 2023/3/5 11:07
from pages.base_page import BasePage, BuyerPage
from pages.buyer.acceptAddress_page import AcceptAddressPage




class PersonCenterPage(BuyerPage):
    '''
    首页进行元素操作，首先需要先定位到元素，再点击输入操作所以需要driver对象，--driver.py
    '''
    def address_meua(self):
        ele_info = self.page_info.get('收货地址菜单')
        self.driver.click(ele_info)
        return AcceptAddressPage(self.driver)
