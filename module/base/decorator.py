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
        from module.schedule.listener import listener
        logger.info("debug_recode is start:%s", func.__name__)
        task_name = func.__name__
        listener.caltimemap[task_name]['start_time'] = datetime.datetime.now().replace(microsecond=0)
        logger.info("task %s is started", func.__name__)
        func(*args, **kwargs)

    return wrapper


def bench_time(n):
    def decorate(func):
        @wraps(func)
        def mywrap(*args, **kwargs):
            start = time.time()
            func(*args, **kwargs)
            end = time.time()
            logger.info("%-20s cost: %-5ss,times: %-2s,avg time: %-4ss", func.__name__, round(end - start, 2), n,
                        round((end - start) / n, 2))

            print("%-20s cost: %-5ss,times: %-2s,avg time: %-4ss" % (func.__name__, round(end - start, 2), n,
                                                                     round((end - start) / n, 2)))

        return mywrap

    return decorate
