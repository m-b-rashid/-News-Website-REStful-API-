from django.conf.urls import url, include
from . import views

urlpatterns = [

    url(r'^$', views.article_list, name='list'),
    url(r'^create/$', views.article_create),
    url(r'^(?P<id>\d+)/$', views.article_detail, name='detail'),
    url(r'^(?P<id>\d+)/edit/$', views.article_update),
    url(r'^(?P<id>\d+)/delete/$', views.article_delete),
    url(r'^filter/$', views.article_filter, name='filter'),
    url(r'^(?P<id>\d+)/likes/$', views.article_like, name='likes'),
    url(r'^(?P<id>\d+)/dislikes/$', views.article_dislike, name='dislikes'),
    url(r'^yolo/$', views.yolo),
]
