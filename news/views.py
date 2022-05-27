from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView)

import NewsPaper.settings
from .models import (
    Author,
    Post,
    PostCategory,
    Comment,
    Category,
    CategorySubscribers)

from django.core.mail import EmailMultiAlternatives  # импортируем класс для создания объекта письма с html
from django.shortcuts import redirect
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from django.urls import resolve

from datetime import datetime
from django.urls import reverse_lazy

from .filters import PostFilter
from .forms import PostForm


# Create your views here.

class PostsList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Post
    permission_required = (
        'news.view_post',
    )
    ordering = 'time_pub'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    # Переопределяем функцию получения списка постов
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = Category.objects.all()
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        context['qs_len'] = len(Post.objects.all())
        return context


class PostDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Post
    template_name = 'post.html'
    permission_required = (
        'news.view_post',
    )
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
        context['comments'] = Post.comment_set.all()
        return context


# Добавляем новое представление для создания постов.
class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    permission_required = (
        'news.add_post',
    )
    template_name = 'post_edit.html'
    success_url = '/posts/'

    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     post.type = 'AR'
    #     return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    permission_required = (
        'news.change_post',
    )
    template_name = 'post_edit.html'
    success_url = '/posts/'


# class ProfileUpdate(LoginRequiredMixin, UpdateView):
#     template_name = 'profile_update.html'
#     form_class = UserForm
#     success_url = '/posts/'
#     login_url = '/accounts/login/'
#     redirect_field_name = 'redirect_to'
#
#     def get_object(self, **kwargs):
#         return self.request.user


# Представление удаляющее товар.
class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    permission_required = (
        'news.change_post',
    )
    template_name = 'post_delete.html'
    # success_url = reverse_lazy('post_list')
    success_url = '/posts/'


class PostSearchView(PostsList):
    template_name = 'post_search.html'


# TODO Везде расписать комменты, какая команда что делает
def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/posts')

    return render(request, 'post_create.html', {'form': form})


class ProtectedView(LoginRequiredMixin, UpdateView):
    template_name = 'protected_page.html'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


#
#
# def profile_edit(request):
#     template_name = 'profile_update.html'
#     form = UserForm
#     return render(request, template_name, {'form': form})

class PostAuthor(ListView):
    model = Post
    template_name = 'filtered.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        queryset = Post.objects.filter(author=Author.objects.get(id=self.id))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        context['name'] = Author.objects.get(user=User.objects.get(id=self.id))

        return context


class PostType(ListView):
    model = Post
    template_name = 'filtered.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        # self.categoryType = self.get_categoryType_display
        self.type = resolve(self.request.path_info).kwargs['type']
        queryset = Post.objects.filter(cats=self.type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        # context['data'] = page_name(self.request)
        context['cat_name'] = self.name

        return context


class PostTag(ListView):
    model = Post
    template_name = 'filtered.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        queryset = Post.objects.filter(cats=Category.objects.get(id=self.id))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        context['name'] = Category.objects.get(id=self.id)

        return context


# Подписка пользователя в категорию новостей
@login_required
def subscribe_to_category(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)

    if not cat.subscribers.filter(id=user.id).exists():
        cat.subscribers.add(user)
        html = render_to_string(  # передаем в шаблон переменные, тут передал категорию для вывода ее в письме
            'subscribed.html',
            {'categories': cat, 'user': user},
        )
        category = f'{cat}'
        email = user.email
        msg = EmailMultiAlternatives(
            subject=f'Subscription to {category} category',
            from_email=NewsPaper.settings.EMAIL_HOST_USER,
            to=[email, ],
        )

        msg.attach_alternative(html, 'text/html')
        try:
            msg.send()
        except Exception as e:
            print(e)

        return redirect('/posts/')

    return redirect('/posts/')  # (request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_from_category(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)

    if cat.subscribers.filter(id=user.id).exists():
        cat.subscribers.remove(user)
    return redirect('/posts/')
