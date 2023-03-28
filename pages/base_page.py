# 
# -*- coding: utf-8 -*-
# ---
# @Project: webui_frame
# @Software: PyCharm
# @File: base_page.py
# @Author: chenhuaishu
# @Time: 2023/3/4 23:43
from common.driver import InitDriver
from common.file_load import read_yml


class BasePage:
    def __init__(self, driver: InitDriver):
        # 将driver设置为属性，后面会多次用到
        self.driver = driver
        # 动态获取类名
        self.page_name = self.__class__.__name__

class BuyerPage(BasePage):
    def __init__(self, driver: InitDriver):
        super().__init__(driver)
        # 将driver设置为属性，后面会多次用到
        self.page_info = read_yml('/pagesfiles/buyer.yml').get(self.page_name)

class SellerPage(BasePage):
    def __init__(self, driver: InitDriver):
        super().__init__(driver)
        # 将driver设置为属性，后面会多次用到
        self.page_info = read_yml('/pagesfiles/seller.yml').get(self.page_name)
