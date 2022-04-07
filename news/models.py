from django.db import models
# from django.utils import timezone
from datetime import datetime, date, time
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    rating = models.SmallIntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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

    def __str__(self):
        return f'{self.user.username}, rating = {self.rating}'


class Category(models.Model):
    cat_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.cat_name


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'

    POST_CHOICES = [
        (ARTICLE, 'article'),
        (NEWS, 'news')
    ]

    type = models.CharField(max_length=2, choices=POST_CHOICES, default=NEWS)
    time_pub = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    body = models.TextField()
    rating = models.SmallIntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    cats = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        post_metadata = f"'{self.title}' by {self.author.user.username},\n \
                          published on: {self.time_pub.strftime('%d/%m/%Y, %H:%M')},\n \
                          the rating of this post is {self.rating}\nPreview: {self.preview()}"
        return post_metadata

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.body) > 124:
            return f'{self.body[:124]}...'
        return self.body


class Comment(models.Model):
    body = models.TextField()
    time_pub = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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


class PostCategory(models.Model):
    post_thru = models.ForeignKey(Post, on_delete=models.CASCADE)
    cat_thru = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post_thru} <-> {self.cat_thru}'
