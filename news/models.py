from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

article = 'ART'
news = 'NEWS'

POST_TYPES = [
    (article, 'article'),
    (news, 'news')
]


class Author(models.Model):
    author_name = models.CharField(max_length=40)
    author_rating = models.FloatField(default=0.0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self, user):
        ...


class Category(models.Model):
    category_name = models.CharField(max_length=40, unique=True)


class Post(models.Model):
    post_type = models.CharField(max_length=5, choices=POST_TYPES, default=news)
    time_pub = models.DateTimeField(auto_now_add=True)
    post_title = models.TextField()
    post_body = models.TextField()
    post_rating = models.FloatField(default=0.0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        ...

    def dislike(self):
        ...

    def preview(self):
        ...


class Comment(models.Model):
    comment_body = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.FloatField(default=0.0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        ...

    def dislike(self):
        ...


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
