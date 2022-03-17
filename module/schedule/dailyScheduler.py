from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger

import module.schedule.baseScheduler
import module.task.daily
import module.task.state


def add_all():
    receive_renwu()
    friend()
    receive_xinyong()
    get_lizhi()
    buy_xinyong_shop()
    recruit_daily()
    xinpian()


def receive_renwu():
    module.schedule.baseScheduler.add_job(module.task.daily.receive_renwu, trigger=CronTrigger(hour="12,20,23"),
                                          id="receive_renwu")


def friend():
    module.schedule.baseScheduler.add_job(module.task.daily.friend, trigger=CronTrigger(hour="6"), id="friend", )


def receive_xinyong():
    module.schedule.baseScheduler.add_job(module.task.daily.receive_xinyong, trigger=CronTrigger(hour="6"),
                                          id="receive_xinyong")


def xinpian():
    module.schedule.baseScheduler.add_job(module.task.daily.xinpian, trigger=CronTrigger(hour="6,18"),
                                          id="xinpian")


def get_lizhi():
    module.schedule.baseScheduler.add_job(module.task.state.get_lizhi, trigger=CronTrigger(hour="6,20"),
                                          id="get_lizhi")


def buy_xinyong_shop():
    module.schedule.baseScheduler.add_job(module.task.daily.buy_xinyong_shop, trigger=CronTrigger(hour="6", minute="5"),
                                          id="buy_xinyong_shop")


def quick_lizhi():
    job = module.schedule.baseScheduler.scheduler.get_job("quick_lizhi")
    if job is None:
        module.schedule.baseScheduler.add_job(module.task.state.get_lizhi, trigger=DateTrigger(),
                                              id="quick_lizhi")
    else:
        module.schedule.baseScheduler.reschedule_job("quick_lizhi", trigger=DateTrigger())


def recruit_daily():
    module.schedule.baseScheduler.add_job(module.task.daily.recruit_daily, trigger=CronTrigger(hour="6,12,18,23"),
                                          id="recruit_daily")


def once_recruit(times):
    module.schedule.baseScheduler.add_job(module.task.daily.once_recruit, args=(times,),
                                          trigger=DateTrigger(), id="once_recruit")
