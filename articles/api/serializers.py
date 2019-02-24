from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField

from articles.models import Article
from comments.models import Comment
from comments.api.serializers import CommentSerializer
from accounts.api.serializers import UserDetailSerializer


class ArticleListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='articles-api:detail', lookup_field = 'articleid', lookup_url_kwarg = 'id')
    user = UserDetailSerializer(read_only=True)
    class Meta:
        model = Article
        fields = [
            'url',
            'user',
            'articleid',
            'title',
            'content',
            'author',
            'genre'
        ]

class ArticleDetailSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='articles-api:detail', lookup_field = 'articleid', lookup_url_kwarg = 'id')
    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()
    likes = SerializerMethodField()
    dislikes = SerializerMethodField()
    comments = SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'url',
            'articleid',
            'title',
            'content',
            'author',
            'user',
            'image',
            'likes',
            'dislikes',
            'comments',
            'genre'
        ]

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_likes(self, obj):
        likes = obj.likes.count()
        return likes

    def get_dislikes(self, obj):
        dislikes = obj.dislikes.count()
        return dislikes

    def get_comments(self, obj):
        c_qs = Comment.objects.filter(article__articleid = obj.articleid)
        comments = CommentSerializer(c_qs, context={'request': None}, many=True).data
        return comments

class ArticleCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'author',
            'genre',
        ]
