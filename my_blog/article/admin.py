from django.contrib import admin
from .models import ArticlePost


admin.site.register(ArticlePost)

from .models import ArticleColumn

# 注册文章
admin.site.register(ArticleColumn)