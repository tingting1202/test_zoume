import unittest
import os
import requests
from unittestreport import ddt, list_data

from common.handle_excel import HandleExcel
from common.handle_path import data_dir
from common.handle_conf import conf
from common.handle_log import my_log


@ddt
class TestNew(unittest.TestCase):
    excel = HandleExcel(os.path.join(data_dir, 'teacher1.0.xlsx'), 'new')
    #读取用例的数据
    cases = excel.read_data()
    #url的读取放在类属性里面，以下所有用例调用一次即可
    #项目的基本地址
    base_url = conf.get('env', 'base_url')
    #请求头（写在类属性里面）,但是get方法识别出来是字符串，不是字典；用eval转换
    headers = eval(conf.get('env', 'headers'))

    @list_data(cases)
    def test_new(self, item):            #item用来接收用例数据

        #第一步：准备测试用例
        #1、接口地址--拼接用例表中的键名（url）,得到完整的接口路径
        url = self.base_url + item['url']
        #2、接口请求参数  (excel里面是字典，所以用eval转换，不然会识别为字符串)
        datas = eval(item['data'])
        # print(params)
        #3、请求头(也可以放在配置文件里面，更灵活，上面类属性已经引用了，这里就不要调用了)
        #4、请求方法（本来就是字符串，无需转换）  (如果获取的方法字符串为大写，可以使用lower进行小写转换)
        method = item['method'].lower()
        #5、用例预期结果
        excepted = eval(item['excepted'])

        #第二步：请求接口，获取返回实际结果
        # requests.post(url=url, data=datas, headers=self.headers)
        reponse = requests.request(method, url, json=datas, headers=self.headers)
        res = (reponse.json())

        #第三步：断言
        print('预期结果', excepted)
        print('实际结果', res)
        try:
            #断言code和Message字段是否一致
            self.assertEqual(excepted['Code'], res['Code'])
            self.assertEqual(excepted['Message'], res['Message'])
        #如果出现了异常，进行捕获,日志输出
        except AssertionError as e:
            #记录日志
            my_log.error('用例---【{}】---执行失败'.format(item['title']))
            #失败的原因也可以记录一下，进行溯源
            # my_log.error(e)
            #记录详细的用exception
            my_log.exception(e)
            #这里可以增加：回写结果到excel  (不建议写，因为会影响速度，这里暂时不写)
            #抛出异常
            raise e
        else:
            my_log.warning('用例---【{}】---执行通过'.format(item['title']))