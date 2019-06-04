import numpy as np
import json
import base64
import requests
import urllib.request
import urllib.parse
from urllib.request import urlopen
import ast
from news.models import article,user, collectArticle, vocabulary
import urllib
import os
import re
import random
from datetime import datetime
import traceback
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


# 获取最合适的10篇文章，sample是用户数据(user)
def top_n(sample):

    try:
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
                item.content = json.load(f)[0] # 只取第一段摘要

            item_dict = dict(
                id=item.id, title=item.title, author=item.author,
                atype=item.atype, picUrl=item.picUrl, lettNum=item.lettNum,
                publish_time=item.publish_time,content = item.content
            )
            res.append(item_dict)
            # print(type(item))
    except Exception as e:
        print(e)

    return res # list，直接返回所有文章信息以及摘要

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
            
            # 判断文件大小，如果为空表示没有扒下来，不存入数据库
            if os.path.getsize(data['content']) == 0:
                continue

            # 存入数据库
            addOne = article(title = data['title'], content = data['content'], author = data['author'],
                    atype = data['types'], picUrl = data['pic'], lettNum = data['totalLett'], publish_time = data['update_time'], 
                    cover_rate = str(data['cover_rate']), date = datetime.now())

            addOne.save()

# 删除单词
def deleteWord(id, word):

    try:
        uuser = user.objects.get(uid = id)
        bookpath = uuser.dict # 获取单词本所在位置


        with open(bookpath, 'r') as f:
            allwords = dict(json.load(f))

        with open(bookpath,'w') as f:
            if word in allwords.keys():
                allwords.pop(word)

            f.write(json.dumps(allwords))

    except Exception as e:
        print("删除单词出错")
        traceback.print_exc()
        return False

    return True

# 添加生词
def addWord(id, word):

    try:
        uuser = user.objects.get(uid = id)
        bookpath = uuser.dict  # get where book stores

        print ("user is " + str(uuser))

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

# 查看单词本
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
    
        
# 收藏文章
def collectArticles(id, aid):

    try:
        # get objects respectively
        print(id)
        print(aid)

        u = user.objects.get(uid = id)
        a = article.objects.get(id = aid)

        print(u)
        print(a)

        new_item = collectArticle(user = u, article = a)
        new_item.save()

        print(collectArticle.objects.all())

    except Exception as e:
        print(e)
        return False

    return True


def get_voice(txt, filename):
    # 获取文本语音
    token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"

    # 获取token
    api_key = "GfaYQjjmykKRdjcf2j3gO0Ew"
    api_secret = "HTNN7irn96nrD8VDRVrXfFzfhFkbT8Ft"
    url = token_url % (api_key, api_secret)

    res = requests.post(url)

    token_str = json.loads(res.text)["access_token"]
    print("token is " + token_str)

    data={'tex':txt,'lan':'zh','spd':5,'vol':9,'pit':5,'per':3,'cuid':"get_voice",'ctp':1,'tok':token_str}
    getvoice_url = "http://tsn.baidu.com/text2audio"
    voice_data=requests.post(getvoice_url,data=data,stream=True)

    print("正在存储 " + filename + "音频...")
    voice_fp = open(base_dir+"\\static\\audio\\" + filename,'wb+')
    voice_fp.write(voice_data.raw.read())
    voice_fp.close() 


def getPic():

    all_article = article.objects.all()

    index = 0
    for item in all_article:

        picUrl = item.picUrl
        curr = article.objects.get(id = item.id)

        html = requests.get("http:" + picUrl)

        filepath = base_dir+"\\static\\pic\\" + "pic" + str(index) + ".jpg"

        with open(filepath,'wb') as f:

            f.write(html.content)
        
        curr.picUrl = filepath
        curr.save()

        index = index + 1






