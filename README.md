# webui_frame

## 项目介绍
本项目是通过采用PO/POM模式和关键字框架实现webUI自动化测试，以及在webUI框架中集成grid。

## 上手指南
1.下载代码到本地
```yaml
git@github.com:lingxiaoshu/webui_frame.git
```
2.修改pytest.ini配置内容后，执行run.py文件

1）运行testcases中的用例
- 单线程执行第一条addopts即可
- 多线程执行第三条addopts
- 用例失败后重新执行，执行第二条addopts
```ini
[pytest]
addopts = -sv  --alluredir ./reports/report --clean-alluredir
;addopts = -sv  --alluredir ./reports/shop --clean-alluredir  --reruns 2
;addopts = -sv  --alluredir ./reports/shop --clean-alluredir  -n 2 --browser chrome

testpaths = ./testcases
python_files = test_*.py
python_classes = Test*
python_funtions = test_*
```
2）运行keyword中的用例
```ini
[pytest]
addopts = -sv  --alluredir ./reports/report --clean-alluredir
;addopts = -sv  --alluredir ./reports/shop --clean-alluredir  --reruns 2
;addopts = -sv  --alluredir ./reports/shop --clean-alluredir  -n 2 --browser chrome

testpaths = ./keyword
python_files = keyword.py
python_classes = Test*
python_funtions = test_*
```
## 技术选型
- python37
- allure-pytest-2.11.1
- Faker-15.1.1,
- assume-2.4.3
- rerunfailures-11.1.1
- parallel-0.1.1
- xdist-3.2.1

## 框架：
### PO/POM模式（page object module）体现分层思想

pages：将单独的页面独立出来，管理自己页面中元素的基本操作

actions：通过组装页面层的基本操作，完成一个页面流程的封装

testcases：调用业务层封装的业务，传递不同的测试数据，实现断言和报告


### 关键字框架
actions：存放业务变量
testcases：存放测试用例
webUI关键字框架通过yaml文件做载体，解析yaml文件获取变量。

### webUI框架中集成 grid 


