import numpy as np
import json
# from news.models import article,user
import urllib
from django.conf import settings
base_dir = settings.BASE_DIR

# 在views部分用到的功能性函数全部放到这里~
# 在views部分只编写接口函数
def hello():
    return "this is function~"


# 获取最合适的10篇文章，dict是文章，sample是用户数据
def top_n(filepath, sample):

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
    # 唤起爬虫,目前并唤不起来
    # filename = execcuteCrawl()

    filename = base_dir + "\\static\\res\\news.json"

    with open(filename, 'r') as f:
        data = json.loads(f)

        # 读出数据

        for item in data:
            print(data)
            break
            # addOne = article(title = , content = , author = ,
            #         type = , picUrl = , lettNum = , time = , cover_rate = )

            # addOne.save()

    # test 尝试获取id为1的对象
    # tmp = Article.objects.filter().filter(id=1)
    # print(tmp)


save_articles()








        

