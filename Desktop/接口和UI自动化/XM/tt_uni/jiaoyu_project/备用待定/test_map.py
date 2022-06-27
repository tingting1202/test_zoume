"""
充值的前提：登录-->提取token
unittest:
    用例级别的前置：setUp
    测试类级别的前置：setUpClass

    该项目运行未成功，参考

"""
import os
import unittest
import requests
from unittestreport import ddt, list_data
from jsonpath import jsonpath

from common.handle_excel import HandleExcel
from common.handle_path import data_dir
from common.handle_conf import conf
from common.handle_log import my_log

@ddt
class TestGetversion(unittest.TestCase):
    excel = HandleExcel(os.path.join(data_dir, 'teacher1.0.xlsx'), 'map333')
    cases = excel.read_data()

    def test_version(self, item):
        #第一步：准备数据
        url = conf.get('env', 'base_url') + item['url']
        params = eval(item['data'])
        #************************************************************************
        expected = eval(item['expected'])
        method = item['method'].lower()

        #第二步：发送请求，获取接口返回的实际结果
        reponse = requests.request(method=method, url=url, json=params, headers=self.headers)
        res = (reponse.json())
        print("预期结果：", expected)
        print("实际结果：", res)


        #第三步：断言
        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
        except AssertionError as e:
            my_log.error('用例--[{}]---执行失败'.format(item['title']))
            my_log.exception(e)
            raise e
        else:
            my_log.info('用例--[{}]---执行通过'.format(item['title']))
