from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
ListAPIView,
RetrieveAPIView,
DestroyAPIView,
 UpdateAPIView,
 CreateAPIView,
 RetrieveUpdateAPIView)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import(
AllowAny,
IsAuthenticated,
IsAdminUser,
IsAuthenticatedOrReadOnly
)

from articles.api.pagination import ArticleLimitOffsetPagination, ArticlePageNumberPagination
from articles.api.permissions import IsOwnerOrReadOnly #default permissions IsAuthenticated for all views (look settings) IsOwnerOrReadOnly is a custom permission in the articles.permissions.py

User = get_user_model()

from .serializers import UserCreateSerializer, UserLoginSerializer, UserDetailSerializer


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.new_data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class UserListAPIView(ListAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter] # filter by url parameters
    search_fields = ['email', 'name', 'is_staff'] #search url parameters
    pagination_class = ArticlePageNumberPagination
    def get_queryset(self, *args, **kwargs):
        queryset = User.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter( # ?q= filter by url parameters
            Q(email__icontains=query)|
            Q(name__icontains=query)|
            Q(is_staff__icontains=query)
            ).distinct()
        return queryset
