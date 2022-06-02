import logging

from django.conf import settings

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.tasks import notify_subscribers_weekly

logger = logging.getLogger(__name__)


def notify_subscribers_weekly_job():
    # Your job processing logic here...
    notify_subscribers_weekly()
    print('notify job')


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=60*60*24*7):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        # scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)

        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            notify_subscribers_weekly_job,
            trigger=CronTrigger(day="*/7"),
            # trigger=CronTrigger(
            #     day_of_week="mon", hour="00", minute="00"
            # ),
            id="notify_subscribers_weekly_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'notify_subscribers_weekly_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить,
            # либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
