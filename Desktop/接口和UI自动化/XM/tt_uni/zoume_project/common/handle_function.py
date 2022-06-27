import random

def random_mobile():
    """随机生成手机号最近号段需要看开发的代码是否支持，如199，测试时，可以确定前三位，也可以修改前三位"""
    phone = str(random.randint(13300000000, 13399999999))
    return (phone)

# 调试：
# phone = random_mobile()
# print(phone)

def random_num():
    """随机生成数值数据"""
    num = str(random.randint(1, 9999))
    return (num)




