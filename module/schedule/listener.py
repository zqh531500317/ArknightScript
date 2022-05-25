import datetime
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED, EVENT_JOB_SUBMITTED, JobSubmissionEvent
from module.utils.core_utils import *
import module.schedule.dailyScheduler

from module.base import *


@singleton
class Listener:
    def __init__(self):
        self.scheduler = None
        # 用于计算task运行时间
        # key job_id value:{'job':job , 'except_start_time':  'start_time':     ,}
        self.caltimemap = dict()

    def init_listener(self, scheduler: BaseScheduler):
        self.scheduler = scheduler
        self.scheduler.add_listener(self.start_listener, EVENT_JOB_SUBMITTED)
        self.scheduler.add_listener(self.finish_listener, EVENT_JOB_ERROR | EVENT_JOB_EXECUTED)
        return self.scheduler

    def start_listener(self, event):
        self.caltime_start(event)
        self.state_start(event)
        self.system_start(event)

    def finish_listener(self, event):
        # store img
        base.store_save_imgs()
        self.caltime_finish(event)
        self.handle_error(event)
        self.state_finish(event)
        self.system_finish(event)

    def caltime_start(self, event: JobSubmissionEvent):
        job_id = event.job_id
        job = self.scheduler.get_job(job_id)
        if job is not None:
            logger.warning("task %s is exist,skip caltime", job_id)
            return
        self.caltimemap[job_id]['except_start_time'] = str(event.scheduled_run_times[0]).split("+")[0]

    def caltime_finish(self, event):
        job_id = event.job_id
        job = self.scheduler.get_job(job_id)
        job_name = job.name
        start_time = self.caltimemap[job_id]['start_time']
        end_time = time.time()
        self.caltimemap.pop(job_id, None)
        logger.info("task running cost: %s minutes", end_time - start_time)
        logger.info("task %s is finished", job_name)

    def handle_error(self, event):
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
            base.send("任务调度出错", contents=content)

    def state_start(self, event):
        jobid = event.job_id
        job = self.scheduler.get_job(jobid)
        base.state.job_start(job)

    def state_finish(self, event):
        base.state.job_finish()

    def system_start(self, event):
        jobid = event.job_id
        if "once" in jobid or "fight" in jobid or "zhuxian" in jobid \
                or "ziyuanshouji" in jobid or "jiaomie" in jobid or "huodong" in jobid:
            base.state.is_fight = "running"
        base.state.running_task_num += 1

    def system_finish(self, event):
        jobid = event.job_id
        if "once_ziyuanshouji" in jobid or "once_jiaomie" in jobid or "once_unknown" in jobid or \
                "once_recently" in jobid or "once_zhuxian" in jobid or "fight" in jobid or \
                "zhuxian" in jobid or "ziyuanshouji" in jobid or "jiaomie" in jobid or "huodong" in jobid:
            base.state.is_fight = "stop"
            module.schedule.dailyScheduler.quick_lizhi()
            return
        # close game
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


listener = Listener()
