import numpy as np
import json
import ast
from news.models import article,user
import urllib
import os
import re
import random
from datetime import datetime
from django.forms.models import model_to_dict
from django.core import serializers
from django.conf import settings
base_dir = settings.BASE_DIR

VOCA_BOOK = base_dir+"\\static\\voca_book\\" # 单词本文件的根目录
RANDOM_WORDS = 10 # 每个词库随机取的词数
# 在views部分用到的功能性函数全部放到这里~
# 在views部分只编写接口函数
def hello():
    return "this is function~"


# 获取最合适的10篇文章，sample是用户数据
def top_n(sample):

    # 对数据库操作
    data = article.objects.all() # get all articles

    # 只抽取文章的内容地址以及覆盖率来比较,key是content，value是cover_rate
    res = {}

    for item in data: # 计算所有文章的相似度
        c_r = item.cover_rate
        cover_rate = ast.literal_eval(c_r) # 将文章覆盖率转成字典
        c_r_list = []

        for key in cover_rate:
            c_r_list.append(cover_rate[key]) # 覆盖率存入list

        dist = np.sqrt(np.sum(np.square(sample - np.asarray(c_r_list)))) # sample是用户词汇覆盖度数据

        res[item.id] = dist # 以id作为字典字段
        
    sort_list = sorted(res.items(), key = lambda item:item[1], reverse = True)
    sort_list = sort_list[:10] # 只取前十个

    # 获取文章内容
    res = []
    for key in sort_list:
        item = article.objects.get(id = key[0])
        with open(item.content, 'r') as f:
            item.content = f.read()

        item_dict = dict(
            id=item.id, title=item.title, author=item.author,
            atype=item.atype, picUrl=item.picUrl, lettNum=item.lettNum,
            publish_time=item.publish_time
        )
        res.append(item_dict)
        # print(type(item))

    return res # list

def get_random_words():
    
    lib_list = os.listdir(base_dir+"\\static\\lib") #获取词库
    
    res = {} # store all lib words
    for lib in lib_list:

        lib_name = re.findall(r'(.+?)\.',str(lib))[0] # 获取词库名

        random_list = [] # store words

        with open(base_dir+"\\static\\lib\\"+lib,'r') as f:
            words = json.load(f)
        
        num = len(words) # 单词总数

        for i in range(RANDOM_WORDS):
            word = words[random.randint(0,num)] # get a random word

            while word in random_list:
                word = random.randint(0,num)
            
            random_list.append(word)

        res[lib_name] = random_list

    return res # 返回字典，key是词库名，value是单词list



# 主程序唤起爬虫操作
# 爬完文章后文章信息存入本地文件
# 读取本地文件，存入数据库

def executeCrawl():
    filename = "hah"
    return filename

# 所有文章存入数据库
def save_articles():
    # 唤起爬虫,目前并唤不起来
    # filename = execcuteCrawl()

    filename = base_dir + "\\static\\res\\news.json"

    with open(filename, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break

            # 读出数据
            data = json.loads(line) # dictionary
            
            # 存入数据库
            addOne = article(title = data['title'], content = data['content'], author = data['author'],
                    atype = data['types'], picUrl = "", lettNum = 0, publish_time = data['update_time'], 
                    cover_rate = str(data['cover_rate']), date = datetime.now())

            addOne.save()

# todo 删除单词，还没测试
def deleteWord(id, word):

    try:
        uuser = user.objects.get(uid = id)
        bookpath = uuser.dict # 获取单词本所在位置


        with open(bookpath, 'w') as f:
            allwords = list(json.loads(f))

            if word in allwords:
                allwords.remove(word)

            f.write(json.dumps(allwords))

    except:
        print("删除单词出错")
        return False

    return True

# todo 添加生词，还没测试
def addWord(id, word):

    try:
        uuser = user.objects.get(uid = id)
        bookpath = uuser.dict  # get where book stores

        allwords = {}

        with open(bookpath, 'r') as f: # read words 
            allwords = dict(json.load(f))

        with open(bookpath, 'w') as f: # write new content
            if word in allwords.keys():
                allwords[word] = allwords[word] + 1
            else:
                allwords[word] = 0

            f.write(json.dumps(allwords))

    except:
        print("添加单词出错...")
        return False
    else:
        return True


def get_book(id):

    try:
        uuser = user.objects.get(uid = id)
        bookpath = uuser.dict  # get where book stores

        with open(bookpath, 'r') as f:
            allw = dict(json.load(f))

        return allw # 返回字典内容
    except:
        print("读取单词本内容出错...")
        return False
    
        





        

