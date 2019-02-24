from django.contrib import admin

# Register your models here.
from .models import Article

class ArticleModelAdmin(admin.ModelAdmin):
    list_display = ["title", "articleid", "author", "postTime"]
    list_filter = ["author", "postTime"]
    search_fields = ["title", "content"]

    class Meta:
        model = Article

admin.site.register(Article, ArticleModelAdmin)
