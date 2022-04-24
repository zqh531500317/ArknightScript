from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger

import module.task.daily
from module.schedule.baseScheduler import base_scheduler


def add_all():
    receive_renwu()
    friend()
    receive_xinyong()
    get_lizhi()
    buy_xinyong_shop()
    recruit_daily()
    xinpian()


def receive_renwu():
    base_scheduler.add_job(module.task.daily.receive_renwu, trigger=CronTrigger(hour="12,18,23"),
                           id="receive_renwu")


def friend():
    base_scheduler.add_job(module.task.daily.friend, trigger=CronTrigger(hour="6"), id="friend", )


def receive_xinyong():
    base_scheduler.add_job(module.task.daily.receive_xinyong, trigger=CronTrigger(hour="6"),
                           id="receive_xinyong")


def xinpian():
    base_scheduler.add_job(module.task.daily.xinpian, trigger=CronTrigger(hour="6,18"),
                           id="xinpian")


def get_lizhi():
    base_scheduler.add_job(module.task.daily.get_lizhi, trigger=CronTrigger(hour="12"),
                           id="get_lizhi")


def buy_xinyong_shop():
    base_scheduler.add_job(module.task.daily.buy_xinyong_shop, trigger=CronTrigger(hour="6"),
                           id="buy_xinyong_shop")


def quick_lizhi():
    job = base_scheduler.scheduler.get_job("quick_lizhi")
    if job is None:
        base_scheduler.add_job(module.task.daily.get_lizhi, trigger=DateTrigger(),
                               id="quick_lizhi")
    else:
        base_scheduler.reschedule_job("quick_lizhi", trigger=DateTrigger())


def recruit_daily():
    base_scheduler.add_job(module.task.daily.recruit_daily, trigger=CronTrigger(hour="6,12,18,23"),
                           id="recruit_daily")


def once_recruit(times):
    base_scheduler.add_job(module.task.daily.once_recruit, args=(times,),
                           trigger=DateTrigger(), id="once_recruit")
