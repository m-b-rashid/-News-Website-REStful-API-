from __future__ import unicode_literals
from django.db import models
from django.conf import settings

from articles.models import Article
# Create your models here.
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    comment = models.TextField(null=True)
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username) + " : " + str(self.comment)
