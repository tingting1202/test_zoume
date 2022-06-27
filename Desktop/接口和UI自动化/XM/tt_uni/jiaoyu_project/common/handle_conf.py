import os
from configparser import ConfigParser
from common.handle_path import conf_dir


#第一种直接创建对象，读取，没有封装
# conf = ConfigParser()
# conf.read(r'/Users/tingting/ningmeng/接口自动化/py35/py35_17day/config.ini')

# 第二种，对以上方法进行封装

class Config(ConfigParser):
    """ 创建对象时，直接加载配置文件的内容"""

    def __init__(self, conf_file):
        super().__init__()
        self.read(conf_file, encoding= 'utf-8')

conf = Config(os.path.join(conf_dir, 'config.ini'))

# if __name__ == '__main__':
#
#     conf = Config(r'/Users/tingting/ningmeng/接口自动化/py35/py35_17day/config.ini')
#     name = conf.get('logging', 'name')
#     level = conf.get('logging', 'level')
#     filename = conf.get('logging', 'filename')
#     sh_level = conf.get('logging', 'sh_level')
#     fh_level = conf.get('logging', 'fh_level')
#
#     print(name)
#     print(level)
#     print(filename)
#     print(sh_level)
#     print(fh_level)