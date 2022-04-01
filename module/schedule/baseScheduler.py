import datetime

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
import copy

from apscheduler.triggers.cron import CronTrigger

from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED, EVENT_JOB_SUBMITTED
import module.task.state
from module.utils.core_email import send
from module.utils.core_control import *
import func_timeout


def startListener(event):
    # logger.info("scheduler %s is started", event.job_id)
    global start_time
    start_time = datetime.datetime.now()
    jobid = event.job_id
    if "once" in jobid or "fight" in jobid or "zhuxian" in jobid \
            or "ziyuanshouji" in jobid or "jiaomie" in jobid or "huodong" in jobid:
        module.task.state.is_fight = "running"
    module.task.state.running_task_num += 1


def finishListener(event):
    # logger.info("scheduler %s is finished", event.job_id)
    module.task.state.running_task_num -= 1
    global end_time
    end_time = datetime.datetime.now()
    jobid = str(event.job_id)
    if isinstance(event.exception, func_timeout.exceptions.FunctionTimedOut):
        stop()
        save2("error")
    if event.exception:
        send("任务调度出错",
             "jobid=" + str(event.job_id) + "\n " + str(event.exception) + "\n " + str(event.traceback))
    if "once_ziyuanshouji" in jobid or "once_jiaomie" in jobid or "once_unknown" in jobid or \
            "once_recently" in jobid or "once_zhuxian" in jobid or "fight" in jobid or \
            "zhuxian" in jobid or "ziyuanshouji" in jobid or "jiaomie" in jobid or "huodong" in jobid:
        module.task.state.is_fight = "stop"
        module.schedule.dailyScheduler.quick_lizhi()
        return
    close_game()


def add_job(func, trigger, id, args=None, misfire_grace_time=7200):
    job = scheduler.get_job(id)
    if job is None:
        scheduler.add_job(func, args=args, trigger=trigger, id=id, name=id, misfire_grace_time=misfire_grace_time)
        white_list = ["jijian_schedule"]
        if id not in white_list:
            pause(id)


def get_jobs():
    jobs = copy.deepcopy(scheduler.get_jobs())
    for s in jobs:
        if s.next_run_time is not None:
            s.next_run_time = s.next_run_time.astimezone(datetime.timezone(
                datetime.timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")

    return jobs


def get_job(id):
    job = copy.deepcopy(scheduler.get_job(id))
    if job.next_run_time is not None:
        job.next_run_time = job.next_run_time.astimezone(datetime.timezone(
            datetime.timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
    return job


def pause(id):
    scheduler.get_job(id).pause()


def resume(id):
    scheduler.get_job(id).resume()


def reschedule_job(id, trigger):
    job = scheduler.get_job(id)
    if job is None:
        logger.debug("不可重新安排一个不能调整的job")
        return False
    else:
        scheduler.reschedule_job(id, trigger=trigger)
        return True


def reschedule_job_part(id, kind, value):
    trigger = get_job(id).trigger
    hour = str(trigger.fields[5])
    minute = str(trigger.fields[6])
    day_of_week = str(trigger.fields[4])
    if kind == "hour":
        hour = value
    elif kind == "minute":
        minute = value
    elif kind == "day_of_week":
        day_of_week = value
    reschedule_job(id, CronTrigger(hour=hour, minute=minute, day_of_week=day_of_week))


# 关闭游戏
def close_game():
    should_close = True
    jobs = scheduler.get_jobs()
    after = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
    logger.info("比较时间为%s", after)
    for job in jobs:
        if job.next_run_time is None:
            continue
        next_time = job.next_run_time.replace(tzinfo=None)
        logger.info("任务%s将在%s执行", job.name, next_time)
        if after > next_time:
            should_close = False
    if module.task.state.running_task_num > 0:
        should_close = False
    logger.debug("当前队列任务数:%s", module.task.state.running_task_num)
    if should_close and isLive():
        for i in range(0, 5):
            logger.info("在%s分钟内无任务,将在%s秒后关闭游戏", minutes, str(10 - 2 * i))
            time.sleep(2)
        stop()
    time.sleep(2)


def pause_scheduler():
    scheduler.pause()


def resume_scheduler():
    scheduler.resume()


def is_scheduler_running():
    state = scheduler.state
    if state == 0:
        return "暂停中"
    elif state == 1:
        return "运行中"
    elif state == 2:
        return "暂停中"


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
flag = configList["Config"]["Game"]["closable"]
minutes = configList["Config"]["Game"]["minutes"]
start_time = datetime.datetime.now()
end_time = datetime.datetime.now()
scheduler = BackgroundScheduler(jobstores=jobstores,
                                executors=executors,
                                job_defaults=job_defaults)
scheduler.start()
scheduler.add_listener(finishListener, EVENT_JOB_ERROR | EVENT_JOB_EXECUTED)
scheduler.add_listener(startListener, EVENT_JOB_SUBMITTED)
