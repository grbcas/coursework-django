import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from mailing.services import frequently_send_mailings

logger = logging.getLogger(__name__)


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way. 
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
  This job deletes APScheduler job execution entries older than `max_age` from the database.
  It helps to prevent the database from filling up with old historical records that are no
  longer useful.

  :param max_age: The maximum length of time to retain historical job execution records.
                  Defaults to 7 days.
  """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            frequently_send_mailings,
            trigger=CronTrigger(day="*/1"),  # Every day
            id="job_one_day_send_mailings",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
            args=['1']
        )
        logger.info("Added job 'job_one_day_send_mailings'.")

        scheduler.add_job(
            frequently_send_mailings,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="job_week_send_mailings",
            max_instances=1,
            replace_existing=True,
            args=['7']
        )
        logger.info(
            "Added weekly job: 'job_week_send_mailings'."
        )

        scheduler.add_job(
            frequently_send_mailings,
            trigger=CronTrigger(month="*/1"),
            id="job_month_send_mailings",
            max_instances=1,
            replace_existing=True,
            args=['30']
        )
        logger.info(
            "Added weekly job: 'job_week_send_mailings'."
        )

        # test каждые 10 сек
        scheduler.add_job(
            frequently_send_mailings,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="frequently_send_mailings",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
            args=['1']
        )
        logger.info("Added job 'frequently_send_mailings'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

