from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
ListAPIView,
RetrieveAPIView,
DestroyAPIView,
 UpdateAPIView,
 CreateAPIView,
 RetrieveUpdateAPIView)
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import(
AllowAny,
IsAuthenticated,
IsAdminUser,
IsAuthenticatedOrReadOnly
)

from articles.api.pagination import ArticleLimitOffsetPagination, ArticlePageNumberPagination
from articles.api.permissions import IsOwnerOrReadOnly  #default permissions IsAuthenticated for all views (look settings) IsOwnerOrReadOnly is a custom permission in the articles.permissions.py
from comments.models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer

class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter] # filter by url parameters
    search_fields = ['user', 'comment']  #search url parameters
    pagination_class = ArticlePageNumberPagination
    def get_queryset(self, *args, **kwargs):
        queryset = Comment.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
            Q(user__icontains=query)| # ?q= filter by url parameters
            Q(conmment__icontains=query)
            ).distinct()
        return queryset


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
