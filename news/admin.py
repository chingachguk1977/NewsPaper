from django.contrib import admin
from .models import (
    Author, Post, PostCategory, Comment, Category,
    CategorySubscribers, AuthorSubscribers)


def nullify_rating(modeladmin, request, queryset):
    # все аргументы уже знакомы, самые нужные из них это
    # request — объект хранящий информацию о запросе и
    # queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(rating=0)
    nullify_rating.short_description = 'Set rating to zero'


# создаём новый класс для представления постов в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице
    # генерируем список имён всех полей для более красивого отображения
    # list_display = [field.name for field in Post._meta.get_fields()]
    list_display = ('title', 'author', 'time_pub', 'body', 'get_cat', 'rating',)
    list_filter = ('rating', 'time_pub',)
    search_fields = ('title', 'cats__cat_name')
    actions = [nullify_rating]


class AuthorAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице
    # генерируем список имён всех полей для более красивого отображения
    # list_display = [field.name for field in Post._meta.get_fields()]
    list_display = ('user', 'rating',)
    list_filter = ('rating',)
    search_fields = ('user', 'rating',)
    actions = [nullify_rating]


# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(CategorySubscribers)
admin.site.register(AuthorSubscribers)
