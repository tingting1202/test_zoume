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
class TestMap01(unittest.TestCase):
    excel = HandleExcel(os.path.join(data_dir, 'teacher1.0.xlsx'), 'map333')
    cases = excel.read_data()

    @classmethod
    def setUpClass(cls) -> None:
        """
        用例类的前置方法：登录提取token
        :return:
        """
        #1、请求登录接口，进行登录
        url = conf.get('env', 'base_url') + '/connect/token'
        datas = {
            "phoneNumber": conf.get("test_data", "phoneNumber"),
            'smsCode': conf.get('test_data', 'smsCode'),
            'client_id': conf.get('test_data', 'client_id'),
            'client_secret': conf.get('test_data', 'client_secret'),
            'grant_type': conf.get('test_data', 'grant_type'),
            'scope': conf.get('test_data', 'userinfo_api%20offline_access')

        }
        headers = eval(conf.get('env', 'headers'))
        response = requests.post(url=url, data=datas, headers=headers)
        res = (response.json())

        #2、登录成功之后再去提取token
        token = jsonpath(res, '$.access_token')[0]
        #将token添加在请求头中
        headers['Authorization'] = 'Bearer' + token
        #保存含有token的请求头为类属性
        cls.headers = headers
        #setattr(TestRecharge, 'headers', headers)
        #3、提取用户的id给充值接口使用
        cls.member_id = jsonpath(res, '$..id')[0]
        print(cls.member_id)


    @list_data(cases)
    def test_recharge(self,item):
        #第一步：准备数据
        url = conf.get('env', 'base_url') + item['url']
        #*****************************动态替换参数************************************
        #动态处理需要进行替换的参数
        item['data'] = item['data'].replaces('#member_id#', str(self.id))
        # print(item['data'])
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
