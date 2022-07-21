from django.db import models
from django.utils import timezone
from datetime import datetime, date, time
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.cache import cache
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy  # ленивый геттекст с подсказкой


class Author(models.Model):
    rating = models.SmallIntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(
        User,
        through='AuthorSubscribers',
        blank=True,
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss',
    )

    def update_rating(self):
        posts_rating = self.post_set.aggregate(post_rating_aggr=Sum('rating'))
        posts_rating_sum = 0
        posts_rating_sum += posts_rating.get('post_rating_aggr')

        comments_rating = self.user.comment_set.aggregate(comments_rating_aggr=Sum('rating'))
        comments_rating_sum = 0
        comments_rating_sum += comments_rating.get('comments_rating_aggr')

        self.rating = posts_rating_sum * 3 + comments_rating_sum

        # author_posts = self.post_set.all()
        # for post in author_posts:
        #     self.rating += post.rating * 3
        #     post_comments = post.comment_set.all()
        #     for comment in post_comments:
        #         self.rating += comment.rating

        self.save()
        return self.rating

    def subscribe(self):
        pass

    # Возвращает автора с лучшим рейтингом
    @staticmethod
    def best_author():
        return Author.objects.all().order_by('-rating')[0]

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} ({self.user})' \
                if (self.user.first_name and self.user.last_name) else f'{self.user}'
        # return f'{self.user.username}, rating = {self.rating}'

    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')


class Category(models.Model):
    cat_name = models.CharField(
        max_length=64,
        unique=True,
        help_text=_('category'),
    )
    subscribers = models.ManyToManyField(
        User,
        through='CategorySubscribers',
        blank=True,
        verbose_name=pgettext_lazy(
            'help text for Category subscribers',
            'subscribers',
        ),
    )

    def subscribe(self):
        pass

    def get_category(self):
        return self.cat_name

    def __str__(self):
        return f'{self.cat_name}'

    @staticmethod
    def is_subscribed(self):
        # self.subscribers.user.id
        cat = Category.objects.get(id=pk)
        return cat.subscribers.filter(id=user.id).exists()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'

    POST_CHOICES = [
        (ARTICLE, 'article'),
        (NEWS, 'news')
    ]

    type = models.CharField(verbose_name=_('type'), max_length=2,
                            choices=POST_CHOICES, default=NEWS)
    time_pub = models.DateTimeField(
        _('time_pub'),
        auto_now_add=True,
        # default=timezone.now,
    )
    title = models.CharField(_('title'), max_length=128)
    body = models.TextField(_('body'), default='')
    rating = models.SmallIntegerField(_('rating'), default=0)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name=pgettext_lazy('help text for Post author', 'author'),
        related_name='author',
    )
    cats = models.ManyToManyField(
        Category,
        through='PostCategory',
        verbose_name=_('category'),
    )
    isUpdated = models.BooleanField(_('edited'), default=False)

    def __str__(self):
        num_of_comments = len(self.comment_set.all())
        post_metadata = f"'{self.title}' by {self.author.user.username},\n \
                          published on: {self.time_pub.strftime('%d/%m/%Y, %H:%M')},\n \
                          the rating of this post is {self.rating}\nPreview: {self.preview()}.\n \
                          It has {num_of_comments} comments."
        return post_metadata
        # return f'ID: {self.id}, Title: {self.title}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.body) > 124:
            return f'{self.body[:124]}...'
        return f'{self.body}'

    def get_absolute_url(self):
        # return f'/posts/{self.id}'
        return reverse('post_detail', args=[str(self.id)])

    def email_preview(self):
        if len(self.body) > 51:
            return f'{self.body[:51]}...'
        return f'{self.body}'

    def get_cat(self):
        return '\n'.join([c.cat_name for c in self.cats.all()])  # f'{self.type}'

    def save(self, *args, **kwargs):
        self.isUpdated = False
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')


class CategorySubscribers(models.Model):
    subscriber_thru = models.ForeignKey(
        User,
        verbose_name=_('subscriber'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    category_thru = models.ForeignKey(
        Category,
        verbose_name=_('category'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def get_user(self):
        return self.subscriber_thru

    def extract_category(self):
        return self.category_thru.cat_name

    def get_category(self):
        return self.category_thru

    def __str__(self):
        return f'{self.subscriber_thru} <-> {self.category_thru.cat_name}'

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')


class AuthorSubscribers(models.Model):
    subscriber_thru = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    author_thru = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)

    def get_user(self):
        return self.subscriber_thru

    def extract_category(self):
        return self.author_thru.user.username

    def get_category(self):
        return self.author_thru

    def __str__(self):
        return f'{self.subscriber_thru} <-> {self.author_thru.user.username}'


class Comment(models.Model):
    body = models.TextField(_('body'))
    time_pub = models.DateTimeField(_('time_pub'), auto_now_add=True)
    rating = models.SmallIntegerField(_('rating'), default=0)
    post = models.ForeignKey(Post, verbose_name=_('comm_post'), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_('login'), on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        comment_metadata = f"{self.user.username} wrote: '{self.body[:64]}',\n \
                             on: {self.time_pub.strftime('%d-%m-%Y, %H:%M')},\n \
                             the rating of this comment is {self.rating}\n"
        return comment_metadata

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class PostCategory(models.Model):
    post_thru = models.ForeignKey(Post, verbose_name=_('corr_post'), on_delete=models.CASCADE)
    cat_thru = models.ForeignKey(Category, verbose_name=_('corr_category'), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.cat_thru} <-> {self.post_thru.title}'

    class Meta:
        verbose_name = _('post category')
        verbose_name_plural = _('post categories')
