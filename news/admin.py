from django.contrib import admin
from django.utils.translation import gettext as _
from .models import (
    Author, Post, PostCategory, Comment, Category,
    CategorySubscribers, AuthorSubscribers)

# импортируем модель амдинки
from modeltranslation.admin import TranslationAdmin


def nullify_rating(request, queryset):
    # все аргументы уже знакомы, самые нужные из них это
    # request — объект хранящий информацию о запросе и
    # queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(rating=0)
    nullify_rating.short_description = 'Set rating to zero'


# создаём новый класс для представления постов в админке
class PostAdmin(TranslationAdmin):  # admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице
    # генерируем список имён всех полей для более красивого отображения
    # list_display = [field.name for field in Post._meta.get_fields()]
    model = Post
    list_display = ('title', 'author', 'time_pub', 'body', 'get_cat', 'rating',)
    list_filter = ('rating', 'time_pub',)
    search_fields = ('title', 'cats__cat_name')
    list_per_page = 5
    actions = [nullify_rating]


class AuthorAdmin(admin.ModelAdmin):  # TranslationAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице
    # генерируем список имён всех полей для более красивого отображения
    # list_display = [field.name for field in Post._meta.get_fields()]
    model = Author
    list_display = ('user', 'rating',)
    list_filter = ('rating',)
    search_fields = ('user', 'rating',)
    actions = [nullify_rating]


class CategoryAdmin(TranslationAdmin):  # admin.ModelAdmin):
    model = Category


class CommentAdmin(TranslationAdmin):  # admin.ModelAdmin):
    model = Comment


# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CategorySubscribers)
admin.site.register(AuthorSubscribers)
