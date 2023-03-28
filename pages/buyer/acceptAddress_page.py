# 
# -*- coding: utf-8 -*-
# ---
# @Project: webui_frame
# @Software: PyCharm
# @File: acceptAddress_page.py
# @Author: chenhuaishu
# @Time: 2023/3/5 11:13
import time

from pages.base_page import BasePage, BuyerPage


class AcceptAddressPage(BuyerPage):
    '''
    首页进行元素操作，首先需要先定位到元素，再点击输入操作所以需要driver对象，--driver.py
    '''
    def add_address(self):
        ele_info = self.page_info.get('添加地址')
        self.driver.click(ele_info)
    def recevier_name(self,name):
        ele_info = self.page_info.get('收货人姓名')
        self.driver.send_keys(ele_info, name)
    def recevier_tel(self,name):
        ele_info = self.page_info.get('输入联系方式')
        self.driver.send_keys(ele_info, name)
    def recevier_address(self,provice, city, area):
        ele_info = self.page_info.get('收货地区')
        # 鼠标悬浮
        self.driver.move_to_element(ele_info)
        time.sleep(2)
        ele_info = {'name':'省', 'type':'linktext', 'value': provice}
        self.driver.click(ele_info)
        time.sleep(2)
        ele_info = {'name':'市', 'type':'linktext', 'value': city}
        self.driver.click(ele_info)
        time.sleep(2)
        ele_info = {'name':'区', 'type':'linktext', 'value': area}
        self.driver.click(ele_info)
        time.sleep(8) #系统需要优化
    def detail_address(self, detail_address):
        ele_info = self.page_info.get('详细地址')
        self.driver.send_keys(ele_info, detail_address)
    def addr_other_name(self, other_name):
        ele_info = self.page_info.get('地址别名')
        self.driver.send_keys(ele_info, other_name)
    def insure_btn(self):
        ele_info = self.page_info.get('确认按钮')
        self.driver.click(ele_info)
