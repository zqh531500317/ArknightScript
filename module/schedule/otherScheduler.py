from module.schedule.baseScheduler import base_scheduler
from apscheduler.triggers.date import DateTrigger
import module.task.other


def test(fc):
    base_scheduler.test_add_job(module.task.other.test, args=(fc,), trigger=DateTrigger(),
                                id="test_" + str(fc))
