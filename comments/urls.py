from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<id>\d+)/post/$', views.Post, name='post'),
    url(r'^(?P<id>\d+)/messages/$', views.Messages, name='messages'),
    url(r'^delete/$', views.DeletePost, name='delete'),

]