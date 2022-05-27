import datetime
from functools import wraps
from logzero import logger
import time


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


def before(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from module.base.base import base
        from module.schedule.listener import listener
        task_name = base.state.running_job['name']
        listener.caltimemap[task_name]['start_time'] = datetime.datetime.now().replace(microsecond=0)
        logger.info("task %s is started", task_name)
        res = func(*args, **kwargs)
        return res

    return wrapper


def bench_time(n):
    def decorate(func):
        @wraps(func)
        def mywrap(*args, **kwargs):
            from module.base.base import base
            start = time.time()
            func(*args, **kwargs)
            end = time.time()
            res = "%-20s cost: %-5ss,times: %-2s,avg time: %-4ss" % (func.__name__, round(end - start, 2), n,
                                                                     round((end - start) / n, 2))
            base.hr_logger.info(res)
            return res

        return mywrap

    return decorate
