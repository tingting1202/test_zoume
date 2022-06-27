"""
1、测试类前面使用ddt
2、在测试方法前使用@list_ddt(测试数据)
3、在测试方法中定义一个参数，用例接收用例数据

setUpClass  ：#测试类级别的前置  ：测试类中的用例执行前执行
tearDownClass  ：#测试类级别的后置  ：测试类中的所有用例执行之后执行

"""

import unittest
import os
import requests
from unittestreport import ddt, list_data
from jsonpath import jsonpath

from common.handle_excel import HandleExcel
from common.handle_conf import conf
from common.handle_path import data_dir, conf_dir
from common.handle_log import my_log

@ddt
class TestClasses(unittest.TestCase):

    #excel路径拼接，指定子表
    excel = HandleExcel(os.path.join(data_dir, 'Class.xlsx'), 'Addclass')
    cases = excel.read_data()

    # 用户id暂时不用
    # excel1 = HandleExcel(os.path.join(conf_dir, 'user.xlsx'), 'user')
    # userid = excel1.read_data()
    # print(userid)

    # 项目地址
    base_url = conf.get('env', 'base_url1')
    #请求头
    headers = eval(conf.get('env', 'headers1'))

    @classmethod
    def setUpClass(cls) -> None:
        """
        :return: 用例类的前置方法，用于返回学校id，给后面接口使用，只执行一次
        """
        #获取所有学校接口
        url = conf.get('env', 'base_url1') + "/ZouMe/GetAllSchoolList"
        headers = eval(conf.get('env', 'headers1'))
        response = requests.post(url=url, headers=headers)
        res = (response.json())
        # print(res)
        #去获取学校id,可选择获取第一个; #提取用户的schoolid给新增班级使用
        cls.schoolid = jsonpath(res, "$.result[0].schoolList[0].schoolID")

        # print(cls.userid)

    @list_data(cases)
    def test_Addclass(self, item):    #用来接收用例数据

        # 新增班级号的接口
        url = self.base_url + item['url']
        #接口参数
        # 先判断是否有schoolID需要替换，#动态处理需要进行替换的参数
        if "${schoolID}" in item['data']:
            item['data'] = item['data'].replace('${schoolID}', str(self.schoolid))
        # if '${UserID}' in item["data"]:
        #     item['data'] = item['data'].replace('${UserID}', str(self.userid))
        # print(item['data'])

        params = eval(item['data'])
        excepted = eval(item['excepted'])
        method = item['method'].lower()

        #第二步：发送请求，获取接口返回的实际结果
        response = requests.request(method=method, url=url, json=params, headers=self.headers)
        res = (response.json())
        print("预期结果：", excepted)
        print("实际结果：", res)

        #第三步：断言
        try:
            self.assertEqual(excepted['code'], res['code'])
            self.assertEqual(excepted['message'], res['message'])
        except AssertionError as e:
            my_log.error('用例--[{}]---执行失败'.format(item['title']))
            my_log.exception(e)
            raise e
        else:
            my_log.info('用例---[{}]---执行通过'.format(item['title']))


