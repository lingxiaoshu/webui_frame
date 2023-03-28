# 
# -*- coding: utf-8 -*-
# ---
# @Project: webui_frame
# @Software: PyCharm
# @File: login.py
# @Author: chenhuaishu
# @Time: 2023/3/4 23:55
# 登录业务
from selenium import webdriver

from common.driver import InitDriver
from pages.buyer.home_page import HomePage


class Login:
    def __init__(self, driver:InitDriver):
        self.driver = driver
    def buyer_login(self):
        # 首页-点击登录链接
        homepage = HomePage(self.driver)
        loginpage = homepage.login_link()
        # 登录页面--账号登录
        loginpage.username_login()
        # 登录页面--用户名
        loginpage.inoput_name(name='yaoyao')
        # 登录页面--密码
        loginpage.input_pwd(password='yaoyao123456')
        # 登录页面--验证码
        loginpage.input_valicode()
        # 登录页面--点击登录按钮
        loginpage.click_login()

if __name__=='__main__':
    driver = InitDriver('Chrome')
    driver.get('http://www.mtxshop.com:3000/')
    Login(driver).buyer_login()

