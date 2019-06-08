from django.urls import path

from . import  views

'''
注意：
1、所有功能均能测试
2、有的参数是通过url直接传递，请务必遵循path第一个参数的格式
3、有的参数是放在request部分，可在代码部分查看（一般就在前几行，形如request.get...）
4、进行用户相关的操作请务必先创建用户
5、404错误一般有可能是url部分错了，没和下面匹配到
6、有bug请务必及时反馈，最好附上截图，方便复现。
7、关于考研/托福/雅思等分类，直接在前端进行判断（根据文章词汇覆盖度最高的一项分类）
8、最近浏览可以直接在前端的缓存中记录/也可以不实现。
'''

urlpatterns = [
    path('test/',views.test),

    # 所有文章/基本信息/摘要
    path('get_brief/',views.get_article_info),

    # 所有文章/基本信息/具体内容
    path('get_detail/',views.get_article), 

    # 创建用户/参数code/返回id（若没有返回id，请检查参数传递方式是否正确）
    path('createUser/',views.createUser), 

    # 获取测试词汇
    path('get_test_words/',views.randomWords),  

    # 根据分类获取文章/分类目前有health/world/sport
    path('get_news_by_type/<str:types>/',views.getNewsByType), 

    # 收藏文章/aid是文章id/uid是用户id
    path('collect_article/<int:aid>/<str:uid>',views.collect),  

    # 获取用户所有收藏文章/id是用户id
    path('get_all_collection/<str:id>/',views.getAllCollection), 

    # 单词本
    path('voca_book/<int:op>/<str:uid>/<str:word>/',views.voca_book),   
    # op:0 -- add, 1 -- delete, 2 -- get all words  如果是获取所有单词，在word部分也要随便传个参数(即，word参数不能为空)
    
    # 根据文章id获取内容
    path('get_article_by_id/<int:aid>/',views.getArticleById),  
    
    # 获取历史测试记录
    path('get_test_history/<str:uid>/',views.getRecordHistory), 

    # 存储测试结果/参数如何传递请看代码部分
    path('save_test_res/',views.saveTestRes),
    
    # 获取文章音频
    path('get_audio/<int:aid>/',views.get_mp3),

    # 获取最适合用户阅读的十篇文章
    path('get_top_10/<str:id>/',views.get_similiar)
]

