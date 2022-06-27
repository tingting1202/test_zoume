"""
INFO:root:这是一条info级别的日志
WARNING:root:这是一条warning级别的日志
ERROR:root:这是一条error级别的日志
CRITICAL:root:这是一条critical级别的日志

"""

import logging
import os
from common.handle_conf import conf     #引入conf对象
from common.handle_path import log_dir


def create_log(name='mylog', level='DEBUG', filename='log.log', fh_level='DEBUG', sh_level='DEBUG'):
    # 1、创建一个日志收集器
    log = logging.getLogger(name)

    # 2、设置只收集DEBUG以上等级的日志
    log.setLevel(level)

    # 3、设置输出日志的等级
    # 3.1 输出到文件
    # 创建一个日志输出的渠道，#只输出WARNING以上等级的日志
    fh = logging.FileHandler(filename, encoding="utf-8")
    fh.setLevel(fh_level)
    log.addHandler(fh)

    # 3.2输出到控制台
    sh = logging.StreamHandler()
    sh.setLevel(sh_level)
    # 2、将输出渠道绑定到日志收集器上
    log.addHandler(sh)

    # 设置日志输出的等级
    formats = "%(asctime)s--%(filename)s-%(lineno)d --%(levelname)s:%(message)s"
    #创建格式对象
    log_format = logging.Formatter(formats)

    # 设置输出到控制台的日志格式
    sh.setFormatter(log_format)
    # 设置输出到文件的日志格式
    fh.setFormatter(log_format)

    #返回一个日志收集器
    return log

my_log = create_log(
    name=conf.get('logging', 'name'),
    level=conf.get('logging', 'level'),
    filename=os.path.join(log_dir, conf.get('logging', 'filename')),
    sh_level=conf.get('logging', 'sh_level'),
    fh_level=conf.get('logging', 'fh_level')
)