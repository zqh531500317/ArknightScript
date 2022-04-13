from apscheduler.triggers.cron import CronTrigger

import module.schedule.baseScheduler

import module.task.jijian
from module.utils.core_config import cf, project_path, configList


def add_all():
    jijian_receive()
    use_electricity()
    jijian_schedule()
    clue()


def jijian_receive():
    module.schedule.baseScheduler.add_job(module.task.jijian.jijian_receive, trigger=CronTrigger(hour="7,15,18,23"),
                                          id="jijian_receive")


def use_electricity():
    module.schedule.baseScheduler.add_job(module.task.jijian.use_electricity, trigger=CronTrigger(hour="7,15,18,23"),
                                          id="use_electricity")


def clue():
    module.schedule.baseScheduler.add_job(module.task.jijian.clue, trigger=CronTrigger(hour="7"),
                                          id="clue")


def jijian_schedule():
    scheduler = module.schedule.baseScheduler.scheduler
    job = scheduler.get_job("jijian_schedule")
    if job is not None:
        scheduler.remove_job(job.id)
    enable_jijian_schedule = configList["Config"]["Game"]["enable_jijian_schedule"]
    if not enable_jijian_schedule:
        return
    cron = cf.read_json(project_path + "/config/schedual.json")["Config"]["cron"]
    hour = cron["hour"]
    minute = cron["minute"]
    if enable_jijian_schedule:
        module.schedule.baseScheduler.add_job(module.task.jijian.schedual,
                                              trigger=CronTrigger(hour=hour, minute=minute),
                                              id="jijian_schedule")
