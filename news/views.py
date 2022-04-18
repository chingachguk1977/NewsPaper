from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Author, Post, PostCategory, Comment, Category
from datetime import datetime


# Create your views here.
class PostsList(ListView):
    model = Post
    ordering = 'time_pub'
    template_name = 'posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = Category.objects.all()
        context['time_now'] = datetime.utcnow()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class CategoryDetail(DetailView):
    # Выводим список категорий. Далее фильтруем посты по категориям и делаем вывод всех постов
    # относящихся к данной категории.
    model = Category
    context_object_name = 'category_detail'

    def get_context_data(self, **kwargs):
        id = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        # Контекст для списка постов в текущей категории.
        context['category_post'] = Post.objects.filter(post_category=id)
        # Контекст постов данной категории.
        context['post_category'] = PostCategory.objects.get(post=self.kwargs['pk']).cats
        return context


"""
class CommentDetail(DetailView):
    model = Comment
    ordering = '-datetime'
    template_name = 'post.html' #TODO это здесь надо?
    context_object_name = 'comments'
"""