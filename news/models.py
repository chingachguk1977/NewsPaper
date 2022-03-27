from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User




class Author(models.Model):
    author_name = models.CharField(max_length=40)
    author_rating = models.SmallIntegerField(default=0)
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self, user):
        all_posts_rating = self.post_set.all().aggregate(post_rating=Sum('post_rating'))
        pRat = 0
        pRat += all_posts_rating.get('post_rating')
        pRat *= 3
        commentRat = self.user.comment_set.all().aggregate(comment_rating=Sum('comment_rating'))
        cRat = 0
        cRat += commentRat.get('comment_rating')
        
        author_posts = self.post_set.all()
        for p in author_posts:                      
            self.rating += p.rating * 3         
            p_comments = p.comment_set.all()
            for c in p_comments:               
                self.rating += c.rating  


class Category(models.Model):
    category_name = models.CharField(max_length=40, unique=True)


class Post(models.Model):

    article = 'ART'
    news = 'NEWS'

    POST_TYPES = [
        (article, 'article'),
        (news, 'news')
    ]
    
    post_type = models.CharField(max_length=5, choices=POST_TYPES, default=news)
    post_time_pub = models.DateTimeField(auto_now_add=True)
    post_title = models.CharField(max_length=128)
    post_body = models.TextField()
    post_rating = models.SmallIntegerField(default=0)
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.post_rating += 1
        self.save()
        return self.post_rating

    def dislike(self):
        self.post_rating -= 1
        self.save()
        return self.post_rating

    def preview(self):
        if len(self.post_body) > 124:
            return self.post_body[:124] + '...'
        return self.post_body


class Comment(models.Model):
    comment_body = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.SmallIntegerField(default=0)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()


class PostCategory(models.Model):
    post_thru = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_thru = models.ForeignKey(Category, on_delete=models.CASCADE)
