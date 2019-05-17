# Create your models here.

# class news(models.Model):
#     # title
#     title = models.CharField(max_length=255)

#     # author
#     author = models.CharField(max_length=255)

#     # TODO 需要定义文章model来读取数据库的内容
#     # content
#     content = models.FilePathField()
from django.db import models

MAX_LENGTH = 500
class article(models.Model): # 自动生成主键并自增

    # 标题
    title = models.CharField(max_length = MAX_LENGTH)

    # 内容，存放文件地址信息
    content = models.CharField(max_length = MAX_LENGTH)

    # 作者
    author = models.CharField(max_length = MAX_LENGTH)

    # 类型
    atype = models.CharField(max_length = MAX_LENGTH)

    # 图片地址
    picUrl = models.CharField(max_length = MAX_LENGTH)

    # 文章字数
    lettNum = models.IntegerField()

    # 报刊文章的发布日期
    publish_time = models.CharField(max_length = MAX_LENGTH) 

    # 文章词汇覆盖率
    cover_rate = models.CharField(max_length = MAX_LENGTH)

    # 文章的获取日期
    date = models.DateField() 

    def __str__(self):
        return self.title


class user(models.Model):

    # 用户唯一标识
    openid = models.CharField(max_length = MAX_LENGTH, primary_key = True)

    # 单词本，存放文件地址
    dict = models.CharField(max_length = MAX_LENGTH, null = True) 

    # 暂时考虑直接存放覆盖率
    cover_rate = models.CharField(max_length = MAX_LENGTH, null = True) 

    # 外键--收藏的文章
    collectArticle = models.ForeignKey(article, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return self.openid



class Blog(models.Model):
    
    title = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title


class test(models.Model):

    name = models.CharField(max_length=100, null = True)







