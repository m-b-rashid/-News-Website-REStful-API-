from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField

from comments.models import Comment
from accounts.api.serializers import UserDetailSerializer

class CommentSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    article = SerializerMethodField()
    detail_url = HyperlinkedIdentityField(view_name='comments-api:detail', lookup_field = 'id', lookup_url_kwarg = 'id')
    article_url = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'id',
            'article',
            'user',
            'comment',
            'dateTime',
            'detail_url',
            'article_url'
        ]
        read_only_fields = [
            'id',
            'article',
            'user',
            'dateTime'
        ]

    def get_article_url(self, obj):
        return obj.article.get_api_url()

    def get_article(self, obj):
        return str(obj.article.title)



class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'article',
            'comment',
        ]
