# from scrapy.cmdline import execute
# import sys
# import os
#
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "education_law"])

# 单线程顺序执行多个爬虫

# 测试1 不会停止
# import os
# while True:
#     os.system("scrapy crawl education_law -s CLOSESPIDER_TIMEOUT=180")  # 新华网
#     os.system("scrapy crawl education_law_2 -s CLOSESPIDER_TIMEOUT=180")

# 测试2  只执行一个
# from scrapy import cmdline
# cmdline.execute("scrapy crawl education_law".split())
# cmdline.execute("scrapy crawl education_law_2".split())

#
# # 测试3单线程依次执行
import time
import os


os.system("scrapy crawl education_law")  # 四川教育网
time.sleep(10)
os.system("scrapy crawl education_law_1")  # 湖北教育厅
time.sleep(10)
os.system("scrapy crawl education_law_2")  # 山东省
time.sleep(10)
os.system("scrapy crawl education_law_3")  # 福建省
time.sleep(10)
os.system("scrapy crawl education_law_4")  # 海南省
time.sleep(10)
os.system("scrapy crawl education_law_5")  # 黑龙江省
