"""
此模块专门用例处理项目中的绝对路径


"""

import os

#项目的根目录的绝对路径
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#用例数据所在目录
data_dir = os.path.join(base_dir, 'datas')

#配置文件的根目录
conf_dir = os.path.join(base_dir, 'conf')

#日志文件所在目录
log_dir = os.path.join(base_dir, 'logs')

#报告所在路径
reports_dir = os.path.join(base_dir,'reports')

#用例目录所在模块
case_dir = os.path.join(base_dir, 'testcases')