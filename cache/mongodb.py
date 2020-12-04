import pymongo
from lib import config
import time

host = config.get_config("mongodb", "host")
port = config.get_config("mongodb", "port")
database = config.get_config("mongodb", "database")

link_url = "mongodb://%s:%s/" % (host, port)
client = pymongo.MongoClient(link_url)
conn = client[database]
table = "job_info"


def insert_info(table, info):
    mycol = conn[table]
    info["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    info["update_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return mycol.insert_one(info)


def get_info_by_where(where):
    mycol = conn[table]
    return mycol.find(where)


def get_count_by_where(where):
    mycol = conn[table]
    return mycol.find(where).count()