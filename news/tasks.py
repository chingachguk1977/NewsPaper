from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.conf import settings
from .models import Post
from datetime import timedelta, date


# from django.utils.timezone import datetime, timedelta, timezone, timestamp


def get_subscribers(category):
    """
    iterate thro all subscribers in Category table, extract their email and form up a list of email recepients
    """
    email_recipients = []
    for user in category.subscribers.all():
        email_recipients.append(user.email)
    return email_recipients


def send_emails(post_object, *args, **kwargs):
    # print(kwargs['template'])
    html = render_to_string(
        kwargs['template'],
        {'category_object': kwargs['category_object'], 'post_object': post_object},
        # передаем в шаблон любые переменные
    )
    # print(f'category: {category}')
    print(kwargs)
    msg = EmailMultiAlternatives(
        subject=kwargs['email_subject'],
        from_email=settings.EMAIL_HOST_USER,
        to=kwargs['email_recipients']  # отправляем всем из списка
    )
    msg.attach_alternative(html, 'text/html')
    msg.send(fail_silently=False)


def new_post_subscription(instance):
    # latest_post = Post.objects.all().order_by('-dateCreated')[0]
    template = 'newpost.html'
    latest_post = instance

    if not latest_post.isUpdated:
        for category in latest_post.cats.all():
            email_subject = f"New Post in Category: '{category}'"
            email_recipients = get_subscribers(category)
            send_emails(
                latest_post,
                category_object=category,
                email_subject=email_subject,
                template=template,
                email_recipients=email_recipients)


def notify_subscribers_weekly():
    week = timedelta(days=7)
    posts = Post.objects.all()
    past_week_posts = []
    template = 'weekly_digest.html'
    email_subject = 'Your News Portal Weekly Digest'

    for post in posts:
        time_delta = date.today() - post.time_pub.date()
        if time_delta < week:
            past_week_posts.append(post)
    # past_week_posts = posts.filter(dateCreated__range=[str(today), str(week)])

    past_week_categories = set()
    for post in past_week_posts:
        # past_week_categories.add(post.postCategory.all())

        for category in post.cats.all():
            past_week_categories.add(category)
            # print(post.postCategory.all().filter(catsub=category))

    # print(past_week_categories)

    email_recipients = set()
    for category in past_week_categories:
        # # print(category.subscribers.all())
        # email_subject = f'New post in category: "{category}"'
        get_user_emails = set(get_subscribers(category))
        email_recipients.update(get_user_emails)
        # print(get_user_emails)

    # print(post.postCategory.all().filter(postCategory=category))
    # print(user_emails)

    for email in email_recipients:
        post_object = []
        categories = set()

        for post in past_week_posts:
            subscription = post.cats.all().values('subscribers').filter(subscribers__email=email)

            if subscription.exists():
                # print(subscription)
                post_object.append(post)
                categories.update(post.cats.filter(subscribers__email=email))
        print(email)
        # print(post_object)
        category_object = list(categories)
        print(category_object)
        # print(set(post.postCategory.all()))

        send_emails(
            post_object,
            category_object=category_object,
            email_subject=email_subject,
            template=template,
            user_emails=[email, ]
        )
