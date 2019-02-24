from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.CommentListAPIView.as_view(), name='list'),
    #url(r'^(?P<id>\d+)/post/$', views.Post, name='post'),
    url(r'^create/$', views.CommentCreateAPIView.as_view(), name='create'),
    url(r'^(?P<id>\d+)/$', views.CommentDetailAPIView.as_view(), name='detail'),
    #url(r'^(?P<id>\d+)/edit/$', views.CommentEditAPIView.as_view(), name='edit'), #delete aswell
    #url(r'^delete/$', views.DeletePost, name='delete'),

]
