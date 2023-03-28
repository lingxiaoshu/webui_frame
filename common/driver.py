# 
# -*- coding: utf-8 -*-
# ---
# @Project: webui_frame
# @Software: PyCharm
# @File: driver.py
# @Author: chenhuaishu
# @Time: 2023/3/4 21:15
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from common.logger import GetLogger
from msedge.selenium_tools import EdgeOptions

class GlobalDriver:
    driver = None


class InitDriver:
    def __init__(self, browser: str, worker_id='master',remote_url=None):
        # grid 去调用操作系统的浏览器的话，remote_url
        self.logger = GetLogger().get_logger(worker_id)
        if remote_url == None:
            # 适配不同浏览器
            if browser.lower() == 'chrome':
                self.driver = webdriver.Chrome()
            elif browser.lower() == 'firefox':
                self.driver = webdriver.Firefox()
            elif browser.lower() == 'ie':
                self.driver = webdriver.Ie()
            else:
                self.logger.error('不支持的浏览器类型{}'.format(browser))
                raise Exception('不支持的浏览器类型{}'.format(browser))
        else:   # 需要grid去执行
            if browser.lower() == 'chrome':
                options = webdriver.ChromeOptions
            elif browser.lower() == 'firefox':
                options = webdriver.FirefoxOptions
            elif browser.lower() == 'ie':
                options = webdriver.IeOptions
            elif browser.lower() == 'edge':
                # pip install msedge-selenium-tools
                options = EdgeOptions()
            else:

                self.logger.error('不支持的浏览器类型{}'.format(browser))
                raise Exception('不支持的浏览器类型{}'.format(browser))
            self.driver = webdriver.Remote(remote_url, options.to_capabilities(), keep_alive=True)
        # 浏览器最大化
        self.driver.maximize_window()
        # 设置隐式等待,一般写10即可
        self.driver.implicitly_wait(20)

    # 对定位元素进行封装
    def find_element(self, ele_info):
        try:
            locator = self.get_by(ele_info)
            el = self.driver.find_element(*locator)
            self.logger.info(f'查找{ele_info}元素成功')
            return el
        except Exception as e:
            self.logger.error(f'查找{ele_info}元素失败，报错信息为{e}')
            raise Exception(f'查找{ele_info}元素失败，报错信息为{e}')

    # 封装地址
    def get(self,url):
        # 打开目标的网址
        self.driver.get(url)
        self.logger.info(f'登录{url}')
    # 点击操作
    def click(self,ele_info):
        # 定位到元素
        # 进行点击
        # el = self.find_element((ele_info))
        # el.click()
        # type = ele_info.get('type')
        # value = ele_info.get('value')
        # locator = type, value
        try:
            locator = self.get_by(ele_info)
            wait = WebDriverWait(self.driver, 20)
            wait.until(element_click_is_success(locator))
            self.logger.info(f'元素{ele_info}点击成功')
        except Exception as e:
            self.logger.error(f'元素{ele_info}点击失败，报错信息为{e}')
            raise Exception(f'元素{ele_info}点击失败，报错信息为{e}')
    def send_keys(self, ele_info, text):
        try:
            element = self.find_element(ele_info)
            element.clear()
            element.send_keys(text)
            self.logger.info(f'元素{ele_info}输入文本内容{text}成功')
        except Exception as e:
            self.logger.error(f'元素{ele_info}输入失败，报错信息为{e}')
            raise Exception(f'元素{ele_info}输入失败，报错信息为{e}')
    # 断言
    def page_source(self):
        try:
            self.logger.info('获取页面源码')
            return self.driver.page_source
        except Exception as e:
            self.logger.error(f'获取页面源码，报错信息为{e}')
            raise Exception(f'获取页面源码，报错信息为{e}')
    # 断言：判断提示信息是否在页面源码中
    def page_contains(self, text):
        try:
            wait = WebDriverWait(self.driver, 20)
            # d表示self.driver对象
            flag = wait.until(lambda d: text in d.page_source)
            self.logger.info(f'元素源码中包含{text}文本')
        except Exception as e:
            flag = False
            self.logger.warning(f'元素源码中不包含{text}文本，报错信息不包含{e}')
        return flag
    # 退出
    def quit(self):
        try:
            self.driver.quit()
            self.logger.info('driver退出成功')
        except Exception as e:
            self.logger.error(f'driver退出失败，报错信息为{e}')
    # 获取定位策略locator,返回一个具体的定位策略
    def get_by(self, ele_info):
        '''
                ele_info = {'type':xpath/id/css, 'value':值}  # 人为定义
                type = ele_info.get('type')  # 定位策略
                value = ele_info.get('value')  # 值
                 driver.find_element(type, value).send_keys('xxxx')
                :return:
                '''
        type = ele_info.get('type')  # 定位策略
        value = ele_info.get('value')  # 值
        if type == 'id':
            locator = (By.ID, value)
        elif type == 'name':
            locator = (By.NAME, value)
        elif type == 'classname':
            locator = (By.CLASS_NAME, value)
        elif type == 'tagname':
            locator = (By.TAG_NAME, value)
        elif type == 'css':
            locator = (By.CSS_SELECTOR, value)
        elif type == 'xpath':
            locator = (By.XPATH, value)
        elif type == 'linktext':
            locator = (By.LINK_TEXT, value)
        elif type == 'plinktext':
            locator = (By.PARTIAL_LINK_TEXT, value)
        else:
            # raise 跑出异常
            self.logger.error('不支持的元素定位方法:{}'.format(type))
            raise Exception('不支持的元素定位方法:{}'.format(type))
        self.logger.info(f'元素的定位策略是{locator}')
        return locator
    def move_to_element(self, ele_info):
        '''
        鼠标悬浮
        :return:
        '''
        # 定位元素
        try:
            el = self.find_element(ele_info)
            action = ActionChains(self.driver)
            action.move_to_element(el).perform()
            self.logger.info(f'鼠标悬浮元素{ele_info}成功')
        except Exception as e:
            self.logger.error(f'鼠标悬浮元素{ele_info}失败，报错信息为{e}')
            raise Exception(f'鼠标悬浮元素{ele_info}失败，报错信息为{e}')
    # 截图
    def get_screenshot_as_png(self):
        try:
            png = self.driver.get_screenshot_as_png()
            self.logger.info('截图成功')
            return png
        except Exception as e:
            self.logger.error(f'截图失败，报错信息为{e}')
            raise Exception(f'截图失败，报错信息为{e}')
    # 截图并保存成文件
    def get_screenshot_as_file(self,filepath):
        try:
            png = self.driver.get_screenshot_as_file(filepath)
            self.logger.info('截图并保存成功')
        except Exception as e:
            self.logger.error(f'截图并保存失败，报错信息为{e}')
            raise Exception(f'截图并保存失败，报错信息为{e}')
    # 切换窗口
    def switch_window(self, filepath):
        time.sleep(3)
        try:
            handles = self.driver.window_handles
            self.driver.switch_to.window(handles[-1])
            self.logger.info('切换窗口成功')
        except Exception as e:
            self.logger.error(f'切换窗口失败，报错信息为{e}')
            raise Exception(f'切换窗口失败，报错信息为{e}')
    # 获取文本内容
    def get_text(self, ele_info):
        el = self.find_element(ele_info)
        try:
            text = el.text
            self.logger.info(f'获取元素文本内容成功，内容是{text}, 类型是{type(text)}')
            return text
        except Exception as e:
            self.logger.error(f'获取元素文本内容失败，报错信息为{e}')
            raise Exception(f'获取元素文本内容失败，报错信息为{e}')
# 显示等待封装无法点击的场景
class element_click_is_success:
    '''
    locator：定位策略
    '''
    def __init__(self, locator):
        self.locator = locator
        # 定义函数的过程：定义参数、返回值、运行代码
    def __call__(self, driver):
        # 函数就是对象=类名() 等价于函数的名字
        try:
            # new一个参数locator，存储定位元素的变量
            # locator = By.CSS_SELECTOR, '#address_list>li:first-child'
            # 不定长参数，可以使用 args元组，
            driver.find_element(*self.locator).click()
            return True
        except Exception as e:
            return False

# 自定义一个显示等待的方法
class window_be_switch_success:
    def __init__(self, handle):
        self.handle = handle

    def __call__(self, driver):
        try:
            driver.switch_to.window(self.handle)
            return True
        except Exception:
            return False