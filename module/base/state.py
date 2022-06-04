from module.base.decorator import singleton
from logzero import logger


@singleton
class State:
    is_config_edit = False
    lizhi = {"time": "0", "lizhi": "0", "maxlizhi": "0"}
    is_fight = "stop"  # stop or running or task(标记不能同时运行的任务)
    running_task_num = 0
    debug_run = False
    running_task_name = ""
    running_job_num = 0
    running_job = {"id": "", "name": ""}
    # 队列 [job]
    blocking_jobs = []

    class LoginRetry:
        def __init__(self, max_retry_time=3):
            logger.info("new login_retry_instance")
            self.retry_time = 0
            self.max_retry_time = max_retry_time

        def if_continue(self):
            logger.info("login:retry_time=%s", self.retry_time)
            if self.retry_time < self.max_retry_time:
                self.retry_time += 1
                return True
            else:
                return False

    login_retry_instance = None

    @classmethod
    def new_login_retry_instance(cls):
        cls.login_retry_instance = cls.LoginRetry()
        return cls.login_retry_instance

    @classmethod
    def job_start(cls, job):
        if cls.running_job_num == 0:
            logger.debug("job_start:set running_job:" + str(job.id) + str(job.name))
            cls.running_job['id'] = job.id
            cls.running_job['name'] = job.name
            cls.running_job_num += 1
        else:
            logger.debug("job_start:add blocking_jobs:" + str(job.id) + str(job.name))
            cls.blocking_jobs.append(job)

    @classmethod
    def job_finish(cls):
        if len(cls.blocking_jobs) != 0:
            job = cls.blocking_jobs.pop(0)
            logger.debug("job_start:remove blocking_jobs to running_job:" + str(job.id) + str(job.name))
            cls.running_job['id'] = job.id
            cls.running_job['name'] = job.name
        else:
            logger.debug("job_start:remove  running_job:" + str(cls.running_job['id']) + str(cls.running_job['name']))
            cls.running_job_num -= 1
            cls.running_job['id'] = ""
            cls.running_job['name'] = ""
