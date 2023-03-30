# 
# -*- coding: utf-8 -*-
# ---
# @Project: webui_frame
# @Software: PyCharm
# @File: login_page.py
# @Author: lxs
# @Time: 2023/3/4 23:36
from common.driver import InitDriver
from common.file_load import read_yml
from pages.base_page import BasePage, BuyerPage


class LoginPage(BuyerPage):
    '''
    首页进行元素操作，首先需要先定位到元素，再点击输入操作所以需要driver对象，--driver.py
    '''
    def username_login(self):
        ele_info = self.page_info.get('账号登录')
        self.driver.click(ele_info)
    def inoput_name(self, name):
        ele_info = self.page_info.get('输入用户名')
        self.driver.send_keys(ele_info, name)
    def input_pwd(self, password):
        ele_info = self.page_info.get('输入密码')
        self.driver.send_keys(ele_info, password)
    def input_valicode(self):
        ele_info = self.page_info.get('输入验证码')
        self.driver.send_keys(ele_info, '1512')
    def click_login(self):
        ele_info = self.page_info.get('点击登录按钮')
        self.driver.click(ele_info)