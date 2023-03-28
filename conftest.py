import os
import time
from threading import Thread

import pytest
import allure
from PIL import Image, ImageFile

from actions.login import Login

from common.driver import InitDriver, GlobalDriver
from setting import DIR_NAME


# hook函数
def pytest_collection_modifyitems(items):
    # item表示每个测试用例，解决测试用例中名称中文显示问题
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode-escape")
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode-escape")
# 失败截图,两个参数是固定的
@pytest.hookimpl(tryfirst=True, hookwrapper= True)
def pytest_runtest_makereport(item, call):
    # 测试用例完成后，得到结果yield
    outcome = yield
    resp = outcome.get_result() #  拿到运行结果的测试报告
    # 判断失败的场景，开始截图
    # resp.when测试用例执行的状态：setup（初始化），teardown（结束），call（测试用例执行）是否等于测试用例&失败
    if resp.when == 'call' and resp.failed:
        img = GlobalDriver.driver.get_screenshot_as_png()
        # 失败的报告粘贴到allure报告中
        # allure.attach(读取出来的内容即bytes, 图片的名字， 附件的类型 )
        allure.attach(img, '失败截图', attachment_type=allure.attachment_type.PNG)

'''
fixture 函数可以实现setup的功能，在测试用例之前执行内容，类似初始化
功能更强大，可以任意命名
@pytest.fixture(scope="",autouse=False)
autouse=False:不自动引用
session：pytest发起请求到结束，只会执行一次（命令行发起pytest请求）
function：函数级别的测试用例和方法级别的测试用例执行一次
class：引用fixture函数的class类，就会执行一次
module:引用fixture函数的python文件，就会执行一次

引用：把fixture装饰的函数的名字当做参数传递到测试用例中调用即可
teardown在conftest.py中如何实现？
只需要yield这个关键字，关键字后写测试用例结束之后需要执行的内容
'''

# 用fixture()方法来写setup和teardown
@pytest.fixture(scope= 'session', autouse= True)
def init_driver(browser_name, worker_id):
    # 实例化driver对象
    GlobalDriver.driver = InitDriver(browser_name, worker_id, remote_url='http://127.0.0.1:4444/wb/hub')   # 生产driver对象
    # 地址
    GlobalDriver.driver.get('http://www.mtxshop.com:3000/')
    # 调用登录业务
    # Login(GlobalDriver.driver).buyer_login()  # 关键字框架运行时注释掉
    yield   # 实现teardown
    GlobalDriver.driver.quit()

@pytest.fixture(scope= 'function', autouse= True)
def case_setup_teardown(worker_id):
    # 生成动态图时候可能会报错：一些文件被占用
    # 解决办法：加以下这行代码
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    # 截图--多线程去执行截图的任务
    th = Thread(target=shot, args=(GlobalDriver.driver, worker_id))
    # 启动线程
    th.start()
    yield
    # 将已截图的图片列举出来
    img_lists = os.listdir('video')
    new_list = []
    for img_name in img_lists:
        if img_name.startswith(worker_id) and img_name.endswith('.png'):
            new_list.append(img_name)
    # 排序,保证稳健性
    if worker_id == 'master':
        new_list.sort(key=lambda x: int(x[6:-4]))
    else:
        new_list.sort(key=lambda x: int(x[3:-4]))
    # 拼接gif
    first_img = Image.open(os.path.join('video', new_list[0]))
    other_imgs = []
    # 其他的照片，需要经过Image.open()进行转换，然后与第一张图片进行拼接
    for i in new_list[1:]:
        fb = Image.open(os.path.join('video', i))
        other_imgs.append(fb)
    # 保存最终的gif图
    first_img.save(DIR_NAME+f'video/{worker_id}_record.gif', # 路径
                   append_images=other_imgs,
                   duration=300,    # 存储时间
                   save_all=True,
                   loop=0)# 持续播放
    time.sleep(2)
    #将gif图贴到allure中
    with open(DIR_NAME+f'video/{worker_id}_record.gif', 'rb') as f:
        content = f.read()
        allure.attach(content, '测试用例播放图', attachment_type=allure.attachment_type.GIF)
    # 每条用例执行完成后都要返回首页
    GlobalDriver.driver.get('http://www.mtxshop.com:3000/')   # 应用driver对象

def shot(dr, worker_id):
    '''
    不断的截图
    :return:
    兼容性：不同的浏览器运行，多进程去运行
    worker_id: 名字是固定的，pytest底层已封装；单进程任务时，worker_id = master
    多任务执行时，worker_id = gw0，gw1，gw2……
    '''
    # 每条测试用例执行之前将video中的所有图片先清空
    img_lists = os.listdir('video')
    for img_name in img_lists:
        if img_name.startswith(worker_id) and img_name.endswith('.png'):
            # 删除包里面的文件内容
            os.remove('/video'+img_name)
    n = 0
    while True:
        try:
            dr.get_screenshot_as_file(DIR_NAME+f'/video/{worker_id}{n}.png')  # 图片名字动态变化
        except:
            return  # 截图失败退出循环
        # 每隔0.2s开始截图
        time.sleep(0.2)
        # 增量
        n += 1
# 增加命令行参数
def pytest_addoption(parser):
    # 把--browser的值收集成列表的形式 ['firefox','chrome']
    parser.addoption('--browser', action='append', default=['chrome'])
# 从命令行获取参数的值
def pytest_generate_tests(metafunc):
    metafunc.parametrize(
        'browser_name',     # 把--browser 这个命令行的值赋值给browser_name这个变量
        metafunc.config.getoption('browser'),
        scope='session'
    )

