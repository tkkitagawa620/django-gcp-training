from django.contrib import admin
from blog.models import Article, Comment, Tag


class TagInLine(admin.TabularInline):
    model = Article.tags.through


class ArticleAdmin(admin.ModelAdmin):
    inlines = [TagInLine]
    exclude = ['tags', ]


admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Tag)
