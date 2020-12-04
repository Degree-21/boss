import configparser

conf = configparser.ConfigParser()
conf.read("conf/app.ini", encoding="utf-8")


# 获取参数
def get_config(index, key):
    return conf.get(index, key)
