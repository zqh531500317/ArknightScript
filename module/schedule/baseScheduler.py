import datetime

import yagmail
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
import copy
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED, EVENT_JOB_SUBMITTED
from apscheduler.triggers.date import DateTrigger
from module.base import *
from module.entity.job_entity import JobEntity
from module.utils.core_utils import random_time_str, save_last_lines
import module.task.daily


@singleton
class BaseScheduler:
    def __init__(self):
        logger.info("class BaseScheduler __init__")
        jobstores = {
            'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
            # 'default': MemoryJobStore()  # 使用内存作为作业存储
        }
        executors = {
            'default': ThreadPoolExecutor(1)
        }
        job_defaults = {
            'coalesce': True,  # 重启后作业如果被堆叠，只执行一次
            'max_instances': 1,
            "misfire_grace_time": 60 * 60
        }
        self.start_time = datetime.datetime.now()
        self.except_start_time = datetime.datetime.now()
        self.end_time = datetime.datetime.now()
        self.scheduler = BackgroundScheduler(jobstores=jobstores,
                                             executors=executors,
                                             job_defaults=job_defaults)
        self.scheduler.start()
        self.scheduler.add_listener(self.finishListener, EVENT_JOB_ERROR | EVENT_JOB_EXECUTED)
        self.scheduler.add_listener(self.startListener, EVENT_JOB_SUBMITTED)

    def quick_lizhi(self):
        job = self.scheduler.get_job("quick_lizhi")
        if job is None:
            self.add_job(module.task.daily.get_lizhi, trigger=DateTrigger(),
                         id="quick_lizhi")
        else:
            self.reschedule_job("quick_lizhi", trigger=DateTrigger())

    def startListener(self, event):
        self.except_start_time = str(event.scheduled_run_times[0]).split("+")[0]
        self.start_time = datetime.datetime.now().replace(microsecond=0)
        jobid = event.job_id
        job = self.scheduler.get_job(jobid)
        if job is None:
            job = JobEntity(jobid, jobid, self.except_start_time)
        base.state.job_start(job)
        if "once" in jobid or "fight" in jobid or "zhuxian" in jobid \
                or "ziyuanshouji" in jobid or "jiaomie" in jobid or "huodong" in jobid:
            base.state.is_fight = "running"
        base.state.running_task_num += 1

    def finishListener(self, event):
        base.state.running_task_num -= 1
        self.end_time = datetime.datetime.now()
        jobid = str(event.job_id)
        base.state.job_finish()
        self.errorhandler(event)
        if "once_ziyuanshouji" in jobid or "once_jiaomie" in jobid or "once_unknown" in jobid or \
                "once_recently" in jobid or "once_zhuxian" in jobid or "fight" in jobid or \
                "zhuxian" in jobid or "ziyuanshouji" in jobid or "jiaomie" in jobid or "huodong" in jobid:
            base.state.is_fight = "stop"
            module.schedule.dailyScheduler.quick_lizhi()
            return
        self.__close_game()

    def errorhandler(self, event):
        if event.exception:
            img = base.screen(memery=True)
            temp = random_time_str()
            base.save('/log/error/{}'.format(temp), img)
            base.stop()
            # 保存日志
            save_last_lines(base.project_path + "/log/log.log",
                            base.project_path + "/log/error/{}/error.log".format(temp))
            # 发送邮件
            path = base.project_path + "/cache/email.png"
            base.write_pic(path, img)
            content = [
                "jobid=" + str(event.job_id) + "\n " + str(event.exception) + "\n " + str(event.traceback),
                yagmail.inline(path)
            ]
            base.send("任务调度出错",
                      contents=content
                      )

    def add_job(self, func, trigger, id, args=None, misfire_grace_time=7200):
        job = self.scheduler.get_job(id)
        if job is None:
            self.scheduler.add_job(func, args=args, trigger=trigger, id=id, name=id,
                                   misfire_grace_time=misfire_grace_time)
            white_list = ["jijian_schedule"]
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

    # 关闭游戏
    def __close_game(self):
        should_close = True
        jobs = self.scheduler.get_jobs()
        after = datetime.datetime.now() + datetime.timedelta(minutes=base.minutes)
        logger.info("比较时间为%s", after)
        for job in jobs:
            if job.next_run_time is None:
                continue
            next_time = job.next_run_time.replace(tzinfo=None)
            logger.info("任务%s将在%s执行", job.name, next_time)
            if after > next_time:
                should_close = False
        if base.state.running_task_num > 0:
            should_close = False
        logger.debug("当前队列任务数:%s", base.state.running_task_num)
        if should_close and base.isLive():
            for i in range(0, 5):
                logger.info("在%s分钟内无任务,将在%s秒后关闭游戏", base.minutes, str(10 - 2 * i))
                time.sleep(2)
            base.stop()
        time.sleep(2)

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
