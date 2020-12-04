# from lib import config
# res = config.get_config("selenium", "web_driver")
# print(res)
import getopt
import sys
import os
from task import boss
from task import echart

try:
    opts, args = getopt.getopt(sys.argv[1:], "-t:", ["type"])
    print(opts)
    for opt_name, opt_value in opts:
        if opt_name in ('-t', '--type'):
            if opt_name == "r":
                boss.run_boss_task()
            else:
                echart.get_all_chart()
except getopt.GetoptError:
    sys.exit()
