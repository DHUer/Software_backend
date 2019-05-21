import numpy as np
import sys
import os
import re
import json
import urllib.request
import random
import base64
import hashlib
from django.shortcuts import render
from scrapy.cmdline import execute 
from django.http import HttpResponse
from news.models import article,user
from django.conf import settings
base_dir = settings.BASE_DIR # where manage.py lies
from news.function import * # 直接用里面的函数就成，不用加function.xx了

VOCA_BOOK = base_dir+"\\static\\voca_book\\" # 单词本根目录
# Create your views here.

def test(request):
    return HttpResponse(base_dir)


# 根据文章路径读取内容
def get_content(filepath): 

    with open(filepath, 'r') as f:
        data = json.load(f) # 直接读出来就是list        
 
    return data # 返回文章中所有单词list


# 返回所有文章基本信息不包含内容，可以考虑从数据库中读取
def get_article_info(request): 

    # 工作目录在root下和manage.py同级,然后res也在root下
    datapath = base_dir + "\\res\\news.json"

    articles = []
    with open(datapath, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break

            # print(line)
            data = json.loads(line)
            articles.append(data)
            # print(data)

    return HttpResponse(json.dumps(articles), content_type="application/json") # 返回所有文章的基本信息


# 获取文章所有信息加内容
def get_article(request):

    datapath = base_dir + "\\static\\res\\news.json"

    article = []
    try:
        with open(datapath, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                
                data = json.loads(line)
                filepath = data['content'] # 获取文章内容所在位置
                data['content'] = get_content(filepath) # 获取文章内容
                print(data['content'])

                article.append(data)
    except:
        print("获取文章信息失败")

    return HttpResponse(json.dumps(article), content_type="application/json")

# 获取读者词汇掌握程度，推荐难度最适合的文章
def get_similiar(request, paramList):

    try:
        user_rate = json.loads(request.GET.get("cover_rate")) # 获取参数
        res = function.top_n(user_rate)
    except:
        print("推荐难度最合适文章出错...")
    

    return HttpResponse(json.dumps(res), content_type="application/json")


# TODO 按不同难度返回文章
def diffidegree(request):

    return True

# 随机从各个词库抽取单词返回给前端
def randomWords(request):

    res = get_random_words()

    return HttpResponse(json.dumps(res), content_type="application/json")


# 创建用户
def createUser(request):

    print("create user...")

    # 这里为了安全性不直接取出数据，而是通过request直接获取
    param = {
        'appid': "wxae69c4033fec8983",
        'secret': "9f0a3ddfc941f313eea51106731e6bb7",
        'js_code': request.GET.get('code'),    # 获取用户初次登陆的code
        'grant_type': 'authorization_code'  
    }

    # get openid and session_key
    url = "https://api.weixin.qq.com/sns/jscode2session?appid=" + param['appid'] + "&secret=" + param['secret'] + "&js_code=" + param['js_code'] + "&grant_type=authorization_code"
    req = urllib.request.urlopen(url)
    res = req.read()  # bytes

    res_str = bytes.decode(res) # bytes to string

    res_dict = json.loads(res_str) # str to dict

    oid = res_dict['openid']
    

    # 加密
    oid_byte = str.encode(oid)

    # 获取hash算法的对象
    hash = hashlib.md5()

    # 设置/追加信息
    hash.update(oid_byte)

    # 获取加密的结果
    en_uid = hash.hexdigest()

    # 在数据库中创建用户数据，以加密后的id作为单词本的文件名
    bookpath = VOCA_BOOK+en_uid+".json"
    newuser = user(uid = en_uid, openid = oid, dict = bookpath)

    with open(bookpath, 'w') as f: # 先创建文件并写入大括弧
        f.write("{}")

    newuser.save()

    return HttpResponse(en_uid) # 直接返回加密的字符串

# todo 收藏文章
def collectArticle(request):


    return True


# todo 为测试对单词本进行操作
# op:0 -- add, 1 -- delete, 2 -- get all words 
def addNewWords(request):

    op = request.GET.get("op")
    id = request.GET.get("id") # 或许应该是session id?

    if op == 0:
        word = request.GET.get("word")
        addWord(id, word)

    elif op == 1:
        word = request.GET.get("word")
        deleteWord(id, word)
    
    else:
        res = get_book(id)
        return HttpResponse(json.dumps(res), content_type="application/json")

# todo 按不同分类返回文章
def getNewsByType(request):
    return True

# todo 查看所有收藏文章
def getAllCollection(request):
    return True

