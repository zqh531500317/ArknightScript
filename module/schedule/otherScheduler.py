from apscheduler.triggers.cron import CronTrigger
from module.schedule.baseScheduler import base_scheduler
from apscheduler.triggers.date import DateTrigger
import module.task.other
from module.base import base


def add_all():
    restart()


def test(fc):
    base_scheduler.test_add_job(module.task.other.test, args=(fc,), trigger=DateTrigger(),
                                id="test_" + str(fc))


def restart():
    base_scheduler.add_job(module.task.other.restart,
                           trigger=CronTrigger(hour=base.restart_hour, minute=base.restart_minute),
                           id="restart", )
