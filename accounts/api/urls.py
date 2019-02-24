from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.UserListAPIView.as_view(), name='list'),
    url(r'^register/$', views.UserCreateAPIView.as_view(), name='register'),
    url(r'^login/$', views.UserLoginAPIView.as_view(), name='login'),
]
