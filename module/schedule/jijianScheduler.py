from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger

import module.task.jijian
from module.schedule.baseScheduler import base_scheduler
from module.base import *


def add_all():
    jijian_receive()
    use_electricity()
    jijian_schedule()
    clue()


def jijian_receive():
    base_scheduler.add_job(module.task.jijian.jijian_receive, trigger=CronTrigger(hour="7,15,18,23"),
                           id="jijian_receive")


def use_electricity():
    base_scheduler.add_job(module.task.jijian.use_electricity, trigger=CronTrigger(hour="7,15,18,23"),
                           id="use_electricity")


def clue():
    base_scheduler.add_job(module.task.jijian.clue, trigger=CronTrigger(hour="7,18"),
                           id="clue")


def jijian_schedule(path="/config/schedual.json"):
    scheduler = base_scheduler.scheduler
    job = scheduler.get_job("jijian_schedule")
    if job is not None:
        scheduler.remove_job(job.id)
    enable_jijian_schedule = base.get("enable_jijian_schedule")
    if not enable_jijian_schedule:
        return
    cron = base.read_json(base.project_path + path)["Config"]["cron"]
    hour = cron["hour"]
    minute = cron["minute"]
    if enable_jijian_schedule:
        base_scheduler.add_job(module.task.jijian.schedual, args=(path,),
                               trigger=CronTrigger(hour=hour, minute=minute),
                               id="jijian_schedule")


def once_jijian_schedule(path="/config/schedual.json"):
    base_scheduler.add_job(module.task.jijian.schedual, args=(path,),
                           trigger=DateTrigger(),
                           id="once_jijian_schedule")
