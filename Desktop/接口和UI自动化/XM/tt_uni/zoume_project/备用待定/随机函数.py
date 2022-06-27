import unittest
import os
import random
import requests
from unittestreport import ddt, list_data

from common.handle_excel import HandleExcel
from common.handle_path import data_dir
from common.handle_conf import conf
from common.handle_log import my_log

@ddt
class TestRegister(unittest.TestCase):
    excel = HandleExcel(os.path.join(data_dir, 'login.xlsx'), 'register')
    #读取用例数据
    cases = excel.read_data()
    #项目的基本地址
    base_url = conf.get('env', 'base_url')
    #请求头
    headers = eval(conf.get('env', 'headers'))

    @list_data(cases)
    def test_register(self, item):       # item用来接收用例数据

        # 第一步：准备测试用例
        # 1、接口地址--拼接用例表中的键名（url）,得到完整的接口路径
        url = self.base_url + item['url']
        # 2、接口请求参数
        #判断是否有手机号需要替换
        if '#mobile#' in item['data']:
            phone = self.random_mobile()
            item['data'] = item['data'].replace('#mobile#', phone)

        params = eval(item['datas'])
        # 3、请求头(也可以放在配置文件里面，更灵活，上面类属性已经引用了，这里就不要调用了)
        # 4、请求方法（本来就是字符串，无需转换）  (如果获取的方法字符串为大写，可以使用lower进行小写转换)
        method = item['method'].lower()
        # 5、用例预期结果
        excepted = eval(item['excepted'])

        # 第二步：请求接口，获取返回实际结果
        # requests.post(url=url, data=datas, headers=self.headers)
        reponse = requests.request(method, url, json=params, headers=self.headers)
        res = (reponse.json())

        # 第三步：断言
        print('预期结果', excepted)
        print('实际结果', res)
        try:
            # 断言code和Message字段是否一致
            self.assertEqual(excepted['Code'], res['Code'])
            self.assertEqual(excepted['Message'], res['Message'])
        # 如果出现了异常，进行捕获,日志输出
        except AssertionError as e:
            # 记录日志
            my_log.error('用例---【{}】---执行失败'.format(item['title']))
            # 失败的原因也可以记录一下，进行溯源
            # my_log.error(e)
            # 记录详细的用exception
            my_log.exception(e)
            # 这里可以增加：回写结果到excel  (不建议写，因为会影响速度，这里暂时不写)
            # 抛出异常
            raise e
        else:
            my_log.warning('用例---【{}】---执行通过'.format(item['title']))
        ...

    def random_mobile(self):
        """随机生成手机号最近号段需要看开发的代码是否支持，如199，测试时，可以确定前三位"""
        #第一种写法：
        phone = str(random.randint(13300000000, 13399999999))
        return (phone)

        # 第二种写法：前三位固定，后面八位随机
        # mobile = '123'
        # for i in range(8):
        #     n = str(random.randint(0,9))
        #     mobile += n

