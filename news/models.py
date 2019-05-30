# Create your models here.

from django.db import models
from django.utils import timezone
import json

MAX_LENGTH = 500


class user(models.Model):

    # 用户唯一标识,加密后的信息
    uid = models.CharField(max_length = MAX_LENGTH, primary_key = True)

    # openid
    openid = models.CharField(max_length = MAX_LENGTH)

    # 单词本，存放文件地址
    dict = models.CharField(max_length = MAX_LENGTH, null = True) 

    # 暂时考虑直接存放覆盖率
    cover_rate = models.CharField(max_length = MAX_LENGTH, null = True) 


    def __str__(self):
        return self.openid

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
    date = models.DateField(default=timezone.now()) 


    def __str__(self):
        return self.title

    def toJSON(self):
        item = {}
        item['id'] = self.id
        item['title'] = self.title
        item['date'] = self.date
        item['content'] = self.content
        item['author'] = self.author
        item['atype'] = self.atype
        item['picUrl'] = self.picUrl
        item['lettNum'] = self.lettNum
        item['publish_time'] = self.publish_time
        item['cover_rate'] = self.cover_rate

        return json.dumps(item)



class vocabulary(models.Model):

    # 词汇量覆盖度
    cover_rate = models.CharField(max_length=MAX_LENGTH, null = True)

    # 外键是用户
    user = models.ForeignKey(user , null = True, on_delete=models.CASCADE)

    # 测试时间
    date = models.DateField(default=timezone.now())



class collectArticle(models.Model):

    # 主键是自动的

    # 设置两个外键
    user = models.ForeignKey(user, on_delete=models.CASCADE)

    article = models.ForeignKey(article, on_delete=models.CASCADE)

    # collect date
    date = models.DateField(default = timezone.now())



class testHistory(models.Model):

    user = models.ForeignKey(user, on_delete=models.CASCADE)

    # 覆盖率
    cover_rate = models.CharField(max_length = MAX_LENGTH)

    # 测试日期
    date = models.DateField(default = timezone.now())


