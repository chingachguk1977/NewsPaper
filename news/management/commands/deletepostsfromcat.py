from django.core.management.base import BaseCommand, CommandError
from news.models import *


class Command(BaseCommand):
    # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    help = 'Удаляет посты из указанных категорий'
    # напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны
    # все миграции (если такие есть)
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('cats2delete', nargs='+', type=str)

    def handle(self, *args, **options):
        # проверяем, что такая категория есть
        # cats = Category.objects.all()

        for cat_id in options['cats2delete']:

            # спрашиваем пользователя действительно ли он хочет удалить все посты из заданной категории
            self.stdout.write(
                'Delete all posts tagged as "%s"? yes/no' % cat_id)
            answer = input()  # считываем подтверждение

            if answer.lower() == 'yes':  # в случае подтверждения действительно удаляем все товары
                try:
                    category = Category.objects.get(cat_name=cat_id)
                    Post.objects.filter(cats=category).delete()
                except Category.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'"{cat_id}" category does not exist'))

                self.stdout.write(self.style.SUCCESS('Successfully deleted posts tagged as "%s"' % cat_id))
                continue

            # в случае неправильного подтверждения, говорим что в доступе отказано
            self.stdout.write(self.style.ERROR('Delete unsuccessful'))
