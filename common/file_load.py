# 
# -*- coding: utf-8 -*-
# ---
# @Project: apiframework
# @Software: PyCharm
# @File: file_load.py
# @Author: chenhuaishu
# @Time: 2022/10/24 17:15
'''
读取yaml 和 Excel 文件
'''
import json

import pandas
import yaml

from setting import DIR_NAME


def read_yml(filename):
    '''
    读取yaml文件
    文件路径：绝对路径不推荐使用；
    相对路径:相对的是运行的文件
    '../data/buynow.yml' 相对file_load.py
    './data/buynow.yml' 相对main.py
    动态生成绝对路径
    1.获取当前项目的绝对路径
    2，跟读取的数据进行拼接
    :return:
    '''
    with open(DIR_NAME + filename, 'r', encoding='utf-8') as f:
        # 读取yml文件
        content = yaml.load(f, Loader=yaml.FullLoader)
        return content

def read_excel(filename,sheet_name):
    pd = pandas.read_excel(DIR_NAME+filename,sheet_name=sheet_name,
                      # 如果遇到空单元格，默认返回null，python无法解析
                      # keep_default_na=False时会返回空字符串
                      keep_default_na=False,
                      engine='openpyxl')
    # 总行数
    lines_count = pd.shape[0] # 获取总行数（不包含头部）
    # 总列数
    col_count = pd.columns.size
    data = []
    for i in range(lines_count):  # 遍历行
        line = []  # 存放同一行中不同列的数据
        for j in range(col_count):  # 遍历列
            text = pd.iloc[i, j]  # 行列交叉定位到单元格，获取内容
            # # 判断 列数=1时，请求参数需要转换成字典（正常读取是字符串）
            # if j == 1:
            #     text = json.loads(text)   # 将json格式的字符串转换成字典
            line.append(text)
        data.append(line)
    return data



if __name__ == '__main__':
    # print(read_yml('/data/buynow.yml')['buynow'])
    # data = read_excel('/data/mtxshop.xlsx', '添加地址')
    # print(data)
    # print(read_yml('/config/db.yml')['test'])
    # print(read_yml('/pagesfiles/buyer.yml'))
    print(read_yml('/keyword/testcases/test001_login.yml'))