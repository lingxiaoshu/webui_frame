# 
# -*- coding: utf-8 -*-
# ---
# @Project: webui_frame
# @Software: PyCharm
# @File: home_page.py
# @Author: chenhuaishu
# @Time: 2023/3/4 23:18
from common.driver import InitDriver
from common.file_load import read_yml
from pages.base_page import BasePage, BuyerPage
from pages.buyer.login_page import LoginPage
from pages.buyer.personcenter_page import PersonCenterPage
from pages.buyer.searchresult_page import SearchResultPage


class HomePage(BuyerPage):
    '''
    首页进行元素操作，首先需要先定位到元素，再点击输入操作所以需要driver对象，--driver.py
    '''
    def login_link(self):
        ele_info = self.page_info.get('登录链接')
        self.driver.click(ele_info)
        return LoginPage(self.driver)
    def person_center(self):
        ele_info = self.page_info.get('进入个人中心')
        self.driver.click(ele_info)
        return PersonCenterPage(self.driver)

    def input_search_text(self,text):
        ele_info = self.page_info.get('搜索框')
        self.driver.send_keys(ele_info,text)

    def click_search_btn(self):
        ele_info = self.page_info.get('搜索按钮')
        self.driver.click(ele_info)
        return SearchResultPage(self.driver)
