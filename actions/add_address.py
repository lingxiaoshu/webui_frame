# 
# -*- coding: utf-8 -*-
# ---
# @Project: webui_frame
# @Software: PyCharm
# @File: add_addr.py
# @Author: chenhuaishu
# @Time: 2023/3/5 11:37
from common.driver import InitDriver
from pages.buyer.home_page import HomePage


class AddAddress:
    def __init__(self, driver:InitDriver):
        self.driver = driver
    def add_address(self, name='默认名字', tel='13623451234', select_address =True,
                    privice ='北京', city= '海淀区', area= '三环以内',
                    detail_address= '默认的地址', other_name= '默认别名'):
        # 首页-进入个人中心
        homepage = HomePage(self.driver)
        personcenterpage = homepage.person_center()
        add_addrpage = personcenterpage.address_meua()
        add_addrpage.add_address()
        add_addrpage.recevier_name(name)
        add_addrpage.recevier_tel(tel)
        if select_address == True:
            add_addrpage.recevier_address(privice,city,area)
        add_addrpage.detail_address(detail_address)
        add_addrpage.addr_other_name(other_name)
        add_addrpage.insure_btn()