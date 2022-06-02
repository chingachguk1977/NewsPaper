from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор

from .apscheduler import its_time
from .models import Post, PostCategory
from .tasks import new_post_subscription, notify_subscribers_weekly


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция,
# и в отправители надо передать также модель
@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        print('notifying subscribers from signals...')
        new_post_subscription(instance)


@receiver(its_time, sender='Weekly')
def notify_subscribers(sender, **kwargs):
    print('sending out weekly digest...')
    notify_subscribers_weekly()
