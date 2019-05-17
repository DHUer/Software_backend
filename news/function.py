import numpy as np
import json
from news.models import article,user
import urllib


# 在views部分用到的功能性函数全部放到这里~
# 在views部分只编写接口函数
def hello():
    return "this is function~"

def top_n(dict, sample):

    for key in dict:
        dist = np.sqrt(np.sum(np.square(sample - dict[key]))) # sample是用户词汇覆盖度数据
        dict[key].append(dist) #将欧式距离加入每个文本的list，位置是最后一个，前7个都是覆盖度

    # print(dict.items())
    sort = sorted(dict.items(), key = lambda item:item[1][7], reverse = True) # 由大到小排列，返回的是list

    title = []
    for index, item in enumerate(sort):

        if index == 10:
            break

        title.append(item[0])

    return title # 返回文章标题



# 主程序唤起爬虫操作
# 爬完文章后文章信息存入本地文件
# 读取本地文件，存入数据库

def executeCrawl():
    filename = "hah"
    return filename

# 讲所有文章存入数据库
def save_articles():
    # 唤起爬虫
    filename = execcuteCrawl()

    with open(filename, 'r') as f:
        data = json.load(f)

        # 读出数据

        for item in data:
            # addOne = article(title = , content = , author = ,
            #         type = , picUrl = , lettNum = , time = , cover_rate = )

            addOne.save()


    # test 尝试获取id为1的对象
    tmp = Article.objects.filter().filter(id=1)
    print(tmp)


# 创建用户
def createUser(request):
    code = request.POST['code'] # 获取用户初次登陆的code

    # 这里为了安全性不直接取出数据，而是通过request直接获取
    param = {
        'appid': request.POST['appid'],
        'secret': request.POST['secret'],
        'js_code': request.POST['code'],
        'grant_type': 'authorization_code'
    }

    # https://www.cnblogs.com/poerli/p/6429673.html






# 收藏文章
def collectArticle(request):


    return True

# 向单词本中添加单词
def addNewWords(request):

    try: 

        id = request.POST['openid']
        word = request.POST['word']

        user = User.objects.get(openid = id)
        filepath = user.dict # 获取用户单词本存放地址

        with open(filepath, 'a') as f:
            wlist = json.load(f)
            # 读成list格式，并添加新的词，然后写回去


        return True

    finally:
        return False


    




# 获得用户测试词汇量数据
def getCoverRate(request):

    try:
        id = request.POST['openid'] # 获取用户id
        data = request.POST['cover_rate'] # 获取词汇测试结果

        user = User.objects.get(openid = id)

        user.cover_rate = data
        user.save()

        return True

    finally:
        return False # 操作失败






        

