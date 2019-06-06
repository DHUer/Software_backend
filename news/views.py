import numpy as np
import sys
import os
import re
import json
import urllib.request
import random
import base64
import ast
import hashlib
from django.shortcuts import render
from scrapy.cmdline import execute 
from django.http import HttpResponse
from django.core import serializers
from news.models import article,user,vocabulary,collectArticle
from django.conf import settings
base_dir = settings.BASE_DIR # where manage.py lies
from news.function import * # 直接用里面的函数就成，不用加function.xx了

VOCA_BOOK = base_dir+"\\static\\voca_book\\" # 单词本根目录
# Create your views here.

def test(request):
    return HttpResponse(open(r"G:\\CloudMusic\\Time travel.mp3",'rb'),content_type="audio/mp3")


# 根据文章路径读取内容
def get_content(filepath): 

    with open(filepath, 'r') as f:
        data = json.load(f) # 直接读出来就是list        

    return data # 返回文章中所有单词list

# 返回所有文章内容
def get_article_content(request):
    datapath = base_dir + "\\static\\res\\news.json"

    res = []

    try:

        article_list = article.objects.all()

        for item in article_list:
            with open(item.content, "r") as f:
                content = json.load(f)

            res.append({
                "title":item.title,
                "id":item.id,
                "type":item.atype,
                "num":item.lettNum,
                "pic":item.picUrl,
                "date":item.publish_time,
                "author":item.author,
                "content":content,
                "cover_rate":item.cover_rate
            })
    except Exception as e:
        print(e)
        print("获取文章信息失败")

    return HttpResponse(json.dumps(res), content_type="application/json")

# 返回所有文章基本信息不包含内容
def get_article_info(request): 

    # 工作目录在root下和manage.py同级,然后res也在root下
    datapath = base_dir + "\\static\\res\\news.json"

    article_list = article.objects.all()
    res = serializers.serialize("json", article_list)

    return HttpResponse(res, content_type="application/json") # 返回所有文章的基本信息

# 获取文章所有信息加摘要
def get_article(request):

    datapath = base_dir + "\\static\\res\\news.json"

    res = []

    try:

        article_list = article.objects.all()

        for item in article_list:
            with open(item.content, "r") as f:
                content = json.load(f)

            res.append({
                "title":item.title,
                "id":item.id,
                "type":item.atype,
                "num":item.lettNum,
                "pic":item.picUrl,
                "date":item.publish_time,
                "author":item.author,
                "content":content[0],
                "cover_rate":item.cover_rate
            })
    except Exception as e:
        print(e)
        print("获取文章信息失败")

    return HttpResponse(json.dumps(res), content_type="application/json")

# 获取读者词汇掌握程度，推荐难度最适合的文章
def get_similiar(request, id):

    try:
        res = {}

        curr_user = user.objects.get(uid = id)
        all_c_r = vocabulary.objects.filter(user = curr_user)

        if len(all_c_r) == 0: # 如果没有测试过，返回假
            res['flag'] = False

        else:
            res['flag'] = True

            c_r  = all_c_r[len(all_c_r) - 1].cover_rate # 获取最新的测试数据

            cover_rate = ast.literal_eval(c_r) # 将文章覆盖率转成字典
            
            c_r_list = []

            for key in cover_rate:
                c_r_list.append(cover_rate[key]) # 覆盖率存入list

            res['article'] = top_n(c_r_list)
            
    except Exception as e:
        print(e)
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

# 收藏文章
def collect(request, aid, uid):

    # aid = request.GET.get("aid") # 获取文章id
    # uid = request.GET.get("openid") # get user id

    if collectArticles(uid, aid):
        return HttpResponse(json.dumps("True"), content_type="application/json") # 收藏失败

    else:
        return HttpResponse(json.dumps("False"), content_type="application/json") # 收藏成功

# 为测试对单词本进行操作
# op:0 -- add, 1 -- delete, 2 -- get all words 
def voca_book(request, uid, op, word):

    if op == 0:

        addWord(uid, word)

    elif op == 1:

        deleteWord(uid, word)
    
    else:
        res = get_book(uid)
        return HttpResponse(json.dumps(res), content_type="application/json")

    return HttpResponse("True")

# 按不同分类返回文章
def getNewsByType(request, types):
    # types = request.POST['type']

    all_articles = article.objects.filter(atype__iexact = types) # case insensitive
    res = serializers.serialize("json", all_articles)

    return HttpResponse(res, content_type="application/json")

# 查看所有收藏文章
def getAllCollection(request,id):

    curr_user = user.objects.get(uid = id)

    print("curr user is " + str(curr_user))

    collection_list = []
    arti_list = collectArticle.objects.filter(user = curr_user).values("article") # 获取该用户所有收藏信息
    
    print(arti_list)

    for item in arti_list:
        aid = item['article']
        news = article.objects.get(id = aid) # get article
        
        collection_list.append(news)

    res = serializers.serialize("json", collection_list)

    return HttpResponse(res , content_type="application/json") # 只返回

# 返回历史测试记录
def getRecordHistory(request, uid):

    curr_user = user.objects.get(uid = uid)

    test_record = vocabulary.objects.filter( user = curr_user)

    res = serializers.serialize("json", test_record)

    return HttpResponse(res , content_type="application/json")

# 获取测试结果并返回分析数据
def saveTestRes(request):

    res = request.GET.get('cover_rate')
    id = request.GET.get('uid')

    curr_user = user.objects.get(uid = id)
    
    print(curr_user)
    print(res)

    record = vocabulary(cover_rate = res, user = curr_user) # 创建新的测试记录

    record.save()

    return HttpResponse("True")

# 根据文章id获取文章内容
def getArticleById(request,aid):

    item = article.objects.get(id = aid)

    filepath = item.content
    
    article_brief_info = {
                "title":item.title,
                "id":item.id,
                "type":item.atype,
                "num":item.lettNum,
                "pic":item.picUrl,
                "date":item.publish_time,
                "author":item.author,
                "content":get_content(filepath),
                "cover_rate":item.cover_rate
    }

    return HttpResponse(json.dumps(article_brief_info), content_type = "application/json")

# 返回音频
def get_mp3(request,aid):

    item = article.objects.get(id = aid)
    filepath = item.content 

    with open(filepath,'r',encoding='UTF-8') as f:
        content = json.load(f)

    txt = ""
    for para in content:
        for word in para:
            txt = txt + word + " "
    filename = str(item.id)+".mp3"

    get_voice(txt, filename)
    
    filepath = base_dir + "\\static\\audio\\" + filename

    with open(filepath, 'rb') as f:
        response = HttpResponse()
        response.write(f.read())
        response['Content-Type'] ='audio/mp3'
        response['Content-Length'] =os.path.getsize(filepath)

    return response



