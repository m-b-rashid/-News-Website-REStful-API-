from django.conf.urls import url, include

from . import views

urlpatterns = [

    url(r'^$', views.ArticleListAPIView.as_view(), name='list'),
    url(r'^create/$', views.ArticleCreateAPIView.as_view(), name='create'),
    url(r'^(?P<id>\d+)/$', views.ArticleDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<id>\d+)/edit/$', views.ArticleUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<id>\d+)/delete/$', views.ArticleDeleteAPIView.as_view(), name='delete'),
    #url(r'^filter/$', views.article_filter, name='filter'),
    #url(r'^yolo/$', views.yolo),
    #url(r'^(?P<id>\d+)/likes/$', views.article_like, name='likes'),
    #url(r'^(?P<id>\d+)/dislikes/$', views.article_dislike, name='dislikes'),
]
