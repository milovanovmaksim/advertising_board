import zoneinfo
from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from .notificate_user_new_ad_weekly import NotificationUserNewAds


time_zone = zoneinfo.ZoneInfo(settings.TIME_ZONE)
weekly_notifier = NotificationUserNewAds(time_zone=time_zone, timedelta=timedelta(days=6))


@util.close_old_connections
def delete_old_job_executions(max_age=604800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            weekly_notifier.run,
            trigger=CronTrigger(second="*/10"),
            id="notification_user_new_ad_weekly",
            max_instances=5,
            replace_existing=True)
        self.stdout.write(self.style.SUCCESS("Added a job with id='notification_user_new_ad_weekly'"))

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="sun", hour="11", minute="00"),
            id="delete_old_job_executions",
            max_instances=5,
            replace_existing=True)
        self.stdout.write(self.style.SUCCESS("Added a job with id='delete_old_job_executions'"))

        try:
            self.stdout.write(self.style.NOTICE("Starting scheduler..."))
            scheduler.start()
        except KeyboardInterrupt:
            self.style.NOTICE('Stopping scheduler...')
            scheduler.shutdown()
            self.stdout.write(self.style.SUCCESS("Scheduler shut down successfully!"))
