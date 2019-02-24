from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
ListAPIView,
RetrieveAPIView,
DestroyAPIView,
 UpdateAPIView,
 CreateAPIView,
 RetrieveUpdateAPIView)

from rest_framework.permissions import(
AllowAny,
IsAuthenticated,
IsAdminUser,
IsAuthenticatedOrReadOnly
)

from .pagination import ArticleLimitOffsetPagination, ArticlePageNumberPagination
from .permissions import IsOwnerOrReadOnly #default permissions IsAuthenticated for all views (look settings) IsOwnerOrReadOnly is a custom permission in the articles.permissions.py

from articles.models import Article
from .serializers import ArticleListSerializer, ArticleDetailSerializer, ArticleCreateUpdateSerializer

class ArticleListAPIView(ListAPIView):
    serializer_class = ArticleListSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]  # filter by url parameters
    search_fields = ['title', 'content', 'author'] #search url parameters
    pagination_class = ArticlePageNumberPagination
    def get_queryset(self, *args, **kwargs):
        queryset = Article.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
            Q(title__icontains=query)| # ?q= filter by url parameters
            Q(content__icontains=query)|
            Q(author__icontains=query)
            ).distinct()
        return queryset

class ArticleDetailAPIView(RetrieveAPIView):
    queryset = Article.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ArticleDetailSerializer
    lookup_field = 'articleid'
    lookup_url_kwarg = 'id'

class ArticleUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleCreateUpdateSerializer
    lookup_field = 'articleid'
    lookup_url_kwarg = 'id'
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class ArticleDeleteAPIView(DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'articleid'
    lookup_url_kwarg = 'id'

    def perform_delete(self, serializer):
        serializer.save(user=self.request.user)

class ArticleCreateAPIView(CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleCreateUpdateSerializer


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
