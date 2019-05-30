from django.urls import path

from . import  views

urlpatterns = [
    path('test/',views.test),

    path('get_brief/',views.get_article_info), # 获取文章基本信息加摘要

    path('get_detail/',views.get_article), # 获取文章所有内容包括具体内容

    path('createUser/',views.createUser), # 创建用户，先别测试

    path('get_test_words/',views.randomWords),  # 获取测试词汇

    path('get_news_by_type/<str:types>/',views.getNewsByType),  # 根据分类获取文章

    path('collect_article/<int:aid>/<str:uid>',views.collect),  # 收藏文章，先别测试

    path('get_all_collection/<str:uid>/',views.getAllCollection),   # 获取所有收藏文章

    path('voca_book/<int:op>/<str:uid>/<str:word>/',views.voca_book),   # 单词本，先别测试
    # op:0 -- add, 1 -- delete, 2 -- get all words  如果是获取所有单词，在word部分也要随便传个参数

    path('get_article_by_id/<int:aid>/',views.getArticleById),  # 根据文章id获取内容

    path('get_test_history/<str:uid>/',views.getRecordHistory), # 获取历史测试记录，别测试

    path('save_test_res/',views.saveTestRes),
    
    path('get_token/<int:aid>/',views.get_mp3),

    path('get_top_10/<str:id>/',views.get_similiar)
]