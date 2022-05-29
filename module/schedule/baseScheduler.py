import datetime
import copy

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from module.base import *
from module.schedule.listener import listener


@singleton
class BaseScheduler:
    def __init__(self):
        logger.info("class BaseScheduler __init__")
        jobstores = {
            'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
        }
        executors = {
            'default': ThreadPoolExecutor(1)
        }
        job_defaults = {
            'coalesce': True,  # 重启后作业如果被堆叠，只执行一次
            'max_instances': 1,
            "misfire_grace_time": 60 * 60
        }
        self.test_scheduler = BackgroundScheduler(jobstores={
            'test': MemoryJobStore()  # 使用内存作为作业存储
        },
            executors=executors,
            job_defaults=job_defaults)
        self.test_scheduler.start()
        self.scheduler = BackgroundScheduler(jobstores=jobstores,
                                             executors=executors,
                                             job_defaults=job_defaults)
        self.scheduler.start()
        # 添加监听器
        listener.init_listener(self.scheduler)

    def test_add_job(self, func, trigger, id, args=None, ):
        job = self.test_scheduler.get_job(id)
        if job is None:
            self.test_scheduler.add_job(func, args=args, trigger=trigger, id=id, name=id)

    def add_job(self, func, trigger, id, args=None, misfire_grace_time=7200):
        job = self.scheduler.get_job(id)
        if job is None:
            self.scheduler.add_job(func, args=args, trigger=trigger, id=id, name=id,
                                   misfire_grace_time=misfire_grace_time)
            white_list = ["jijian_schedule", "restart"]
            if isinstance(trigger, DateTrigger):
                return
            if id not in white_list:
                self.pause(id)

    def get_jobs(self):
        jobs = copy.deepcopy(self.scheduler.get_jobs())
        for s in jobs:
            if s.next_run_time is not None:
                s.next_run_time = s.next_run_time.astimezone(datetime.timezone(
                    datetime.timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")

        return jobs

    def get_job(self, id):
        job = copy.deepcopy(self.scheduler.get_job(id))
        if job.next_run_time is not None:
            job.next_run_time = job.next_run_time.astimezone(datetime.timezone(
                datetime.timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
        return job

    def pause(self, id):
        self.scheduler.get_job(id).pause()

    def resume(self, id):
        self.scheduler.get_job(id).resume()

    def reschedule_job(self, id, trigger):
        job = self.scheduler.get_job(id)
        if job is None:
            logger.debug("不可重新安排一个不能调整的job")
            return False
        else:
            self.scheduler.reschedule_job(id, trigger=trigger)
            return True

    def reschedule_job_part(self, id, kind, value):
        trigger = self.get_job(id).trigger
        hour = str(trigger.fields[5])
        minute = str(trigger.fields[6])
        day_of_week = str(trigger.fields[4])
        if kind == "hour":
            hour = value
        elif kind == "minute":
            minute = value
        elif kind == "day_of_week":
            day_of_week = value
        self.reschedule_job(id, CronTrigger(hour=hour, minute=minute, day_of_week=day_of_week))

    def pause_scheduler(self):
        self.scheduler.pause()

    def resume_scheduler(self):
        self.scheduler.resume()

    def is_scheduler_running(self):
        state = self.scheduler.state
        if state == 0:
            return "暂停中"
        elif state == 1:
            return "运行中"
        elif state == 2:
            return "暂停中"


base_scheduler = BaseScheduler()
