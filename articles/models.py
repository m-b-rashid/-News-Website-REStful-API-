from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings


# Create your models here.
class Article(models.Model):
	#genre choices are fixed. so if you want to add a new genre, it needs to be added here
    GENRE_CHOICES = (
        ('TE', 'Technology'),
        ('SC', 'Science'),
        ('HE', 'Health'),
        ('ED', 'Education'),
        ('EN', 'Entertainment'),
        ('SP', 'Sports'),
        ('BU', 'Business'),
        ('UK', 'General'),
    )

    articleid = models.AutoField(primary_key=True)
    image = models.FileField(null=True, blank=True)
    title = models.CharField(max_length=64)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    author = models.CharField(max_length=64)
    postTime = models.DateTimeField(auto_now_add=True)
    genre = models.CharField(max_length=2, choices=GENRE_CHOICES, default='UK')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_dislikes')

    def  __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("articles:detail", kwargs={"id" : self.articleid})

    def get_api_url(self):
            return reverse("articles-api:detail", kwargs={"id" : self.articleid})

    def get_like_url(self):
        return reverse("articles:likes", kwargs={"id" : self.articleid})

    def get_dislike_url(self):
        return reverse("articles:dislikes", kwargs={"id" : self.articleid})


    #makes default author the user that created article
    def save(self, *args, **kwargs):
        if not self.author:
            self.author = self.user
        super(Article, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-postTime"]
