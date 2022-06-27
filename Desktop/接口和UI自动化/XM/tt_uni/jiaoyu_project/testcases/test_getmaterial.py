import unittest
import requests
import os
from unittestreport import ddt, list_data

from common.handle_excel import HandleExcel
from common.handle_path import data_dir
from common.handle_conf import conf
from common.handle_log import my_log

@ddt
class TestMaterial(unittest.TestCase):
    excel = HandleExcel(os.path.join(data_dir, 'teacher1.0.xlsx'), 'GetMaterial')
    cases = excel.read_data()
    base_url = conf.get('env', 'base_url')    #IP
    # 请求头（写在类属性里面）,但是get方法识别出来是字符串，不是字典；用eval转换
    headers = eval(conf.get('env', 'headers') ) #请求头放在类下，全局引用
    print(headers)

    @list_data(cases)
    def test_getmaterial(self, item):
        #第一步：准备测试用例
        #得到完整的接口路径地址
        url = self.base_url + item['url']
        datas = eval(item['data'])
        method = item["method"].lower()
        excepted = eval(item['excepted'])

        #第二步：请求接口，接受返回数据
        response = requests.request(method, url, data=datas, headers=self.headers)
        res = (response.json())

        #第三步：断言
        print('预期结果', excepted)
        print('实际结果', res)
        try:
            #断言code和Message、status字段是否一致
            self.assertEqual(excepted['Code'], res['Code'])
            self.assertEqual(excepted['Message'], res['Message'])
            self.assertEqual(excepted['Status'], res['Status'])
        except AssertionError as e:
            my_log.error("用例---【{}】---执行失败".format(item['title']))
            my_log.error(e)
            raise e
        else:
            my_log.warning("用例----【{}】---执行通过".format(item["title"]))










