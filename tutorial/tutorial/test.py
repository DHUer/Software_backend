from scrapy.cmdline import execute
import os
import re
import sys

def executeSpider():

    cwd = os.getcwd()
    filepath = re.findall(r'(.+?)\\seprojext', cwd) # 获取项目文件绝对路径
    filedir = filepath[0]+"\\seprojext\\tutorial\\tutorial\\spiders"
    sys.path.append(filepath[0]+"\\seprojext\\tutorial\\tutorial")

    os.chdir(filedir)
    print(os.getcwd())
    execute("scrapy crawl cnn".split())

executeSpider()